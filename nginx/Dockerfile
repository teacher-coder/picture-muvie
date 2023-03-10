# Build step 1(installing node modules and preparing compiled build)
FROM node:19.6.0-alpine as build-stage

WORKDIR /app/

COPY frontend/package.json frontend/package-lock.json /app/

RUN npm cache verify && \
    npm install --silent

COPY frontend /app/

RUN npm run build


# Build step 2(Deploying build on NGINX)
FROM nginx:1.23-alpine as production-stage

COPY nginx/prod.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist /dist/

# Copy openssl certificate to docker image
COPY openssl/certs /etc/ssl/certs
COPY openssl/private /etc/ssl/private

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]