# AWS SageMaker + Snowflake ML Pipeline

[![CI](https://github.com/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline/branch/main/graph/badge.svg)](https://codecov.io/gh/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline)
[![License](https://img.shields.io/github/license/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline)](LICENSE)

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

---

## Installation & Quick Start

### Prerequisites

- Docker (≥ 19.x)  
- AWS credentials with permissions for SageMaker, S3, and IAM  
- Snowflake account + `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, and role with privileges  

### Clone & Build

```bash
git clone https://github.com/Trojan3877/AWS-SageMaker-Snowflake-ML-Pipeline.git
cd AWS-SageMaker-Snowflake-ML-Pipeline
