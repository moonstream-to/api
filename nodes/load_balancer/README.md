# Node Balancer application

## Installation

- Prepare environment variables
- Build application

```bash
go build -o nodebalancer
```

- Run with following parameters:

```bash
nodebalancer -host 0.0.0.0 -port 8544 -healthcheck
```
