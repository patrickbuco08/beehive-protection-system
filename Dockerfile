FROM python:3.9-slim

# Set non-interactive frontend to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal system dependencies for training on Mac/Windows
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy application code
COPY . /app/

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir tensorflow==2.12.0 matplotlib
RUN pip install --no-cache-dir numpy==1.24.4


# Install Jupyter Notebook
RUN pip install --no-cache-dir jupyter notebook

# Install the project as a package
RUN pip install -e .

# Copy and make entrypoint.sh executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose Jupyter port
EXPOSE 8888

# Set the default command with entry point script
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["app"]
