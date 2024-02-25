FROM python:3.9-slim

WORKDIR /app

COPY app.py requirements.txt ./
RUN pip install -r requirements.txt
RUN apt update && apt install -y curl

CMD ["python", "app.py"]
