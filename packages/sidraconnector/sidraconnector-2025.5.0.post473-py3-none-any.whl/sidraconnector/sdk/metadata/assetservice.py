from sidraconnector.sdk.databricks.utils import Utils
from sidraconnector.sdk.api.sidra.core.utils import Utils as CoreApiUtils
from sidraconnector.sdk.log.logging import Logger
from sidraconnector.sdk import constants
from pyspark.sql import SparkSession
from tenacity import retry, wait_random, stop_after_delay, before_sleep
import SidraCoreApiPythonClient
import uuid

class AssetService():
  def __init__(self, spark):
    self.logger = Logger(spark, self.__class__.__name__)
    self.utils = Utils(spark)
    sidra_core_api_client = CoreApiUtils(spark).get_SidraCoreApiClient()
    self.metadata_asset_api_instance = SidraCoreApiPythonClient.MetadataAssetsAssetsApi(sidra_core_api_client)
    self.ingestion_api_instance = SidraCoreApiPythonClient.IngestionIngestionApi(sidra_core_api_client)
    
  def get_asset(self, id_asset):
    # Returns MetadataAssetsAssetFullDTO
    self.logger.debug(f"[Asset Service][get_asset] Retrieve asset {id_asset} information")
    asset = self.metadata_asset_api_instance.api_metadata_assets_id_get(id_asset, api_version=constants.API_VERSION)
    return asset
  
  def log_retries(retry_state):
    _spark = SparkSession.builder.getOrCreate()
    _logger = Logger(_spark, f"AssetService{uuid.uuid4()}")
    _logger.retry_attempt(retry_state)

  @retry(wait=wait_random(min=60, max=120), stop=stop_after_delay(1200), before_sleep = log_retries) 
  def register_asset(self, asset_uri):
    # Returns APIDataIngestionModelAssetFromLanding
    self.logger.debug(f"[Asset Service][register_asset] Register asset located in: {asset_uri}")
    api_response = self.ingestion_api_instance.api_ingestion_registerasset_post(asset_uri=asset_uri, api_version=constants.API_VERSION)
    return api_response
  
  @retry(wait=wait_random(min=60, max=120), stop=stop_after_delay(1200), before_sleep = log_retries)
  def register_info(self, registered_asset): 
    # registered_asset is the result of register_asset() function and it is an APIDataIngestionModelAssetFromLanding
    # Returns APICommonCorePipelineParameter
    self.logger.debug(f"[Asset Service][register_info] Update information for asset id: {registered_asset.asset_id}")
    api_response = self.ingestion_api_instance.api_ingestion_registerinfo_post(body=registered_asset, api_version=constants.API_VERSION)
    return api_response  
   
  @retry(wait=wait_random(min=60, max=120), stop=stop_after_delay(1200), before_sleep = log_retries)
  def update_asset_loaded(self, asset_id, entities_count):
    self.logger.debug(f"[Asset Service][update_asset_loaded] Update information for asset id: {asset_id} after load is finished")   
    body = SidraCoreApiPythonClient.IngestionAssetLoadedDTO() 
    body.entities = entities_count
    self.ingestion_api_instance.api_ingestion_asset_asset_id_loaded_post(asset_id, body=body, api_version=constants.API_VERSION)
  
  # The function most recent asset for the specified entity. If modified_since is empty it gets all assets for the entity
  @retry(wait=wait_random(min=60, max=120), stop=stop_after_delay(1200), before_sleep = log_retries) 
  def get_recent_entity_assets(self, entity_id: int, modified_since = ""):
    self.logger.debug(f"[Asset Service][get_recent_entity_assets] Get entity: {entity_id} modified since: {modified_since}")
    body = {entity_id : modified_since}
    api_response = self.metadata_asset_api_instance.api_metadata_assets_modified_since_post(body=body, api_version=constants.API_VERSION)
    return api_response


