# Quantifiable Metrics

Below are the key metrics for both the ML model and the end-to-end pipeline. Wherever possible, we give **absolute numbers** (e.g., minutes, seconds, USD).

---

## 1. Model‐Performance Metrics

| Metric            | Value     | Notes                                              |
|-------------------|-----------|----------------------------------------------------|
| Training Dataset  | 50,000 rows | Raw transaction records used for training          |
| Validation Set    | 10,000 rows | Held-out for early stopping and hyperparam tuning |
| Test Set          | 15,000 rows | Final evaluation                                   |
| ROC AUC           | 0.962     | On test set (threshold at 0.5 probability)         |
| Precision @ 0.5   | 0.915     | High‐precision threshold for fraud alerts          |
| Recall @ 0.5      | 0.872     | Captures 87.2% of fraud cases                      |
| F1 Score @ 0.5    | 0.893     | Harmonic mean of precision & recall                |
| PR AUC           | 0.941     | Precision‐Recall area under curve                  |
| False Positive Rate | 0.023  | FPR @ model threshold = 0.5                         |
| False Negative Rate | 0.128  | FNR @ model threshold = 0.5                         |
| Train Time         | 8 min 37 sec | On a ml.m5.xlarge instance (4 vCPU, 16 GB RAM)     |
| Inference Latency  | 120 ms     | Single‐record prediction on ml.t2.medium           |
| Model Size         | 85 MB      | Serialized XGBoost model artifact                  |

> **Note:**  
> – “@ 0.5” refers to the probability threshold used (you may have chosen a different value).  
> – Train Time measured from SageMaker log: `StartTime=…` to `EndTime=…`.  
> – Inference Latency averaged over 100 randomly sampled test records.

---

## 2. Pipeline‐Performance Metrics

| Stage                        | Environment                  | Duration / Throughput           | Cost Estimate (USD)       |
|------------------------------|------------------------------|---------------------------------|---------------------------|
| Data Ingestion → Snowflake  | Snowflake X-Small warehouse | Processed 650,000 rows in 3m 12s | \$0.15 (compute only)      |
| Feature Engineering (SageMaker Processing Job) | ml.m5.large (2 vCPU, 8 GB) | Completed in 5m 45s (50k rows) | \$0.72                    |
| Model Training (SageMaker Training Job) | ml.m5.2xlarge (8 vCPU, 32 GB) | Completed in 8m 37s             | \$1.85                    |
| Model Hosting (SageMaker Endpoint) | ml.t2.medium (2 vCPU, 4 GB) | Average cold start 3.2 s         | \$0.08/hour (provisioned) |
| API Serving (Flask on EC2 t3.medium) | t3.medium (2 vCPU, 4 GB)    | 120 ms latency / ~130 req/s     | \$0.0376/hour + \$0.10 EBS |
| S3 Storage (model/artifacts) | Standard S3 bucket          | —                                | \$0.023/GB-month          |
| Total Monthly Cost (approx.) | —                            | —                                | ~\$50/month (for dev env)  |

> **How these were measured:**  
> 1. **Snowflake ingestion**: Ran `COPY INTO …` on an X-Small warehouse, timing logged by Snowflake Query History.  
> 2. **Processing & Training**: Taken directly from SageMaker job logs (`billable_seconds * instance_hourly_rate`).  
> 3. **Endpoint**: Deployed one ml.t2.medium instance in us-east-1; invoked 1000 test calls via a simple script and averaged the latency.  
> 4. **Flask API**: Benchmarked using `ab` (ApacheBench) with `ab -n 500 -c 50 http://<ec2-ip>:5000/predict`.  
> 5. **Cost**: Based on AWS on-demand pricing at the time of measurement (e.g., ml.m5.2xlarge = \$0.46/hour).

---

## 3. Cost vs. Accuracy Trade‐offs (Optional)

| Instance Type      | Train Time | Train Cost | Inference Latency | Inference Cost/hour | Test AUC |
|--------------------|------------|------------|-------------------|---------------------|----------|
| ml.m5.large        | 11 min     | \$1.10     | —                 | —                   | 0.947    |
| ml.m5.2xlarge      | 8 min 37 sec| \$1.85    | 120 ms            | —                   | 0.962    |
| ml.m5.4xlarge      | 6 min 12 sec| \$3.60    | 90 ms             | —                   | 0.963    |
| endpoint ml.t2.medium | —       | —          | 120 ms            | \$0.08/hour         | —        |
| endpoint ml.m5.large    | —       | —          | 60 ms             | \$0.15/hour         | —        |

> **Insight:**  
> – Upgrading to ml.m5.4xlarge shaves ~2 min off training (at 95% higher cost) but only improves AUC by ~~0.001.  
> – For inference, ml.m5.large halves latency compared to ml.t2.medium at ~2× cost.

---

**Once you’ve filled in your actual numbers** and saved `docs/metrics.md`, commit and push it:

```bash
git add docs/metrics.md
git commit -m "Add quantifiable metrics (model & pipeline) in docs/metrics.md"
git push
