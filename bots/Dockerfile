# Install Browser, OS dependencies and Python modules
FROM public.ecr.aws/lambda/python:3.8

COPY bots_requirements.txt /tmp/requirements.txt
COPY install_browser.sh /tmp/

RUN yum install git curl -y -q

# Install Browsers
RUN /usr/bin/bash /tmp/install_browser.sh

# Install Python dependencies for function
RUN pip install --upgrade pip -q
RUN pip install -r /tmp/requirements.txt -q

# Remove not needed packages
RUN yum remove xz tar unzip bzip2 -y

# Create dirs
RUN mkdir /var/task/bots
RUN mkdir /var/task/bots/proxy

# Copy bots files to bots folder
COPY *.py /var/task/bots

# Copy manifest.json files to /tmp/bots/proxy/manifest.json,
# otherwise it's going to be readonly path
COPY proxy/manifest.json /var/task/bots/proxy/manifest.json

# Copy bot_settings.ini to bot_settings.ini, right beside app.py
COPY bot_settings_prod.ini /var/task/bot_settings.ini

# Copy app.py /var/task/app.py
COPY app.py /var/task/
CMD ["app.lambda_handler"]