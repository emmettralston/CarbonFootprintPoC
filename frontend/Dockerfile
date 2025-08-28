FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json next.config.js ./
RUN npm install --frozen-lockfile || npm install
COPY src ./src
EXPOSE 3000
CMD ["npm", "run", "dev"]

