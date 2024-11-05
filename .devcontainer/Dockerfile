# Build image
FROM python:3.13-alpine AS builder
# Install build dependencies
RUN apk add --no-cache git build-base
# Set the working directory
WORKDIR /workspaces
# Get everything from working directory like files, folders, etc
COPY . .
# Runtime image
FROM python:3.13-alpine
# Install runtime dependencies
RUN apk add --no-cache git
# Set the working directory
WORKDIR /workspaces
RUN pip install --no-cache-dir python-dotenv
# Copy only the necessary files from the builder stage
COPY --from=builder /workspaces /workspaces
#Ensure the entrypoint is set to bash for interactive use
ENTRYPOINT ["/bin/sh"]