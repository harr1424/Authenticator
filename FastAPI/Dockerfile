# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
ENV AWS_DEFAULT_REGION=us-west-2
ENV AWS_ACCESS_KEY_ID="REDACTED"
ENV AWS_SECRET_ACCESS_KEY="REDACTED"
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./main.py /app/main.py
EXPOSE 5555
CMD [ "uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5555" ]