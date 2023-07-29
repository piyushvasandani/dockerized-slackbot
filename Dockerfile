FROM python:3.9-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY .env /app/.env
COPY . .

EXPOSE 8080

CMD [ "flask", "run","--host","0.0.0.0","--port","8080"]

