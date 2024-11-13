## Running tests

```
pip install tox
tox
```

## Running the app

Let lagoon deploy it? For local work, I think something like:

```
export SLACK_SIGNING_SECRET=foo
export SLACK_BOT_TOKEN=bar
export AV_KEY=ALPHAVANTAGE_APIKEY_foobar
docker-compose up
```
