import json
import boto3

lambda_client = boto3.client('lambda', region_name='us-east-1')
for i in range(4):
    payload = json.dumps({'key': i}).encode()
    lambda_client.invoke(
        FunctionName='worker_bots',
        InvocationType='Event',
        LogType='Tail',
        ClientContext='string',
        Payload=payload)
