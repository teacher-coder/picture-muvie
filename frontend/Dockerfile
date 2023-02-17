FROM node:19.6.0-alpine as build-stage

RUN mkdir -p /app
WORKDIR /app/

COPY package.json package-lock.json /app/

RUN npm cache verify

RUN npm install

COPY . /code/

EXPOSE 5173

CMD ["npm", "run", "dev"]