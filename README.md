# moonstream

\[[Live at https://moonstream.to/](https://moonstream.to)\] | \[[Join us on Discord](https://discord.gg/pYE65FuNSz)\]

## What is Moonstream?

Moonstream is a product which helps anyone participate in decentralized finance. From the most
sophisticated flash arbitrageurs to people looking for yield from currency that would otherwise lie
dormant in their exchange accounts.

Moonstream users can subscribe to events from any blockchain - from the activity of specific accounts
or smart contracts to updates about general market movements. This information comes from the blockchains
themselves, from their mempools/transaction pools, and from centralized exchanges, social media, and
the news. This forms a stream of information tailored to their specific needs.

They can use this information to execute transactions directly from the Moonstream frontend or they
can set up programs which execute (on- or off-chain) when their stream meets certain conditions.

## Who uses Moonstream?

1. **Development teams deploying decentralized applications.** They use Moonstream to analyze how
   users are calling their dapps, and set up alerts for suspicious activity.
2. **Algorithmic funds.** They use Moonstream to execute transactions directly on-chain under
   prespecified conditions.
3. **Crypto traders.** They use Moonstream to evaluate trading strategies based on data from
   centralized exchanges, the blockchain, and the transaction pool.

## Free software

Proprietary technologies are not inclusive technologies, and we believe in inclusion.

All of our technology is open source. This repository contains all the code that powers
https://moonstream.to. The code is licensed with the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

You are and _will always be_ free to host your own instance of Moonstream.

## Architecture

This monorepo contains the following components:

1. [`frontend`](./frontend): A web frontend for Moonstream. Allows users to perform API operations
   through a visual interface. The frontend also offers charting and analysis functionality. Built
   in [React](https://reactjs.org/).
2. [`backend`'](./backend): The Moonstream API. This portion of the code base implements a REST API
   through which users can manage the events that show up in their stream and actually consume their
   stream data. Built in [Python](https://www.python.org/) using [Fast API](https://fastapi.tiangolo.com/).
3. [`crawlers`](./crawlers): This part of the code base contains workers which extract data from
   blockchains, transaction pools, and other sources. Currently contains a single [Python](https://www.python.org/)
   package but we will soon be addding crawlers implemented in other languages: [Go](https://golang.org/),
   [Rust](https://www.rust-lang.org/)), and [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).
4. [`db`](./db): Moonstream stores blockchain data in [Postgres](https://www.postgresql.org/). This
   directory contains the code we use to manage the schema in our Postgres database. For sources that
   send higher volumes of data, we use a separate Postgres database and interface with it using
   [Bugout](https://bugout.dev). For more information on how that data is processed, check how the API
   inserts events from those sources into a stream.

### Installation and setup

#### Run server with Docker Compose

If you want to deploy Moonstream in isolation against live services, then docker compose is your choice!

- Run script `backend/configs/docker_generate_env.sh` which prepare for you:
  - `backend/configs/docker.moonstreamapi.env` with environment variables
- Run script `db/configs/docker_generate_env.sh` which prepare for you:
  - `db/configs/alembic.moonstreamdb.ini` with postgresql uri

```bash
./backend/configs/docker_generate_env.sh
./db/configs/docker_generate_env.sh
```

- Run local setup

```bash
docker-compose up --build
```

## Contributing

If you would like to contribute to Moonstream, please reach out to @zomglings on the [Moonstream Discord](https://discord.gg/pYE65FuNSz).
