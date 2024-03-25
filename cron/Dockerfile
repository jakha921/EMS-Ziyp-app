# Use the official Ubuntu image
FROM ubuntu:latest

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the script into the container
COPY send_request.sh /send_request.sh

# Grant execution permissions to the script
RUN chmod +x /send_request.sh

# Run the script
CMD ["/bin/bash", "/send_request.sh"]
