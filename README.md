to run:

```
export SLACK_SIGNING_SECRET=xxx
export SLACK_BOT_TOKEN=yyy
docker build .
# VIRTUAL_HOST and LETSENCRYPT_HOST are for docker-gen/nginx things
docker run \
    --publish 3000:3000 \
    --expose 3000 \
    --name hbcbot \
    --env "VIRTUAL_HOST=hbc.jroll.io" \
    --env "LETSENCRYPT_HOST=hbc.jroll.io" \
    --env "SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET" \
    --env "SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN" \
    $image_id
