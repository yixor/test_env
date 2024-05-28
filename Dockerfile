    FROM python:3.11.9-alpine3.20

    WORKDIR /app

    COPY . /app

    RUN apk update && apk upgrade && apk add --no-cache gcc musl-dev linux-headers

    RUN python -m pip install --upgrade pip

    RUN pip install --no-cache-dir -r requirements.txt

    ENV DB_URL=postgresql://iam:123123@postgres:5432/test HOST_ADDRESS=0.0.0.0 \
    PORT=8000 DATA_PATH=/data/ REDIS_HOST=redis REDIS_PORT=6379 REDIS_DB=0

    RUN python -m compileall /app

    CMD ["python", "main.py"]