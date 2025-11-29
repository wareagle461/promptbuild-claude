# Your Setup - Ready to Go! ✓

## What's Already Configured

Your Ollama installation has been detected with the following models:

### ✓ Uncensored Text Model
**gdisney/mistral-uncensored:latest** (auto-detected as default)
- This is an excellent uncensored model for generating prompts
- No content restrictions or filtering

### ✓ Vision Model
**llava:latest** (auto-detected as default)
- Supports image reference analysis
- Can describe and enhance based on reference images

### ✓ Other Available Models
You also have 12 other models available:
- gpt-oss:latest
- llama2, vicuna
- qwen2.5, qwen2.5-coder, qwen2.5vl
- deepseek-coder, deepseek-r1:14b
- llama3.1
- benevolentjoker/nsfwwurm (another uncensored option!)
- And more...

## Quick Start - 3 Ways to Use

### 1. Interactive Mode (Recommended)
```bash
py prompt_generator.py
```

Then type your requests:
```
[IMAGE] > a dark fantasy warrior
[IMAGE] > /video
[VIDEO] > epic battle with dragons
[VIDEO] > /list        # See all your models
[VIDEO] > /model benevolentjoker/nsfwwurm  # Switch models
```

### 2. Command Line (One-shot)
```bash
# Generate an image prompt
py prompt_generator.py "a cyberpunk street scene"

# Generate a video prompt
py prompt_generator.py "epic battle scene" --type video

# Use a reference image
py prompt_generator.py "make it darker" --image reference.jpg

# Use a specific model
py prompt_generator.py "fantasy scene" --model benevolentjoker/nsfwwurm
```

### 3. Windows Launcher
Just double-click:
```
run.bat
```

## Your Current Models Explained

### Best for Uncensored Prompts:
1. **gdisney/mistral-uncensored** ⭐ (current default)
   - Fast and uncensored
   - Great for detailed prompts

2. **benevolentjoker/nsfwwurm** ⭐
   - Highly uncensored
   - Good for adult/mature content prompts
   - Use with: `/model benevolentjoker/nsfwwurm`

### Best for Image References:
1. **llava** ⭐ (current default)
   - Standard vision model
   - Good for analyzing reference images

2. **qwen2.5vl**
   - Alternative vision model
   - Use with: `/model qwen2.5vl`

### General Purpose Models:
- **deepseek-r1:14b** - Larger, more capable (slower)
- **llama3.1** - Meta's latest, very capable
- **qwen2.5-coder** - Good for technical prompts

## Examples to Try Right Now

### Example 1: Simple Prompt
```bash
py prompt_generator.py "a warrior in dark armor"
```

### Example 2: Explicit Uncensored Model
```bash
py prompt_generator.py "sensual portrait" --model benevolentjoker/nsfwwurm
```

### Example 3: With Reference Image
```bash
# First, put an image in this folder (e.g., reference.jpg)
py prompt_generator.py "similar style but darker" --image reference.jpg
```

### Example 4: Video Prompt
```bash
py prompt_generator.py "camera flying through clouds" --type video
```

### Example 5: Interactive Session
```bash
py prompt_generator.py

# Then inside:
[IMAGE] > /model benevolentjoker/nsfwwurm
[IMAGE] > a detailed erotic scene
[IMAGE] > /video
[VIDEO] > intense action sequence with violence
[VIDEO] > /list   # See all models
```

## Switching Models

You have 2 great uncensored models installed:

**For most prompts:** (already default)
```bash
py prompt_generator.py "your prompt"
```

**For maximum uncensored:** (using nsfwwurm)
```bash
py prompt_generator.py "your prompt" --model benevolentjoker/nsfwwurm
```

**In interactive mode:**
```
[IMAGE] > /model benevolentjoker/nsfwwurm
[IMAGE] > your prompt here
```

## Want More Models?

### Add Dolphin (highly recommended uncensored)
```bash
ollama pull dolphin-mistral
```

### Add Better Vision
```bash
ollama pull llava:34b
```

### Add More Uncensored Options
```bash
ollama pull dolphin-mixtral
ollama pull nous-hermes2
ollama pull wizardlm-uncensored
```

See [MODELS.md](MODELS.md) for complete model guide.

## Environment Variables (Optional)

If you ever move Ollama to a different port or host:
```bash
# Windows
set OLLAMA_HOST=http://localhost:11434
py prompt_generator.py

# Or pass directly
py prompt_generator.py "prompt" --host http://localhost:11434
```

## Troubleshooting

**Script won't start?**
- Make sure: `ollama serve` is running
- Check: `curl http://localhost:11434/api/tags`

**Want to see all models?**
```bash
ollama list
```

**Model not working?**
```bash
ollama run gdisney/mistral-uncensored "test"
```

## What You Have vs What Was Planned

| Feature | Status |
|---------|--------|
| Ollama Running | ✅ Working |
| Uncensored Model | ✅ You have 2! |
| Vision Support | ✅ llava installed |
| Auto-detection | ✅ Configured |
| CLI Mode | ✅ Ready |
| Interactive Mode | ✅ Ready |
| Image Reference | ✅ Ready |
| Video Prompts | ✅ Ready |

## You're All Set!

Your system is already configured with:
- ✅ Ollama running
- ✅ 2 uncensored models ready to use
- ✅ Vision model for image references
- ✅ 14 total models available

Just run:
```bash
py prompt_generator.py
```

And start generating! No additional setup needed.
