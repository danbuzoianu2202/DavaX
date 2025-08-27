# Use a small, secure base
FROM python:3.11-slim

# Create a non-root user
ENV APP_HOME=/app
WORKDIR $APP_HOME
RUN useradd -m appuser

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY app.py .

# Drop privileges
USER appuser

# Expose app port
EXPOSE 8000

# Production server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
