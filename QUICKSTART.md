# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Ollama

**Windows:**
1. Download from https://ollama.com/download/windows
2. Run the installer
3. Ollama will start automatically

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

## Step 2: Install the Models

Open a terminal and run:

```bash
# Essential: Uncensored text model (choose ONE)
ollama pull dolphin-mistral

# Optional: For image reference support
ollama pull llava
```

Wait for downloads to complete (this may take a few minutes).

## Step 3: Install Python Requirements

```bash
pip install -r requirements.txt
```

## Step 4: Run It!

```bash
python prompt_generator.py
```

## First Commands to Try

Once the interactive prompt appears:

```
# Generate an image prompt
[IMAGE] > a dragon flying over mountains

# Switch to video mode
[IMAGE] > /video

# Generate a video prompt
[VIDEO] > cinematic battle scene with explosions

# Use a reference image
[VIDEO] > /img
[IMAGE] > /image my_reference.jpg
[IMAGE] > create something similar but darker
```

## That's It!

You now have a fully functional, uncensored, local prompt generator.

## Common Issues

**"Cannot connect to Ollama"**
- Make sure Ollama is running: `ollama serve`
- Check if it's running: open http://localhost:11434 in your browser

**"Model not found"**
- Install it: `ollama pull dolphin-mistral`
- Check installed models: `ollama list`

**Need help?**
- See [README.md](README.md) for full documentation
- Check model compatibility: `ollama list`
