FROM python:alpine

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5656

COPY . .

CMD ["python","-u","server.py"]