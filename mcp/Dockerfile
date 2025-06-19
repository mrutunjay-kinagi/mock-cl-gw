# mcp/Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy MCP code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Expose MCP service port
EXPOSE 8002

# Start the orchestrator
CMD ["python", "orchestrator.py"]
