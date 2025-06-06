from flask import Flask, request, jsonify
import boto3
import json
import os

app = Flask(__name__)
sm_client = boto3.client(
    "sagemaker-runtime", 
    region_name=os.environ["AWS_REGION"]
)
ENDPOINT_NAME = os.environ["SAGEMAKER_ENDPOINT_NAME"]

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.json  # e.g., {"transaction_amount": 129.50, ...}
    response = sm_client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=json.dumps(payload)
    )
    result = json.loads(response["Body"].read().decode())
    return jsonify({"fraud_probability": result[0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
