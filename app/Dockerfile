FROM python:3.13-alpine
ENV PATH="${PATH}:/root/.local/bin"
COPY ./src /app/src
COPY alembic /app/migrations
COPY alembic.ini /app/
COPY requirements.txt /app/
ENV PYTHONPATH /app/src
WORKDIR /app
RUN pip install -r ./requirements.txt

RUN chmod +x ./src/entry.sh
EXPOSE 8000