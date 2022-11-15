FROM python:3.9.15-slim-buster
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=5000"]
