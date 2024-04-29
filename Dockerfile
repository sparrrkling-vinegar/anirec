FROM ubuntu:focal

WORKDIR /anirec

RUN apt -y update && \
    apt install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt -y install python3.11 python3-pip && \
    apt-get install -y sqlcipher libsqlcipher-dev python-dev python3-dev python3.11-dev && \
    python3 -m pip install --upgrade pip  && \
    pip3 install poetry

COPY . .

RUN poetry install --no-root

ENTRYPOINT ["sh", "-c", "python3 -m poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]
