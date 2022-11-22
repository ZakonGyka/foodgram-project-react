FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -U --force-reinstall pip && pip3 install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
