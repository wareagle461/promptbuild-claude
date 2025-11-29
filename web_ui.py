#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web UI for Uncensored Prompt Generator with Image Upload Support
"""

from flask import Flask, render_template_string, request, jsonify
from prompt_generator import PromptGenerator
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = '/app/images/uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

generator = PromptGenerator()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML Template with Image Upload
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uncensored Prompt Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .status {
            background: rgba(255,255,255,0.95);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }

        .status-item {
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }

        .status-label {
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }

        .status-value {
            font-weight: 600;
            color: #333;
        }

        .main-card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .form-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }

        textarea, select, input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e1e1;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            transition: border-color 0.3s;
        }

        textarea:focus, select:focus, input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        .file-upload-area {
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9fa;
        }

        .file-upload-area:hover {
            background: #e9ecef;
            border-color: #764ba2;
        }

        .file-upload-area.dragover {
            background: #e9ecef;
            border-color: #764ba2;
            transform: scale(1.02);
        }

        #fileInput {
            display: none;
        }

        .upload-icon {
            font-size: 3em;
            margin-bottom: 10px;
            color: #667eea;
        }

        .upload-text {
            color: #666;
            margin-bottom: 5px;
        }

        .upload-hint {
            font-size: 0.85em;
            color: #999;
        }

        .image-preview {
            display: none;
            margin-top: 15px;
            position: relative;
        }

        .image-preview.show {
            display: block;
        }

        .preview-img {
            max-width: 100%;
            max-height: 300px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .remove-image {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 18px;
            line-height: 1;
        }

        .remove-image:hover {
            background: #c82333;
        }

        .model-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        button[type="submit"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        button[type="submit"]:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        button[type="submit"]:active:not(:disabled) {
            transform: translateY(0);
        }

        button[type="submit"]:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .result {
            display: none;
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }

        .result.show {
            display: block;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .result h3 {
            color: #333;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .result-text {
            color: #555;
            line-height: 1.8;
            white-space: pre-wrap;
            font-size: 15px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            max-height: 500px;
            overflow-y: auto;
        }

        .btn-secondary {
            background: #28a745;
            padding: 8px 20px;
            font-size: 14px;
            display: inline-block;
            width: auto;
            margin-top: 10px;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
        }

        .btn-secondary:hover {
            background: #218838;
        }

        .info-badge {
            display: inline-block;
            padding: 4px 12px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: normal;
        }

        .alert {
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .alert.show {
            display: block;
        }

        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }

        .trigger-section {
            margin-bottom: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 2px solid #e9ecef;
        }

        .trigger-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .trigger-title {
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }

        .trigger-toggle {
            background: #667eea;
            color: white;
            border: none;
            padding: 6px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85em;
            transition: background 0.3s;
        }

        .trigger-toggle:hover {
            background: #764ba2;
        }

        .trigger-category {
            margin-bottom: 15px;
        }

        .category-title {
            font-size: 0.85em;
            color: #666;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .trigger-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .trigger-chip {
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
            padding: 6px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s;
            user-select: none;
        }

        .trigger-chip:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }

        .trigger-chip.active {
            background: #667eea;
            color: white;
        }

        .trigger-chip.hot {
            border-color: #dc3545;
            color: #dc3545;
        }

        .trigger-chip.hot:hover, .trigger-chip.hot.active {
            background: #dc3545;
            color: white;
        }

        .trigger-section.collapsed .trigger-chips {
            display: none;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }

            .main-card {
                padding: 20px;
            }

            .model-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Prompt Generator</h1>
            <p>Uncensored AI-Powered Prompt Generation with Image Reference</p>
        </div>

        <div class="status">
            <div class="status-grid">
                <div class="status-item">
                    <div class="status-label">Connection</div>
                    <div class="status-value" id="connection-status">{{ status }}</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Default Text Model</div>
                    <div class="status-value" id="text-model-display">{{ text_model }}</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Vision Model</div>
                    <div class="status-value" id="vision-model-display">{{ vision_model }}</div>
                </div>
                <div class="status-item">
                    <div class="status-label">Total Models</div>
                    <div class="status-value" id="total-models-display">{{ total_models }}</div>
                </div>
            </div>

            <div class="settings-section" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e9ecef;">
                <div style="display: flex; gap: 10px; align-items: flex-end; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 250px;">
                        <label style="font-size: 0.85em; color: #666; margin-bottom: 5px; display: block;">Ollama URL</label>
                        <input
                            type="text"
                            id="ollamaUrl"
                            value="{{ ollama_host }}"
                            placeholder="http://localhost:11434"
                            style="padding: 8px 12px; border: 2px solid #e1e1e1; border-radius: 5px; font-size: 14px; width: 100%;"
                        >
                    </div>
                    <button type="button" onclick="testConnection()" id="testBtn" style="padding: 8px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600; white-space: nowrap;">
                        Test Connection
                    </button>
                    <button type="button" onclick="saveOllamaUrl()" id="saveUrlBtn" style="padding: 8px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600; white-space: nowrap;">
                        Save URL
                    </button>
                </div>
                <div id="connectionTestResult" style="margin-top: 10px; display: none;"></div>
            </div>
        </div>

        <div class="main-card">
            <div id="alertBox" class="alert alert-info">
                <strong>📸 Image Reference Active!</strong> Using vision model to analyze your image.
            </div>

            <form id="promptForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="prompt">What do you want to create?</label>
                    <textarea
                        id="prompt"
                        name="prompt"
                        placeholder="Describe your vision... Or upload an image for reference and describe how to modify it."
                        required
                    ></textarea>
                </div>

                <div class="trigger-section" id="triggerSection">
                    <div class="trigger-header">
                        <div class="trigger-title">🔥 Explicit Trigger Words</div>
                        <button type="button" class="trigger-toggle" onclick="toggleTriggers()">Hide</button>
                    </div>

                    <div class="trigger-category">
                        <div class="category-title">Body Parts</div>
                        <div class="trigger-chips">
                            <span class="trigger-chip hot" data-word="naked">naked</span>
                            <span class="trigger-chip hot" data-word="tits">tits</span>
                            <span class="trigger-chip hot" data-word="breasts">breasts</span>
                            <span class="trigger-chip hot" data-word="nipples">nipples</span>
                            <span class="trigger-chip hot" data-word="ass">ass</span>
                            <span class="trigger-chip hot" data-word="pussy">pussy</span>
                            <span class="trigger-chip hot" data-word="cock">cock</span>
                            <span class="trigger-chip hot" data-word="dick">dick</span>
                            <span class="trigger-chip" data-word="thighs">thighs</span>
                            <span class="trigger-chip" data-word="legs">legs</span>
                        </div>
                    </div>

                    <div class="trigger-category">
                        <div class="category-title">Actions</div>
                        <div class="trigger-chips">
                            <span class="trigger-chip hot" data-word="fucking">fucking</span>
                            <span class="trigger-chip hot" data-word="sucking">sucking</span>
                            <span class="trigger-chip hot" data-word="cumming">cumming</span>
                            <span class="trigger-chip hot" data-word="cumshot">cumshot</span>
                            <span class="trigger-chip hot" data-word="riding">riding</span>
                            <span class="trigger-chip" data-word="touching">touching</span>
                            <span class="trigger-chip" data-word="spreading">spreading</span>
                            <span class="trigger-chip" data-word="moaning">moaning</span>
                            <span class="trigger-chip" data-word="screaming">screaming</span>
                            <span class="trigger-chip" data-word="biting">biting</span>
                        </div>
                    </div>

                    <div class="trigger-category">
                        <div class="category-title">Positions</div>
                        <div class="trigger-chips">
                            <span class="trigger-chip hot" data-word="doggy style">doggy style</span>
                            <span class="trigger-chip hot" data-word="POV">POV</span>
                            <span class="trigger-chip" data-word="bent over">bent over</span>
                            <span class="trigger-chip" data-word="on knees">on knees</span>
                            <span class="trigger-chip" data-word="legs spread">legs spread</span>
                            <span class="trigger-chip" data-word="on top">on top</span>
                            <span class="trigger-chip" data-word="from behind">from behind</span>
                            <span class="trigger-chip" data-word="close-up">close-up</span>
                        </div>
                    </div>

                    <div class="trigger-category">
                        <div class="category-title">Modifiers</div>
                        <div class="trigger-chips">
                            <span class="trigger-chip hot" data-word="wet">wet</span>
                            <span class="trigger-chip hot" data-word="dripping">dripping</span>
                            <span class="trigger-chip hot" data-word="hard">hard</span>
                            <span class="trigger-chip hot" data-word="rough">rough</span>
                            <span class="trigger-chip" data-word="sweaty">sweaty</span>
                            <span class="trigger-chip" data-word="oiled">oiled</span>
                            <span class="trigger-chip" data-word="messy">messy</span>
                            <span class="trigger-chip" data-word="intense">intense</span>
                            <span class="trigger-chip" data-word="explicit">explicit</span>
                            <span class="trigger-chip" data-word="detailed">detailed</span>
                        </div>
                    </div>

                    <div class="trigger-category">
                        <div class="category-title">Camera/View</div>
                        <div class="trigger-chips">
                            <span class="trigger-chip" data-word="POV shot">POV shot</span>
                            <span class="trigger-chip" data-word="close-up shot">close-up shot</span>
                            <span class="trigger-chip" data-word="wide angle">wide angle</span>
                            <span class="trigger-chip" data-word="top view">top view</span>
                            <span class="trigger-chip" data-word="side view">side view</span>
                            <span class="trigger-chip" data-word="low angle">low angle</span>
                            <span class="trigger-chip" data-word="first person">first person</span>
                        </div>
                    </div>

                    <div class="trigger-category">
                        <div class="category-title">Body Types</div>
                        <div class="trigger-chips">
                            <span class="trigger-chip" data-word="busty">busty</span>
                            <span class="trigger-chip" data-word="curvy">curvy</span>
                            <span class="trigger-chip" data-word="thick">thick</span>
                            <span class="trigger-chip" data-word="petite">petite</span>
                            <span class="trigger-chip" data-word="slim">slim</span>
                            <span class="trigger-chip" data-word="athletic">athletic</span>
                            <span class="trigger-chip" data-word="fit">fit</span>
                            <span class="trigger-chip" data-word="muscular">muscular</span>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="wordLimit">
                        📊 Keyword Limit: <span id="wordLimitValue">50</span> keywords
                    </label>
                    <input
                        type="range"
                        id="wordLimit"
                        name="wordLimit"
                        min="20"
                        max="100"
                        value="50"
                        style="width: 100%; cursor: pointer;"
                    >
                    <small style="color: #666; display: block; margin-top: 5px;">
                        Limit the number of keywords in the generated prompt (Stable Diffusion best practice: 30-60 keywords)
                    </small>
                </div>

                <div class="form-group">
                    <label style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" id="consistencyMode" style="width: auto; margin: 0;">
                        🎯 Character Consistency Mode
                        <span class="info-badge">Keep character/style consistent</span>
                    </label>
                    <div id="seedContainer" style="display: none; margin-top: 10px;">
                        <input
                            type="text"
                            id="seed"
                            name="seed"
                            placeholder="Enter seed (leave blank for random) e.g., 1234567890"
                            style="font-family: monospace;"
                        >
                        <small style="color: #666; display: block; margin-top: 5px;">
                            💡 Use the same seed to keep character and style consistent across generations
                        </small>
                    </div>
                </div>

                <div class="form-group">
                    <label>Reference Image (Optional) <span class="info-badge">Uses Vision AI</span></label>
                    <div class="file-upload-area" id="uploadArea">
                        <div class="upload-icon">📁</div>
                        <div class="upload-text">Click to upload or drag & drop</div>
                        <div class="upload-hint">PNG, JPG, GIF, BMP, WEBP (Max 16MB)</div>
                        <input type="file" id="fileInput" name="image" accept="image/*">
                    </div>
                    <div class="image-preview" id="imagePreview">
                        <button type="button" class="remove-image" onclick="removeImage()">×</button>
                        <img id="previewImg" class="preview-img" src="" alt="Preview">
                    </div>
                    <div id="breakdownContainer" style="display: none; margin-top: 10px;">
                        <label style="display: flex; align-items: center; gap: 10px;">
                            <input type="checkbox" id="breakdownMode" style="width: auto; margin: 0;">
                            🎬 Break Down Image
                            <span class="info-badge">Separate subject & background</span>
                        </label>
                        <small style="color: #666; display: block; margin-top: 5px;">
                            AI will analyze and create separate prompts for the subject/character and background
                        </small>
                    </div>
                </div>

                <div class="model-grid">
                    <div class="form-group">
                        <label for="type">Type</label>
                        <select id="type" name="type" onchange="updateTargetModels()">
                            <option value="image">Image Prompt</option>
                            <option value="video">Video Prompt</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="targetModel">Target Service <span class="info-badge">Format optimized</span></label>
                        <select id="targetModel" name="targetModel">
                            <!-- Options populated by JavaScript -->
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label for="model">Ollama Model <span class="info-badge">Auto-detects best</span></label>
                    <select id="model" name="model">
                        <option value="">Auto-select (Recommended)</option>
                        {% for model in models %}
                        <option value="{{ model }}">{{ model }}</option>
                        {% endfor %}
                    </select>
                </div>

                <button type="submit" id="generateBtn">Generate Prompt</button>
            </form>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="color: #667eea; font-weight: 600;">Generating your prompt...</p>
            </div>

            <div class="result" id="result">
                <h3>
                    Generated Prompt
                    <button type="button" class="btn-secondary" onclick="copyResult()">Copy</button>
                </h3>
                <div class="result-text" id="resultText"></div>
            </div>
        </div>
    </div>

    <script>
        let uploadedFile = null;
        let activeTriggers = new Set();

        // Target models configuration
        const TARGET_MODELS = {
            image: [
                { value: 'stable-diffusion', label: 'Stable Diffusion (SD 1.5/SDXL) - Keywords', description: 'Classic comma-separated tags' },
                { value: 'flux', label: 'Flux (Black Forest Labs) - Natural Language', description: 'Complete sentences preferred' },
                { value: 'sd3', label: 'Stable Diffusion 3 - Natural Language', description: 'Better natural language understanding' }
            ],
            video: [
                { value: 'wan', label: 'Wan - Keywords', description: 'Comma-separated video keywords' },
                { value: 'sora', label: 'Sora (OpenAI) - Natural Language', description: 'Cinematic descriptions' },
                { value: 'veo3', label: 'Veo 3 (Google) - Natural Language', description: 'Motion and realism focused' }
            ]
        };

        // Update target model dropdown based on type
        function updateTargetModels() {
            const type = document.getElementById('type').value;
            const targetModelSelect = document.getElementById('targetModel');
            const models = TARGET_MODELS[type] || TARGET_MODELS.image;

            // Clear existing options
            targetModelSelect.innerHTML = '';

            // Add new options
            models.forEach((model, index) => {
                const option = document.createElement('option');
                option.value = model.value;
                option.textContent = model.label;
                option.title = model.description;
                if (index === 0) option.selected = true;
                targetModelSelect.appendChild(option);
            });
        }

        // Toggle trigger section visibility
        function toggleTriggers() {
            const section = document.getElementById('triggerSection');
            const btn = section.querySelector('.trigger-toggle');

            section.classList.toggle('collapsed');
            btn.textContent = section.classList.contains('collapsed') ? 'Show' : 'Hide';
        }

        // Handle trigger chip clicks
        function setupTriggerChips() {
            const chips = document.querySelectorAll('.trigger-chip');
            const promptTextarea = document.getElementById('prompt');

            chips.forEach(chip => {
                chip.addEventListener('click', () => {
                    const word = chip.getAttribute('data-word');
                    const currentText = promptTextarea.value.trim();

                    if (chip.classList.contains('active')) {
                        // Remove word
                        chip.classList.remove('active');
                        activeTriggers.delete(word);

                        // Remove from textarea
                        const words = currentText.split(',').map(w => w.trim()).filter(w => w);
                        const newWords = words.filter(w => w !== word);
                        promptTextarea.value = newWords.join(', ');
                    } else {
                        // Add word
                        chip.classList.add('active');
                        activeTriggers.add(word);

                        // Add to textarea
                        if (currentText) {
                            promptTextarea.value = currentText + ', ' + word;
                        } else {
                            promptTextarea.value = word;
                        }
                    }
                });
            });
        }

        // Initialize trigger chips on page load
        document.addEventListener('DOMContentLoaded', () => {
            setupTriggerChips();
            setupConsistencyMode();
            setupWordLimitSlider();
            updateTargetModels(); // Initialize target model dropdown
        });

        // Setup consistency mode toggle
        function setupConsistencyMode() {
            const checkbox = document.getElementById('consistencyMode');
            const seedContainer = document.getElementById('seedContainer');

            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    seedContainer.style.display = 'block';
                } else {
                    seedContainer.style.display = 'none';
                }
            });
        }

        // Setup word limit slider
        function setupWordLimitSlider() {
            const slider = document.getElementById('wordLimit');
            const valueDisplay = document.getElementById('wordLimitValue');

            slider.addEventListener('input', () => {
                valueDisplay.textContent = slider.value;
            });
        }

        // Upload area click handler
        document.getElementById('uploadArea').addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });

        // File input change handler
        document.getElementById('fileInput').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                uploadedFile = file;
                showImagePreview(file);
            }
        });

        // Drag and drop handlers
        const uploadArea = document.getElementById('uploadArea');

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');

            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                uploadedFile = file;
                document.getElementById('fileInput').files = e.dataTransfer.files;
                showImagePreview(file);
            }
        });

        // Show image preview
        function showImagePreview(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                document.getElementById('previewImg').src = e.target.result;
                document.getElementById('imagePreview').classList.add('show');
                document.getElementById('alertBox').classList.add('show');
                document.getElementById('breakdownContainer').style.display = 'block';
            };
            reader.readAsDataURL(file);
        }

        // Remove image
        function removeImage() {
            uploadedFile = null;
            document.getElementById('fileInput').value = '';
            document.getElementById('imagePreview').classList.remove('show');
            document.getElementById('alertBox').classList.remove('show');
            document.getElementById('breakdownContainer').style.display = 'none';
            document.getElementById('breakdownMode').checked = false;
        }

        // Form submit handler
        document.getElementById('promptForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const prompt = document.getElementById('prompt').value;
            const type = document.getElementById('type').value;
            const targetModel = document.getElementById('targetModel').value;
            const model = document.getElementById('model').value;
            const consistencyMode = document.getElementById('consistencyMode').checked;
            const seed = document.getElementById('seed').value;
            const wordLimit = document.getElementById('wordLimit').value;
            const breakdownMode = document.getElementById('breakdownMode').checked;

            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            document.getElementById('generateBtn').disabled = true;

            try {
                const formData = new FormData();
                formData.append('prompt', prompt);
                formData.append('type', type);
                formData.append('target_model', targetModel);
                formData.append('word_limit', wordLimit);
                if (model) formData.append('model', model);
                if (uploadedFile) {
                    formData.append('image', uploadedFile);
                    if (breakdownMode) formData.append('breakdown_mode', 'true');
                }
                if (consistencyMode) {
                    formData.append('consistency_mode', 'true');
                    if (seed) formData.append('seed', seed);
                }

                const response = await fetch('/api/generate', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('loading').classList.remove('show');

                    // Display result based on mode
                    let resultHTML = '';

                    if (data.seed) {
                        resultHTML += `<div style="background: #fff3cd; padding: 10px; border-radius: 5px; margin-bottom: 15px; border-left: 4px solid #ffc107;">
                            <strong>🎯 Consistency Seed:</strong> <code style="background: white; padding: 2px 8px; border-radius: 3px; font-size: 1.1em;">${data.seed}</code>
                            <br><small style="color: #856404;">Copy this seed and use it in your image generator's seed field</small>
                        </div>`;
                    }

                    // Check if breakdown mode returned multiple prompts
                    if (data.subject_prompt || data.background_prompt) {
                        window.currentPrompt = data.combined_prompt || data.subject_prompt;

                        resultHTML += `<div style="margin-bottom: 20px;">
                            <h4 style="color: #667eea; margin-bottom: 10px;">📸 Subject / Character Prompt:</h4>
                            <div class="prompt-output" style="background: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; border-left: 4px solid #667eea;">
                                ${data.subject_prompt}
                            </div>
                            <button type="button" class="btn-secondary" onclick="copyToClipboard('${data.subject_prompt.replace(/'/g, "\\'")}')">Copy Subject</button>
                        </div>`;

                        resultHTML += `<div style="margin-bottom: 20px;">
                            <h4 style="color: #764ba2; margin-bottom: 10px;">🌄 Background / Environment Prompt:</h4>
                            <div class="prompt-output" style="background: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; border-left: 4px solid #764ba2;">
                                ${data.background_prompt}
                            </div>
                            <button type="button" class="btn-secondary" onclick="copyToClipboard('${data.background_prompt.replace(/'/g, "\\'")}')">Copy Background</button>
                        </div>`;

                        if (data.combined_prompt) {
                            resultHTML += `<div style="margin-bottom: 20px;">
                                <h4 style="color: #28a745; margin-bottom: 10px;">✨ Combined Full Prompt:</h4>
                                <div class="prompt-output" style="background: white; padding: 15px; border-radius: 5px; margin-bottom: 15px; border-left: 4px solid #28a745;">
                                    ${data.combined_prompt}
                                </div>
                                <button type="button" class="btn-secondary" onclick="copyToClipboard('${data.combined_prompt.replace(/'/g, "\\'")}')">Copy Combined</button>
                            </div>`;
                        }
                    } else {
                        // Standard single prompt
                        window.currentPrompt = data.result;
                        resultHTML += `<div class="prompt-output">${data.result}</div>`;
                    }

                    document.getElementById('resultText').innerHTML = resultHTML;
                    document.getElementById('result').classList.add('show');
                } else {
                    throw new Error(data.error || 'Generation failed');
                }
            } catch (error) {
                document.getElementById('loading').classList.remove('show');
                alert('Error generating prompt: ' + error.message);
            } finally {
                document.getElementById('generateBtn').disabled = false;
            }
        });

        function copyResult() {
            // Copy only the prompt, not the seed
            const text = window.currentPrompt || document.getElementById('resultText').textContent;
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ Copied!';
                btn.style.background = '#28a745';
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                }, 2000);
            });
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ Copied!';
                btn.style.background = '#28a745';
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                }, 2000);
            });
        }

        // Auto-focus textarea
        document.getElementById('prompt').focus();

        // Test Ollama connection
        async function testConnection() {
            const url = document.getElementById('ollamaUrl').value.trim();
            const testBtn = document.getElementById('testBtn');
            const resultDiv = document.getElementById('connectionTestResult');

            if (!url) {
                showTestResult('error', 'Please enter an Ollama URL');
                return;
            }

            testBtn.disabled = true;
            testBtn.textContent = 'Testing...';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<div style="color: #666;">Testing connection...</div>';

            try {
                const response = await fetch('/api/test-connection', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });

                const data = await response.json();

                if (data.success) {
                    showTestResult('success',
                        `<strong>Connection successful!</strong><br>` +
                        `Response time: ${data.response_time_ms}ms<br>` +
                        `Models found: ${data.models_count}`
                    );
                } else {
                    showTestResult('error',
                        `<strong>Connection failed</strong><br>` +
                        `Error: ${data.error}<br>` +
                        `Type: ${data.error_type}`
                    );
                }
            } catch (error) {
                showTestResult('error', `Request failed: ${error.message}`);
            } finally {
                testBtn.disabled = false;
                testBtn.textContent = 'Test Connection';
            }
        }

        // Save Ollama URL
        async function saveOllamaUrl() {
            const url = document.getElementById('ollamaUrl').value.trim();
            const saveBtn = document.getElementById('saveUrlBtn');
            const resultDiv = document.getElementById('connectionTestResult');

            if (!url) {
                showTestResult('error', 'Please enter an Ollama URL');
                return;
            }

            saveBtn.disabled = true;
            saveBtn.textContent = 'Saving...';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<div style="color: #666;">Connecting and saving...</div>';

            try {
                const response = await fetch('/api/settings/ollama-url', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });

                const data = await response.json();

                if (data.success) {
                    showTestResult('success',
                        `<strong>URL saved successfully!</strong><br>` +
                        `Text Model: ${data.text_model}<br>` +
                        `Vision Model: ${data.vision_model}<br>` +
                        `Models found: ${data.models_count}`
                    );
                    // Update the displayed values
                    document.getElementById('connection-status').textContent = '✓ Connected';
                    document.getElementById('connection-status').style.color = '#28a745';
                    document.getElementById('text-model-display').textContent = data.text_model;
                    document.getElementById('vision-model-display').textContent = data.vision_model;
                    document.getElementById('total-models-display').textContent = data.models_count;

                    // Refresh the model dropdown
                    refreshModelDropdown();
                } else {
                    showTestResult('error',
                        `<strong>Failed to save URL</strong><br>` +
                        `Error: ${data.error}<br>` +
                        `The previous URL is still active.`
                    );
                }
            } catch (error) {
                showTestResult('error', `Request failed: ${error.message}`);
            } finally {
                saveBtn.disabled = false;
                saveBtn.textContent = 'Save URL';
            }
        }

        // Show test result with styling
        function showTestResult(type, message) {
            const resultDiv = document.getElementById('connectionTestResult');
            resultDiv.style.display = 'block';

            if (type === 'success') {
                resultDiv.innerHTML = `<div style="background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; border-left: 4px solid #28a745;">${message}</div>`;
            } else {
                resultDiv.innerHTML = `<div style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; border-left: 4px solid #dc3545;">${message}</div>`;
            }
        }

        // Refresh model dropdown after URL change
        async function refreshModelDropdown() {
            try {
                const response = await fetch('/api/models');
                const models = await response.json();

                const modelSelect = document.getElementById('model');
                const currentValue = modelSelect.value;

                // Clear and rebuild options
                modelSelect.innerHTML = '<option value="">Auto-select (Recommended)</option>';
                models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    if (model === currentValue) option.selected = true;
                    modelSelect.appendChild(option);
                });
            } catch (error) {
                console.error('Failed to refresh models:', error);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    models = generator.list_models()
    connected = generator.check_ollama_connection()

    return render_template_string(
        HTML_TEMPLATE,
        status="✓ Connected" if connected else "✗ Disconnected",
        text_model=generator.text_model,
        vision_model=generator.vision_model,
        total_models=len(models),
        models=models,
        ollama_host=generator.ollama_host
    )

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate prompt API endpoint with image support"""
    try:
        # Handle both JSON and multipart/form-data
        if request.is_json:
            data = request.json
            image_file = None
        else:
            data = request.form.to_dict()
            image_file = request.files.get('image')

        prompt = data.get('prompt', '')
        prompt_type = data.get('type', 'image')
        target_model = data.get('target_model', 'stable-diffusion')
        model = data.get('model', None)
        consistency_mode = data.get('consistency_mode') == 'true'
        seed = data.get('seed', '')
        word_limit = int(data.get('word_limit', 50))
        breakdown_mode = data.get('breakdown_mode') == 'true'

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Handle consistency mode
        response_seed = None
        if consistency_mode:
            # Generate random seed if not provided
            if not seed:
                import random
                seed = str(random.randint(1000000000, 9999999999))
            response_seed = seed

            # Add consistency keywords to prompt
            consistency_keywords = "same character, consistent character design, character reference, same style, same person"
            prompt = f"{prompt}, {consistency_keywords}"
            print(f"🎯 Consistency Mode: seed={seed}")

        image_path = None

        # Handle uploaded image
        if image_file and allowed_file(image_file.filename):
            # Generate unique filename
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

            # Save the file
            image_file.save(image_path)
            print(f"📸 Image uploaded: {image_path}")

        # Generate prompt - check if breakdown mode is enabled
        if breakdown_mode and image_path:
            # Breakdown mode: generate separate prompts for subject and background
            breakdown_result = generator.breakdown_image_prompt(
                prompt,
                image_path=image_path,
                prompt_type=prompt_type,
                model_override=model if model else None,
                word_limit=word_limit,
                target_model=target_model
            )

            # Clean up uploaded image
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass

            response_data = {
                'subject_prompt': breakdown_result.get('subject'),
                'background_prompt': breakdown_result.get('background'),
                'combined_prompt': breakdown_result.get('combined')
            }
            if response_seed:
                response_data['seed'] = response_seed

            return jsonify(response_data)
        else:
            # Standard mode: single prompt
            result = generator.generate_prompt(
                prompt,
                prompt_type=prompt_type,
                image_path=image_path,
                model_override=model if model else None,
                word_limit=word_limit,
                target_model=target_model
            )

            # Clean up uploaded image
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass

            response_data = {'result': result}
            if response_seed:
                response_data['seed'] = response_seed

            return jsonify(response_data)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models')
def models():
    """List available models"""
    return jsonify(generator.list_models())

@app.route('/api/status')
def status():
    """Check status"""
    return jsonify({
        'connected': generator.check_ollama_connection(),
        'ollama_host': generator.ollama_host,
        'text_model': generator.text_model,
        'vision_model': generator.vision_model,
        'models': generator.list_models()
    })

@app.route('/api/test-connection', methods=['GET', 'POST'])
def test_connection():
    """Test Ollama connection with detailed diagnostics"""
    # If POST with a URL, test that specific URL without changing settings
    if request.method == 'POST':
        data = request.json or {}
        test_url = data.get('url', '').strip()
        if test_url:
            # Create temporary generator to test the URL
            from prompt_generator import PromptGenerator
            temp_generator = PromptGenerator(ollama_host=test_url)
            result = temp_generator.test_ollama_connection()
            return jsonify(result)

    # GET request - test current connection
    result = generator.test_ollama_connection()
    return jsonify(result)

@app.route('/api/settings/ollama-url', methods=['GET', 'POST'])
def ollama_url_setting():
    """Get or set Ollama URL"""
    if request.method == 'GET':
        return jsonify({
            'ollama_host': generator.ollama_host,
            'text_model': generator.text_model,
            'vision_model': generator.vision_model
        })

    # POST - update the URL
    data = request.json or {}
    new_url = data.get('url', '').strip()

    if not new_url:
        return jsonify({'error': 'URL is required'}), 400

    # Validate URL format
    if not new_url.startswith('http://') and not new_url.startswith('https://'):
        return jsonify({'error': 'URL must start with http:// or https://'}), 400

    result = generator.set_ollama_host(new_url)

    if result['success']:
        print(f"✓ Ollama URL updated to: {new_url}")
        return jsonify(result)
    else:
        print(f"✗ Failed to connect to: {new_url} - {result['error']}")
        return jsonify(result), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    print(f"🚀 Starting Prompt Generator Web UI on port {port}")
    print(f"🔗 Open: http://localhost:{port}")
    print(f"🔗 Ollama: {generator.ollama_host}")
    print(f"📝 Text Model: {generator.text_model}")
    print(f"📸 Vision Model: {generator.vision_model}")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    app.run(host='0.0.0.0', port=port, debug=False)
