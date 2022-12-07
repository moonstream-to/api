![github read me header](https://user-images.githubusercontent.com/8016073/203381867-f7b56861-04ca-4ae4-a5e6-53e97804817a.png)

# moonstream

[Website](https://moonstream.to)

[Join our Discord](https://discord.gg/pYE65FuNSz)

## What is Moonstream?

Moonstream creates comprehensive economic infrastructure for web3 projects with a focus on blockchain games. 
To do this, we created data analytics tools which help people gather actionable data; plus, we are continually creating on-chain mechanics, so that users can act on the data gathered. 

We build a lot of technology to crawl blockchains and make sense of crawled transactions and events. This repository contains that code.

## Important resources
1. [Documentation](https://docs.moonstream.to/)
2. [Status page](https://moonstream.to/status/)
3. [On-chain mechanics](https://moonstream.to/features/)
4. [How to create a dashboard to analyze a smart contract?](https://voracious-gerbil-120.notion.site/Creating-dashboard-for-a-smart-contract-288b1bfa64984b109b79895f69129fce)

## Who uses Moonstream?

People from different backgrounds who are interested in data, crypto and code.
We know especially well how Moonstream tools can benefit web3 games, and some of the people who can use the tools to advance their projects are game designers and economists, data scientists, smart contract developers, backend engineers, and teams managing loyalty programs for blockchain projects.

Some of our prominents customers:

1. [Laguna Games](https://laguna.games), makers of [Crypto Unicorns](https://cryptounicorns.fun)
2. [RealtyBits](https://realtybits.com)
3. [Champions Ascension](https://www.champions.io/)

To know more about our web3 games related use cases please read [the Game Master's Guide to Moonstream Solutions](https://docs.google.com/document/d/1mjfF8SgRrAZvtCVVxB2qNSUcbbmrH6dTEYSMfHKdEgc/view).

Our [Moonworm tool](https://github.com/bugout-dev/moonworm) is used to build datasets of on-chain data related to market activity. We have a dataset with on-chain activity from the Ethereum NFT market (April 1 to September 25, 2021) [on Kaggle](https://www.kaggle.com/datasets/simiotic/ethereum-nfts). And [here](https://github.com/bugout-dev/moonstream/blob/main/datasets/nfts/papers/ethereum-nfts.pdf) is our full report on it. We’re working on V2 of the dataset above, you can collaborate with us. Reach out to @zomglings on the [Moonstream Discord](https://discord.gg/pYE65FuNSz) if interested.  

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
