FROM python:3.8-slim-buster

# Update packages and
# prepare alembic for docker compose setup
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir psycopg2-binary alembic

WORKDIR /usr/src/moonstreamdb

COPY . /usr/src/moonstreamdb

# Install Moonstream DB package
RUN pip3 install --no-cache-dir -e .

ENTRYPOINT ["./migrate.sh"]