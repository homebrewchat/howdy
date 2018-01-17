# Brubot, a bot built on [Botkit](http://howdy.ai/botkit)

## Running Locally

There are two options for running locally, directly via `yarn`, or in a docker container. In either case, you will need to have a Slack token available as an environment variable named `SLACK_TOKEN`.

### Run via yarn
`SLACK_TOKEN=xoxb-slbirkjnxxxxxxxxxxx yarn run dev`

### Run via docker
Edit the `docker-compose` file and add to the `environment` stanza your `SLACK_TOKEN`

```
environment:
  - SLACK_TOKEN=xoxb-sdlg4ins0b84n0sn4bxxxxxxxx
```

Start the container with `docker-compose up --build`
