# Metadata Crawler Architecture

## Overview
The metadata crawler is designed to fetch and store metadata for NFTs (Non-Fungible Tokens) from various blockchains. It supports both traditional database TokenURI view methods queries and Spire journal-based job configurations, with the ability to handle both v2 and v3 database structures.


## Core Components

### 1. Update Strategies

#### Leak-Based Strategy (Legacy v2)
- Uses probabilistic approach to determine which tokens to update
- Controlled by `max_recrawl` parameter
- Suitable for large collections with infrequent updates

#### SQL-Based Strategy (v3)
- Uses SQL queries to determine which tokens need updates
- More precise tracking of token updates
- Better suited for active collections

### 2. Database Connections

The crawler supports multiple database connection strategies:
- Default Moonstream database connection
- Custom database URI via `--custom-db-uri`
- Per-customer instance connections (v3)
  ```json
  {
    "customer_id": "...",
    "instance_id": "...",
    "blockchain": "ethereum",
    "v3": true
  }
  ```

### 3. Job Configuration
Jobs can be configured in two ways:
- Through Spire journal entries with tags `#metadata-job #{blockchain}`
- Direct database queries (legacy mode) using TokenURI view method
Example Spire journal entry:
```json
{
    "type": "metadata-job",
    "query_api": {
        "name": "new_tokens_to_crawl",
        "params": {
            "address": "0x...",
            "blockchain": "ethereum"
        }
    },
    "contract_address": "0x...",
    "blockchain": "ethereum",
    "update_existing": false,
    "v3": true,
    "customer_id": "...", // Optional, for custom database
    "instance_id": "..." // Optional, for custom database
}
```

### 2. Data Flow
1. **Token Discovery**
   - Query API integration for dynamic token discovery
   - Database queries for existing tokens
   - Support for multiple addresses per job

2. **Metadata Fetching**
   - Parallel processing with ThreadPoolExecutor
   - IPFS gateway support
   - Automatic retry mechanism
   - Rate limiting and batch processing

3. **Storage**
   - Supports both v2 and v3 database structures
   - Batch upsert operations
   - Efficient cleaning of old labels

### 3. Database Structures

v2:
```python
{
    "label": METADATA_CRAWLER_LABEL,
    "label_data": {
        "type": "metadata",
        "token_id": "...",
        "metadata": {...}
    },
    "block_number": 1234567890
    "block_timestamp": 456
}
```

v3:
```python
{
    "label": METADATA_CRAWLER_LABEL,
    "label_type": "metadata",
    "label_data": {
        "token_id": "...",
        "metadata": {...}
    },
    "address": "0x...",
    "block_number": 123,
    "block_timestamp": 456,
    "block_hash": "0x..."
}

```

## Key Features

1. **Flexible Token Selection**
   - Query API integration
   - Support for multiple addresses
   - Configurable update strategies

2. **Efficient Processing**
   - Batch processing
   - Parallel metadata fetching
   - Optimized database operations

3. **Error Handling**
   - Retry mechanism for failed requests
   - Transaction management
   - Detailed logging

4. **Database Management**
   - Efficient upsert operations
   - Label cleaning
   - Version compatibility (v2/v3)

## Usage

### CLI Options

```bash
metadata-crawler crawl \
--blockchain ethereum \
--commit-batch-size 50 \
--max-recrawl 300 \
--threads 4 \
--spire true \
--custom-db-uri "postgresql://..." # Optional
```
### Environment Variables
- `MOONSTREAM_ADMIN_ACCESS_TOKEN`: Required for API access
- `METADATA_CRAWLER_LABEL`: Label for database entries
- `METADATA_TASKS_JOURNAL_ID`: Journal ID for metadata tasks


### Database Modes

1. **Legacy Mode (v2)**
   - Uses leak-based update strategy
   - Single database connection
   - Simple metadata structure

2. **Modern Mode (v3)**
   - SQL-based update tracking
   - Support for multiple database instances
   - Enhanced metadata structure
   - Per-customer database isolation


## Best Practices

1. **Job Configuration**
   - Use descriptive job names
   - Group related addresses
   - Set appropriate update intervals

2. **Performance Optimization**
   - Adjust batch sizes based on network conditions
   - Monitor thread count vs. performance
   - Use appropriate IPFS gateways

3. **Maintenance**
   - Regular cleaning of old labels
   - Monitor database size
   - Check for failed metadata fetches
