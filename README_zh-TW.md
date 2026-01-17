# TranslateGemma Web

一個自架式網頁翻譯介面，使用 Google 的 [TranslateGemma](https://ai.google.dev/gemma/docs/core/translategemma) 模型透過 Ollama 在本地運行。擁有類似 Google 翻譯的介面設計，完全保護你的隱私——資料不會離開你的電腦。

![TranslateGemma](https://img.shields.io/badge/Model-TranslateGemma-blue)
![Languages](https://img.shields.io/badge/Languages-55+-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

[English](README.md) | [繁體中文](#功能特色)

## 功能特色

- 🌍 **55+ 種語言** - 支援中文、英文、日文、韓文、西班牙文、法文、德文等多種語言
- 🎨 **現代化介面** - 深色模式、玻璃擬態設計、流暢動畫
- 🔄 **語言互換** - 一鍵交換來源語言和目標語言
- 📋 **複製功能** - 快速複製翻譯結果
- 🔒 **隱私優先** - 使用 Ollama 完全在本地運行，資料不會傳送到外部伺服器
- 🔌 **[沉浸式翻譯](https://immersivetranslate.com/)相容** - 可作為瀏覽器擴充功能的自訂翻譯 API
- 🤖 **多模型選擇** - 可選擇 TranslateGemma 4B（較快）或 12B（較高品質）

## 系統需求

- Docker 和 Docker Compose
- NVIDIA GPU（建議，用於加速推理）
- 至少 8GB RAM
- 約 4GB 磁碟空間（4B 模型）或約 9GB（12B 模型）

## 快速開始

### 1. Clone 專案

```bash
git clone https://github.com/YOUR_USERNAME/translate-gemma-web.git
cd translate-gemma-web
```

### 2. 啟動服務

```bash
docker compose up -d
```

### 3. 等待模型下載

首次啟動時，會自動下載 TranslateGemma 4B 模型（~3.3GB）。查看下載進度：

```bash
docker compose logs -f model-init
```

### 4. 開啟網頁

瀏覽器開啟 [http://localhost:8080](http://localhost:8080)

## 使用方式

### 網頁介面

1. 從下拉選單選擇來源語言和目標語言
2. 在左側輸入要翻譯的文字
3. 點擊 **「翻譯」** 按鈕或按 `Ctrl + Enter`
4. 翻譯結果會顯示在右側
5. 點擊複製按鈕將結果複製到剪貼簿

### 切換模型

點擊頁首的模型選擇器來切換：
- **TranslateGemma 4B** - 較快，適合日常翻譯
- **TranslateGemma 12B** - 較高品質，翻譯更準確

使用 12B 模型前，需要先手動下載：

```bash
docker exec -it ollama-translate ollama pull translategemma:12b
```

### 鍵盤快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl + Enter` | 翻譯 |

## 沉浸式翻譯整合

本專案提供與[沉浸式翻譯](https://immersivetranslate.com/)瀏覽器擴充功能相容的自訂 API 端點，讓你可以使用 TranslateGemma 翻譯網頁內容。

### 設定步驟

1. **開啟開發者模式**
   - 打開沉浸式翻譯擴展 → **設定** → **開發者設定**
   - 啟用 **Beta 測試特性**

2. **選擇自定義 API**
   - 返回 **常規** 設定
   - 翻譯服務選擇 **自定義 API**

3. **設定 API URL**
   
   使用以下 URL 格式：
   ```
   http://localhost:8080/api/immersive-translate?model=translategemma:4b
   ```
   
   或使用 12B 模型：
   ```
   http://localhost:8080/api/immersive-translate?model=translategemma:12b
   ```

4. **測試連線**
   
   前往 [http://localhost:8080/immersive-config.html](http://localhost:8080/immersive-config.html) 測試設定是否正確。

> **提示**：如果要從區域網路中的其他裝置連接，請將 `localhost` 替換為你的電腦 IP 地址。

## API 參考

### 翻譯端點

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

回應：
```json
{
  "translated_text": "你好，世界！"
}
```

### 沉浸式翻譯端點

```http
POST /api/immersive-translate?model=translategemma:4b
Content-Type: application/json

{
  "source_lang": "en",
  "target_lang": "zh-TW",
  "text_list": ["Hello", "World"]
}
```

回應：
```json
{
  "translations": [
    {"detected_source_lang": "en", "text": "你好"},
    {"detected_source_lang": "en", "text": "世界"}
  ]
}
```

### 取得支援的語言

```http
GET /api/languages
```

### 取得可用模型

```http
GET /api/models
```

## 架構

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  FastAPI (8080) │────▶│  Ollama (11434) │
│   HTML/CSS/JS   │     │     Python      │     │ TranslateGemma  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 專案結構

```
translate-gemma-web/
├── docker-compose.yml          # Docker 配置
├── Dockerfile                  # Web 應用容器
├── LICENSE                     # MIT 授權
├── README.md                   # 說明文件（英文）
├── README_zh-TW.md             # 說明文件（繁體中文）
└── app/
    ├── main.py                 # FastAPI 後端
    ├── requirements.txt        # Python 依賴
    └── static/
        ├── index.html          # 主翻譯介面
        ├── immersive-config.html  # 沉浸式翻譯設定指南
        ├── styles.css          # 樣式表
        └── script.js           # 前端邏輯
```

## 常見問題

### 模型下載失敗怎麼辦？

手動下載模型：

```bash
docker exec -it ollama-translate ollama pull translategemma:4b
```

### 沒有 NVIDIA GPU 可以使用嗎？

可以，但翻譯速度會較慢。編輯 `docker-compose.yml`，移除 `ollama` 服務下的 `deploy` 區塊。

### 如何停止服務？

```bash
docker compose down
```

### 如何完全清除（包含模型資料）？

```bash
docker compose down -v
```

### 如何更新到最新版本？

```bash
git pull
docker compose down
docker compose up -d --build
```

## 關於 TranslateGemma

[TranslateGemma](https://ai.google.dev/gemma/docs/core/translategemma) 是 Google 開發的專用翻譯模型，設計用於提供 55+ 種語言的高品質翻譯。它有兩種大小：

- **4B** - 3.3GB，推理速度較快，適合日常使用
- **12B** - 8.1GB，品質較高，適合專業翻譯

了解更多請參閱[官方文件](https://ai.google.dev/gemma/docs/core/translategemma)。

## 貢獻

歡迎貢獻！請：

1. Fork 此專案
2. 建立功能分支（`git checkout -b feature/amazing-feature`）
3. 提交變更（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 開啟 Pull Request

## 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

> **注意**：TranslateGemma 模型受 [Google 的 Gemma 使用條款](https://ai.google.dev/gemma/terms)約束。
