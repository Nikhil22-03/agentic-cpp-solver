# Use a lightweight Alpine Linux base image
FROM alpine:latest

# Install the g++ compiler
RUN apk add --no-cache g++

# Set the working directory inside the container
WORKDIR /app