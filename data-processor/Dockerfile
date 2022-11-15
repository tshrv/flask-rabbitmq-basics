FROM python:3.9.15-slim-buster
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["python3"]
CMD ["main.py"]
