# Docker Configuration for MLOps Student Performance Prediction

This document provides comprehensive instructions for using Docker with this MLOps project.

## Prerequisites

- Docker installed (version 20.10 or higher)
- Docker Compose installed (version 1.29 or higher)

## Quick Start

### Development Environment

1. Build and run the application:
```bash
docker-compose up --build
```

2. Access the application at `http://localhost:5001`

3. Stop the application:
```bash
docker-compose down
```

## Docker Files Overview

- **Dockerfile**: Main Docker image configuration
- **docker-compose.yml**: Development environment orchestration
- **docker-compose.prod.yml**: Production environment orchestration
- **.dockerignore**: Files to exclude from Docker build context
- **.env.example**: Template for environment variables

## Detailed Usage

### Building the Docker Image

Build the image manually:
```bash
docker build -t mlops-student-performance:latest .
```

### Running with Docker Compose

#### Development Mode
```bash
# Start services in foreground
docker-compose up

# Start services in background (detached mode)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Production Mode
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Stop production services
docker-compose -f docker-compose.prod.yml down
```

### Running with Docker Run

```bash
# Run container directly
docker run -d \
  --name mlops-app \
  -p 5001:5001 \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/logs:/app/logs \
  mlops-student-performance:latest
```

## Environment Variables

Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit the `.env` file to customize settings:
- `FLASK_ENV`: Set to `development` or `production`
- `PORT`: Application port (default: 5001)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Volume Management

### Persisted Data

The application uses Docker volumes to persist:
- `/app/artifacts` - ML models and preprocessors
- `/app/logs` - Application logs

### Managing Volumes

List volumes:
```bash
docker volume ls
```

Inspect a volume:
```bash
docker volume inspect mlops-artifacts
```

Remove volumes:
```bash
docker-compose down -v
```

## Health Checks

The container includes health checks that:
- Run every 30 seconds
- Timeout after 10 seconds
- Allow 40 seconds for startup
- Retry 3 times before marking as unhealthy

Check container health:
```bash
docker ps
docker inspect --format='{{.State.Health.Status}}' mlops-student-performance
```

## Networking

### Access from Host

The application is accessible at:
- Development: `http://localhost:5001`
- Inside network: `http://mlops-app:5001`

### Custom Network

Services run on the `mlops-network` bridge network.

Inspect the network:
```bash
docker network inspect mlops-network
```

## Troubleshooting

### View Container Logs
```bash
docker-compose logs -f mlops-app
```

### Execute Commands Inside Container
```bash
docker-compose exec mlops-app bash
```

### Rebuild Without Cache
```bash
docker-compose build --no-cache
docker-compose up
```

### Check Container Resource Usage
```bash
docker stats mlops-student-performance
```

### Remove All Containers and Images
```bash
# Stop all containers
docker-compose down

# Remove all images
docker rmi $(docker images -q mlops-student-performance)

# Clean up system
docker system prune -a
```

## Production Deployment

### Best Practices

1. **Use Production Compose File**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Set Environment Variables**
   - Set `FLASK_ENV=production`
   - Disable debug mode
   - Configure proper logging

3. **Resource Limits**
   - CPU: Limited to 2 cores
   - Memory: Limited to 2GB

4. **Security**
   - Application runs as non-root user (mluser)
   - Minimal base image (slim-buster)
   - No development files in production image

5. **Monitoring**
   - Check health status regularly
   - Monitor logs for errors
   - Track resource usage

### Scaling

Scale the application (if load balancer is configured):
```bash
docker-compose -f docker-compose.prod.yml up -d --scale mlops-app=3
```

## Development Workflow

1. **Make Code Changes**
   - Files are mounted as volumes in development
   - Changes reflect immediately (Flask debug mode)

2. **Rebuild After Dependency Changes**
   ```bash
   docker-compose up --build
   ```

3. **Run Tests Inside Container**
   ```bash
   docker-compose exec mlops-app pytest
   ```

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Build Docker Image
  run: docker build -t mlops-app:${{ github.sha }} .

- name: Run Tests
  run: docker run mlops-app:${{ github.sha }} pytest
```

## Additional Commands

### Cleanup
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Complete cleanup
docker system prune -a --volumes
```

### Export/Import Images
```bash
# Save image to tar
docker save mlops-student-performance:latest > mlops-app.tar

# Load image from tar
docker load < mlops-app.tar
```

## Support

For issues related to Docker configuration, please check:
1. Docker daemon is running
2. Sufficient disk space available
3. Ports are not already in use
4. Environment variables are properly set

For application-specific issues, refer to the main README.md file.
