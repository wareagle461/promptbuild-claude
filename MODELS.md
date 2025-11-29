# Uncensored Models Guide

Complete guide to uncensored and capable models for prompt generation.

## Recommended Uncensored Text Models

### Tier 1: Best for Prompt Generation

#### dolphin-mistral
```bash
ollama pull dolphin-mistral
```
- **Size**: ~4GB
- **Speed**: Fast
- **Censorship**: None - highly uncensored
- **Best for**: Quick, detailed prompts without restrictions
- **Recommended**: ✅ Primary choice

#### dolphin-mixtral
```bash
ollama pull dolphin-mixtral
```
- **Size**: ~26GB
- **Speed**: Slower
- **Censorship**: None - highly uncensored
- **Best for**: Complex, highly detailed prompts
- **Recommended**: For users with powerful hardware

### Tier 2: Alternative Uncensored Models

#### nous-hermes2
```bash
ollama pull nous-hermes2
```
- **Size**: ~4GB
- **Censorship**: Minimal restrictions
- **Best for**: Creative writing, detailed descriptions

#### wizardlm-uncensored
```bash
ollama pull wizardlm-uncensored
```
- **Size**: ~4GB
- **Censorship**: Minimal restrictions
- **Best for**: Technical prompts, detailed specifications

#### neural-chat
```bash
ollama pull neural-chat
```
- **Size**: ~4GB
- **Censorship**: Low restrictions
- **Best for**: Conversational prompt refinement

## Vision Models (Image Reference Support)

### llava
```bash
ollama pull llava
```
- **Size**: ~4GB
- **Vision**: Yes
- **Best for**: Standard image analysis
- **Recommended**: ✅ Primary vision model

### llava:34b
```bash
ollama pull llava:34b
```
- **Size**: ~20GB
- **Vision**: Yes
- **Best for**: Detailed image analysis
- **Requires**: 32GB+ RAM

### bakllava
```bash
ollama pull bakllava
```
- **Size**: ~4GB
- **Vision**: Yes
- **Best for**: Alternative to llava

## Experimental/Advanced Models

### dolphin2.2-mistral
```bash
ollama pull dolphin2.2-mistral
```
- Latest Dolphin variant
- Enhanced capabilities
- ~4GB

### openchat
```bash
ollama pull openchat
```
- Strong general performance
- Minimal restrictions
- ~4GB

### starling-lm
```bash
ollama pull starling-lm
```
- High quality outputs
- Good for creative prompts
- ~4GB

## Model Selection Guide

### For Beginners
Start with:
```bash
ollama pull dolphin-mistral
ollama pull llava
```

### For Power Users
```bash
ollama pull dolphin-mixtral
ollama pull llava:34b
```

### For Limited Hardware
```bash
ollama pull dolphin-mistral
# Skip vision models if needed
```

### For Maximum Quality
```bash
ollama pull dolphin-mixtral
ollama pull llava:34b
ollama pull nous-hermes2  # backup
```

## Hardware Requirements

### Minimum (4GB VRAM/RAM)
- dolphin-mistral
- llava
- Any single 7B model

### Recommended (16GB RAM)
- dolphin-mistral + llava
- Multiple 7B models
- Good performance

### Optimal (32GB+ RAM)
- dolphin-mixtral
- llava:34b
- Multiple large models
- Best quality

## Testing Models

After installation, test each model:

```bash
# Test text generation
ollama run dolphin-mistral "Write a detailed scene description"

# Test vision (with image path)
ollama run llava "Describe this image in detail" /path/to/image.jpg
```

## Model Performance Comparison

| Model | Size | Speed | Quality | Uncensored | Vision |
|-------|------|-------|---------|------------|--------|
| dolphin-mistral | 4GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | ✅✅✅ | ❌ |
| dolphin-mixtral | 26GB | ⚡ | ⭐⭐⭐⭐⭐ | ✅✅✅ | ❌ |
| nous-hermes2 | 4GB | ⚡⚡ | ⭐⭐⭐ | ✅✅ | ❌ |
| llava | 4GB | ⚡⚡ | ⭐⭐⭐ | ➖ | ✅ |
| llava:34b | 20GB | ⚡ | ⭐⭐⭐⭐⭐ | ➖ | ✅ |

## Switching Models in the Tool

### Interactive Mode
```bash
python prompt_generator.py
> /model dolphin-mixtral
> your prompt here
```

### CLI Mode
```bash
python prompt_generator.py "your prompt" --model dolphin-mixtral
```

### In Code
```python
from prompt_generator import PromptGenerator

generator = PromptGenerator()
generator.text_model = "dolphin-mixtral"  # Change default
generator.vision_model = "llava:34b"      # Change vision model

# Or override per-call
result = generator.generate_prompt(
    "your prompt",
    model_override="nous-hermes2"
)
```

## Keeping Models Updated

Check for updates:
```bash
ollama list  # See installed models
ollama pull dolphin-mistral  # Update specific model
```

## Removing Models

If you need space:
```bash
ollama rm model-name
```

Example:
```bash
ollama rm llava:34b  # Remove large vision model
```

## Finding More Models

Browse all available models:
```bash
ollama search uncensored
ollama search vision
```

Or visit: https://ollama.com/library

## Pro Tips

1. **Keep 2-3 models**: One fast (mistral), one quality (mixtral), one vision (llava)
2. **Test before committing**: Try a model with `ollama run` before using in tool
3. **Mix and match**: Use fast models for iteration, slow models for final prompts
4. **Monitor resources**: Check RAM/VRAM usage with larger models
5. **Update regularly**: New uncensored models are released frequently

## Troubleshooting

**Model won't load:**
- Check available RAM/VRAM
- Try smaller model variant
- Close other applications

**Poor quality outputs:**
- Try larger model (mixtral vs mistral)
- Adjust your prompt for clarity
- Use vision model if you have reference images

**Too slow:**
- Switch to smaller model
- Use GPU acceleration if available
- Check if other Ollama instances are running
