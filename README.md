# TranslateGemma Web

A self-hosted web translation interface powered by Google's [TranslateGemma](https://ai.google.dev/gemma/docs/core/translategemma) model running locally via Ollama. Features a Google Translate-style UI with full privacy—no data leaves your machine.

This an English translation.

![TranslateGemma](https://img.shields.io/badge/Model-TranslateGemma-blue)
![Languages](https://img.shields.io/badge/Languages-55+-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

[English](#features) | [繁體中文](README_zh-TW.md)

## Features

- 🌍 **55+ Languages** - Supports Chinese, English, Japanese, Korean, Spanish, French, German, and many more
- 🎨 **Modern UI** - Dark mode, glassmorphism design, smooth animations
- 🔄 **Swap Languages** - One-click language swap
- 📋 **Copy to Clipboard** - Quick copy translation results
- 🔒 **Privacy First** - Runs entirely locally with Ollama, no data sent to external servers
- 🔌 **[Immersive Translate](https://immersivetranslate.com/) Compatible** - Use as a custom translation API for browser extensions
- 🤖 **Multiple Models** - Choose between TranslateGemma 4B (faster) and 12B (higher quality)

## Requirements

- Docker and Docker Compose
- NVIDIA GPU (recommended for faster inference)
- 8GB+ RAM
- ~4GB disk space for the model (4B) or ~9GB (12B)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Harrison-Dev/translate-gemma-web.git
cd translate-gemma-web
```

### 2. Start the services

```bash
docker compose up -d
```

### 3. Wait for model download

First run will automatically download TranslateGemma 4B (~3.3GB). Check progress:

```bash
docker compose logs -f model-init
```

### 4. Open the web interface

Navigate to [http://localhost:8080](http://localhost:8080)

## Usage

### Web Interface

1. Select source and target languages from the dropdowns
2. Enter text in the left panel
3. Click **"Translate"** or press `Ctrl + Enter`
4. Results appear in the right panel
5. Click the copy button to copy results to clipboard

### Switch Models

Click the model selector in the header to switch between:
- **TranslateGemma 4B** - Faster, good for everyday translation
- **TranslateGemma 12B** - Higher quality, more accurate translations

To use the 12B model, manually pull it first:

```bash
docker exec -it ollama-translate ollama pull translategemma:12b
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | Translate |

## Immersive Translate Integration

This project provides a custom API endpoint compatible with the [Immersive Translate](https://immersivetranslate.com/) browser extension, allowing you to use TranslateGemma for translating web pages.

### Setup Guide

1. **Enable Developer Mode**
   - Open Immersive Translate extension → **Settings** → **Developer Settings**
   - Enable **Beta Testing Features**

2. **Select Custom API**
   - Go back to **General** settings
   - Set Translation Service to **Custom API**

3. **Configure API URL**
   
   Use the following URL format:
   ```
   http://localhost:8080/api/immersive-translate?model=translategemma:4b
   ```
   
   Or for the 12B model:
   ```
   http://localhost:8080/api/immersive-translate?model=translategemma:12b
   ```

4. **Test the Connection**
   
   Visit [http://localhost:8080/immersive-config.html](http://localhost:8080/immersive-config.html) to test your setup.

> **Note**: If connecting from other devices on your network, replace `localhost` with your computer's IP address.

## API Reference

### Translation Endpoint

```http
POST /api/translate
Content-Type: application/json

{
  "text": "Hello, world!",
  "source_lang": "en",
  "target_lang": "zh-Hant",
  "model": "translategemma:4b"
}
```

Response:
```json
{
  "translated_text": "你好，世界！"
}
```

### Immersive Translate Endpoint

```http
POST /api/immersive-translate?model=translategemma:4b
Content-Type: application/json

{
  "source_lang": "en",
  "target_lang": "zh-TW",
  "text_list": ["Hello", "World"]
}
```

Response:
```json
{
  "translations": [
    {"detected_source_lang": "en", "text": "你好"},
    {"detected_source_lang": "en", "text": "世界"}
  ]
}
```

### Get Supported Languages

```http
GET /api/languages
```

### Get Available Models

```http
GET /api/models
```

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  FastAPI (8080) │────▶│  Ollama (11434) │
│   HTML/CSS/JS   │     │     Python      │     │ TranslateGemma  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Project Structure

```
translate-gemma-web/
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Web app container
├── LICENSE                     # MIT License
├── README.md                   # Documentation (English)
├── README_zh-TW.md             # Documentation (繁體中文)
└── app/
    ├── main.py                 # FastAPI backend
    ├── requirements.txt        # Python dependencies
    └── static/
        ├── index.html          # Main translation UI
        ├── immersive-config.html  # Immersive Translate setup guide
        ├── styles.css          # Styles
        └── script.js           # Frontend logic
```

## FAQ

### Model download failed?

Manually pull the model:

```bash
docker exec -it ollama-translate ollama pull translategemma:4b
```

### Can I use without NVIDIA GPU?

Yes, but translations will be slower. Edit `docker-compose.yml` and remove the `deploy` section under the `ollama` service.

### How to stop services?

```bash
docker compose down
```

### How to completely remove (including model data)?

```bash
docker compose down -v
```

### How to update to the latest version?

```bash
git pull
docker compose down
docker compose up -d --build
```

## About TranslateGemma

[TranslateGemma](https://ai.google.dev/gemma/docs/core/translategemma) is a specialized translation model developed by Google, designed to provide high-quality translations across 55+ languages. It comes in two sizes:

- **4B** - 3.3GB, faster inference, suitable for everyday use
- **12B** - 8.1GB, higher quality, better for professional translations

Learn more at the [official documentation](https://ai.google.dev/gemma/docs/core/translategemma).

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

> **Note**: The TranslateGemma model is subject to [Google's Gemma Terms of Use](https://ai.google.dev/gemma/terms).
