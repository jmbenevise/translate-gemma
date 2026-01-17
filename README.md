# TranslateGemma Web - AI 翻譯介面

使用 TranslateGemma 4B 模型的網頁翻譯介面，類似 Google 翻譯的設計。

![TranslateGemma](https://img.shields.io/badge/Model-TranslateGemma%204B-blue)
![Languages](https://img.shields.io/badge/Languages-55+-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## 功能特色

- 🌍 **55+ 種語言** - 支援中文、英文、日文、韓文、西班牙文等多種語言
- 🎨 **現代化介面** - 深色模式、玻璃擬態設計、流暢動畫
- 🔄 **語言互換** - 一鍵交換來源語言和目標語言
- 📋 **複製功能** - 快速複製翻譯結果
- ⚡ **本地運行** - 使用 Ollama 本地運行，保護隱私

## 系統需求

- Docker 和 Docker Compose
- NVIDIA GPU (建議，用於加速推理)
- 至少 8GB RAM
- 約 4GB 磁碟空間 (用於模型)

## 快速開始

### 1. 啟動服務

```bash
docker compose up -d
```

### 2. 等待模型下載

首次啟動時，會自動下載 TranslateGemma 4B 模型 (~3.3GB)。
查看下載進度：

```bash
docker compose logs -f model-init
```

### 3. 開啟網頁

瀏覽器開啟 [http://localhost:8080](http://localhost:8080)

## 使用方式

1. 選擇來源語言和目標語言
2. 在左側輸入要翻譯的文字
3. 點擊「翻譯」按鈕或按 `Ctrl + Enter`
4. 翻譯結果會顯示在右側
5. 點擊複製按鈕將結果複製到剪貼簿

## 鍵盤快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl + Enter` | 翻譯 |

## 技術架構

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  FastAPI (8080) │────▶│  Ollama (11434) │
│   HTML/CSS/JS   │     │     Python      │     │ TranslateGemma  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 專案結構

```
translate-gemma-testground/
├── docker-compose.yml     # Docker 配置
├── Dockerfile             # Web 應用容器配置
├── README.md              # 說明文件
└── app/
    ├── main.py            # FastAPI 後端
    ├── requirements.txt   # Python 依賴
    └── static/
        ├── index.html     # 前端頁面
        ├── styles.css     # 樣式表
        └── script.js      # 前端邏輯
```

## 常見問題

### Q: 模型下載失敗怎麼辦？

手動下載模型：

```bash
docker exec -it ollama-translate ollama pull translategemma:4b
```

### Q: 沒有 NVIDIA GPU 可以使用嗎？

可以，但速度會較慢。編輯 `docker-compose.yml`，移除 `deploy` 區塊中的 GPU 配置。

### Q: 如何停止服務？

```bash
docker compose down
```

### Q: 如何完全清除（包含模型）？

```bash
docker compose down -v
```

## 授權

本專案僅供學習和個人使用。TranslateGemma 模型受 Google 授權條款約束。
