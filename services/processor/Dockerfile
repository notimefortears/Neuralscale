FROM python:3.11-slim

WORKDIR /app

COPY services/processor/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY shared /app/shared
RUN pip install --no-cache-dir -e /app/shared

COPY services/processor/app /app/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app.main"]
