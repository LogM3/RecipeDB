FROM python:3.7-slim
WORKDIR /app
COPY foodgram/requirements.txt .
RUN apt-get update && apt-get install -y pkg-config libcairo2-dev gcc
RUN pip3 install -r requirements.txt --no-cache-dir
COPY foodgram .
RUN python manage.py collectstatic --no-input
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]