FROM amazeeio/node:8

COPY src/ /app/
RUN yarn install --pure-lockfile

CMD yarn run start
