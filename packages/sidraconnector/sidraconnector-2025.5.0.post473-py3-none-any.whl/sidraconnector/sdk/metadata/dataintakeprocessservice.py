from sidraconnector.sdk import constants
from sidraconnector.sdk.api.sidra.core.utils import Utils as CoreApiUtils
from sidraconnector.sdk.log.logging import Logger
from pyspark.sql import SparkSession
from tenacity import retry, wait_random, stop_after_delay
import SidraCoreApiPythonClient
import uuid

class DataIntakeProcessService():
    def __init__(self,spark):
        self.logger = Logger(spark, self.__class__.__name__)
        self.utils = CoreApiUtils(spark)
        sidra_core_api_client = self.utils.get_SidraCoreApiClient()
        self._metadata_dataintakeprocess_api_instance = SidraCoreApiPythonClient.MetadataDataIntakeProcessesDataIntakeProcessApi(sidra_core_api_client)

    def log_retries(retry_state):
        _spark = SparkSession.builder.getOrCreate()
        _logger = Logger(_spark, f"DataIntakeProcessService{uuid.uuid4()}")
        _logger.retry_attempt(retry_state)

  
    @retry(wait=wait_random(min=60, max=120), stop=stop_after_delay(1200), before_sleep = log_retries)
    def get_dataintakeprocess(self, id_dataintakeprocess):
        if (not id_dataintakeprocess):
            self.logger.warning("[DataIntakeProcess Service][get_dataintakeprocess] DataIntakeProcess information cannot be retrieved, id_dataintakeprocess is None")
            return None
        
        self.logger.debug(f"[DataIntakeProcess Service][get_dataintakeprocess] Retrieve dataintakeprocess {id_dataintakeprocess} information")
        dataintakeprocess = self._metadata_dataintakeprocess_api_instance.api_metadata_data_intake_processes_simple_id_get(id_dataintakeprocess, api_version = constants.API_VERSION)
        return dataintakeprocess

    @retry(wait=wait_random(min=60, max=120), stop=stop_after_delay(1200), before_sleep = log_retries)
    def update_run_id(self, id_dataintakeprocess, asset_id, run_id):
        self.logger.debug(f"[DataIntakeProcess Service][update_run_id] Update dataintakeprocess {id_dataintakeprocess} information")
        self._metadata_dataintakeprocess_api_instance.api_metadata_data_intake_processes_data_intake_process_id_assets_asset_id_run_id_post(id_dataintakeprocess, asset_id, run_id)
