# agents/supervisor.py

import os
import yaml
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
    def __init__(self, config_path: str):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file context missing at verified path target: {config_path}")
            
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
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
        # Safely resolve target log directory destination path relative to the runtime root location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_location = os.path.normpath(os.path.join(current_dir, "..", "DailyLog.md"))
        
        if not os.path.exists(log_location) and os.path.exists("DailyLog.md"):
            log_location = "DailyLog.md"
            
        try:
            with open(log_location, "a") as f:
                f.write(log_entry)
            logger.info("Operational metrics appended safely to GitOps execution ledger file.")
        except Exception as e:
            logger.error(f"Failed to append metadata telemetry entry blocks onto tracking ledger filesystem: {str(e)}")

if __name__ == "__main__":
    # Absolute path calculation lookup standard
    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_location = os.path.normpath(os.path.join(current_directory, "..", "config", "agent_config.yaml"))
    
    # Fallback absolute check optimization supporting direct root folder runs natively
    if not os.path.exists(config_location):
        config_location = "config/agent_config.yaml"
        
    supervisor = MLOpsSupervisor(config_location)
    supervisor.run_pipeline_orchestration()