# Stage 1: Build the Angular application
FROM node:18 AS build
 
WORKDIR /app
 
# Copy the rest of the application code
COPY . .
 
# Install dependencies
RUN npm install
 
# Build the application
RUN npm run build
 
# Stage 2: Serve the application using Nginx
FROM nginx:alpine
 
# Copy the built application from Stage 1
COPY --from=build /app/dist/document_management_frontend/browser/* /usr/share/nginx/html/
 
# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
 
# Expose port 4200
EXPOSE 80
 
# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
