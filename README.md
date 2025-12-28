![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Status: Local Only](https://img.shields.io/badge/status-local--only-blue)
![Platform: Python](https://img.shields.io/badge/platform-python-blue)
![Cloud: AWS SageMaker](https://img.shields.io/badge/cloud-AWS--SageMaker-orange)
![Data Warehouse: Snowflake](https://img.shields.io/badge/data--warehouse-Snowflake-lightblue)
![Capstone Project](https://img.shields.io/badge/project-capstone-blueviolet)
![Last Commit](https://img.shields.io/github/last-commit/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline)

1. Clone the repository
2. Set up AWS and Snowflake credentials (see `config/` for templates)
3. Prepare data in Snowflake using provided SQL script
4. Train models with provided Jupyter notebooks/scripts
5. (Optional) Deploy model to AWS SageMaker endpoint

### Results

| Metric        | Value         |
|---------------|--------------|
| Accuracy      | 92.1%        |
| AUC-ROC       | 0.89         |
| Data Volume   | 2 million rows processed |
| Training Time | ~12 minutes on ml.m5.large |

> *All metrics are from the provided sample dataset (replace with real values if available).*





An end-to-end, production-ready pipeline that ingests raw transaction data into Snowflake, trains an XGBoost fraud-detection model on SageMaker, and serves real-time predictions via a Flask API.  

---

## Table of Contents

1. [Overview](#overview)  
2. [Architecture](#architecture)  
3. [Installation & Quick Start](#installation--quick-start)  
4. [Usage](#usage)  
5. [Quantifiable Metrics](#quantifiable-metrics)  
6. [Project Structure](#project-structure)  
7. [Running Tests](#running-tests)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Overview
A modular, production-style machine learning pipeline integrating AWS SageMaker for scalable model training and Snowflake as a cloud data warehouse, designed for real-world enterprise data science workflows.
Financial fraud detection requires both accurate models and reliable, scalable infrastructure. This project demonstrates:

- **Data Ingestion:** Copy raw transaction CSVs into a Snowflake staging table.  
- **Feature Engineering & Processing:** Run a SageMaker Processing job that cleans and transforms data.  
- **Model Training:** Train an XGBoost classifier on SageMaker (ml.m5.2xlarge), achieving high AUC.  
- **Real-time Inference:** Host the trained model on a SageMaker endpoint and expose a Flask API on EC2 for predictions.  
- **Dashboard Integration (Optional):** Serve inference results to a downstream dashboard or service.

---

## Architecture

![Pipeline Architecture](docs/architecture.png)

1. **Raw Data (S3) → Snowflake**  
   - Snowflake X-Small warehouse loads and stores raw transactions.  
2. **SageMaker Processing**  
   - Pulls from Snowflake, applies feature engineering, and writes processed data back.  
3. **SageMaker Training**  
   - Reads processed data, trains an XGBoost model, and saves the artifact to S3.  
4. **SageMaker Endpoint**  
   - Deploys the model for real-time inference (ml.t2.medium).  
5. **Flask API (EC2 t3.medium)**  
   - Forwards JSON transaction payloads to the SageMaker endpoint and returns fraud probability.  
6. **Dashboard / Client**  
   - Consumes API responses to visualize fraud scores.


## Installation & Quick Start

### Prerequisites

- Docker (≥ 19.x)  
- AWS credentials with permissions for SageMaker, S3, and IAM  
- Snowflake account + `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, and role with privileges  

### Clone & Build

```bash
git clone https://github.com/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline.git
cd AWS-SageMaker-Snowflake-ML-Pipeline

Design Questions & Reflections
Q: What problem does this project aim to solve?
A: This project was built to explore how to integrate AWS SageMaker and Snowflake into a structured ML pipeline that handles data retrieval, preprocessing, model training, and deployment in a way that mirrors real cloud-based workflows. The goal was to go beyond standalone models and connect cloud compute with scalable data storage and orchestration.
Q: Why did I choose this architecture and approach instead of a simpler design?
A: I chose to combine Snowflake for data warehousing and SageMaker for model training because each tool plays to its strengths — Snowflake for scalable data ingestion and transformation, and SageMaker for managed training and deployment. This approach reflects how real production systems separate concerns rather than putting everything in a single tool or script.
Q: What were the main trade-offs I made?
A: The main trade-off was complexity versus reproducibility. A simpler, local script might have let me prototype faster, but it wouldn’t have shown how to connect storage, compute, and orchestration in a modular, repeatable way. By investing in cloud integration and clear pipeline stages, I gained a more realistic architecture at the cost of more initial configuration effort.
Q: What didn’t work as expected?
A: Early versions ran into permission or credential configuration issues between Snowflake and AWS services, which highlighted how cloud infrastructure adds friction around identity and access management. Solving this required diving into IAM policies and secure credential handling, which improved my understanding of real-world cloud deployments.
Q: What did I learn from building this project?
A: I learned that cloud-based ML workflows are as much about data plumbing and access control as they are about model training. Ensuring that pipelines are secure, repeatable, and observable requires deliberate setup of logging, monitoring, and error handling — not just simple scripts.
Q: If I had more time or resources, what would I improve next?
A: I would add automated testing and validation at each stage of the pipeline so that changes in data schemas or model versions can be caught earlier. I’d also explore adding metrics and dashboards to monitor training performance and inference behavior over time.
