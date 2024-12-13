# Node Balancer application

## Installation

-   Prepare environment variables, according to `sample.env`.
-   Build application

```bash
go build -o nodebalancer .
```

## Work with nodebalancer

**IMPORTANT** Do not use flag `-debug` in production.

### add-access

Add new access for user:

```bash
nodebalancer add-access \
	--user-id "<user_uuid>" \
	--access-id "<access_uuid>" \
	--name "Access name" \
	--description "Description of access" \
	--extended-methods false \
	--blockchain--access true
```

### delete-access

Delete user access:

```bash
nodebalancer delete-access \
	--user-id "<user_uuid>" \
	--access-id "<access_uuid>"
```

If `access-id` not specified, all user accesses will be deleted.

### users

```bash
nodebalancer users | jq .
```

This command will return a list of bugout resources of registered users to access node balancer with their `crawlers/app/project` (in our project we will call it `crawlers`).

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
nodebalancer server -host 0.0.0.0 -port 8544 -healthcheck
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
