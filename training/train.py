# training/train.py
"""
SageMaker Training Job Launcher
---------------------------------
Submits a SageMaker Training job that runs src/train_script.py
inside a managed SKLearn container.
"""

import argparse
import boto3
import sagemaker
from sagemaker.sklearn.estimator import SKLearn


def launch_training_job(region, role_arn, input_s3, output_s3,
                        instance_type, instance_count, job_name):
    """Submit a SageMaker training job."""
    boto_session = boto3.Session(region_name=region)
    sm_session = sagemaker.Session(boto_session=boto_session)

    estimator = SKLearn(
        entry_point='src/train_script.py',
        role=role_arn,
        instance_type=instance_type,
        instance_count=instance_count,
        framework_version='1.0-1',
        py_version='py3',
        output_path=output_s3,
        sagemaker_session=sm_session,
        base_job_name=job_name,
        hyperparameters={
            'n_estimators': 100,
            'max_depth': 10,
            'random_state': 42,
        },
    )

    estimator.fit({'train': input_s3}, job_name=job_name)
    print(f"Training job '{job_name}' completed. Model at: {estimator.model_data}")
    return estimator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch SageMaker training job.')
    parser.add_argument('--region', required=True)
    parser.add_argument('--role-arn', required=True)
    parser.add_argument('--input_s3', required=True, help='S3 URI of processed training data')
    parser.add_argument('--output_s3', required=True, help='S3 URI for model artifacts')
    parser.add_argument('--instance_type', default='ml.m5.2xlarge')
    parser.add_argument('--instance_count', type=int, default=1)
    parser.add_argument('--job_name', required=True)
    args = parser.parse_args()

    launch_training_job(
        region=args.region,
        role_arn=args.role_arn,
        input_s3=args.input_s3,
        output_s3=args.output_s3,
        instance_type=args.instance_type,
        instance_count=args.instance_count,
        job_name=args.job_name,
    )
