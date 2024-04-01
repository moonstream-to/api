# Moonstream Python client

This is the Python client library for the Moonstream API.

## Installation

This library assumes you are using Python 3.6 or greater.

Install using `pip`:

```bash
pip install moonstream
```

## Usage

-   Source environment variable with access token to Moonstream, you can create one on page https://moonstream.to/account/tokens/

```python
access_token = os.environ.get("MOONSTREAM_ACCESS_TOKEN")
```

-   Create an object of Moonstream client and authorize

```python
mc = Moonstream()
mc.authorize(access_token)
```

## create_stream method

Return a stream of event for time range.

**From timestamp to None, from bottom to top**

When `end_time` is not set.

```python
for events in mc.create_stream(
    start_time=1637834400, end_time=None, q="type:ethereum_blockchain"
):
    event_timestamp_list = [e["event_timestamp"] for e in events["events"]]
    print(event_timestamp_list)
```

In this case we will be receiving events from bottom of history to recent time in next order:

```python
[1637836177, ..., 1637834440]
[1637837980, ..., 1637836226]
# Until we will get latest event,
# then we will be receiving empty lists
[]
[]
# Until new events will be available
[1637839306, 1637839306, 1637839306, 1637839306]
[]
# Continuing...
```

**From timestamp to timestamp, from top to bottom**

When `start_time` is greater then `end_time`.

```python
for events in mc.create_stream(
    start_time=1637839281, end_time=1637830890, q="type:ethereum_blockchain"
):
    event_timestamp_list = [e["event_timestamp"] for e in events["events"]]
    print(event_timestamp_list)
```

Stream of event packs will be generating from recent timestamp to older and inner list of transactions for each pack will be in most recent to older event timestamp range:

```python
[1637839280, ..., 1637838094]
[1637838086, ..., 1637836340]
...
[1637834488, ..., 1637832699]
[1637832676, ..., 1637830903]
```

**From timestamp to timestamp, from bottom to top**

When `start_time` is less than `end_time`.

```python
for events in mc.create_stream(
    start_time=1637830890, end_time=1637839281, q="type:ethereum_blockchain"
):
    event_timestamp_list = [e["event_timestamp"] for e in events["events"]]
    print(event_timestamp_list)
```

You start receiving list of older events from bottom of history to newest:

```python
[1637832676, ..., 1637830903]
[1637834488, ..., 1637832699]
...
[1637838086, ..., 1637836340]
[1637839280, ..., 1637838094]
```
