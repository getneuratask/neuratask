# Development stage
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install all dependencies (including devDependencies)
RUN npm install

# Copy source code
COPY . .

# Expose port 3000 for Vite dev server
EXPOSE 3000

# Start development server with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]