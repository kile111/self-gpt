# Self-GPT: 超级整合助手

一个强大的多模态 AI 助手，基于 Streamlit、OpenAI GPT-5、Whisper、OCR 和网页搜索集成构建。支持文件读取、语音输入、实时网页搜索等多种功能。

## Features

- **与 GPT-5 聊天**：支持高级推理、链式思维和自定义系统提示词。
- **文件上传与解析**：支持 PDF、DOCX、TXT、CSV、Excel 及图片 OCR（JPG/PNG）。
- **语音输入**：通过麦克风使用 Whisper 实现语音转文字。
- **文本转语音**：将 AI 回复内容转换为音频。
- **实时网页搜索**：集成 SerpAPI 获取最新信息。
- **多模式界面**：支持聊天、同声传译和实时字幕。
- **会话记忆**：记住聊天历史，可随时清除。
- **安全 API 密钥管理**：通过 `.env` 文件存储敏感密钥。

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/self-gpt.git
   cd self-gpt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SERP_API_KEY=your_serpapi_key
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Usage

- 在浏览器中打开 Streamlit 网页界面。
- 选择模式：聊天、同声传译或实时字幕。
- 上传文件或图片进行解析和 OCR 识别。
- 使用麦克风进行语音输入。
- 提问、请求网页搜索或生成图片。

## File Support

- **Text**: PDF, DOCX, TXT, CSV, XLSX
- **Images**: JPG, PNG (OCR extraction)
- **Audio**: Microphone input (Whisper)

## Security

- **Never commit your `.env` file or API keys to public repositories.**
- `.gitignore` is configured to exclude sensitive and unnecessary files.

## Requirements

- Python 3.8+
- OpenAI API key
- SerpAPI key (for web search)
- [See `requirements.txt` for all dependencies]

## Project Structure

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

## Acknowledgements

- [OpenAI](https://openai.com/)
- [Streamlit](https://streamlit.io/)
- [SerpAPI](https://serpapi.com/)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [PyPDF2, python-docx, pandas, etc.]

---

Let me know if you want to add badges, usage GIFs, or more sections!
