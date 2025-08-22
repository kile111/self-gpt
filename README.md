# Self-GPT：超级整合助手

一个强大的多模态 AI 助手，基于 Streamlit、OpenAI GPT-5、Whisper、OCR 和网页搜索集成构建。支持文件读取、语音输入、实时网页搜索等多种功能。

## 功能特色

- **与 GPT-5 聊天**：支持高级推理、链式思维和自定义系统提示词。
- **文件上传与解析**：支持 PDF、DOCX、TXT、CSV、Excel 及图片 OCR（JPG/PNG）。
- **语音输入**：通过麦克风使用 Whisper 实现语音转文字。
- **文本转语音**：将 AI 回复内容转换为音频。
- **实时网页搜索**：集成 SerpAPI 获取最新信息。
- **多模式界面**：支持聊天、同声传译和实时字幕。
- **会话记忆**：记住聊天历史，可随时清除。
- **安全 API 密钥管理**：通过 `.env` 文件存储敏感密钥。

## 安装方法

1. **克隆仓库**
   ```bash
   git clone https://github.com/<your-username>/self-gpt.git
   cd self-gpt
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**

   在项目根目录下创建 `.env` 文件：
   ```
   OPENAI_API_KEY=你的_openai_api_key
   SERP_API_KEY=你的_serpapi_key
   ```

4. **运行应用**
   ```bash
   streamlit run app.py
   ```

## 使用说明

- 在浏览器中打开 Streamlit 网页界面。
- 选择模式：聊天、同声传译或实时字幕。
- 上传文件或图片进行解析和 OCR 识别。
- 使用麦克风进行语音输入。
- 提问、请求网页搜索或生成图片。

## 文件支持

- **文本**：PDF、DOCX、TXT、CSV、XLSX
- **图片**：JPG、PNG（OCR 识别）
- **音频**：麦克风输入（Whisper）

## 安全性

- **切勿将你的 `.env` 文件或 API 密钥提交到公共仓库。**
- `.gitignore` 已配置排除敏感和不必要的文件。

## 环境要求

- Python 3.8 及以上
- OpenAI API 密钥
- SerpAPI 密钥（用于网页搜索）
- [所有依赖见 `requirements.txt`]

## 项目结构

```
self-gpt/
├── app.py
├── requirements.txt
├── .env.example
├── utils/
│   ├── file_reader.py
│   ├── data_analysis.py
│   └── ocr_utils.py
├── chat_memory.json
└── ...
```

## 鸣谢

- [OpenAI](https://openai.com/)
- [Streamlit](https://streamlit.io/)
- [SerpAPI](https://serpapi.com/)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [PyPDF2, python-docx, pandas 等]

---

如需添加徽章、使用演示 GIF 或更多内容，欢迎告知！
