FROM python:3.11-alpine

# Install cron and dependencies
RUN apk add --no-cache curl bash ca-certificates \
    && pip install --no-cache-dir -r requirements.txt

# Copy your Python code
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Copy crontab
COPY crontab /etc/cron.d/worker-cron

# Make cron file executable and load it
RUN chmod 0644 /etc/cron.d/worker-cron \
    && crontab /etc/cron.d/worker-cron

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["crond", "-f", "-l", "2"]
