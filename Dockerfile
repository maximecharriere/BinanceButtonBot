# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD [ "python", "./Runner.py"]