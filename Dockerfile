# SpaceD Mission Terminal - Web Interface for Hackathon
FROM python:3.11-slim
RUN echo "Building SpaceD Mission Terminal Web Interface Docker Image. Very first line of Dockerfile. Should appear in build logs."

# Install system dependencies
RUN echo "Installing system dependencies."
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
RUN echo "Setting working directory to /app."
WORKDIR /app

# Copy the entire repo into the image
RUN echo "Copying application files to /app."
COPY . /app

# Install Python dependencies
RUN echo "Installing Python dependencies."
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN echo "Creating non-root user 'app' and setting permissions."
RUN useradd --create-home --shell /bin/bash app

# Ensure all files and folders are owned by 'app' and accessible
RUN echo "Setting ownership and permissions for /app."
RUN chown -R app:app /app && chmod -R u+rwX /app
USER app

# Set environment variables
RUN echo "Setting environment variables."
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=web_terminal.py \
    PORT=8080

# Expose port for web access
RUN echo "Exposing port 8080."
EXPOSE 8080

# Health check
RUN echo "Setting up health check."
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the web application with Gunicorn and eventlet for production
RUN echo "Starting the web application using Gunicorn with eventlet."
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:8080", "web_terminal:app"]
