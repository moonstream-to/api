![github read me header](https://user-images.githubusercontent.com/8016073/203381867-f7b56861-04ca-4ae4-a5e6-53e97804817a.png)

# moonstream

[Website](https://moonstream.to)

[Join our Discord](https://discord.gg/pYE65FuNSz)

## What is Moonstream?

Moonstream creates economic infrastructure for web3 projects with a focus on blockchain games. 

This repository contains Moonstream's complete data analysis stack. The emphasis of it is on collecting actionable data related to the blockchain. The repository contains:

1. Database management tools
2. Blockchain node management tools
3. Blockchain data crawlers
4. Access-controlled API which exposes collected data

## Important resources
1. [Documentation](https://docs.moonstream.to/)
2. [Status page](https://moonstream.to/status/)
3. [On-chain mechanics](https://github.com/bugout-dev/engine)
4. [How to create a dashboard to analyze a smart contract?](https://voracious-gerbil-120.notion.site/Creating-dashboard-for-a-smart-contract-288b1bfa64984b109b79895f69129fce)

## Who uses Moonstream?

People from different backgrounds who are interested in data, crypto and code.
Moonstream tools are often used by game designers and economists, data scientists, smart contract developers, backend engineers, and teams managing loyalty programs for blockchain projects.

Some projects currently using Moonstream:

1. [Laguna Games](https://laguna.games), makers of [Crypto Unicorns](https://cryptounicorns.fun)
2. [Game7](https://game7.io)
3. [Champions Ascension](https://www.champions.io/)

Please read [the Game Master's Guide to Moonstream Solutions](https://docs.google.com/document/d/1mjfF8SgRrAZvtCVVxB2qNSUcbbmrH6dTEYSMfHKdEgc/view) if you want to know how Moonstream tools are applied in web3 games. 

[Moonworm tool](https://github.com/bugout-dev/moonworm) is used to build datasets of on-chain data related to market activity. The dataset with on-chain activity from the Ethereum NFT market (April 1 to September 25, 2021) is available [on Kaggle](https://www.kaggle.com/datasets/simiotic/ethereum-nfts). The full report on it is published on [GitHub](https://github.com/bugout-dev/moonstream/blob/main/datasets/nfts/papers/ethereum-nfts.pdf). 

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

We are working on contributing guidelines. In the meantime, please reach out to @zomglings on the [Moonstream Discord](https://discord.gg/pYE65FuNSz).
