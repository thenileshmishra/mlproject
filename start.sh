#!/bin/bash

# MLOps Application Startup Script

set -e

echo "Starting MLOps Student Performance Application..."

# Check if running in production mode
if [ "$FLASK_ENV" = "production" ]; then
    echo "Running in PRODUCTION mode"

    # Install gunicorn if not already installed
    pip install gunicorn 2>/dev/null || true

    # Run with gunicorn for production
    exec gunicorn \
        --bind 0.0.0.0:${PORT:-5001} \
        --workers ${WORKERS:-4} \
        --threads ${THREADS:-2} \
        --timeout ${TIMEOUT:-120} \
        --access-logfile - \
        --error-logfile - \
        --log-level ${LOG_LEVEL:-info} \
        app:app
else
    echo "Running in DEVELOPMENT mode"

    # Run with Flask development server
    exec python app.py
fi
