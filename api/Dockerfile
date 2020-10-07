FROM python:3.7

LABEL description "Renderable Core API."
LABEL version "1.0.0"
LABEL maintainer "Danilo Peixoto <danilo@therenderable.com>"

WORKDIR /usr/src/api/
COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
