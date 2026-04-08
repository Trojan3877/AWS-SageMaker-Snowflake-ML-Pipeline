# deployment/deploy.py
"""
SageMaker Model & Endpoint Deployment
--------------------------------------
Registers the trained model artifact with SageMaker and deploys it
as a real-time inference endpoint.
"""

import argparse
import boto3
import sagemaker
from sagemaker.sklearn.model import SKLearnModel


def deploy_model(region, role_arn, model_s3_uri, endpoint_name,
                 instance_type, initial_instance_count):
    """
    Create a SageMaker SKLearn model from an S3 artifact and deploy it.
    """
    boto_session = boto3.Session(region_name=region)
    sm_session = sagemaker.Session(boto_session=boto_session)

    model = SKLearnModel(
        model_data=model_s3_uri,
        role=role_arn,
        framework_version='1.0-1',
        py_version='py3',
        sagemaker_session=sm_session,
    )

    predictor = model.deploy(
        initial_instance_count=initial_instance_count,
        instance_type=instance_type,
        endpoint_name=endpoint_name,
    )
    print(f"Endpoint '{endpoint_name}' deployed successfully.")
    return predictor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy fraud-detection model to SageMaker.')
    parser.add_argument('--region', required=True)
    parser.add_argument('--role-arn', required=True)
    parser.add_argument('--model_s3', required=True, help='S3 URI of model.tar.gz')
    parser.add_argument('--endpoint_name', required=True)
    parser.add_argument('--instance_type', default='ml.t2.medium')
    parser.add_argument('--initial_instance_count', type=int, default=1)
    args = parser.parse_args()

    deploy_model(
        region=args.region,
        role_arn=args.role_arn,
        model_s3_uri=args.model_s3,
        endpoint_name=args.endpoint_name,
        instance_type=args.instance_type,
        initial_instance_count=args.initial_instance_count,
    )
