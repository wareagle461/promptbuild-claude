# 🎨 Start Here - Prompt Generator

Complete uncensored prompt generator for images and videos. Runs 100% locally using your Ollama installation.

## ✅ Your Setup Status

- ✓ Ollama running at `localhost:11434`
- ✓ 14 models available
- ✓ Uncensored models: `gdisney/mistral-uncensored`, `benevolentjoker/nsfwwurm`
- ✓ Vision support: `llava`
- ✓ Docker ready
- ✓ Python ready

**You're all set!** Choose how you want to run it below.

## 🚀 3 Ways to Run

### 1. Native Python (Fastest)

**Just run:**
```bash
py prompt_generator.py
```

Or double-click: `run.bat`

**Pros:** Fastest, direct access to Ollama
**Use when:** Quick interactive sessions

### 2. Docker CLI

**Just run:**
```bash
docker-run.bat
```

Or:
```bash
docker-compose run --rm prompt-generator-cli
```

**Pros:** Isolated, portable, reproducible
**Use when:** Want containerization, deployment

### 3. Docker Web UI

**Just run:**
```bash
docker-web.bat
```

Then open: http://localhost:8080

**Pros:** Beautiful interface, team access, copy-paste friendly
**Use when:** Multiple users, prefer GUI

## 📖 Quick Examples

### Interactive Mode (Any Method)

```
[IMAGE] > a dark warrior in fantasy armor

🔄 Generating prompt...
============================================================
GENERATED PROMPT:
============================================================
A dark warrior clad in ornate fantasy armor, standing in...
============================================================

[IMAGE] > /model benevolentjoker/nsfwwurm
[IMAGE] > sensual portrait
[IMAGE] > /video
[VIDEO] > epic battle scene
[VIDEO] > /list
[VIDEO] > /quit
```

### CLI Mode

```bash
# Python
py prompt_generator.py "cyberpunk city"

# Docker
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "fantasy scene" --type image
```

### With Reference Image

```bash
# Put image in ./images/ folder first
py prompt_generator.py "similar style" --image images/ref.jpg

# Or in interactive:
[IMAGE] > /image images/reference.jpg
[IMAGE] > make it darker with more contrast
```

## 🎯 Choose Your Guide

**Brand new?**
→ [QUICKSTART.md](QUICKSTART.md) - 5 minute guide for Python
→ [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md) - Docker quick start

**Your specific setup:**
→ [YOUR_SETUP.md](YOUR_SETUP.md) - Tailored to your installed models

**Want everything:**
→ [README.md](README.md) - Complete Python guide
→ [DOCKER.md](DOCKER.md) - Complete Docker guide

**Need models?**
→ [MODELS.md](MODELS.md) - All about uncensored models

## 💡 Quick Tips

### Available Commands
```
/image [path]  - Set reference image
/video         - Switch to video prompts
/img           - Switch to image prompts
/model [name]  - Override model
/list          - Show all models
/clear         - Clear reference
/quit          - Exit
```

### Your Best Models

**Most uncensored:**
- `benevolentjoker/nsfwwurm` - Maximum freedom
- `gdisney/mistral-uncensored` - Fast & uncensored (default)

**Best for images:**
- Auto-detects best model
- Override with `/model [name]`

**For reference images:**
- `llava` - Standard vision (default)
- `qwen2.5vl` - Alternative vision

### Switch Models

```
# In interactive mode:
[IMAGE] > /model benevolentjoker/nsfwwurm
[IMAGE] > your prompt here

# In CLI:
py prompt_generator.py "prompt" --model benevolentjoker/nsfwwurm
```

## 🏃 Quickest Start

**Want it NOW?** Run this:

```bash
# Windows
run.bat

# Or Docker
docker-run.bat
```

Then just type your prompt!

## 📁 Project Structure

```
promptbuild-claude/
├── prompt_generator.py       # Main application
├── run.bat                   # Windows Python launcher
├── docker-run.bat            # Windows Docker launcher
├── docker-web.bat            # Windows Docker Web UI
├── Dockerfile                # Docker image config
├── docker-compose.yml        # Docker orchestration
├── requirements.txt          # Python dependencies
│
├── START-HERE.md            # ← You are here!
├── QUICKSTART.md            # 5-min Python guide
├── DOCKER-QUICKSTART.md     # Quick Docker guide
├── YOUR_SETUP.md            # Your specific setup
├── README.md                # Full Python guide
├── DOCKER.md                # Full Docker guide
└── MODELS.md                # Model guide
```

## 🎨 Example Output

**Input:** "a dark warrior"

**Output:**
```
A dark warrior clad in ornate fantasy armor, standing in a
misty battlefield at dusk. The warrior is a tall, imposing
figure with a scarred face partially hidden by a helmet with
intricate engravings. The armor is black steel with crimson
accents, featuring shoulder pauldrons shaped like dragon heads.
In their right hand, they grip a massive two-handed sword with
runes glowing along the blade...
[continues with detailed description]
```

## ⚙️ Common Tasks

### Generate 10 prompts quickly
```bash
py prompt_generator.py "warrior" > output/1.txt
py prompt_generator.py "dragon" > output/2.txt
# etc...
```

### Use most uncensored model
```bash
py prompt_generator.py "your prompt" --model benevolentjoker/nsfwwurm
```

### Batch processing
```python
# batch.py
from prompt_generator import PromptGenerator
g = PromptGenerator()

for topic in ["warrior", "dragon", "castle"]:
    print(f"\n{topic}:")
    print(g.generate_prompt(topic))
```

Then: `py batch.py`

### Deploy to server
```bash
docker-compose --profile web up -d
# Access from anywhere at: http://your-server:8080
```

## 🐛 Problems?

### Can't connect to Ollama
```bash
# Check if running
curl http://localhost:11434/api/tags

# Or just run:
ollama serve
```

### Python not found
- Install from: https://python.org
- Or use Docker instead

### Docker not working
- Start Docker Desktop
- Check: `docker info`

### No models
```bash
ollama list  # Check what you have
ollama pull dolphin-mistral  # Add more
```

## 🎯 Your Next Steps

1. **Choose your method:** Python or Docker?
2. **Read the quick guide:** [QUICKSTART.md](QUICKSTART.md) or [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md)
3. **Run it:** `run.bat` or `docker-run.bat`
4. **Start creating!**

## 🌟 Features Recap

✅ 100% Local & Private
✅ Uncensored - No restrictions
✅ Image reference support
✅ Video & Image prompts
✅ 14 models available
✅ Auto-detects best models
✅ CLI & Web interfaces
✅ Docker & Python support
✅ Batch processing ready
✅ Team deployment ready

## 📞 Help & Documentation

**Quick help:**
```bash
py prompt_generator.py --help
```

**Guides by skill level:**
- Beginner: [QUICKSTART.md](QUICKSTART.md)
- Intermediate: [README.md](README.md)
- Advanced: [DOCKER.md](DOCKER.md), [MODELS.md](MODELS.md)

**Your setup:**
- [YOUR_SETUP.md](YOUR_SETUP.md) - Specific to your installation

## 🚀 Ready to Go!

You have everything configured. Just run:

**Python:**
```bash
run.bat
```

**Docker:**
```bash
docker-run.bat
```

**Web UI:**
```bash
docker-web.bat
```

Pick one and start generating! 🎨
