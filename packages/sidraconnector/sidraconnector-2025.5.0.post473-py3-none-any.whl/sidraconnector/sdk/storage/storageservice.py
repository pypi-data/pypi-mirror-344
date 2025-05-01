from sidraconnector.sdk.databricks.utils import Utils
from sidraconnector.sdk.storage.utils import Utils as StorageUtils
from datetime import datetime, timedelta, timezone
from operator import attrgetter
import re
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ResourceTypes, AccountSasPermissions, generate_account_sas, ContainerSasPermissions, generate_container_sas
import time
import os



class StorageService():
    def __init__(self, spark):
        self.spark = spark
        self.databricks_utils = Utils(spark)
        self.storage_utils = StorageUtils(spark)
        self.dbutils = self.databricks_utils.get_db_utils()
        self.default_container = "dataextraction" # Same used by the pipelines

    def mount_dataextraction_container(self):
        storage_account = self.databricks_utils.get_databricks_secret("resources", "additional_storage_account_name")
        self.mount_container(storage_account, self.databricks_utils.get_databricks_secret("resources", "additional_storage_account_key"), self.default_container)

    def mount_container(self, storage_account, storage_key, container):
        config_key = f"fs.azure.account.key.{storage_account}.blob.core.windows.net"
        source = f"wasbs://{container}@{storage_account}.blob.core.windows.net"
        mount_point = f"/mnt/{storage_account}_{container}"
        dbutils = self.databricks_utils.get_db_utils()
        try:
            dbutils.fs.mount(
            source = source,
            mount_point = mount_point,
            extra_configs = {config_key:storage_key})
        except:
            if not any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
                raise(f"Could not mount {mount_point}")    
        return mount_point
            
    def export_for_ingestion(self, df, provider_name, entity_name, storage_account=None, storage_key=None, container=None):
        if ((not storage_account) & (not storage_key)):
            storage_account = self.databricks_utils.get_databricks_secret("resources", "additional_storage_account_name")
            storage_key = self.databricks_utils.get_databricks_secret("resources", "additional_storage_account_key")

        if (not container):
            container = self.default_container

        service = self.get_blob_storage_service_client()
        self.get_or_create_container(service, container) #ensure that the container exists

        mount_point = self.mount_container(storage_account, storage_key, container)

        relative_path_to_folder = f'{provider_name}/{entity_name}/'
        destination_file_name = f'{provider_name}_{entity_name}_{datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")}.parquet'
        destination_path = f'dbfs:{mount_point}/{relative_path_to_folder}'
        destination_file = f'{destination_path}{destination_file_name}'

        df.repartition(1).write.mode("append").save(destination_path)

        dbutils = self.databricks_utils.get_db_utils()
        files_in_folder = dbutils.fs.ls(destination_path)
        [dbutils.fs.rm(f.path, True) for f in files_in_folder if (f.name == "_delta_log/")]
        files_in_folder = dbutils.fs.ls(destination_path)
        generated_file = max(files_in_folder, key=attrgetter('modificationTime')).path
        dbutils.fs.mv(generated_file, destination_file)
        asset_uri = f'https://{storage_account}.blob.core.windows.net/{container}/{relative_path_to_folder}{destination_file_name}'
        return asset_uri

    def sanitize_container(container_name):
        container_pattern = re.compile('[^a-zA-Z0-9]')
        return re.sub(container_pattern, '-', container_name.lower())
    
    def get_or_create_container(self, blob_service_client, destination_container) -> str:
        if not [ container for container in blob_service_client.list_containers(destination_container) if container.name == destination_container ]:
            try:
                blob_service_client.create_container(destination_container.lower())
            except ResourceExistsError as e:
                # Ignore error if the container already exists because it could happen due a race condition and if the container already exists simply return the destination container
                if e.error_code != 'ContainerAlreadyExists':
                    raise e    
        return destination_container
    
    def delete_file(self, file_uri):
        self.dbutils.fs.rm(self.storage_utils.https_to_wasbs(file_uri))
    
    def delete_folder(self, file_uri):
        self.dbutils.fs.rm(self.storage_utils.https_to_wasbs(file_uri), True)
    
    def get_blob_storage_service_client(self):
        storage_account_name = self.dbutils.secrets.get(scope='resources', key='additional_storage_account_name')
        storage_account_key = self.dbutils.secrets.get(scope='resources', key='additional_storage_account_key')
        service = BlobServiceClient(account_url='https://{addsto}.blob.core.windows.net/'.format(addsto = storage_account_name), credential=storage_account_key)
        return service

    def copy_file(self, source_uri, destination_container, destination_path, use_sync_copy = False):
        service = self.get_blob_storage_service_client()
        self.get_or_create_container(service, destination_container)
        copied_blob = service.get_blob_client(destination_container, destination_path)
        copied_blob.start_copy_from_url(source_uri, use_sync_copy)
        return copied_blob.url

    def get_container_sas_token(self, storage_account_name, storage_access_key, container_name):
        container_sas_token = generate_container_sas(
        account_name=storage_account_name,
        container_name=container_name,
        account_key=storage_access_key,
        permission=ContainerSasPermissions(read=True, write=True, list=True, delete=True),
        expiry=datetime.now(timezone.utc) + timedelta(hours=1))
        return container_sas_token
    
    def delete_data_lake_container(self, container_name) -> None:
        storage_account_name = self.dbutils.secrets.get(scope='resources', key='principal_storage_account_name')
        storage_account_key = self.dbutils.secrets.get(scope='resources', key='principal_storage_account_key')
        service = BlobServiceClient(account_url='https://{addsto}.blob.core.windows.net/'.format(addsto = storage_account_name), credential=storage_account_key)
        self.delete_container(service, container_name)

    def delete_container(self, blob_service_client, container_name) -> None:
       if [container for container in blob_service_client.list_containers(container_name) if container.name == container_name ]:
           blob_service_client.delete_container(container_name)

    def is_folder(self, uri):
        # Check if the URI ends with a slash (suggesting a folder)
        if uri.endswith('/'):
            return True

        service = self.get_blob_storage_service_client()
        wasb = self.storage_utils.https_to_wasbs(uri)
        container = wasb.split('@')[0].replace('wasbs://', '')
        path = wasb.split('/', 3)[3]
        
        # Get the container client
        container_client = service.get_container_client(container)

        # Try to get the blob properties to check if it exists as a blob
        try:
            blob_client = container_client.get_blob_client(path)
            blob_properties = blob_client.get_blob_properties()
            return False
        except Exception as e:
            # If it fails, check if it's a folder by listing blobs with the prefix
            blobs_list = container_client.list_blobs(name_starts_with=path + '/')
            if any(blobs_list):
                return True
            return None

    def copy_folder(self, source_uri, destination_container, destination_path):
        service = self.get_blob_storage_service_client()
        self.get_or_create_container(service, destination_container)
        source_wasb = self.storage_utils.https_to_wasbs(source_uri)
        source_container = source_wasb.split('@')[0].replace('wasbs://', '')
        source_path = source_wasb.split('/', 3)[3]
        source_container_client = service.get_container_client(source_container)
        blobs_list = source_container_client.list_blobs(name_starts_with=source_path)
        storage_account_uri = f'https://{source_wasb.split("@")[1].split("/")[0]}'
        copied_blobs = []
        for blob in blobs_list:
            blob_url = f"{storage_account_uri}/{source_container}/{blob.name}"
            print(f"Copying {blob_url} to {destination_path}/{os.path.basename(blob.name)}")
            copied_blob_client = service.get_blob_client(destination_container, f'{destination_path}/{os.path.basename(blob.name)}')
            copy_op = copied_blob_client.start_copy_from_url(blob_url)
            copied_blobs.append(copied_blob_client)
        
        for cp in copied_blobs:
            self._wait_for_copy(cp)


    def _wait_for_copy(self, blob_client):    
        count = 0
        props = blob_client.get_blob_properties()
        print(props.copy.status)
        while props.copy.status == 'pending':
            print(f"Waiting for {blob_client.blob_name} to be copied")
            count = count + 1
            print(count)
            if count > 12:
                raise TimeoutError('Timed out waiting for async copy to complete.')
            time.sleep(5)
            props = blob_client.get_blob_properties()
        return props