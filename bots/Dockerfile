# Install Browser, OS dependencies and Python modules
FROM public.ecr.aws/lambda/python:3.8

COPY bots_requirements.txt /tmp/requirements.txt

RUN yum install git -y

# Install Python dependencies for function
RUN pip install --upgrade pip -q
RUN pip install -r /tmp/requirements.txt -q

# Remove not needed packages
RUN yum remove xz tar unzip bzip2 -y

# Copy function code
COPY *.py /var/task/
CMD ["app.lambda_handler"]