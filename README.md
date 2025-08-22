# Self-GPT: 超级整合助手

A powerful, multi-modal AI assistant built with Streamlit, OpenAI GPT-5, Whisper, OCR, and web search integration. Supports file reading, voice input, real-time web search, and more.

## Features

- **Chat with GPT-5**: Advanced reasoning, chain-of-thought, and customizable system prompts.
- **File Upload & Parsing**: Supports PDF, DOCX, TXT, CSV, Excel, and image OCR (JPG/PNG).
- **Voice Input**: Use your microphone for speech-to-text with Whisper.
- **Text-to-Speech**: Converts AI answers to audio.
- **Real-Time Web Search**: Integrates with SerpAPI for up-to-date information.
- **Multi-Mode UI**: Chat, simultaneous interpretation, and real-time captioning.
- **Session Memory**: Remembers chat history and can clear on demand.
- **Secure API Key Handling**: Uses `.env` for sensitive keys.

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

- Open the Streamlit web UI in your browser.
- Choose a mode: Chat, Simultaneous Interpretation, or Real-Time Captioning.
- Upload files or images for parsing and OCR.
- Use your microphone for voice input.
- Ask questions, request web searches, or generate images.

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
