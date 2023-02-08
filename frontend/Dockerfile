# Build step 1(installing node modules and preparing compiled build)
FROM node:19.6.0-alpine as build-stage

WORKDIR /app/

COPY package.json ./

RUN npm cache verify

RUN npm i --silent && \
    npm install --silent

COPY . ./

EXPOSE 8080

CMD ["npm", "run", "dev"]


# Build step 2(Deploying build on NGINX)
# FROM nginx:1.23

# RUN apt-get update && \
#     apt-get install -y wget && \
#     rm -rf /var/lib/apt/lists/*

# RUN rm -rf /usr/share/nginx/html/*

# COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf:ro
# COPY --from=build /app/dist /usr/share/nginx/html