FROM python:3.12.2-alpine3.19

WORKDIR /anirec
RUN adduser -D user && chown -R user /anirec

COPY --chown=user:user . .

USER user

RUN pip install poetry
RUN export PATH=$PATH:/home/user/.local/bin
RUN python -m poetry install --no-root

ENTRYPOINT ["sh", "-c", "python -m poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]
