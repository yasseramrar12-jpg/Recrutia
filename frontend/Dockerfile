# Image du frontend RECRUT'IA : compilation Vite puis service statique Nginx
FROM node:22-slim AS compilation
WORKDIR /application
COPY package.json .
RUN npm install
COPY vite.config.js index.html ./
COPY src ./src
RUN npm run build

FROM nginx:alpine
COPY --from=compilation /application/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
