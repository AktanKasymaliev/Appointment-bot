FROM python:3.8

RUN pip3 install --upgrade pip

WORKDIR /config

COPY ./webservice-requirements.txt ./
COPY ./settings.ini ./settings.ini
COPY ./entrypoint.sh ./
RUN chmod +x entrypoint.sh
RUN pip3 install -r webservice-requirements.txt

COPY . .

# Collect static files
RUN python3 manage.py collectstatic --no-input

ENTRYPOINT ["/config/entrypoint.sh"]