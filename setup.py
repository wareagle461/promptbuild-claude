#!/usr/bin/env python3
"""
Setup script for Uncensored Prompt Generator
Helps install required models and verify setup
"""

import subprocess
import sys
import requests
from pathlib import Path

def check_python():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} found, need 3.7+")
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    print("\nChecking Ollama...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama is running")
            return True, response.json().get('models', [])
    except requests.exceptions.ConnectionError:
        print("✗ Ollama is not running")
        print("  Start it with: ollama serve")
        return False, []
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False, []

def install_pip_requirements():
    """Install Python requirements"""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Python dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def install_ollama_model(model_name):
    """Install an Ollama model"""
    print(f"\nInstalling {model_name}...")
    print("This may take several minutes...")
    try:
        subprocess.check_call(["ollama", "pull", model_name])
        print(f"✓ {model_name} installed")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {model_name}")
        return False
    except FileNotFoundError:
        print("✗ 'ollama' command not found")
        print("  Install Ollama from: https://ollama.com")
        return False

def main():
    print("=" * 60)
    print("Uncensored Prompt Generator - Setup")
    print("=" * 60)

    all_good = True

    # Check Python
    if not check_python():
        all_good = False
        print("\n⚠ Please upgrade Python to 3.7 or higher")

    # Check Ollama
    ollama_running, installed_models = check_ollama()
    if not ollama_running:
        all_good = False
        print("\n⚠ Please start Ollama:")
        print("  Run: ollama serve")
        print("  Or install from: https://ollama.com")
        print("\nThen run this setup script again.")
        return

    # Get installed model names
    installed_names = [m['name'] for m in installed_models] if installed_models else []
    print(f"\nCurrently installed models: {', '.join(installed_names) if installed_names else 'none'}")

    # Install pip requirements
    if not install_pip_requirements():
        all_good = False

    # Prompt for model installation
    print("\n" + "=" * 60)
    print("Model Installation")
    print("=" * 60)

    print("\nRecommended models:")
    print("  1. dolphin-mistral (Uncensored, fast, ~4GB)")
    print("  2. llava (Vision support for images, ~4GB)")
    print("  3. dolphin-mixtral (More capable, slower, ~26GB)")
    print("  4. llava:34b (Better vision, ~20GB)")

    models_to_install = []

    # Check for text model
    has_text_model = any(name.startswith(('dolphin', 'nous-hermes', 'wizard')) for name in installed_names)
    if not has_text_model:
        response = input("\nInstall dolphin-mistral (uncensored text model)? [Y/n]: ").strip().lower()
        if response != 'n':
            models_to_install.append("dolphin-mistral")

    # Check for vision model
    has_vision_model = any('llava' in name or 'bakllava' in name for name in installed_names)
    if not has_vision_model:
        response = input("Install llava (vision model for image reference)? [Y/n]: ").strip().lower()
        if response != 'n':
            models_to_install.append("llava")

    # Optional advanced models
    if has_text_model or 'dolphin-mistral' in models_to_install:
        response = input("\nInstall dolphin-mixtral (larger, more capable)? [y/N]: ").strip().lower()
        if response == 'y':
            models_to_install.append("dolphin-mixtral")

    # Install selected models
    if models_to_install:
        print("\n" + "=" * 60)
        print("Installing Models")
        print("=" * 60)
        print("\nThis will download several GB of data...")
        for model in models_to_install:
            if not install_ollama_model(model):
                all_good = False

    # Final summary
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)

    if all_good:
        print("\n✓ Everything is ready!")
        print("\nRun the prompt generator:")
        print("  python prompt_generator.py")
        print("\nOr see examples:")
        print("  python example_batch.py")
        print("\nRead the docs:")
        print("  See README.md or QUICKSTART.md")
    else:
        print("\n⚠ Some issues occurred during setup")
        print("Please resolve the errors above and try again")

if __name__ == "__main__":
    main()
