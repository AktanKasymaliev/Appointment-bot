import json
import boto3

# This is a test file which is used for reference.
# TODO(murat): remove this

# lambda_client = boto3.client('lambda', region_name='us-east-1')
# for i in range(1):
#     payload = json.dumps({'key': i}).encode()
#     lambda_client.invoke(
#         FunctionName='worker_bots',
#         InvocationType='Event',
#         LogType='Tail',
#         ClientContext='string',
#         Payload=payload)

from bots.app import lambda_handler
lambda_handler({}, None)