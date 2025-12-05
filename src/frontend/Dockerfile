# Stage 1: Build the React application
FROM node:18-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY src/frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY src/frontend/ .

# Build the app
RUN npm run build

# Stage 2: Serve the React application with Nginx
FROM nginx:alpine

# Copy the build output to replace the default nginx contents.
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
