FROM python:3.12.8-bookworm

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "app.py"]

