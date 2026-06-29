# agents/supervisor.py

import os
import logging
from datetime import datetime

# Enforce system module search paths for robust runner package resolution
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.snowflake_monitor_agent import SnowflakeMonitorAgent
from agents.sagemaker_ops_agent import SageMakerOpsAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MLOps_Supervisor")

class MLOpsSupervisor:
    """
    The central coordinator routing tasks based on state transitions, 
    telemetry, and performance thresholds.
    """
    def __init__(self, config_dict: dict):
        # Configuration is now loaded directly from an inline dictionary config
        self.config = config_dict
        
        self.sf_agent = SnowflakeMonitorAgent(self.config['snowflake'])
        self.sm_agent = SageMakerOpsAgent(self.config['sagemaker'])

    def run_pipeline_orchestration(self):
        logger.info("Initializing multi-agent operational loop checking cloud states...")
        
        new_records = self.sf_agent.check_new_arrivals()
        drift_status = self.sf_agent.inspect_data_drift()
        
        # Automation decision criteria threshold matching
        if drift_status or new_records >= self.config['snowflake']['min_new_records_trigger']:
            logger.info(f"Condition thresholds reached ({new_records} records). Dispatching operational container triggers...")
            s3_feature_store = "s3://my-snowflake-sagemaker-pipeline-bucket/features/latest/"
            
            try:
                job_id = self.sm_agent.trigger_retraining(s3_feature_store)
                is_promotable = self.sm_agent.verify_model_metrics(job_id)
                
                if is_promotable:
                    logger.info(f"Pipeline Success! Model {job_id} cleared metrics threshold verification passes.")
                    self.log_to_daily_file("SUCCESS", f"Automated training complete. Job {job_id} cleared metrics threshold.")
                else:
                    logger.warning(f"Job {job_id} completed but performance metrics were insufficient for deployment staging.")
                    self.log_to_daily_file("WARNING", f"Job {job_id} completed but performance metrics were insufficient.")
            except Exception as e:
                logger.error(f"Pipeline execution encountered unhandled critical exceptions: {str(e)}")
                self.log_to_daily_file("FAILED", f"Pipeline failed during infrastructure execution: {str(e)}")
        else:
            logger.info("System state normal. Data variations remain safely within target thresholds.")
            self.log_to_daily_file("IDLE", "Data volume and drift properties within expected operating targets.")

    def log_to_daily_file(self, status: str, message: str):
        log_entry = f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | {status} | {message} |\n"
        
        # Look for DailyLog.md directly at the repository root folder
        log_location = "DailyLog.md"
            
        try:
            with open(log_location, "a") as f:
                f.write(log_entry)
            logger.info("Operational metrics appended safely to GitOps execution ledger file.")
        except Exception as e:
            logger.error(f"Failed to append metadata telemetry entry blocks onto tracking ledger filesystem: {str(e)}")

if __name__ == "__main__":
    # INLINE HARDCODED CONFIGURATION - Bypasses external file lookup entirely
    embedded_config = {
        'snowflake': {
            'account': "your_account_locator",
            'warehouse': "COMPUTE_WH",
            'database': "PROD_DB",
            'schema': "PUBLIC",
            'table_name': "CUSTOMER_FEATURES",
            'drift_threshold_psi': 0.1,
            'min_new_records_trigger': 10000
        },
        'sagemaker': {
            'region': "us-east-1",
            'role_arn': "arn:aws:iam::123456789012:role/SageMakerExecutionRole",
            'image_uri': "123456789012.dkr.ecr.us-east-1.amazonaws.com/xgboost-production:latest",
            'instance_type': "ml.m5.xlarge",
            'instance_count': 1,
            's3_output_path': "s3://my-snowflake-sagemaker-pipeline-bucket/models/",
            'target_accuracy_threshold': 0.88
        }
    }
        
    supervisor = MLOpsSupervisor(embedded_config)
    supervisor.run_pipeline_orchestration()
