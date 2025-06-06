python training/train.py \
  --region us-east-1 \
  --role-arn arn:aws:iam::<your_account_id>:role/SageMakerRole \
  --input_s3 s3://<your-bucket>/processed-data/ \
  --output_s3 s3://<your-bucket>/models/ \
  --instance_type ml.m5.2xlarge \
  --instance_count 1 \
  --job_name fraud-detection-$(date +%Y%m%d%H%M%S)

python deployment/deploy.py \
  --region us-east-1 \
  --role-arn arn:aws:iam::<your_account_id>:role/SageMakerRole \
  --model_s3 s3://<your-bucket>/models/fraud-model.tar.gz \
  --endpoint_name fraud-endpoint \
  --instance_type ml.t2.medium \
  --initial_instance_count 1
