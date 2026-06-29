# agents/supervisor.py

import os
import yaml
import logging
from datetime import datetime
from agents.snowflake_monitor_agent import SnowflakeMonitorAgent
from agents.sagemaker_ops_agent import SageMakerOpsAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MLOps_Supervisor")

class MLOpsSupervisor:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.sf_agent = SnowflakeMonitorAgent(self.config['snowflake'])
        self.sm_agent = SageMakerOpsAgent(self.config['sagemaker'])

    def run_pipeline_orchestration(self):
        logger.info("Initializing multi-agent operational loop...")
        
        new_records = self.sf_agent.check_new_arrivals()
        drift_status = self.sf_agent.inspect_data_drift()
        
        # Automation decision criteria
        if drift_status or new_records >= self.config['snowflake']['min_new_records_trigger']:
            logger.info("Condition thresholds reached. Dispatching training jobs...")
            s3_feature_store = "s3://my-snowflake-sagemaker-pipeline-bucket/features/latest/"
            
            try:
                job_id = self.sm_agent.trigger_retraining(s3_feature_store)
                is_promotable = self.sm_agent.verify_model_metrics(job_id)
                
                if is_promotable:
                    self.log_to_daily_file("SUCCESS", f"Automated training complete. Job {job_id} cleared metrics threshold.")
                else:
                    self.log_to_daily_file("WARNING", f"Job {job_id} completed but performance metrics were insufficient.")
            except Exception as e:
                self.log_to_daily_file("FAILED", f"Pipeline failed during infrastructure execution: {str(e)}")
        else:
            logger.info("System state normal. Threshold limits not exceeded.")
            self.log_to_daily_file("IDLE", "Data volume and drift properties within expected operating targets.")

    def log_to_daily_file(self, status: str, message: str):
        log_entry = f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | {status} | {message} |\n"
        with open("DailyLog.md", "a") as f:
            f.write(log_entry)

if __name__ == "__main__":
    # Point directly to config layer root
    config_location = os.path.join(os.path.dirname(__file__), "..", "config", "agent_config.yaml")
    supervisor = MLOpsSupervisor(config_location)
    supervisor.run_pipeline_orchestration()
