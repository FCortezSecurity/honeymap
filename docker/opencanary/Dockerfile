FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir opencanary
RUN mkdir -p /var/log/opencanary /etc/opencanaryd
CMD ["opencanaryd", "--dev"]