# moonstream

\[[Live at https://moonstream.to/](https://moonstream.to)\] | \[[Join us on Discord](https://discord.gg/pYE65FuNSz)\]

## What is Moonstream?

Moonstream makes tools that help people build, manage, and maintain their blockchain economies.

In order to provide this functionality, we build a lot of technology to crawl blockchains and makes sense of crawled transactions and events. This repository contains that code.

## Who uses Moonstream?

Game designers and economists, data scientists, smart contract developers, backend engineers, and teams managing loyalty programs for blockchain projects.

Some of our prominents customers:

1. [Laguna Games](https://laguna.games), makers of [Crypto Unicorns](https://cryptounicorns.fun)
2. [RealtyBits](https://realtybits.com)

## Free software

Proprietary technologies are not inclusive technologies, and we believe in inclusion.

All of our technology is open source. This repository contains all the code that powers
https://moonstream.to. The code is licensed with the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

You are and _will always be_ free to host your own instance of Moonstream.

## Architecture

This monorepo contains the following components:

1. [`frontend`](./frontend): A web frontend for Moonstream. Allows users to create dashboards and monitor the activity of accounts and smart contracts on multiple blockchains. Built in [React](https://reactjs.org/).
2. [`backend`'](./backend): The Moonstream API allows users to programmatically consume data about transactions and events taking place on blockchains crawled by Moonstream. Built in [Python](https://www.python.org/) using [Fast API](https://fastapi.tiangolo.com/).
3. [`crawlers`](./crawlers): This part of the code base contains workers which extract data from blockchains, transaction pools, and other sources. We have many crawlers and each crawler can utilize a different tech stack.
4. [`db`](./db): Moonstream stores blockchain data in [Postgres](https://www.postgresql.org/). This
   directory contains the code we use to manage the schema in our Postgres database. For sources that
   send higher volumes of data, we use a separate Postgres database and interface with it using
   [Bugout](https://bugout.dev).

### Installation and setup

#### Run server with Docker Compose

If you want to deploy Moonstream in isolation against live services, then docker compose is your choice!

- Run script `backend/configs/docker_generate_env.bash` which prepare for you:
  - `backend/configs/docker.moonstreamapi.env` with environment variables
- Run script `db/configs/docker_generate_env.bash` which prepare for you:
  - `db/configs/alembic.moonstreamdb.ini` with postgresql uri

```bash
./backend/configs/docker_generate_env.bash
./db/configs/docker_generate_env.bash
```

- Run local setup

```bash
docker-compose up --build
```

## Contributing

If you would like to contribute to Moonstream, please reach out to @zomglings on the [Moonstream Discord](https://discord.gg/pYE65FuNSz).
