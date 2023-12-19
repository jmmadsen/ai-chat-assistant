FROM node:14.21.3-alpine as build

WORKDIR /usr/src/app/

COPY package*.json ./

RUN npm ci --silent

COPY . .

RUN npm run build

# production
FROM nginx:stable-alpine

COPY --from=build /usr/src/app/build /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]