# Docker Deployment Guide

Complete guide to running the Prompt Generator in Docker.

## Quick Start

### Option 1: Use Your Existing Ollama (Recommended)

Since you already have Ollama running, just start the CLI container:

```bash
# Build the image
docker-compose build prompt-generator-cli

# Run interactively
docker-compose run --rm prompt-generator-cli

# Or use CLI mode
docker-compose run --rm prompt-generator-cli python prompt_generator.py "your prompt here"
```

### Option 2: Run Web Interface

```bash
# Start the web UI (connects to your existing Ollama)
docker-compose --profile web up -d prompt-generator-web

# Access at: http://localhost:8080
```

### Option 3: Full Stack (with new Ollama instance)

```bash
# Start everything including a new Ollama instance
docker-compose --profile with-ollama --profile web up -d

# Pull models into the new Ollama
docker-compose exec ollama ollama pull dolphin-mistral
docker-compose exec ollama ollama pull llava
```

## Deployment Options

### 1. CLI Mode (Connect to Existing Ollama)

This connects to your existing Ollama instance on the host machine.

**Build:**
```bash
docker build -t prompt-generator .
```

**Run Interactive:**
```bash
docker run -it --rm \
  --network host \
  -e OLLAMA_HOST=http://localhost:11434 \
  -v "$(pwd)/images:/app/images" \
  prompt-generator
```

**Run CLI:**
```bash
docker run --rm \
  --network host \
  -e OLLAMA_HOST=http://localhost:11434 \
  prompt-generator \
  python prompt_generator.py "a cyberpunk city"
```

**With docker-compose:**
```bash
# Interactive
docker-compose run --rm prompt-generator-cli

# CLI
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "your prompt" --type image
```

### 2. Web UI Mode

Run a web interface on port 8080:

**Start:**
```bash
docker-compose --profile web up -d prompt-generator-web
```

**Access:**
- Open browser to: http://localhost:8080
- Clean, modern web interface
- Auto-detects available models
- Copy results to clipboard

**Stop:**
```bash
docker-compose --profile web down
```

### 3. Standalone with Ollama

Run both Ollama and Prompt Generator in Docker:

**Start:**
```bash
docker-compose --profile with-ollama up -d
```

**Install models:**
```bash
# Enter Ollama container
docker-compose exec ollama bash

# Pull models
ollama pull dolphin-mistral
ollama pull gdisney/mistral-uncensored
ollama pull llava
```

**Use CLI:**
```bash
docker-compose run --rm prompt-generator-cli
```

**Stop:**
```bash
docker-compose --profile with-ollama down
```

## Environment Variables

Configure with environment variables:

```bash
# Ollama host
OLLAMA_HOST=http://localhost:11434

# Or for Docker service
OLLAMA_HOST=http://ollama:11434

# Or for host machine's Ollama
OLLAMA_HOST=http://host.docker.internal:11434
```

**In docker-compose.yml:**
```yaml
environment:
  - OLLAMA_HOST=http://your-ollama-host:11434
```

**With docker run:**
```bash
docker run -e OLLAMA_HOST=http://ollama:11434 prompt-generator
```

## Volume Mounts

### Reference Images

Mount a directory for reference images:

```bash
docker run -v ./images:/app/images prompt-generator

# Then use in commands:
[IMAGE] > /image /app/images/reference.jpg
```

### Output Directory

Save generated prompts:

```bash
docker run -v ./output:/app/output prompt-generator
```

### In docker-compose:

```yaml
volumes:
  - ./images:/app/images
  - ./output:/app/output
```

## Networking

### Connect to Host's Ollama

**Option 1: Host Network (Linux)**
```bash
docker run --network host prompt-generator
```

**Option 2: host.docker.internal (Windows/Mac)**
```bash
docker run -e OLLAMA_HOST=http://host.docker.internal:11434 prompt-generator
```

**Option 3: Docker Network**
```bash
# Create network
docker network create ollama-net

# Connect your existing Ollama
docker network connect ollama-net <your-ollama-container>

# Run prompt generator
docker run --network ollama-net \
  -e OLLAMA_HOST=http://<ollama-container-name>:11434 \
  prompt-generator
```

### Connect to Separate Ollama Container

```bash
# In docker-compose.yml
services:
  prompt-generator-cli:
    environment:
      - OLLAMA_HOST=http://ollama:11434
    networks:
      - ollama-network

  ollama:
    networks:
      - ollama-network

networks:
  ollama-network:
    driver: bridge
```

## Common Use Cases

### 1. Quick One-Off Prompts

```bash
# Build once
docker-compose build

# Run anytime
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "fantasy landscape" --type image
```

### 2. Interactive Sessions

```bash
docker-compose run --rm prompt-generator-cli

# Inside container:
[IMAGE] > /list
[IMAGE] > your prompt here
[IMAGE] > /quit
```

### 3. Web Interface for Teams

```bash
# Start web UI
docker-compose --profile web up -d

# Share URL: http://your-server:8080
# Stop when done
docker-compose --profile web down
```

### 4. Batch Processing

```bash
# Mount your images
docker run -v ./images:/app/images \
  -v ./batch_script.py:/app/batch_script.py \
  prompt-generator \
  python batch_script.py
```

### 5. API Service

The web profile runs a simple HTTP API:

**Endpoints:**
- `GET /` - Web UI
- `GET /api/models` - List available models
- `POST /api/generate` - Generate prompts

**Example:**
```bash
curl -X POST http://localhost:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "cyberpunk city", "type": "image"}'
```

## Docker Compose Profiles

We use profiles to control what starts:

```bash
# Default (nothing starts automatically)
docker-compose up

# Start CLI container
docker-compose run --rm prompt-generator-cli

# Start web UI
docker-compose --profile web up -d

# Start with Ollama
docker-compose --profile with-ollama up -d

# Start everything
docker-compose --profile web --profile with-ollama up -d
```

## Troubleshooting

### Cannot Connect to Ollama

**Check Ollama is running:**
```bash
curl http://localhost:11434/api/tags
```

**Check from inside container:**
```bash
docker-compose run --rm prompt-generator-cli \
  curl http://host.docker.internal:11434/api/tags
```

**Fix:** Update `OLLAMA_HOST` environment variable

### No Models Available

**For existing Ollama:**
```bash
ollama list  # Check installed models
ollama pull dolphin-mistral  # Install models
```

**For Docker Ollama:**
```bash
docker-compose exec ollama ollama list
docker-compose exec ollama ollama pull dolphin-mistral
```

### Permission Denied

The container runs as non-root user (uid 1000). Fix permissions:

```bash
# On host
chown -R 1000:1000 ./images ./output

# Or run as root (not recommended)
docker run --user root prompt-generator
```

### Port Already in Use

Change the port in docker-compose.yml:

```yaml
ports:
  - "8081:8080"  # Use 8081 instead of 8080
```

### Web UI Can't Connect

Check the `OLLAMA_HOST` environment variable:

```yaml
environment:
  # For host Ollama
  - OLLAMA_HOST=http://host.docker.internal:11434

  # For Docker Ollama
  - OLLAMA_HOST=http://ollama:11434
```

## Building for Production

### Optimized Build

```bash
# Build with build args
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  -t prompt-generator:latest \
  .

# Multi-platform build
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t prompt-generator:latest \
  .
```

### Push to Registry

```bash
# Tag
docker tag prompt-generator your-registry/prompt-generator:latest

# Push
docker push your-registry/prompt-generator:latest
```

### Deploy to Server

```bash
# On server
docker pull your-registry/prompt-generator:latest

# Run with existing Ollama
docker run -d \
  --name prompt-generator \
  --network host \
  -e OLLAMA_HOST=http://localhost:11434 \
  your-registry/prompt-generator:latest
```

## Resource Limits

Limit container resources:

```yaml
services:
  prompt-generator-web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Health Checks

Add health check to docker-compose.yml:

```yaml
services:
  prompt-generator-web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Logs

View logs:

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs prompt-generator-web

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail 100
```

## Updates

Update the application:

```bash
# Rebuild
docker-compose build

# Restart
docker-compose --profile web down
docker-compose --profile web up -d

# Or for CLI
docker-compose build prompt-generator-cli
```

## Complete Examples

### Example 1: Connect to Your Existing Ollama

```bash
cd z:\promptbuild-claude

# Build
docker-compose build prompt-generator-cli

# Run interactive
docker-compose run --rm prompt-generator-cli

# Inside container:
[IMAGE] > a dark warrior
[IMAGE] > /quit
```

### Example 2: Web UI

```bash
# Edit docker-compose.yml - ensure correct OLLAMA_HOST
# For your setup:
environment:
  - OLLAMA_HOST=http://host.docker.internal:11434

# Start
docker-compose --profile web up -d

# Open browser
start http://localhost:8080

# Stop
docker-compose --profile web down
```

### Example 3: Full Stack

```bash
# Start everything
docker-compose --profile with-ollama --profile web up -d

# Install models
docker-compose exec ollama ollama pull dolphin-mistral
docker-compose exec ollama ollama pull llava

# Use web UI at http://localhost:8080
# Or CLI:
docker-compose run --rm prompt-generator-cli
```

## Your Current Setup

Based on your existing Ollama at `localhost:11434`:

**Best option:**
```bash
docker-compose run --rm prompt-generator-cli
```

**Or for web UI:**
```bash
docker-compose --profile web up -d
# Access at http://localhost:8080
```

Both will connect to your existing Ollama with all your models!
