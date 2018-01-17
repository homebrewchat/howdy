FROM amazeeio/node:8

COPY ./env/ /app/
RUN yarn install --pure-lockfile

CMD yarn run start
