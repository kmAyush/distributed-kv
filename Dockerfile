FROM python:3.12.7

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install locust

EXPOSE 5000

CMD ["python", "router.py"]