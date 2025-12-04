FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy source code
COPY . .

# Expose Vite port
EXPOSE 3000

# Run Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]
