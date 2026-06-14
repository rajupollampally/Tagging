FROM python:3.11-slim

WORKDIR /app

COPY DevOps-Automation-Platform/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY DevOps-Automation-Platform/ ./DevOps-Automation-Platform/
WORKDIR /app/DevOps-Automation-Platform

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
