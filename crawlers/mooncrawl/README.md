# Moonstream Crawlers

## Installation

(Use Python 3)

```bash
pip install -e .
```

### Database access and environment variables

Make sure that the `MOONSTREAM_DB_URI` environment variable is set as a Postgres connection string.

For a sample, view [`sample.env`](./sample.env).

## Crawlers

### Ethereum Signature Database

This crawler retrieves Ethereum function signatures from the Ethereum Signature Database at
[https://www.4byte.directory](https://www.4byte.directory).

#### Crawling ESD function signatures

```bash
python -m mooncrawl.esd --interval 0.3 functions
```

#### Crawling ESD event signatures

```bash
python -m mooncrawl.esd --interval 0.3 events
```

### Ethereum contract registrar

This crawler scans new transactions for smart contract deployments and retrieves their deployment
addresses from transaction receipts.

To run this crawler:

```bash
python -m mooncrawl.cli ethcrawler contracts update
```

Output is JSON list of pairs `[..., (<transaction_hash>, <contract_address>), ...]`, so you can pipe to `jq`:

```bash
python -m mooncrawl.cli ethcrawler contracts update | jq .
```

You can also specify an output file:

```bash
python -m mooncrawl.cli ethcrawler contracts update -o new_contracts.json
```
