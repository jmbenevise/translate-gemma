# TranslateGemma Web

A self-hosted web translation interface powered by Google's TranslateGemma model running locally via Ollama. Google Translate-style UI with privacy in mind.

[English](#english) | [繁體中文](#繁體中文)

---

## English

![TranslateGemma](https://img.shields.io/badge/Model-TranslateGemma-blue)
![Languages](https://img.shields.io/badge/Languages-55+-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

### ✨ Features

- 🌍 **55+ Languages** - Chinese, English, Japanese, Korean, Spanish, and many more
- 🎨 **Modern UI** - Dark mode, glassmorphism design, smooth animations
- 🔄 **Swap Languages** - One-click language swap
- 📋 **Copy to Clipboard** - Quick copy translation results
- 🔒 **Privacy First** - Runs locally with Ollama, no data sent to external servers
- 🔌 **Immersive Translate Compatible** - Use as custom translation API for browser extensions

### 📋 Requirements

- Docker and Docker Compose
- NVIDIA GPU (recommended for faster inference)
- 8GB+ RAM
- ~4GB disk space for the model

### 🚀 Quick Start

#### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/translate-gemma-web.git
cd translate-gemma-web
```

#### 2. Start the services

```bash
docker compose up -d
```

#### 3. Wait for model download

First run will automatically download TranslateGemma 4B (~3.3GB).
Check progress:

```bash
docker compose logs -f model-init
```

#### 4. Open the web interface

Navigate to [http://localhost:8080](http://localhost:8080)

### 🖥️ Usage

1. Select source and target languages
2. Enter text in the left panel
3. Click "Translate" or press `Ctrl + Enter`
4. Results appear in the right panel
5. Click copy button to copy results

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | Translate |

### 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  FastAPI (8080) │────▶│  Ollama (11434) │
│   HTML/CSS/JS   │     │     Python      │     │ TranslateGemma  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 📁 Project Structure

```
translate-gemma-web/
├── docker-compose.yml     # Docker orchestration
├── Dockerfile             # Web app container
├── LICENSE                # MIT License
├── README.md              # Documentation
└── app/
    ├── main.py            # FastAPI backend
    ├── requirements.txt   # Python dependencies
    └── static/
        ├── index.html     # Main translation UI
        ├── immersive-config.html  # Immersive Translate config
        ├── styles.css     # Styles
        └── script.js      # Frontend logic
```

### ❓ FAQ

**Q: Model download failed?**

Manually pull the model:
```bash
docker exec -it ollama-translate ollama pull translategemma:4b
```

**Q: Can I use without NVIDIA GPU?**

Yes, but slower. Remove the `deploy` section in `docker-compose.yml`.

**Q: How to stop services?**
```bash
docker compose down
```

**Q: How to completely remove (including model)?**
```bash
docker compose down -v
```

### 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

> **Note**: The TranslateGemma model is subject to Google's licensing terms.

---

## 繁體中文

### ✨ 功能特色

- 🌍 **55+ 種語言** - 支援中文、英文、日文、韓文、西班牙文等多種語言
- 🎨 **現代化介面** - 深色模式、玻璃擬態設計、流暢動畫
- 🔄 **語言互換** - 一鍵交換來源語言和目標語言
- 📋 **複製功能** - 快速複製翻譯結果
- 🔒 **隱私優先** - 使用 Ollama 本地運行，資料不會傳送到外部伺服器
- 🔌 **支援沉浸式翻譯** - 可作為瀏覽器擴充功能的自訂翻譯 API

### 📋 系統需求

- Docker 和 Docker Compose
- NVIDIA GPU（建議，用於加速推理）
- 至少 8GB RAM
- 約 4GB 磁碟空間（用於模型）

### 🚀 快速開始

#### 1. Clone 專案

```bash
git clone https://github.com/YOUR_USERNAME/translate-gemma-web.git
cd translate-gemma-web
```

#### 2. 啟動服務

```bash
docker compose up -d
```

#### 3. 等待模型下載

首次啟動時，會自動下載 TranslateGemma 4B 模型（~3.3GB）。
查看下載進度：

```bash
docker compose logs -f model-init
```

#### 4. 開啟網頁

瀏覽器開啟 [http://localhost:8080](http://localhost:8080)

### 🖥️ 使用方式

1. 選擇來源語言和目標語言
2. 在左側輸入要翻譯的文字
3. 點擊「翻譯」按鈕或按 `Ctrl + Enter`
4. 翻譯結果會顯示在右側
5. 點擊複製按鈕將結果複製到剪貼簿

### ❓ 常見問題

**Q: 模型下載失敗怎麼辦？**

手動下載模型：
```bash
docker exec -it ollama-translate ollama pull translategemma:4b
```

**Q: 沒有 NVIDIA GPU 可以使用嗎？**

可以，但速度會較慢。編輯 `docker-compose.yml`，移除 `deploy` 區塊中的 GPU 配置。

**Q: 如何停止服務？**
```bash
docker compose down
```

**Q: 如何完全清除（包含模型）？**
```bash
docker compose down -v
```

### 🤝 貢獻

歡迎貢獻！請：

1. Fork 此專案
2. 建立功能分支（`git checkout -b feature/amazing-feature`）
3. 提交變更（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 開啟 Pull Request

### 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

> **注意**：TranslateGemma 模型受 Google 授權條款約束。
