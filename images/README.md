# Reference Images Directory

Place your reference images here to use with the prompt generator.

## Usage

### Python
```bash
py prompt_generator.py "similar style" --image images/your-image.jpg
```

### Interactive
```
[IMAGE] > /image images/your-image.jpg
[IMAGE] > make it darker and more dramatic
```

### Docker
```bash
# Images are automatically mounted to /app/images
docker-compose run --rm prompt-generator-cli \
  python prompt_generator.py "similar" --image /app/images/your-image.jpg
```

## Supported Formats

- JPG/JPEG
- PNG
- GIF
- BMP
- WEBP

## Tips

1. Higher resolution images work better
2. Clear, well-lit images produce better analysis
3. The vision model will describe composition, style, lighting, colors, etc.
4. You can then ask to modify aspects while keeping the style

## Example Workflow

1. Put `reference.jpg` in this directory
2. Run: `[IMAGE] > /image images/reference.jpg`
3. Request: `[IMAGE] > same style but with a warrior instead`
4. The generator will analyze your image and create a prompt matching that style
