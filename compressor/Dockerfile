FROM python:3.7

LABEL description "Renderable compressing worker."
LABEL version "1.0.0"
LABEL maintainer "Danilo Peixoto <danilopeixoto@outlook.com>"

WORKDIR /usr/src/resource-worker/
COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
