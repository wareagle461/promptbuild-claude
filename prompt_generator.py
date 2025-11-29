#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uncensored Prompt Generator using Ollama
Generates detailed image and video prompts with optional image reference support
"""

import requests
import json
import base64
import sys
import os
from pathlib import Path
from typing import Optional

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class PromptGenerator:
    def __init__(self, ollama_host: str = None):
        # Support environment variable for Docker/custom setups
        self.ollama_host = ollama_host or os.getenv("OLLAMA_HOST", "http://localhost:11434")

        # Try to auto-detect best available models
        self.text_model = self._find_best_text_model()
        self.vision_model = self._find_best_vision_model()

    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=10)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.Timeout:
            return False
        except Exception:
            return False

    def test_ollama_connection(self) -> dict:
        """Test Ollama connection with detailed diagnostics"""
        result = {
            'success': False,
            'ollama_host': self.ollama_host,
            'error': None,
            'error_type': None,
            'models_count': 0,
            'response_time_ms': 0
        }

        import time
        start_time = time.time()

        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=10)
            result['response_time_ms'] = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                models = response.json().get('models', [])
                result['success'] = True
                result['models_count'] = len(models)
            else:
                result['error'] = f"HTTP {response.status_code}: {response.text[:200]}"
                result['error_type'] = 'http_error'

        except requests.exceptions.ConnectionError as e:
            result['response_time_ms'] = int((time.time() - start_time) * 1000)
            result['error'] = f"Connection refused - Ollama may not be running at {self.ollama_host}"
            result['error_type'] = 'connection_refused'
        except requests.exceptions.Timeout:
            result['response_time_ms'] = int((time.time() - start_time) * 1000)
            result['error'] = f"Connection timed out after 10 seconds"
            result['error_type'] = 'timeout'
        except requests.exceptions.InvalidURL:
            result['response_time_ms'] = int((time.time() - start_time) * 1000)
            result['error'] = f"Invalid URL: {self.ollama_host}"
            result['error_type'] = 'invalid_url'
        except Exception as e:
            result['response_time_ms'] = int((time.time() - start_time) * 1000)
            result['error'] = str(e)
            result['error_type'] = 'unknown'

        return result

    def set_ollama_host(self, host: str) -> dict:
        """Update Ollama host and re-detect models"""
        old_host = self.ollama_host
        self.ollama_host = host.rstrip('/')

        # Test the new connection
        test_result = self.test_ollama_connection()

        if test_result['success']:
            # Re-detect models with new host
            self.text_model = self._find_best_text_model()
            self.vision_model = self._find_best_vision_model()
            return {
                'success': True,
                'ollama_host': self.ollama_host,
                'text_model': self.text_model,
                'vision_model': self.vision_model,
                'models_count': test_result['models_count']
            }
        else:
            # Revert to old host on failure
            self.ollama_host = old_host
            return {
                'success': False,
                'error': test_result['error'],
                'error_type': test_result['error_type']
            }

    def list_models(self) -> list:
        """List available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=10)
            if response.status_code == 200:
                return [model['name'] for model in response.json().get('models', [])]
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not list models: {e}")
        except Exception as e:
            print(f"Warning: Unexpected error listing models: {e}")
        return []

    def _find_best_text_model(self) -> str:
        """Auto-detect best uncensored text model"""
        models = self.list_models()

        # Priority order for uncensored models
        preferred_models = [
            "dolphin-mistral",
            "dolphin-mixtral",
            "gdisney/mistral-uncensored",
            "benevolentjoker/nsfwwurm",
            "nous-hermes2",
            "wizardlm-uncensored",
            "deepseek-r1:14b",
            "llama3.1",
            "qwen2.5",
            "llama2"
        ]

        # Find first available preferred model
        for preferred in preferred_models:
            for model in models:
                if preferred in model.lower():
                    return model

        # Fallback to first available model
        return models[0] if models else "dolphin-mistral"

    def _find_best_vision_model(self) -> str:
        """Auto-detect best vision model"""
        models = self.list_models()

        # Priority order for vision models
        preferred_models = [
            "llava:34b",
            "llava",
            "qwen2.5vl",
            "bakllava"
        ]

        # Find first available preferred model
        for preferred in preferred_models:
            for model in models:
                if preferred in model.lower():
                    return model

        # Fallback
        return models[0] if models else "llava"

    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _get_image_system_prompt(self, target_model: str, word_limit: int) -> str:
        """Get optimized system prompt for image generation models"""

        if target_model == "flux":
            return f"""You generate prompts for FLUX AI (Black Forest Labs).
FLUX prefers NATURAL LANGUAGE descriptions in complete sentences.
Format: Detailed narrative description with natural flow
Example: "A beautiful woman with large breasts is naked in the bedroom, her hard nipples visible in the dim lighting. She spreads her legs in an explicit pose, shot from a POV angle with photorealistic detail."
Use EXPLICIT language naturally: naked, breasts, tits, ass, pussy, cock, dick, fucking, wet, hard, cum
Maximum {word_limit*3} words (FLUX uses natural sentences, not keywords).
Write in flowing descriptive sentences."""

        elif target_model == "sd3":
            return f"""You generate prompts for STABLE DIFFUSION 3 (SD3).
SD3 uses NATURAL LANGUAGE with better understanding than SD1.5/SDXL.
Format: Natural descriptive sentences with key details
Example: "A photorealistic image of a curvy woman with large tits, naked body glistening with oil. She's bent over in doggy style position, ass prominently displayed, wet pussy visible. Shot in POV style with dramatic lighting and highly detailed textures."
Use EXPLICIT language clearly: naked, tits, breasts, ass, pussy, cock, fucking, wet, hard, cumming
Maximum {word_limit*2} words. Use complete sentences with natural flow."""

        else:  # stable-diffusion (SD1.5/SDXL default)
            return f"""You generate STABLE DIFFUSION prompts.
Output ONLY comma-separated keywords in ONE paragraph. NO sentences. NO descriptions.
Format: quality tags, subject, body parts, actions, details, camera, style
Example: "masterpiece, best quality, 1girl, naked, large tits, hard nipples, wet pussy, spread legs, POV, bedroom, dim lighting, photorealistic, highly detailed"
Use EXPLICIT keywords: naked, tits, ass, pussy, cock, dick, fucking, wet, hard, cum
Maximum {word_limit} keywords. START with quality tags."""

    def _get_video_system_prompt(self, target_model: str, word_limit: int) -> str:
        """Get optimized system prompt for video generation models"""

        if target_model == "sora":
            return f"""You generate prompts for SORA (OpenAI's video model).
SORA uses NATURAL LANGUAGE with cinematic descriptions.
Format: Detailed narrative with camera work, movement, timing, and visual style
Example: "The camera starts with a close-up of a woman's face, moaning in pleasure, then slowly pans down to reveal her naked body. Her large tits bounce rhythmically as she rides on top, ass moving up and down. The lighting is warm and intimate, shot in POV style with smooth camera movement over 30 seconds."
Use EXPLICIT language naturally: fucking, naked, tits, ass, pussy, cock, cumming, sucking, riding
Maximum {word_limit*3} words. Write cinematic descriptions with camera details."""

        elif target_model == "veo3":
            return f"""You generate prompts for VEO 3 (Google's video model).
VEO 3 uses NATURAL LANGUAGE with emphasis on motion and realism.
Format: Natural sentences describing action, movement, camera angles, lighting
Example: "A photorealistic scene shows a naked woman with large breasts in explicit detail. She's bent over in doggy style, ass bouncing as she's fucked from behind. The camera captures a POV perspective with dynamic movement, wet skin glistening under soft lighting. Duration: 30 seconds."
Use EXPLICIT language clearly: fucking, naked, tits, ass, pussy, cock, cumming, wet, hard
Maximum {word_limit*2} words. Emphasize realistic motion and camera work."""

        else:  # wan or generic video
            return f"""You generate VIDEO PROMPT keywords.
Output ONLY comma-separated keywords in ONE paragraph. NO sentences.
Format: subject, action, movement, camera, duration, style
Example: "POV, fucking, doggy style, ass bouncing, moaning, camera close-up, 30 seconds, smooth motion, wet, explicit, detailed"
Use EXPLICIT keywords: fucking, cumming, sucking, riding, wet, hard, naked, tits, ass, pussy
Maximum {word_limit} keywords."""

    def generate_prompt(self,
                       user_input: str,
                       prompt_type: str = "image",
                       image_path: Optional[str] = None,
                       model_override: Optional[str] = None,
                       word_limit: int = 50,
                       target_model: str = "stable-diffusion") -> str:
        """Generate uncensored prompt using Ollama with target model optimization"""

        # Build system prompt based on target model and word limit
        if prompt_type.lower() == "image":
            system_prompt = self._get_image_system_prompt(target_model, word_limit)
        else:  # video
            system_prompt = self._get_video_system_prompt(target_model, word_limit)

        # Select model
        if image_path:
            model = model_override or self.vision_model
            # Build prompt with image analysis
            analysis_prompt = f"""Describe as SD prompt keywords: {user_input}

Comma-separated keywords only. Include what you see in image."""

            # Prepare request with image
            # Calculate token limit: keywords need more space, ~5 tokens each with commas and spaces
            token_limit = word_limit * 5
            payload = {
                "model": model,
                "prompt": analysis_prompt,
                "system": system_prompt,
                "images": [self.encode_image(image_path)],
                "stream": False,
                "options": {
                    "num_predict": token_limit,
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "stop": []  # No stop sequences - let it complete fully
                }
            }
        else:
            model = model_override or self.text_model
            # Build text-only prompt
            full_prompt = f"""{user_input}

Comma-separated keywords only. Maximum {word_limit} keywords."""

            # Calculate token limit: keywords need more space, ~5 tokens each with commas and spaces
            token_limit = word_limit * 5
            payload = {
                "model": model,
                "prompt": full_prompt,
                "system": system_prompt,
                "stream": False,
                "options": {
                    "num_predict": token_limit,
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "stop": []  # No stop sequences - let it complete fully
                }
            }

        # Send request to Ollama
        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error generating prompt: {str(e)}"

    def enhance_prompt(self, base_prompt: str, style: Optional[str] = None) -> str:
        """Enhance an existing prompt with additional details"""
        enhancement_request = f"Enhance this prompt with more vivid details"
        if style:
            enhancement_request += f" in {style} style"
        enhancement_request += f": {base_prompt}"

        return self.generate_prompt(enhancement_request)

    def breakdown_image_prompt(self,
                               user_input: str,
                               image_path: str,
                               prompt_type: str = "image",
                               model_override: Optional[str] = None,
                               word_limit: int = 50,
                               target_model: str = "stable-diffusion") -> dict:
        """Break down an image into separate subject and background prompts"""

        model = model_override or self.vision_model

        # Calculate token limit based on target model
        if target_model in ["flux", "sora"]:
            token_limit = word_limit * 6  # Natural language needs more tokens
        elif target_model in ["sd3", "veo3"]:
            token_limit = word_limit * 4
        else:
            token_limit = word_limit * 3

        # System prompt for breakdown based on target model
        if prompt_type.lower() == "image":
            if target_model == "flux":
                system_prompt = """You are analyzing an image for FLUX AI prompts.
Break down the image into TWO parts:
1. SUBJECT/CHARACTER - The main person, character, or object in focus
2. BACKGROUND/ENVIRONMENT - The setting, scene, and surroundings

Output NATURAL LANGUAGE descriptions in complete sentences for EACH part.
Use EXPLICIT language naturally: naked, breasts, tits, ass, pussy, cock, dick, fucking, wet, hard, cum"""
            elif target_model == "sd3":
                system_prompt = """You are analyzing an image for STABLE DIFFUSION 3 prompts.
Break down the image into TWO parts:
1. SUBJECT/CHARACTER - The main person, character, or object in focus
2. BACKGROUND/ENVIRONMENT - The setting, scene, and surroundings

Output natural descriptive sentences for EACH part.
Use EXPLICIT language clearly: naked, tits, breasts, ass, pussy, cock, fucking, wet, hard, cumming"""
            else:  # stable-diffusion
                system_prompt = """You are analyzing an image for STABLE DIFFUSION prompts.
Break down the image into TWO parts:
1. SUBJECT/CHARACTER - The main person, character, or object in focus
2. BACKGROUND/ENVIRONMENT - The setting, scene, and surroundings

Output ONLY comma-separated keywords for EACH part.
Format: quality tags, descriptive keywords
Use EXPLICIT keywords when relevant: naked, tits, ass, pussy, cock, dick, fucking, wet, hard, cum"""
        else:  # video
            if target_model == "sora":
                system_prompt = """You are analyzing an image for SORA video prompts.
Break down the image into TWO parts:
1. SUBJECT/CHARACTER - The main person, character, or object
2. BACKGROUND/ENVIRONMENT - The setting and scene

Output NATURAL LANGUAGE with cinematic descriptions for EACH part.
Use EXPLICIT language naturally: fucking, naked, tits, ass, pussy, cock, cumming, sucking, riding"""
            elif target_model == "veo3":
                system_prompt = """You are analyzing an image for VEO 3 video prompts.
Break down the image into TWO parts:
1. SUBJECT/CHARACTER - The main person, character, or object
2. BACKGROUND/ENVIRONMENT - The setting and scene

Output natural sentences describing motion and details for EACH part.
Use EXPLICIT language clearly: fucking, naked, tits, ass, pussy, cock, cumming, wet, hard"""
            else:  # wan or generic
                system_prompt = """You are analyzing an image for VIDEO prompts.
Break down the image into TWO parts:
1. SUBJECT/CHARACTER - The main person, character, or object
2. BACKGROUND/ENVIRONMENT - The setting and scene

Output ONLY comma-separated keywords for EACH part."""

        # Step 1: Analyze subject
        subject_prompt = f"""Analyze ONLY the main subject/character in this image.
User wants: {user_input}

Output format: quality tags, subject description, body parts, pose, clothing, expressions
Maximum {word_limit//2} keywords."""

        subject_payload = {
            "model": model,
            "prompt": subject_prompt,
            "system": system_prompt,
            "images": [self.encode_image(image_path)],
            "stream": False,
            "options": {
                "num_predict": (token_limit // 2) + 50,  # Extra buffer
                "temperature": 0.9,
                "top_p": 0.95,
                "stop": []  # No stop sequences - let it complete
            }
        }

        # Step 2: Analyze background
        background_prompt = f"""Analyze ONLY the background/environment in this image.
User wants: {user_input}

Output format: location, setting, lighting, atmosphere, details, style
Maximum {word_limit//2} keywords."""

        background_payload = {
            "model": model,
            "prompt": background_prompt,
            "system": system_prompt,
            "images": [self.encode_image(image_path)],
            "stream": False,
            "options": {
                "num_predict": (token_limit // 2) + 50,  # Extra buffer
                "temperature": 0.9,
                "top_p": 0.95,
                "stop": []  # No stop sequences - let it complete
            }
        }

        try:
            # Generate subject prompt
            print(f"🎬 Analyzing subject...")
            subject_response = requests.post(
                f"{self.ollama_host}/api/generate",
                json=subject_payload,
                timeout=120
            )

            subject_result = ""
            if subject_response.status_code == 200:
                subject_result = subject_response.json().get('response', '').strip()

            # Generate background prompt
            print(f"🌄 Analyzing background...")
            background_response = requests.post(
                f"{self.ollama_host}/api/generate",
                json=background_payload,
                timeout=120
            )

            background_result = ""
            if background_response.status_code == 200:
                background_result = background_response.json().get('response', '').strip()

            # Combine them
            combined_result = f"{subject_result}, {background_result}"

            return {
                'subject': subject_result,
                'background': background_result,
                'combined': combined_result
            }

        except Exception as e:
            return {
                'subject': f"Error: {str(e)}",
                'background': f"Error: {str(e)}",
                'combined': f"Error: {str(e)}"
            }


def interactive_mode():
    """Run in interactive mode"""
    print("=" * 60)
    print("Uncensored Prompt Generator - Ollama Edition")
    print("=" * 60)

    generator = PromptGenerator()

    # Check Ollama connection
    print("\nChecking Ollama connection...")
    if not generator.check_ollama_connection():
        print("❌ Cannot connect to Ollama!")
        print("Make sure Ollama is running: ollama serve")
        print(f"Expected at: {generator.ollama_host}")
        sys.exit(1)

    print(f"✓ Connected to Ollama at {generator.ollama_host}")

    # Show selected default models
    print(f"\n✓ Default text model: {generator.text_model}")
    print(f"✓ Default vision model: {generator.vision_model}")

    # List available models
    models = generator.list_models()
    if models:
        print(f"\n📚 Total models available: {len(models)}")
        print(f"   ({', '.join(models[:5])}{'...' if len(models) > 5 else ''})")
    else:
        print("\n⚠ No models found. Install recommended models:")
        print("  ollama pull dolphin-mistral  # Uncensored text model")
        print("  ollama pull llava            # Vision model for image analysis")

    print("\n" + "=" * 60)
    print("Commands:")
    print("  Type your request directly")
    print("  /image [path] - Set reference image")
    print("  /video - Switch to video prompt mode")
    print("  /img - Switch to image prompt mode")
    print("  /model [name] - Override model")
    print("  /list - List all available models")
    print("  /clear - Clear reference image")
    print("  /quit - Exit")
    print("=" * 60 + "\n")

    # State
    reference_image = None
    prompt_type = "image"
    model_override = None

    while True:
        try:
            user_input = input(f"\n[{prompt_type.upper()}] > ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith('/'):
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()

                if command == '/quit':
                    print("Goodbye!")
                    break
                elif command == '/image' and len(parts) > 1:
                    image_path = parts[1].strip()
                    if Path(image_path).exists():
                        reference_image = image_path
                        print(f"✓ Reference image set: {image_path}")
                    else:
                        print(f"❌ Image not found: {image_path}")
                elif command == '/clear':
                    reference_image = None
                    print("✓ Reference image cleared")
                elif command == '/video':
                    prompt_type = "video"
                    print("✓ Switched to VIDEO prompt mode")
                elif command == '/img':
                    prompt_type = "image"
                    print("✓ Switched to IMAGE prompt mode")
                elif command == '/model' and len(parts) > 1:
                    model_override = parts[1].strip()
                    print(f"✓ Model override set: {model_override}")
                elif command == '/list':
                    all_models = generator.list_models()
                    print(f"\n📚 All available models ({len(all_models)}):")
                    for idx, model in enumerate(all_models, 1):
                        marker = ""
                        if model == generator.text_model:
                            marker = " (default text)"
                        elif model == generator.vision_model:
                            marker = " (default vision)"
                        print(f"  {idx}. {model}{marker}")
                else:
                    print("❌ Unknown command or missing argument")
                continue

            # Generate prompt
            print("\n🔄 Generating prompt...")
            result = generator.generate_prompt(
                user_input,
                prompt_type=prompt_type,
                image_path=reference_image,
                model_override=model_override
            )

            print("\n" + "=" * 60)
            print("GENERATED PROMPT:")
            print("=" * 60)
            print(result)
            print("=" * 60)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def cli_mode(args):
    """Run in CLI mode with arguments"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate uncensored image/video prompts")
    parser.add_argument("prompt", help="Your prompt request")
    parser.add_argument("-t", "--type", choices=["image", "video"], default="image",
                       help="Prompt type (default: image)")
    parser.add_argument("-i", "--image", help="Reference image path")
    parser.add_argument("-m", "--model", help="Override default model")
    parser.add_argument("--host", default=None,
                       help="Ollama host (default: env OLLAMA_HOST or http://localhost:11434)")

    parsed_args = parser.parse_args(args)

    generator = PromptGenerator(ollama_host=parsed_args.host)

    if not generator.check_ollama_connection():
        print("❌ Cannot connect to Ollama at", parsed_args.host)
        sys.exit(1)

    result = generator.generate_prompt(
        parsed_args.prompt,
        prompt_type=parsed_args.type,
        image_path=parsed_args.image,
        model_override=parsed_args.model
    )

    print(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode(sys.argv[1:])
    else:
        interactive_mode()
