FROM python:3.8.5-slim

COPY requirements.txt /requirements.txt 
RUN pip install -r requirements.txt

COPY main.py /main.py
COPY uploads /uploads
COPY database.db /database.db


ENTRYPOINT ["python main.py"]
