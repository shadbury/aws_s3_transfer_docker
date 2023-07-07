FROM python:3.9

RUN apt update -y
RUN apt install python3 pip -y
RUN pip install boto3 progressbar

WORKDIR /app

COPY app.py .
COPY functions.py .

ENTRYPOINT ["python", "gui.py"]