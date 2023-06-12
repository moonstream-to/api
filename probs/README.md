# probs

Running multiple operations simultaneously under one application.

Execute one command:

```bash
probs engine clean-call-requests --db-uri "${ENGINE_DB_URI}"
```

Run service with configuration:

```bash
probs service --config "~/.probs/config.json"
```

Config example:

```json
[
  {
    "name": "engine",
    "db_uri": "ENGINE_DB_URI",
    "workers": [
      {
        "name": "clean-call-requests",
        "interval": 10
      }
    ]
  }
]
```
