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
    "balances": {
        "ethereum": {
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": "1000000000000000000",
            "0x6B175474E89094C44Da98b954EedeAC495271d0F": "2000000000000000000",
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": "3000000000000000"
        },
        "polygon": {
            "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270": "4000000000000000000",
            "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174": "5000000000000000",
            "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063": "6000000000000000000"
        }
    }
}
```

Where:
- The outer object contains a `balances` field mapping blockchain names to token balances
- Each blockchain object maps token contract addresses to their respective balances
- All balances are returned as strings in the token's smallest unit (e.g., wei for ETH)

### Features

1. **Caching**: Responses are cached for 10 seconds to minimize blockchain RPC calls
2. **Multicall**: Uses Multicall3 contract to batch balance queries for efficiency
3. **Error Handling**: Individual token or blockchain failures don't affect other results

### Supported Tokens

#### Ethereum
- WETH: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`
- DAI: `0x6B175474E89094C44Da98b954EedeAC495271d0F`
- USDC: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`

#### Polygon
- WMATIC: `0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270`
- USDC: `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`
- DAI: `0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063`

### Error Responses

- 400 Bad Request: Invalid Ethereum address
- 500 Internal Server Error: Server-side errors

### Example

```bash
curl "http://localhost:8080/balances?address=0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
```
