FROM python:3.10
WORKDIR /app
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir requests
COPY . .
ENTRYPOINT [ "python3", "main.py" ]
