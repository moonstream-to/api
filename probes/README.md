# probes

Running multiple operations simultaneously under one application.

Execute one command:

```bash
probes engine clean-call-requests --db-uri "${ENGINE_DB_URI}"
```

Run service with configuration:

```bash
probes service \
    --config /home/ubuntu/.probes/engine-clean-call-requests.js
```

Config example:

```json
{
    "application": "engine",
    "db_uri": "ENGINE_DB_URI",
    "db_timeout": "15s",
    "probe": {
        "name": "clean-call-requests",
        "interval": 10
    }
}
```
