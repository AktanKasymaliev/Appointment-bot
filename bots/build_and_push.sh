# Log in to AWS Elastic Container Registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 697552332837.dkr.ecr.us-east-1.amazonaws.com

# Build a container
docker build -t worker_bots .
# Put a tag
docker tag worker_bots:latest 697552332837.dkr.ecr.us-east-1.amazonaws.com/worker_bots:latest
# Push the container to the AWS Elastic Container Registry
docker push 697552332837.dkr.ecr.us-east-1.amazonaws.com/worker_bots:latest
# update function code
aws lambda update-function-code --region us-east-1 --function-name worker_bots --image-uri 697552332837.dkr.ecr.us-east-1.amazonaws.com/worker_bots:latest
