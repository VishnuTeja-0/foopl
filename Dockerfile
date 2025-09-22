FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip git docker.io

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

RUN git clone https://github.com/aldinokemal/go-whatsapp-web-multidevice.git /app/gowa

WORKDIR /app/gowa

RUN docker-compose up -d --build

WORKDIR /app

CMD ["python3", "-m", "app.py"]
