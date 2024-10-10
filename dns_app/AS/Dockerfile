# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the server code into the container
COPY authoritative_server.py .

# Expose the UDP port
EXPOSE 53533

# Run the server
CMD ["python", "authoritative_server.py"] 
