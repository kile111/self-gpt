import os
import json
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import requests
import easyocr
from utils.file_reader import read_file

# ===== 初始化 =====
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
serpapi_key = os.getenv("SERP_API_KEY")
client = OpenAI(api_key=api_key)
MEMORY_FILE = "chat_memory.json"

# ===== 聊天记忆 =====
def load_memory():
    if Path(MEMORY_FILE).exists():
        return json.loads(Path(MEMORY_FILE).read_text(encoding="utf-8"))
    return []
def save_memory(history):
    Path(MEMORY_FILE).write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_memory()

# ===== 自动触发联网搜索判断 =====
def need_live_search(user_prompt: str):
    keywords = [
        # 金融/币价
        "价格", "最新价格", "当前价格", "实时价格",
        "BTC", "比特币", "ETH", "以太坊",
        "股票", "股价", "上涨", "下跌",
        "美元汇率", "人民币汇率", "汇率",
        # 新闻
        "新闻", "最新消息", "实时新闻", "发生了什么", "刚刚发生",
        # 时间
        "今天", "现在", "最新", "最近", "当前",
        # 天气
        "天气", "气温", "气候", "降雨", "台风", "实时天气",
        # 体育
        "比赛结果", "赛果", "实时比分", "进球", "比分", "冠军"
    ]
    for kw in keywords:
        if kw.lower() in user_prompt.lower():
            return True
    return False

# ===== OCR 图片解析 =====
def ocr_image_easyocr(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    reader = easyocr.Reader(['ch', 'en'])
    result = reader.readtext(temp_path)
    return "\n".join([res[1] for res in result])

# ===== 联网搜索 =====
def search_web_serpapi(query, num_results=5):
    url = "https://serpapi.com/search.json"
    params = {"q": query, "hl": "zh-cn", "gl": "cn", "num": num_results, "api_key": serpapi_key}
    resp = requests.get(url, params=params)
    data = resp.json()
    results_text = []
    if "organic_results" in data:
        for item in data["organic_results"]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            results_text.append(f"{title}\n{snippet}\n{link}\n")
    return "\n".join(results_text) if results_text else "没有搜索到相关信息。"

# ===== Whisper 语音识别 =====
class SpeechToTextProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []
    def recv_audio_frame(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame)
        return frame

def audio_frames_to_wav(frames, filename="temp.wav"):
    import wave
    import numpy as np
    if not frames: return None
    audio = np.concatenate([f.to_ndarray() for f in frames])
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio.tobytes())
    return filename

def speech_to_text(frames):
    wav_file = audio_frames_to_wav(frames)
    if not wav_file: return ""
    with open(wav_file, "rb") as f:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=f)
    return transcript.text

# ===== GPT-5 推理（可隐藏推理过程） =====
def gpt_ask(user_input, system_prompt=None, effort="high", reasoning_tokens=1200, output_tokens=800):
    if system_prompt is None:
        system_prompt = st.session_state.get(
            "system_prompt",
            "你是一个具备高级推理能力的 GPT‑5 模型，请在回答中分为两个部分：先写推理过程，再写最终答案。"
        )

    effort_map = {
        "low": "简短概述推理过程并快速给出结论。",
        "medium": "分步骤推理并有条理地得出结论。",
        "high": "详细展示推理链路（Chain-of-Thought），分析每个关键因素，最后给出明确结论。"
    }

    reasoning_prompt = f"""
{effort_map.get(effort, effort_map['high'])}
请严格按照格式输出：
推理过程:
...(推理部分)...
最终答案:
...(简洁结论)...
限制推理tokens不超过 {reasoning_tokens}。
问题：{user_input}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        *st.session_state.chat_history,
        {"role": "user", "content": reasoning_prompt}
    ]
    
    reply_obj = client.chat.completions.create(
        model="gpt-5-chat-latest",
        messages=messages,
        max_tokens=output_tokens
    )

    full_answer = reply_obj.choices[0].message.content

    if not st.session_state.show_reasoning:
        if "最终答案:" in full_answer:
            answer = full_answer.split("最终答案:")[-1].strip()
        else:
            answer = full_answer
    else:
        answer = full_answer

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    save_memory(st.session_state.chat_history)
    return answer

# ===== 文本转语音 =====
def speak_text(text):
    audio_file = "output.mp3"
    with client.audio.speech.with_streaming_response.create(model="gpt-4o-mini-tts", voice="alloy", input=text) as response:
        response.stream_to_file(audio_file)
    st.audio(audio_file, format="audio/mp3")

# ===== 页面 UI =====
st.set_page_config(page_title="GPT-5 超级助手", page_icon="🦄", layout="wide")
st.title("🦄 GPT‑5 超级整合助手（终极版)")

# Sidebar
mode = st.sidebar.radio("选择模式", ["聊天", "同声传译", "实时字幕同传"])
default_prompt = "你是基于 GPT‑5 提供准确、有条理回答的模型。"
st.session_state.system_prompt = st.sidebar.text_area("📝 自定义角色设定", value=st.session_state.get("system_prompt", default_prompt), height=100)
effort = st.sidebar.selectbox("推理等级", ["low", "medium", "high"], index=2)
reasoning_tokens = st.sidebar.slider("推理 tokens", 200, 2000, 1200, step=100)
output_tokens = st.sidebar.slider("输出 tokens", 200, 2000, 800, step=100)
st.session_state.show_reasoning = st.sidebar.checkbox("显示推理过程", value=True)
if st.sidebar.button("🗑 清空记忆"):
    st.session_state.chat_history = []
    save_memory([])
    st.rerun()

# ===== 聊天模式 =====
if mode == "聊天":
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # 语音输入
    rtc_ctx = webrtc_streamer(key="chat-voice", mode=WebRtcMode.SENDONLY,
                              audio_processor_factory=SpeechToTextProcessor,
                              media_stream_constraints={"audio": True, "video": False})
    if rtc_ctx.audio_processor and rtc_ctx.audio_processor.frames:
        if st.button("🎤 语音转文字"):
            st.session_state.voice_input = speech_to_text(rtc_ctx.audio_processor.frames)

    # 文件上传
    uploaded_files = st.file_uploader(
        "📎 上传文件或图片 (PDF/DOCX/TXT/CSV/Excel/JPG/PNG)",
        type=["pdf", "docx", "txt", "csv", "xlsx", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    file_contents = ""
    if uploaded_files:
        for file in uploaded_files:
            suffix = Path(file.name).suffix.lower()
            if suffix in [".png", ".jpg", ".jpeg"]:
                file_contents += f"\n[图片 {file.name} OCR]:\n{ocr_image_easyocr(file)}\n"
            else:
                file_contents += f"\n[文件 {file.name} 内容]:\n{read_file(file)}\n"

    # 主输入
    if st.session_state.get("voice_input"):
        user_prompt = st.session_state.pop("voice_input")
    else:
        user_prompt = st.chat_input("请输入...")

    if user_prompt or file_contents:
        merged_prompt = ""
        if file_contents:
            merged_prompt += f"以下是用户上传的文件/图片解析结果：\n{file_contents}\n\n"

        # 自动触发联网
        if user_prompt and need_live_search(user_prompt):
            search_results = search_web_serpapi(user_prompt)
            merged_prompt += f"以下是实时联网搜索的结果：\n{search_results}\n\n请结合以上资料回答问题：{user_prompt}"

        # 图片生成
        elif user_prompt and ("画" in user_prompt or "生成图片" in user_prompt.lower()):
            with st.spinner("🎨 AI 正在为你画图..."):
                image_resp = client.images.generate(model="gpt-image-1", prompt=user_prompt, size="1024x1024")
                st.image(image_resp.data[0].url, caption="AI生成图片")
            merged_prompt = None
        else:
            merged_prompt += user_prompt if user_prompt else ""

        if merged_prompt:
            reply = gpt_ask(
                merged_prompt.strip(),
                system_prompt=st.session_state.system_prompt,
                effort=effort,
                reasoning_tokens=reasoning_tokens,
                output_tokens=output_tokens
            )
            st.markdown(reply)
            if st.button("🔊 播放回答"):
                speak_text(reply)

# ===== 其他模式 =====
elif mode == "同声传译":
    st.write("🎧 同声传译模式...（保留实现）")
elif mode == "实时字幕同传":
    st.write("📺 实时字幕同传模式...（保留实现）")