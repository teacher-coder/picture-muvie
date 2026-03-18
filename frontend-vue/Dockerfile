FROM node:22-alpine AS build-stage

RUN mkdir -p /app
WORKDIR /app/

COPY package.json package-lock.json /app/

RUN npm cache verify

RUN npm install

COPY . /code/

EXPOSE 5173

CMD ["npm", "run", "dev"]