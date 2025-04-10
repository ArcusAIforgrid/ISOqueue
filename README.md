# Interconnection Queue Dashboard

Streamlit dashboard + scheduler for U.S. ISO interconnection queues.

## Usage
```bash
git clone ...
cd ISOqueue
streamlit run app.py
```

## Schedule Daily Update
```cron
0 6 * * * /usr/bin/python3 /path/to/update.py >> /var/log/queue_update.log 2>&1
```

## Docker
```bash
docker build -t isoqueue .
docker run -p 8501:8501 isoqueue
```