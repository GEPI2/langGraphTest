# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
# Add docker library manually if not in requirements.txt (it should be)
RUN pip install --no-cache-dir -r requirements.txt docker

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "src/ui/app.py", "--server.address=0.0.0.0"]
