# Docker Quick Start - Your Setup

Since you already have Ollama running, here's how to use the Prompt Generator in Docker.

## 🚀 Option 1: Quick CLI (Recommended)

### Build Once
```bash
docker-compose build prompt-generator-cli
```

### Use Anytime
```bash
# Interactive mode
docker-compose run --rm prompt-generator-cli

# One-shot prompt
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "your prompt here"

# Video prompt
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "epic scene" --type video
```

### Or Use the Batch Script
```bash
# Just double-click or run:
docker-run.bat
```

## 🌐 Option 2: Web Interface

### Start Web UI
```bash
# Edit docker-compose.yml first to set correct OLLAMA_HOST
docker-compose --profile web up -d
```

**Or use the batch script:**
```bash
docker-web.bat
```

**Access at:** http://localhost:8080

### Stop Web UI
```bash
docker-compose --profile web down
```

## ⚙️ Configuration for Your Setup

Your Ollama is at `http://localhost:11434` on the host machine.

### For CLI Container (already configured):
```yaml
environment:
  - OLLAMA_HOST=http://host.docker.internal:11434
```

### Test Connection
```bash
docker-compose run --rm prompt-generator-cli python -c "
from prompt_generator import PromptGenerator
g = PromptGenerator()
print(f'Connected: {g.check_ollama_connection()}')
print(f'Model: {g.text_model}')
"
```

Expected output:
```
Connected: True
Model: gdisney/mistral-uncensored:latest
```

## 📝 Usage Examples

### Example 1: Quick Prompt
```bash
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "cyberpunk warrior"
```

### Example 2: Interactive Session
```bash
docker-compose run --rm prompt-generator-cli

# Inside container:
[IMAGE] > /list
[IMAGE] > a dark fantasy scene
[IMAGE] > /model benevolentjoker/nsfwwurm
[IMAGE] > sensual portrait
[IMAGE] > /quit
```

### Example 3: With Reference Image
```bash
# First, put your image in ./images/ folder
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "similar style" --image /app/images/reference.jpg
```

### Example 4: Video Prompt
```bash
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "camera flying through clouds" --type video
```

### Example 5: Specific Model
```bash
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "fantasy scene" \
  --model benevolentjoker/nsfwwurm
```

## 🔧 Customization

### Change Ollama Host
Edit `docker-compose.yml`:
```yaml
services:
  prompt-generator-cli:
    environment:
      # For host machine Ollama (default)
      - OLLAMA_HOST=http://host.docker.internal:11434

      # Or for different host
      - OLLAMA_HOST=http://your-server:11434
```

### Mount Directories

Already configured in docker-compose.yml:
```yaml
volumes:
  - ./images:/app/images    # Put reference images here
  - ./output:/app/output    # Save output here
```

Create these directories:
```bash
mkdir images output
```

## 📚 Available Models (From Your Ollama)

Your prompt generator will automatically use:
- **Text:** `gdisney/mistral-uncensored:latest`
- **Vision:** `llava:latest`

Plus access to all 14 models in your Ollama instance!

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Test host connection
curl http://localhost:11434/api/tags

# Test from container
docker run --rm appropriate/curl \
  curl http://host.docker.internal:11434/api/tags
```

### "No models available"
Check your Ollama:
```bash
ollama list
```

### Permission errors
```bash
# Fix permissions for mounted directories
mkdir -p images output
chmod 777 images output
```

### Port conflicts (Web UI)
Change port in docker-compose.yml:
```yaml
ports:
  - "8081:8080"  # Use 8081 instead
```

## 🎯 Recommended Workflow

### For Quick Prompts
```bash
docker-run.bat
# Then type your prompts
```

### For Web Interface
```bash
docker-web.bat
# Open browser to http://localhost:8080
```

### For Batch Processing
```bash
# Create a script file
echo "
from prompt_generator import PromptGenerator
g = PromptGenerator()

prompts = ['warrior', 'dragon', 'castle']
for p in prompts:
    result = g.generate_prompt(p)
    print(f'{p}: {result}\\n')
" > batch.py

# Run it
docker-compose run --rm prompt-generator-cli python batch.py
```

## 📖 Full Documentation

- **Full Docker Guide:** [DOCKER.md](DOCKER.md)
- **General Usage:** [README.md](README.md)
- **Your Local Setup:** [YOUR_SETUP.md](YOUR_SETUP.md)

## 💡 Tips

1. **Build once, use forever:** After initial build, the container is ready
2. **Auto-detection:** The tool automatically finds your best models
3. **Reference images:** Put them in `./images/` directory
4. **Logs:** Add `-d` to run in background, check logs with `docker-compose logs`

## ✅ You're Ready!

Your Docker setup connects to your existing Ollama with all your models.

**Simplest command:**
```bash
docker-run.bat
```

Or:
```bash
docker-compose run --rm prompt-generator-cli
```

Start generating uncensored prompts! 🎨
