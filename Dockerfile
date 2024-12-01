# docker compose up --build

FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Define entry point
CMD ["python", "pre-commit-server.py"]
