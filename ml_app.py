import html
import json
import os
import re
from datetime import datetime

import joblib
import nltk
import numpy as np
import streamlit as st
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


@st.cache_resource
def initialize_resources():
    nltk.download("punkt")
    nltk.download("punkt_tab")
    nltk.download("stopwords")

    factory = StemmerFactory()
    return factory.create_stemmer()


stemmer = initialize_resources()
indonesian_stopwords = set(stopwords.words("indonesian"))


def clean(text):
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = text.lower().strip()
    text = word_tokenize(text)
    text = [stemmer.stem(word) for word in text if word not in indonesian_stopwords]
    text = " ".join(text)
    return text


def load_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file), "rb"))
    return loaded_model


try:
    optimal_thresholds_fitur = json.load(open("optimal_thresholds_svc_fitur.json", "r"))
    optimal_thresholds_masalah = json.load(open("optimal_thresholds_svc_masalah.json", "r"))
    optimal_thresholds_respon = json.load(open("optimal_thresholds_svc_respon.json", "r"))
except Exception:
    optimal_thresholds_fitur = None
    optimal_thresholds_masalah = None
    optimal_thresholds_respon = None


def apply_threshold_prediction(proba_score, optimal_thresholds):
    thresholds = {int(k): v for k, v in optimal_thresholds.items()}
    pred_binary = [
        1 if proba_score[i] >= thresholds[i] else 0
        for i in range(len(proba_score))
    ]

    if sum(pred_binary) == 0:
        return np.argmax(proba_score)

    return np.argmax(
        [proba_score[i] * pred_binary[i] for i in range(len(proba_score))]
    )


def get_default_assistant_message():
    return {
        "role": "assistant",
        "content": (
            "Halo, saya Audore Assistant. Silakan ceritakan keluhan "
            "atau pertanyaan Anda."
        ),
    }


def build_chat_title(messages):
    for message in messages:
        if message.get("role") == "user":
            title = message.get("content", "").strip()
            if len(title) > 42:
                title = title[:42].rstrip() + "..."
            return title

    return "Chat baru"


def initialize_chat_sessions():
    if "assistant_chat_counter" not in st.session_state:
        st.session_state.assistant_chat_counter = 1

    if "assistant_chat_sessions" not in st.session_state:
        existing_messages = st.session_state.get("messages")

        if existing_messages:
            initial_messages = existing_messages
        else:
            initial_messages = [get_default_assistant_message()]

        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        st.session_state.assistant_chat_sessions = [
            {
                "id": "chat_1",
                "title": build_chat_title(initial_messages),
                "messages": initial_messages,
                "created_at": now,
                "updated_at": now,
            }
        ]

    if "active_assistant_chat_id" not in st.session_state:
        st.session_state.active_assistant_chat_id = (
            st.session_state.assistant_chat_sessions[0]["id"]
        )


def get_current_chat_session():
    initialize_chat_sessions()

    for session in st.session_state.assistant_chat_sessions:
        if session["id"] == st.session_state.active_assistant_chat_id:
            return session

    st.session_state.active_assistant_chat_id = (
        st.session_state.assistant_chat_sessions[0]["id"]
    )
    return st.session_state.assistant_chat_sessions[0]


def update_current_chat_session(messages):
    current_session = get_current_chat_session()
    current_session["messages"] = messages
    current_session["title"] = build_chat_title(messages)
    current_session["updated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.session_state.messages = messages


def create_new_chat_session():
    st.session_state.assistant_chat_counter += 1
    chat_id = f"chat_{st.session_state.assistant_chat_counter}"
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    new_session = {
        "id": chat_id,
        "title": "Chat baru",
        "messages": [get_default_assistant_message()],
        "created_at": now,
        "updated_at": now,
    }

    st.session_state.assistant_chat_sessions.insert(0, new_session)
    st.session_state.active_assistant_chat_id = chat_id
    st.session_state.messages = new_session["messages"]


def clear_all_chat_sessions():
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.session_state.assistant_chat_counter = 1
    st.session_state.assistant_chat_sessions = [
        {
            "id": "chat_1",
            "title": "Chat baru",
            "messages": [get_default_assistant_message()],
            "created_at": now,
            "updated_at": now,
        }
    ]
    st.session_state.active_assistant_chat_id = "chat_1"
    st.session_state.messages = st.session_state.assistant_chat_sessions[0]["messages"]


def render_message(message, user_initial, probability_labels):
    content_html = html.escape(message["content"]).replace("\n", "<br>")

    if message["role"] == "user":
        st.markdown(
            f"""
            <div class="chat-row user">
                <div class="chat-bubble user">{content_html}</div>
                <div class="chat-avatar user">{user_initial}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="chat-row assistant">
            <div class="chat-avatar assistant">A</div>
            <div class="chat-bubble assistant">{content_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "probabilities" not in message:
        return

    proba_html = ""

    for label, score in zip(probability_labels, message["probabilities"]):
        percent = score * 100
        proba_html += f"""
        <div class="proba-row">
            <div class="proba-label">
                <span>{label}</span>
                <span>{percent:.2f}%</span>
            </div>
            <div class="proba-track">
                <div class="proba-fill" style="width: {percent:.2f}%;"></div>
            </div>
        </div>
        """

    clean_text = html.escape(message.get("clean_text", "-"))
    prediction_label = html.escape(message.get("prediction_label", "-"))
    confidence_score = message.get("confidence_score", 0)

    st.markdown(
        f"""
        <div class="model-card">
            <h4>Hasil Analisis Model</h4>
            <div class="model-meta">
                Model: <b>TF-IDF + Support Vector Classifier</b><br>
                Teks setelah preprocessing: <b>{clean_text}</b><br>
                Prediksi: <b>{prediction_label}</b><br>
                Confidence tertinggi: <b>{confidence_score:.2f}%</b>
            </div>
            {proba_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_bot_response(respon_prediction):
    if respon_prediction == 0:
        return (
            "Untuk informasi lebih lanjut mengenai masalah tersebut, "
            "silakan melakukan konsultasi melalui fitur Konsultasi."
        )

    if respon_prediction == 1:
        return (
            "Kesulitan memperoleh informasi yang jelas mengenai ASD dapat "
            "membuat caregiver merasa bingung dalam mengambil keputusan "
            "terkait pengasuhan maupun terapi. Anda dapat mengakses fitur "
            "Edukasi untuk memperoleh informasi dan materi yang relevan."
        )

    if respon_prediction == 2:
        return (
            "Kurangnya dukungan dari lingkungan sekitar dapat membuat "
            "caregiver merasa sendirian dalam menghadapi tantangan "
            "pengasuhan. Anda dapat memanfaatkan fitur Komunitas untuk "
            "terhubung dengan caregiver lainnya."
        )

    if respon_prediction == 3:
        return (
            "Saya memahami bahwa tanggung jawab pengasuhan yang terus-menerus "
            "dapat menimbulkan kelelahan fisik dan emosional. Anda dapat "
            "memanfaatkan fitur Konsultasi untuk berdiskusi lebih lanjut "
            "mengenai strategi pengelolaan stres dan dukungan yang sesuai."
        )

    return (
        "Terima kasih telah berbagi cerita. Perasaan yang Anda rasakan "
        "adalah hal yang valid dan penting untuk mendapatkan dukungan "
        "yang sesuai. Jika Anda merasa sangat tertekan atau terdapat "
        "risiko membahayakan diri sendiri maupun orang lain, segera "
        "hubungi tenaga profesional atau layanan bantuan darurat."
    )


def run_ml_app():
    st.markdown(
        """
        <style>
        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"] {
            color-scheme: light;
        }

        .assistant-page {
            max-width: 1040px;
            margin: 0 auto;
        }

        .assistant-toolbar {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 20px;
            padding: 0.85rem 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 12px 28px rgba(88, 72, 124, 0.07);
        }

        .assistant-toolbar-title {
            color: #2F2A38;
            font-size: 0.95rem;
            font-weight: 800;
            margin: 0;
        }

        .assistant-toolbar-subtitle {
            color: #6A6278;
            font-size: 0.82rem;
            margin: 0.2rem 0 0 0;
        }

        .assistant-hero {
            background:
                radial-gradient(circle at top left, #FFDDE7 0%, transparent 38%),
                radial-gradient(circle at bottom right, #E9E1FF 0%, transparent 42%),
                linear-gradient(145deg, #FFFFFF 0%, #FFF9FA 100%);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 28px;
            box-shadow: 0 18px 42px rgba(88, 72, 124, 0.10);
            padding: 2.2rem 2.4rem;
            margin-bottom: 1.4rem;
        }

        .assistant-badge {
            display: inline-block;
            background: #FFDDE7;
            color: #3A2E3F;
            border-radius: 999px;
            padding: 0.45rem 0.85rem;
            font-size: 0.86rem;
            font-weight: 700;
            margin-bottom: 1.1rem;
        }

        .assistant-hero h1 {
            color: #111111;
            font-size: 2.25rem;
            font-weight: 800;
            margin: 0 0 0.65rem 0;
            letter-spacing: 0;
        }

        .assistant-hero p {
            color: #5F5870;
            font-size: 1.05rem;
            line-height: 1.7;
            margin: 0;
        }

        .assistant-info-card {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 22px;
            padding: 1.1rem 1.25rem;
            margin-bottom: 1.4rem;
            box-shadow: 0 14px 34px rgba(88, 72, 124, 0.08);
        }

        .assistant-info-card h3 {
            color: #2F2A38;
            font-size: 1.05rem;
            font-weight: 800;
            margin: 0 0 0.35rem 0;
        }

        .assistant-info-card p {
            color: #4F485D;
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
        }

        .history-item {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 16px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.75rem;
        }

        .history-title {
            color: #2F2A38;
            font-size: 0.92rem;
            font-weight: 800;
            margin: 0;
        }

        .history-meta {
            color: #7A728A;
            font-size: 0.78rem;
            margin-top: 0.15rem;
        }

        .chat-row {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            margin-bottom: 1rem;
            width: 100%;
        }

        .chat-row.user {
            justify-content: flex-end;
        }

        .chat-row.assistant {
            justify-content: flex-start;
        }

        .chat-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            font-size: 0.82rem;
            font-weight: 800;
        }

        .chat-avatar.assistant {
            background: #FFDDE7;
            color: #3A2E3F;
        }

        .chat-avatar.user {
            background: #E9E1FF;
            color: #3A2E3F;
        }

        .chat-bubble {
            max-width: 68%;
            padding: 0.95rem 1.05rem;
            border-radius: 20px;
            font-size: 0.98rem;
            line-height: 1.65;
            word-break: break-word;
            white-space: pre-wrap;
            box-shadow: 0 12px 28px rgba(88, 72, 124, 0.07);
        }

        .chat-bubble.assistant {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(122, 90, 248, 0.10);
            color: #2F2A38;
            border-top-left-radius: 8px;
        }

        .chat-bubble.user {
            background: #FFF0C9;
            border: 1px solid rgba(255, 210, 110, 0.35);
            color: #2F2A38;
            border-top-right-radius: 8px;
        }

        .model-card {
            max-width: 68%;
            margin: -0.35rem 0 1.2rem 3rem;
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(122, 90, 248, 0.12);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 12px 28px rgba(88, 72, 124, 0.07);
        }

        .model-card h4 {
            margin: 0 0 0.7rem 0;
            color: #2F2A38;
            font-size: 0.95rem;
            font-weight: 800;
        }

        .model-meta {
            color: #5F5870;
            font-size: 0.82rem;
            line-height: 1.5;
            margin-bottom: 0.7rem;
        }

        .proba-row {
            margin-bottom: 0.55rem;
        }

        .proba-label {
            display: flex;
            justify-content: space-between;
            color: #3A3442;
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .proba-track {
            height: 8px;
            background: #F1EDF8;
            border-radius: 999px;
            overflow: hidden;
        }

        .proba-fill {
            height: 100%;
            background: linear-gradient(90deg, #FFDDE7, #E9E1FF);
            border-radius: 999px;
        }

        label,
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] p,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p {
            color: #2F2A38 !important;
        }

        div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.86) !important;
            border: 1px solid rgba(122, 90, 248, 0.10) !important;
            border-radius: 18px !important;
            color: #2F2A38 !important;
        }

        div[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] summary p {
            color: #2F2A38 !important;
            font-weight: 800 !important;
        }

        div[data-testid="stChatInput"] {
            max-width: 1040px;
            margin: 0 auto;
            background: transparent !important;
        }

        div[data-testid="stChatInput"] > div {
            background: rgba(255, 255, 255, 0.96) !important;
            border: 1px solid rgba(122, 90, 248, 0.16) !important;
            border-radius: 18px !important;
            box-shadow: 0 14px 34px rgba(88, 72, 124, 0.10) !important;
        }

        div[data-testid="stChatInput"] textarea {
            background: rgba(255, 255, 255, 0.96) !important;
            color: #2F2A38 !important;
            caret-color: #2F2A38 !important;
            border-radius: 18px !important;
            border: 0 !important;
        }

        div[data-testid="stChatInput"] textarea::placeholder {
            color: #8A819A !important;
            opacity: 1 !important;
        }

        div[data-testid="stChatInput"] button {
            background: #F3F0FF !important;
            color: #2F2A38 !important;
            border-radius: 14px !important;
        }

        div[data-testid="stButton"] > button {
            border-radius: 999px;
            font-weight: 700;
            min-height: 2.55rem;
            background: rgba(255, 255, 255, 0.92) !important;
            color: #514568 !important;
            border: 1px solid rgba(122, 90, 248, 0.18) !important;
            box-shadow: 0 10px 22px rgba(122, 90, 248, 0.10);
        }

        div[data-testid="stButton"] > button:hover {
            background: #F8FBFF !important;
            color: #2F2A38 !important;
            border-color: rgba(122, 90, 248, 0.28) !important;
        }

        @media (max-width: 768px) {
            .assistant-hero {
                padding: 1.5rem;
            }

            .assistant-hero h1 {
                font-size: 1.85rem;
            }

            .chat-bubble,
            .model-card {
                max-width: 82%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    initialize_chat_sessions()
    current_session = get_current_chat_session()
    messages = current_session["messages"]

    st.markdown('<div class="assistant-page">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="assistant-toolbar">
            <p class="assistant-toolbar-title">Audore Assistant</p>
            <p class="assistant-toolbar-subtitle">
                Kelola percakapan, buka riwayat, atau kembali ke halaman utama.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    back_col, new_chat_col, empty_col = st.columns([1, 1, 3], gap="small")

    with back_col:
        if st.button("Kembali", use_container_width=True):
            st.session_state.active_page = "Home"
            st.rerun()

    with new_chat_col:
        if st.button("Chat Baru", use_container_width=True):
            create_new_chat_session()
            st.rerun()

    with st.expander("Riwayat Chat", expanded=False):
        if not st.session_state.assistant_chat_sessions:
            st.info("Belum ada riwayat chat.")
        else:
            for session in st.session_state.assistant_chat_sessions:
                is_active = session["id"] == st.session_state.active_assistant_chat_id
                active_label = "Aktif" if is_active else "Buka"
                safe_title = html.escape(session["title"])
                safe_time = html.escape(session["updated_at"])

                st.markdown(
                    f"""
                    <div class="history-item">
                        <p class="history-title">{safe_title}</p>
                        <div class="history-meta">Terakhir diperbarui: {safe_time}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    active_label,
                    key=f"open_history_{session['id']}",
                    use_container_width=True,
                    disabled=is_active,
                ):
                    st.session_state.active_assistant_chat_id = session["id"]
                    st.session_state.messages = session["messages"]
                    st.rerun()

        if st.button("Hapus Semua Riwayat", use_container_width=True):
            clear_all_chat_sessions()
            st.rerun()

    st.markdown(
        """
        <div class="assistant-hero">
            <div class="assistant-badge">Audore Assistant</div>
            <h1>Audore Assistant</h1>
            <p>
                Sampaikan keluhan atau pertanyaan Anda mengenai pengasuhan,
                terapi, pendidikan, maupun kondisi psikologis terkait Autism
                Spectrum Disorder.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="assistant-info-card">
            <h3>Ruang pendampingan awal</h3>
            <p>
                Audore Assistant membantu mengarahkan keluhan caregiver ke
                informasi, komunitas, atau konsultasi yang lebih sesuai.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tfidf_respon = load_model("tfidf_respon.pkl")
    svc_respon_data = load_model("svc_respon.pkl")

    response_labels = {
        0: "Konsultasi",
        1: "Edukasi",
        2: "Komunitas",
        3: "Konsultasi Pengasuhan",
        4: "Dukungan Profesional",
    }

    probability_labels = [
        "Konsultasi",
        "Edukasi",
        "Komunitas",
        "Konsultasi Pengasuhan",
        "Dukungan Profesional",
    ]

    user_name = st.session_state.get("user_name", "Pengguna")
    user_initial = user_name[:1].upper() if user_name else "U"

    for message in messages:
        render_message(message, user_initial, probability_labels)

    st.markdown("</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ketikkan keluhan Anda"):
        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        clean_prompt = clean(prompt)

        try:
            tfidf_prompt_respon = tfidf_respon.transform([clean_prompt])
            respon_proba = svc_respon_data.predict_proba(tfidf_prompt_respon)[0]

            if optimal_thresholds_respon is not None:
                respon_prediction = apply_threshold_prediction(
                    respon_proba,
                    optimal_thresholds_respon,
                )
            else:
                respon_prediction = np.argmax(respon_proba)

            confidence_score = respon_proba[respon_prediction] * 100
            prediction_label = response_labels.get(
                respon_prediction,
                "Kategori Tidak Diketahui",
            )

            bot_response = get_bot_response(respon_prediction)

            messages.append(
                {
                    "role": "assistant",
                    "content": bot_response,
                    "prediction_label": prediction_label,
                    "confidence_score": confidence_score,
                    "probabilities": respon_proba.tolist(),
                    "clean_text": clean_prompt,
                }
            )

        except Exception as e:
            messages.append(
                {
                    "role": "assistant",
                    "content": f"Gagal memproses model: {str(e)}",
                }
            )

        update_current_chat_session(messages)
        st.rerun()