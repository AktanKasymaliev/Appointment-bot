### Configure async invokation

```bash
aws lambda put-function-event-invoke-config --region us-east-1 --function-name worker_bots \
--maximum-event-age-in-seconds 3600 --maximum-retry-attempts 2
```

### Configure async AWS SNS messaging (for testing only)

```bash
aws lambda update-function-event-invoke-config --region us-east-1 --function-name worker_bots \
--destination-config '{"OnFailure":{"Destination": "arn:aws:sns:us-east-1:697552332837:worker_bots.fifo"}}'

aws lambda update-function-event-invoke-config --region us-east-1 --function-name worker_bots \
--destination-config '{"OnSuccess":{"Destination": "arn:aws:sns:us-east-1:697552332837:worker_bots.fifo"}}'
```

### Test run 3 parallel function instances

```bash
aws lambda invoke --region us-east-1 \
  --function-name worker_bots \
      --invocation-type Event \
          --cli-binary-format raw-in-base64-out \
              --payload '{ "key": "value1" }' response.json && aws lambda invoke --region us-east-1 \
  --function-name worker_bots \
      --invocation-type Event \
          --cli-binary-format raw-in-base64-out \
              --payload '{ "key": "value2" }' response.json && aws lambda invoke --region us-east-1 \
  --function-name worker_bots \
      --invocation-type Event \
          --cli-binary-format raw-in-base64-out \
              --payload '{ "key": "value3" }' response.json
```
