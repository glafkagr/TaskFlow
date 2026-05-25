FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Δημιουργία φακέλου για uploads
RUN mkdir -p uploads

ENV FLASK_APP=wsgi.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
