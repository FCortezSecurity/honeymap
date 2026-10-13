FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY dashboard ./dashboard
COPY run_ingest.py .
CMD ["python", "run_ingest.py", "/data/logs/opencanary.log", "--follow"]