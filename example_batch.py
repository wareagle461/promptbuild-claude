#!/usr/bin/env python3
"""
Example: Batch prompt generation
Shows how to use the PromptGenerator programmatically
"""

from prompt_generator import PromptGenerator

def main():
    # Initialize generator
    generator = PromptGenerator()

    # Check connection
    if not generator.check_ollama_connection():
        print("Error: Ollama not running. Start it with: ollama serve")
        return

    print("Connected to Ollama!\n")

    # Example 1: Simple text prompts
    print("=" * 60)
    print("Example 1: Generating image prompts")
    print("=" * 60)

    requests = [
        "cyberpunk street scene",
        "fantasy forest with magical creatures",
        "futuristic space station interior"
    ]

    for request in requests:
        print(f"\nRequest: {request}")
        print("-" * 40)
        result = generator.generate_prompt(request, prompt_type="image")
        print(result)
        print()

    # Example 2: Video prompts
    print("\n" + "=" * 60)
    print("Example 2: Generating video prompts")
    print("=" * 60)

    video_requests = [
        "camera flying through clouds at sunset",
        "time lapse of city at night"
    ]

    for request in video_requests:
        print(f"\nRequest: {request}")
        print("-" * 40)
        result = generator.generate_prompt(request, prompt_type="video")
        print(result)
        print()

    # Example 3: With reference image (if you have one)
    print("\n" + "=" * 60)
    print("Example 3: Using reference image")
    print("=" * 60)
    print("\nTo use a reference image:")
    print("  result = generator.generate_prompt(")
    print("      'your request',")
    print("      prompt_type='image',")
    print("      image_path='/path/to/image.jpg'")
    print("  )")

    # Example 4: Model override
    print("\n" + "=" * 60)
    print("Example 4: Using different models")
    print("=" * 60)

    available_models = generator.list_models()
    print(f"\nAvailable models: {', '.join(available_models)}")

    if available_models:
        print("\nTo use a specific model:")
        print("  result = generator.generate_prompt(")
        print("      'your request',")
        print(f"      model_override='{available_models[0]}'")
        print("  )")

if __name__ == "__main__":
    main()
