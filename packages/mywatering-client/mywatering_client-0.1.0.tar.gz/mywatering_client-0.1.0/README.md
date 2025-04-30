# My watering client

## Installation

```
uv tool install mywatering-client
```

## Running

```
watering-cli temperature -s "https://your.server.com" -c <client number> -u <user> -p <password>
watering-cli water -s "https://your.server.com" -c <client number> -u <user> -p <password>
```

## Contributing

Please sync repository and install `pre-commit` before commiting and pushing your changes.

```
uv sync
uv run pre-commit install
```
