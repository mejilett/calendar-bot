#Group 4: Allen Liu, Scarlet Mejia
FROM python:3.11-slim

WORKDIR /app

# just install python libraries
RUN pip install requests google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 pytz python-dateutil

COPY . .

CMD ["python3", "framework.py"]
