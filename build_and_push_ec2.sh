aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 697552332837.dkr.ecr.us-east-1.amazonaws.com
docker build -f Dockerfile.bots -t custom_esc_image:latest .
docker tag custom_esc_image:latest 697552332837.dkr.ecr.us-east-1.amazonaws.com/custom_esc_image:latest
docker push 697552332837.dkr.ecr.us-east-1.amazonaws.com/custom_esc_image:latest
