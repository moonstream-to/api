# Moonstream architecture

Moonstream consists of:
1. A colder data store in which we store large amounts of transactional data and metadata directly
from various blockchains.
2. A warmer data store in which we store data that streams in very quickly, for example from the
Ethereum transaction pool. The data in the warm data store is not stored permanently. All data here
is removed after a certain data-specific time-to-live (TTL).
3. Crawlers which collect data from different blockchain related sources and insert them into either
the slow data store or the fast one.
4. The Moonstream API, which allows users to sign up to Moonstream, subscribe to different sources
of data in Moonstream, and serve their requests for this data.
5. The Moonstream frontend ([live](https://moonstream.to)) through which users can interact with
Moonstream in their browsers.
6. Moonstream client libraries through which users can interact with Moonstream from the programming
environment of their choice.

This document gives a brief explanation of the role of each of these components and points you to
more detailed information about whichever components you are particularly interested in.

It also tries to answer any questions you may have about why certain decisions/trade-offs were made.

## Data storage

[Codebase: `../db`](../db/)

### Fast vs. slow

Blockchains like Ethereum and Solana implement smart contract functionality by recording the state
of accounts on the blockchain at every block. This record of state grows over time. Ethereum state
already takes hundreds of gigabytes of storage. Solana state is even larger, and they host historical
state centrally on a Google BigTable instance.

Moonstream is an open source project, and we intend for people to host Moonstream themselves. We cannot
assume that someone hosting Moonstream has tons of cash to spend on high-quality storage (e.g. latest
generation SSD). The most cost-effective way to store the large amount of state data (without relying
on cloud object storage) is on a magnetic hard disk.

Although this makes storage cheaper, it makes it slower to read and write data from the data store.
Since we have some crawlers which collect volatile data, like the data in the Ethereum transaction pool,
we *also* need a fast storage layer that we can store and retrieve data from faster.

This is why we have two different classes of storage in Moonstream.

### Slow data store: Postgres

We use a Postgres database as the slow datastore. The code in the [`db/`](../db/) directory defines
the schema for this Postgres database as well as migrations that you can use to set up a similar
database yourself.

The [`db/`](../db/) directory contains:
1. A Python package called `moonstreamdb` which defines the database schema and can be used as a
Python library to interact with the data store.
2. [Alembic](https://alembic.sqlalchemy.org/en/latest/) migrations which can be used via the
[`alembic.sh`](../db/alembic.sh) shell script to run the migrations against a Postgres database
server.

The Ethereum blockchain crawler ([accessed through the `ethcrawler blocks` command](../crawlers/mooncrawl))
stores Ethereum state in the slow database.

We also have other crawlers (e.g. the CoinMarketCap crawler) which store address and transaction
metadata in the slow database. This is because the slow database is permanent whereas the fast database
is assumed to be ephemeral.

### Fast data store: Bugout

Since different crawlers store data in the fast data store using different schemas, we use [Bugout](https://bugout.dev)
as our fast data store with no extra assumptions about schema.

Bugout is open source and can be self-hosted as well from the following repositories:
1. [Brood](https://github.com/bugout-dev/brood) - For authentication
2. [Spire](https://github.com/bugout-dev/spire) - Data storage and access

Our Bugout instance also uses a Postgres database as the underlying data store. This Postgres server
is provisioned on high-throughput SSD.

The crawlers that use the fast data store write to a single Bugout journal using a write-only token.
Each crawler tags the data it writes with the type and any additional schema information.

The API reads from that journal using a read token. Queries are resolved using the tags that the crawlers created.

## Crawlers

[Codebase: `../crawlers`](../crawlers/)

Many of the Moonstream crawlers are written in Python. These are all packaged together in a single Python
package called [`mooncrawl`](../crawlers/mooncrawl/).

Crawlers can be written in any programming language - some programming languages may be more preferable
for certain kinds of data. For example, we plan to write our Solana crawlers in Rust because the Solana
library support for "Solana programs" (their version of smart contracts) is much better in their native
Rust.

The [Ethereum transaction pool crawler](../crawlers/ethtxpool/), for example, is written in Go.

## Moonstream API

[Codebase: `../backend`](../backend/)

The Moonstream API is written in Python and uses the [FastAPI framework](https://fastapi.tiangolo.com/).

API routes are defined in [`backend/moonstream/api.py`](../backend/moonstream/api.py), and that file
is the right entrypoint into understanding the API codebase.

The API uses [Bugout](https://bugout.dev) for authentication and to manage resources like user subscriptions
to different types of data.

It also defines [event providers](../backend/moonstream/providers/__init__.py), which are responsible for
retrieving data of each available type (e.g. `ethereum_blockchain`, `ethereum_txpool`, etc.) from the
fast and/or slow data stores and serving it to Moonstream users.

## Frontend

The Moonstream frontend is a [React](https://reactjs.org/) application. It uses the [Chakra UI](https://chakra-ui.com/)
component library and [react-query](https://react-query.tanstack.com/) to manage data.

## Client libraries

These are still under development. If you would like to build a Moonstream client library for your
favorite language, [reach out to @zomglings on Discord](https://discord.gg/K56VNUQGvA).

These are the languages we currently have libraries for:

### Python

This is a work in progress. [Pull request](https://github.com/bugout-dev/moonstream/pull/266).
