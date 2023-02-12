FROM node:19.6.0-alpine as build-stage

WORKDIR /app/

COPY package.json ./

RUN npm cache verify

RUN npm i --silent && \
    npm install --silent

COPY . ./

EXPOSE 5173

CMD ["npm", "run", "dev"]