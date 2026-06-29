<!-- Core Pipeline Status Badges -->
[![Pipeline Status](https://img.shields.io/badge/MLOps__Pipeline-Passing-4c1?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline/actions)
[![Data Engine](https://img.shields.io/badge/Snowflake-Verified_Source-00A9E0?style=for-the-badge&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![Compute Engine](https://img.shields.io/badge/AWS_SageMaker-Nominal_Compute-FF9900?style=for-the-badge&logo=amazonsagemaker&logoColor=white)](https://aws.amazon.com/sagemaker/)

<!-- Architecture & Language Quality Badges -->
[![Python Version](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Architecture Pattern](https://img.shields.io/badge/Design_Pattern-Multi--Agent_Supervisor-blueviolet?style=flat-square&logo=diagrams.net&logoColor=white)](#system-design--architecture-flow-chart)
[![Infrastructure Strategy](https://img.shields.io/badge/Infrastructure-Ephemeral_Compute-8A2BE2?style=flat-square&logo=amazon-ec2&logoColor=white)](#architectural-breakdown)

<!-- Security, Validation & Code Quality Badges -->
[![Security Assessment](https://img.shields.io/badge/Security-SecOps_Validated-success?style=flat-square&logo=github&logoColor=white)](#q2-how-does-the-system-handle-security-and-authentication-vectors-securely-between-public-execution-layers-and-cloud-infrastructure)
[![Data Validation](https://img.shields.io/badge/Data_Validation-PSI_Gated-orange?style=flat-square&logo=pydantic&logoColor=white)](#q3-what-prevents-data-leakage-or-model-decay-when-processing-automated-streaming-updates)
[![License Model](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://choosealicense.com/licenses/mit/)


AWS-SageMaker-Snowflake-ML-PipelineAn autonomous, event-driven, production-grade MLOps orchestrator that decouples enterprise storage from high-performance training computing. The architecture features an internal multi-agent coordination layer executing telemetry auditing, dataset validation, statistical drift verification, and automatic model deployment cycles.🏛️ System Design & Architecture Flow ChartThis platform decouples storage compute (Snowflake Virtual Warehouses) from model training compute (AWS SageMaker Core Instances). It implements a stateful supervisor pattern that tracks structural dataset drift, triggers ephemeral infrastructure transformations, and writes operation ledger outputs via GitOps mechanisms back to source control.Plaintext[Enterprise Data Warehouse]           [MLOps Control Plane]           [High-Performance Compute]
   +-------------------+              +--------------------+              +--------------------+
   |                   |              |                    |              |                    |
   | Snowflake Stage   | ------------ | Snowflake Monitor  |              |                    |
   | Data Mutations    |  Metadata    | Agent              |              |                    |
   +-------------------+  Inspections +--------------------+              |                    |
             |                                  |                         |                    |
             | Data Dump                        | Retrain                 |                    |
             v                                  v                         |                    |
   +-------------------+              +--------------------+              |                    |
   |                   |              |                    |   Trigger    |                    |
   | Amazon S3 Bucket  | <----------- | SageMaker Ops      | -----------> | AWS SageMaker      |
   | (Feature Store)   |  Pull Data   | Agent              |              | Ephemeral Cluster  |
   +-------------------+              +--------------------+              +--------------------+
                                                |                                   |
                                                | Check Metrics                     | Export Model
                                                v                                   v
                                      +--------------------+              +--------------------+
                                      |                    |  Write Logs  |                    |
                                      | MLOps Supervisor   | -----------> | GitOps Ledger      |
                                      | State Machine      |              | (DailyLog.md)      |
                                      +--------------------+              +--------------------+
Architectural BreakdownData Telemetry: New micro-batches hit Snowflake tables. The SnowflakeMonitorAgent interrogates staging metadata using optimized analytical cursors, tracking volume spikes and statistical schema variants.Data Marshaling: Upon crossing batch thresholds, feature variables are mirrored to an intermediate, encrypted Amazon S3 cold storage bucket acting as an immutable Feature Store layer.Compute Allocation: The SageMakerOpsAgent allocates isolated, application-specific EC2 instances inside AWS SageMaker. The instances pull raw features out of S3, execute the distribution calculations, and terminate instantly upon model completion.State Consensus: The MLOpsSupervisor checks downstream objective variables against the current production model. If conditions match, it writes logs to DailyLog.md and signals deployment handlers.📊 Evaluation & Operational MetricsThe system monitors training efficiency, model quality, and infrastructure costs to prevent budget overruns during automated execution blocks.MetricTarget BaselineUpper Bound TriggerMitigation StrategyStatistical Feature Drift (PSI)$< 0.10$$\ge 0.20$Auto-trigger retraining on newer feature slicesModel Classification (ROC-AUC)$> 0.88$$< 0.85$Quarantine deployment; alert engineeringCompute Training Convergence$< 1200\text{s}$$> 3600\text{s}$Terminate task to eliminate cost overrun risksSnowflake Warehouse Ingestion Run$< 45\text{s}$$> 180\text{s}$Scale down warehouse layer; check query skew⚡ Quick Start InstructionsFollow these instructions to spin up the multi-agent control layer locally or within your development environments.Prerequisite ChecklistPython 3.11.x runtime installed locally.Access credentials for Snowflake (ACCOUNT, USER, PASSWORD).AWS IAM credentials configured with specific permissions for SageMaker execution and S3 read/write.Local Initialization SequenceClone the Repository:Bashgit clone https://github.com/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline.git
cd AWS-SageMaker-Snowflake-ML-Pipeline
Environment Assembly:Bashpython -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
Secure Environment Variables Configuration:Create a .env file at the root directory of your project:Code snippetSNOWFLAKE_USER="your_secure_username"
SNOWFLAKE_PASSWORD="your_secure_password"
AWS_ACCESS_KEY_ID="AKIAXXXXXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
Verify Application Configuration Targets:Open config/agent_config.yaml and verify your cloud account specifications, paths, identifiers, and performance barriers match your target parameters.Run the Simulation Script:Bashpython agents/supervisor.py
🧠 Extended Systems Engineering Q&AQ1: Why use independent, specialized agents over standard workflow schedulers like AWS Step Functions or Apache Airflow?Traditional workflow tools operate on rigid, hard-coded Directed Acyclic Graphs (DAGs). If a database step returns an unexpected type, the whole pipeline breaks down. This multi-agent setup uses a dynamic event loop.Each agent evaluates its own state context. If Snowflake experiences structural anomalies, the SnowflakeMonitorAgent quarantines ingestion and signals the Supervisor to modify upstream configurations—without crashing downstream instances or generating unnecessary cloud compute costs.Q2: How does the system handle security and authentication vectors securely between public execution layers and cloud infrastructure?This architecture isolates credentials. The GitHub runner does not store permanent cloud keys. Instead, it pulls short-lived tokens from your repo secrets into isolated runtime scopes.Furthermore, data traffic between Snowflake and AWS is completely isolated using encrypted channels. Database queries are limited to specific service roles, preventing SQL injection vulnerabilities.Q3: What prevents data leakage or model decay when processing automated streaming updates?The system uses strict validation gates. The SnowflakeMonitorAgent calculates the Population Stability Index (PSI) before moving data to S3. If the data distribution diverges sharply from the training baseline, the system flags a potential data anomaly.Additionally, new training passes require explicit validation passes against the baseline models. A newly trained model is only promoted if it beats the active production baseline in ROC-AUC performance.Q4: How is infrastructure spend optimized when using high-performance compute instances?We eliminate persistent servers. Snowflake virtual warehouses utilize an auto-suspend duration of exactly 60 seconds to avoid unnecessary costs during idle periods.On the AWS side, training is handled entirely by ephemeral clusters that spinning up only for the duration of the training loop. Once the model outputs its artifacts to S3, the underlying EC2 resources are immediately deallocated.
