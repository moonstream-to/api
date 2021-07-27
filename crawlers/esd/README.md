# Crawler: Ethereum Signature Database

This crawler retrieves Ethereum function signatures from the Ethereum Signature Database at
[https://4byte.directory](https://4byte.directory).

### Installation

(Use Python 3)

```bash
pip install -r requirements.txt
```

### Database access

Make sure that the `EXPLORATION_DB_URI` environment variable is set as a Postgres connection string.

For a sample, view [`sample.env`](./sample.env).

### Crawling ESD function signatures

```bash
python esd.py --interval 0.3 functions
```

### Crawling ESD event signatures

```bash
python esd.py --interval 0.3 events
```