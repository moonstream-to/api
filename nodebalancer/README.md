# Node Balancer application

## Installation

-   Prepare environment variables, according to `sample.env`.
-   Build an application

```bash
go build -o nodebalancer .
```

## CLI

**IMPORTANT** Do not use flag `-debug` in production.

Node balancer access manipulation requires an administration token to create and modify resources within the Bugout moonstream application.

### add new access

Add new access for user:

```bash
./nodebalancer access add \
	--access-token "<bugout_access_token>"
	--name "Access name" \
	--description "Description of access"
```

### delete access

Delete user access:

```bash
./nodebalancer access delete \
	--access-token "<bugout_access_token>"
	--access-id "<access_uuid>"
```

If `access-id` not specified, all user accesses will be deleted.

### users

```bash
./nodebalancer access list --access-token "<bugout_access_token>" | jq .
```

This command will return a list of bugout resources of registered users to access node balancer.

```json
[
	{
		"user_id": "<user_id_from_any_bugout_application>",
		"access_id": "<access_uuid_which_provided_with_query>",
		"name": "<short_description_of_purpose_of_this_crawler>",
		"description": "<long_description>",
		"blockchain_access": true,
		"extended_methods": false
	}
]
```

`access_id` - token which allows access to nodebalancer, could be specified in both ways:

-   as a header `x-moonstream-access-id` with value `access_id`
-   as query parameter `access_id=access_id`

`blockchain_access` - boolean which allows you or not to have access to blockchain node, otherwise you will be redirected to database

`extended_methods` - boolean which allows you to call not whitelisted method to blockchain node, by default for new user this is equal to `false`

### server

```bash
./nodebalancer server --host 0.0.0.0 --port 8544 --healthcheck
```

Flag `--healthcheck` will execute background process to ping-pong available nodes to keep their status and current block number.
Flag `--debug` will extend output of each request to server and healthchecks summary.

## Work with node

Common request to fetch block number

```bash
curl --request POST 'http://127.0.0.1:8544/nb/ethereum/jsonrpc?access_id=<access_id>&data_source=<blockchain/database>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "jsonrpc":"2.0",
        "method":"eth_getBlockByNumber",
        "params":["latest", false],
        "id":1
    }'
```

For Web3 providers `access_id` and `data_source` could be specified in headers

```bash
--header 'x-node-balancer-data-source: <blockchain/database>'
--header 'x-node-balancer-access-id: <access_id>'
```

## Tests

### Running all tests

```bash
/usr/local/go/bin/go test -run ^*$ github.com/bugout-dev/moonstream/nodes/node_balancer/cmd/nodebalancer -v -count=1
```

### Running specified test

```bash
/usr/local/go/bin/go test -run ^TestCleanInactiveClientNodes$ github.com/bugout-dev/moonstream/nodes/node_balancer/cmd/nodebalancer -v -count=1
```

## Migrations

To run migration:

```bash
python migrations/migrations.py run --key 20230522 \
    --token-current-owner "$NB_CONTROLLER_TOKEN" \
    --token-new-owner "$MOONSTREAM_ADMIN_OR_OTHER_CONTROLLER" \
    --new-application-id "$MOONSTREAM_APPLICATION_ID"
```

## Balances Endpoint

The `/balances` endpoint allows you to retrieve token balances for a specified Ethereum address across multiple blockchains.

### Request

```
GET /balances?address=<ethereumAddress>
```

Parameters:
- `address` (required): The Ethereum address to query balances for

### Response

The endpoint returns a JSON object with the following structure:

```json
{
  "1": {
    "chain_id": "1",
    "name": "ethereum",
    "image_url": "https://example.com/eth.png",
    "balances": {
      "0x0000000000000000000000000000000000000000": "1000000000000000000",
      "0xdac17f958d2ee523a2206206994597c13d831ec7": "2000000000000000000",
      "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "3000000000000000"
    }
  },
  "137": {
    "chain_id": "137", 
    "name": "polygon",
    "image_url": "https://example.com/matic.png",
    "balances": {
      "0x0000000000000000000000000000000000000000": "4000000000000000000",
      "0x2791bca1f2de4661ed88a30c99a7a9449aa84174": "5000000000000000",
      "0xc2132d05d31c914a87c6611c10748aeb04b58e8f": "6000000000000000000"
    }
  }
}
```

Where:
- The top-level keys are chain IDs (e.g. "1" for Ethereum, "137" for Polygon)
- Each chain object contains:
  - `chain_id`: The chain identifier as a string
  - `name`: The human-readable name of the chain
  - `image_url`: URL to the chain's logo/image
  - `balances`: Map of token addresses to their balances
    - Native token (ETH, MATIC etc) is represented by the zero address: `0x0000000000000000000000000000000000000000`
    - All balances are returned as strings in the token's smallest unit (e.g., wei for ETH)

### Features

1. **Caching**: Responses are cached for 10 seconds to minimize blockchain RPC calls
2. **Multicall**: Uses Multicall3 contract to batch balance queries for efficiency
3. **Error Handling**: Individual token or blockchain failures don't affect other 

### Example

```bash
curl "http://localhost:8080/balances?address=0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
```

### Contracts Config Structure

The `contracts.json` file should follow this structure:

```json
{
  "ethereum": {
    "multicall3": "0xcA11bde05977b3631167028862bE2a173976CA11",
    "chain_id": "1",
    "name": "Ethereum",
    "image_url": "https://example.com/eth.png",
    "native_token": "ETH",
    "tokens": {
      "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
      "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC"
    }
  },
  "polygon": {
    "multicall3": "0xcA11bde05977b3631167028862bE2a173976CA11",
    "chain_id": "137",
    "name": "Polygon",
    "image_url": "https://example.com/matic.png",
    "native_token": "MATIC",
    "tokens": {
      "0x2791bca1f2de4661ed88a30c99a7a9449aa84174": "USDC",
      "0xc2132d05d31c914a87c6611c10748aeb04b58e8f": "USDT"
    }
  }
}
```

Where:
- Top-level keys are blockchain identifiers used internally
- Each chain configuration contains:
  - `multicall3`: Address of the Multicall3 contract on that chain
  - `chain_id`: The chain identifier (e.g. "1" for Ethereum)
  - `name`: Human-readable name of the chain
  - `image_url`: URL to the chain's logo/image
  - `native_token`: Symbol for the chain's native token (ETH, MATIC etc)
  - `tokens`: Map of token addresses to their symbols
