FROM amazeeio/node:8

COPY package.json /app/
COPY yarn.lock /app/
COPY src/ /app/
RUN yarn install --pure-lockfile

CMD yarn run start
