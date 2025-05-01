import sys
from sidraconnector.sdk import constants
from sidraconnector.sdk.log.logging import Logger
from sidraconnector.sdk.storage.utils import Utils
from sidraconnector.sdk.databricks.dsuingestion.tabularingestionservice import TabularIngestionService
from sidraconnector.sdk.databricks.datapreview.datapreviewservice import DataPreviewService
from sidraconnector.sdk.databricks.reader.readerservice import ReaderService
from sidraconnector.sdk.metadata.entityservice import EntityService
from sidraconnector.sdk.metadata.marservice import MarService
from datetime import datetime, timezone
from dateutil.parser import parse, ParserError
from wrapt_timeout_decorator import timeout
from pyspark.sql.types import StructType

class TabularIngestion():
    def __init__(self, spark):
        self.spark = spark
        self.utils =  Utils(spark)
        self.logger = Logger(spark, self.__class__.__name__)
        self.reader_service = ReaderService(spark, self.logger)
        self.data_preview_service = DataPreviewService(spark, self.logger)
        self.entity_service = EntityService(spark)

    def process(self, asset_id : int, asset_uri : str, asset_is_full_extract : bool, intake_run_id : str = None, intake_execution_date : datetime = None):
        ingestion_start_date = self._get_execution_date(intake_execution_date)

        self.logger.debug(f"[TabularIngestion] Asset_Id: {asset_id}, Asset_Uri:{asset_uri}, Asset_Is_Full_Extract: {asset_is_full_extract}")
        self.tabular_service = TabularIngestionService(self.spark, self.logger, asset_uri, asset_id, asset_is_full_extract)
        self.mar_service = MarService(self.spark)

        if self.tabular_service.asset_is_registered is False:
            registered_asset = self.tabular_service.register_asset()
            self.logger.debug(f"[TabularIngestion]: Registered asset: {registered_asset}")
            asset_path = self.tabular_service.get_wasbs_file(registered_asset.destination_uri)
            self.logger.debug(f"[TabularIngestion]: Copying file: {registered_asset.source_uri} to {asset_path}")
            asset_copied = self.tabular_service.copy_raw_file(registered_asset.source_uri, asset_path)
            registered_asset_info = self.tabular_service.register_info(registered_asset)
            self.tabular_service.delete_source_file(registered_asset.source_uri)
        else:
            asset_copied = True
            asset_path = self.utils.https_to_wasbs(self.tabular_service.asset_uri)

        self.tabular_service.set_metadata_information()
        edl = self.entity_service.get_edl_for_entity(self.tabular_service.entity.id)
        is_incremental = self.entity_service.is_incremental(edl)

        if (asset_copied is True):
            file_dataframe = self.reader_service.read_file(asset_path, self.tabular_service.entity)
            file_dataframe = self.tabular_service.add_is_deleted_column(file_dataframe)
        else: 
            empty_schema=StructType([])
            file_dataframe = self.spark.createDataFrame([],schema=empty_schema)            

        # Remove old data if needed
        self.remove_old_data_if_needed(file_dataframe, is_incremental)

        column_names = self.tabular_service.get_non_calculated_field_names()
        self.tabular_service.delete_from_table()
        
        entity = self.tabular_service.get_entity() 
        if file_dataframe.count() > 0:
            # Get max value for Incremental Load
            incremental_load_new_max_value = None
            incremental_column = [c for c in file_dataframe.columns if c.lower()==constants.TEMPORAL_FIELD_NAME_DELTA_VALUE.lower()]
            if (len(incremental_column)>0):
                incremental_load_new_max_value = file_dataframe.agg({incremental_column[0]: "max"}).collect()[0][0]
                file_dataframe = file_dataframe.drop(incremental_column[0])
            else:
                # Note that, this will work with the main delta column only, not the secondary one, which is used for dates and expected to be included as column constants.TEMPORAL_FIELD_NAME_DELTA_VALUE
                delta_column = self.entity_service.get_delta_attribute_name(entity.attributes, edl)
                if (delta_column is not None):
                    incremental_load_new_max_value = file_dataframe.agg({delta_column: "max"}).collect()[0][0]


            file_dataframe = file_dataframe.toDF(*column_names)
            self.tabular_service.create_staging_table(file_dataframe)
            self.tabular_service.configure_query_optimization()
            self.tabular_service.create_table_staging_query()
            
            #if tabular_service.has_to_generate_change_data_feed() is True:
                # TODO: Not Implemented yet: It will be changed for Change Data Feed from Databricks
                #tabular_service.insert_data_into_delta_table() 
            #
            
            consolidation_mode = self.tabular_service.get_consolidation_mode(is_incremental)
            self.ingest_data(ingestion_start_date, file_dataframe, entity, consolidation_mode, is_incremental)
            self.tabular_service.finish_loading(file_dataframe.count())
            
            # Update EntityDeltaLoad in incremental loads
            self.entity_service.update_entity_delta_load_in_incremental_loads(entity, incremental_load_new_max_value, edl)

            self.tabular_service.drop_staging_tables()
        else:
            self.tabular_service.finish_loading(file_dataframe.count())            

        if (intake_run_id is not None):
            self.tabular_service.add_asset_to_dip_run(intake_run_id)          

        if file_dataframe.count() > 0:
            #Mar
            self.mar_service.execute(entity.id, entity.id_provider, entity.id_data_intake_process, consolidation_mode, ingestion_start_date, self.tabular_service._get_full_table_name(), file_dataframe.count(), is_incremental)

            # Generate Data Preview
            self.generate_data_preview(entity)
   
        # Data Quality validations
        self.execute_data_validations(intake_run_id, ingestion_start_date)
   
        # Anomaly Detection
        self.execute_anomaly_detection()

    def ingest_data(self, ingestion_start_date, file_dataframe, entity, consolidation_mode, is_incremental):
        self.logger.debug(f"[TabularIngestion]: Starting ingestion with consolidation mode: {consolidation_mode}")
        if consolidation_mode == constants.CONSOLIDATION_MODE_SNAPSHOT:
            self.tabular_service.insert_snapshot_data_into_final_table()
        elif consolidation_mode == constants.CONSOLIDATION_MODE_MERGE:
            self.tabular_service.insert_merge_data_into_final_table() 
        elif ((consolidation_mode == constants.CONSOLIDATION_MODE_OVERWRITE) or (consolidation_mode == constants.CONSOLIDATION_MODE_OVERWRITE_IF_NOT_EMPTY)):
            self.tabular_service.insert_overwrite_data_into_final_table() 
        else: 
            error_message = f"[TabularIngestion] Consolidation mode {consolidation_mode} is not implemented"
            self.logger.error(error_message)
            self.mar_service.execute(entity.id, entity.id_provider, entity.id_data_intake_process, constants.CONSOLIDATION_MODE_UNKNOWN, ingestion_start_date, self.tabular_service._get_full_table_name(), file_dataframe.count(), is_incremental)
            raise Exception(error_message)

    def remove_old_data_if_needed(self, file_dataframe, is_incremental):
        if self.tabular_service.get_consolidation_mode(is_incremental) == constants.CONSOLIDATION_MODE_SNAPSHOT:
            self.tabular_service.truncate_old_partition_from_same_file()
        elif self.tabular_service.get_consolidation_mode(is_incremental) == constants.CONSOLIDATION_MODE_OVERWRITE:
            self.tabular_service.truncate_and_vacuum_table()
        elif ((self.tabular_service.get_consolidation_mode(is_incremental) == constants.CONSOLIDATION_MODE_OVERWRITE_IF_NOT_EMPTY) and (file_dataframe.count() > 0)):
            self.tabular_service.truncate_and_vacuum_table()

    
    def generate_data_preview(self, entity):
        if self.tabular_service.has_to_generate_data_preview() is True:
            try: 
                self.update_data_preview(entity)
            except:
                self.logger.exception('Error on create_sqlserver_datapreview_table: %s' %sys.exc_info()[1])

    @timeout(300)
    def update_data_preview(self, entity):
        provider_database = self.tabular_service.get_provider_database()                 
        entity_id = entity.id
        entity_table = entity.table_name
        asset_id = self.tabular_service.get_asset_id()
        self.data_preview_service.create_sqlserver_datapreview_table(asset_id, constants.DATACATALOG_SAMPLE_NUMBER_RECORDS, provider_database, entity_table, entity_id)

    def execute_data_validations(self, intake_run_id, ingestion_start_date):
        entity = self.tabular_service.get_entity() 
        asset_id = self.tabular_service.get_asset_id()
        try:
            import sidradataquality.sdk.databricks.utils as ValidationDatabricksUtils
            databricks_utils = ValidationDatabricksUtils.Utils(self.spark)

            if databricks_utils.service_is_enabled():
                self.logger.debug(f"Executing Data Quality validations.")
                from sidradataquality.sdk.data.validationservice import ValidationService as ValidationCheckService
                validation_check_service = ValidationCheckService(self.spark)
                executed = validation_check_service.execute_validations_for_entity_asset(entity.id, asset_id, intake_run_id, ingestion_start_date)
                if not executed:
                    self.logger.debug(f"Validations not available for current entity '{entity.table_name}' ({entity.id}).")
            else:
                self.logger.debug(f"Data Quality not deployed in current DSU.")

        except Exception as e:
            self.logger.exception("Exception on Asset {asset_id} Data Quality: {e}".format(asset_id= asset_id, e=e))

    def execute_anomaly_detection(self):
        entity = self.tabular_service.get_entity() 
        asset_id = self.tabular_service.get_asset_id()

        try:
            if (entity.load_properties.anomaly_detection):
                self.logger.debug(f"Executing Anomaly Detection.")
                # import delayed in case it fails (old cluster without pyod, is catched by the try/except)
                from sidraconnector.sdk.databricks.anomalydetection.anomalydetection import AnomalyDetection
                anomaly_detector = AnomalyDetection(self.spark)
                anomaly_detection_results = anomaly_detector.execute(entity.id, asset_id, constants.ANOMALY_DETECTION_DEFAULT_MAX_ASSET_HISTORY_LENGTH)
                return anomaly_detection_results
            else: 
                self.logger.debug(f"Anomaly Detection skipped as configured.")
        except Exception as e:
            self.logger.exception("Exception on Asset {asset_id} Anomaly Detection: {e}".format(asset_id= asset_id, e=e))

    def _get_execution_date(self, intake_execution_date):
        try:
            if intake_execution_date is None:
                execution_date = datetime.now(timezone.utc)
            else:
                if type(intake_execution_date) is datetime:
                    execution_date = intake_execution_date
                else:
                    execution_date = parse(intake_execution_date)
        except ParserError:
            execution_date = datetime.now(timezone.utc)
            self.logger.warning(f"Incorrect format for the intake execution date: {intake_execution_date}, applying {execution_date}")
        except Exception:
            execution_date = datetime.now(timezone.utc)
            self.logger.warning(f"Incorrect type for the intake execution date: {intake_execution_date}, applying {execution_date}")

        return execution_date