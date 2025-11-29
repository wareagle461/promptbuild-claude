# Uncensored Prompt Generator

A local, privacy-focused prompt generator for image and video generation using Ollama. Supports reference image analysis and generates detailed, uncensored prompts.

## Features

- 🔓 **Uncensored**: Runs locally with no content restrictions
- 🖼️ **Image Reference**: Analyze and incorporate reference images
- 🎬 **Multi-Format**: Generate prompts for both images and videos
- 🏠 **100% Local**: All processing happens on your machine
- 🚀 **Interactive & CLI modes**: Use interactively or in scripts

## Requirements

- Python 3.7+
- Ollama installed and running

## Installation

### 1. Install Ollama

**Windows:**
Download from [ollama.com](https://ollama.com/download/windows)

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Recommended Ollama Models

**Uncensored text models (choose one or more):**

```bash
# Dolphin Mistral (Recommended - highly uncensored)
ollama pull dolphin-mistral

# Dolphin Mixtral (Larger, more capable)
ollama pull dolphin-mixtral

# Nous Hermes (Alternative uncensored model)
ollama pull nous-hermes2

# WizardLM Uncensored
ollama pull wizardlm-uncensored
```

**Vision models (for image reference support):**

```bash
# LLaVA (Recommended)
ollama pull llava

# BakLLaVA (Alternative)
ollama pull bakllava

# LLaVA 34B (Larger, more detailed)
ollama pull llava:34b
```

## Usage

### Interactive Mode

Simply run the script:

```bash
python prompt_generator.py
```

**Commands:**
- Type your request directly to generate prompts
- `/image [path]` - Set a reference image
- `/video` - Switch to video prompt mode
- `/img` - Switch to image prompt mode
- `/model [name]` - Override the default model
- `/clear` - Clear reference image
- `/quit` - Exit

**Example session:**
```
[IMAGE] > a cyberpunk city at night

🔄 Generating prompt...

============================================================
GENERATED PROMPT:
============================================================
A sprawling cyberpunk metropolis under a neon-lit night sky...
============================================================

[IMAGE] > /image reference.jpg
✓ Reference image set: reference.jpg

[IMAGE] > create similar but with rain
```

### CLI Mode

Use in scripts or one-off generations:

```bash
# Basic usage
python prompt_generator.py "a fantasy landscape"

# Video prompt
python prompt_generator.py "epic battle scene" --type video

# With reference image
python prompt_generator.py "enhance this style" --image reference.jpg

# Override model
python prompt_generator.py "portrait" --model dolphin-mixtral
```

## Recommended Uncensored Models

### Best for Prompt Generation:

1. **dolphin-mistral** - Fast, highly uncensored, great for prompts
2. **dolphin-mixtral** - More capable but slower
3. **nous-hermes2** - Good alternative
4. **wizardlm-uncensored** - Reliable uncensored option

### For Image Analysis:

1. **llava** - Standard vision model
2. **llava:34b** - Higher quality analysis (requires more RAM)
3. **bakllava** - Alternative vision model

## Configuration

Edit the script to change default models:

```python
self.text_model = "dolphin-mistral"  # Your preferred text model
self.vision_model = "llava"           # Your preferred vision model
```

Or use the `/model` command in interactive mode.

## Tips for Best Results

1. **Be Specific**: The more details you provide, the better the output
2. **Use References**: Image references help maintain style consistency
3. **Iterate**: Generate, refine, and regenerate for best results
4. **Model Selection**: Larger models (mixtral, 34b) give more detailed prompts but are slower

## Troubleshooting

### "Cannot connect to Ollama"

Make sure Ollama is running:
```bash
ollama serve
```

### "Model not found"

Pull the model first:
```bash
ollama pull dolphin-mistral
ollama pull llava
```

### Slow generation

- Use smaller models (mistral instead of mixtral)
- Close other applications
- Check if GPU acceleration is working: `ollama list`

### Out of memory

- Use smaller models
- For vision models, try `llava:7b` instead of `llava:34b`
- Close other applications

## Privacy & Safety

- ✅ 100% local processing
- ✅ No data sent to external servers
- ✅ No logging or tracking
- ✅ Full control over content generation

## Advanced Usage

### Batch Processing

Create a script to generate multiple prompts:

```python
from prompt_generator import PromptGenerator

generator = PromptGenerator()

prompts = [
    "fantasy castle",
    "sci-fi spaceship",
    "portrait of warrior"
]

for prompt in prompts:
    result = generator.generate_prompt(prompt)
    print(f"{prompt} -> {result}\n")
```

### Custom System Prompts

Modify the system prompts in the script for different output styles.

## License

Free to use and modify for any purpose.

## Disclaimer

This tool is for creative and artistic purposes. Users are responsible for ensuring their use complies with applicable laws and the terms of service of any platforms where generated content is used.
