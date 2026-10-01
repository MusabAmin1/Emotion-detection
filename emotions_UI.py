import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

# ==============================
# Page Configuration
# ==============================

st.set_page_config(
    page_title="Emotion AI",
    page_icon="😊",
    layout="centered"
)


# ==============================
# Emotion Mapping (unchanged)
# ==============================

emotion_mapping = {
    0: "sadness",
    1: "anger",
    2: "love",
    3: "surprise",
    4: "fear",
    5: "joy"
}


emotion_emoji = {
    "sadness": "😢",
    "anger": "😡",
    "love": "❤️",
    "surprise": "😮",
    "fear": "😨",
    "joy": "😊"
}


emotion_description = {
    "sadness": "The text expresses feelings of sadness or disappointment.",
    "anger": "The text expresses anger, frustration, or irritation.",
    "love": "The text expresses affection, care, or love.",
    "surprise": "The text expresses something unexpected or surprising.",
    "fear": "The text expresses fear, worry, or anxiety.",
    "joy": "The text expresses happiness, excitement, or positivity."
}


# UI only: each emotion gets its own accent color and soft background tint
emotion_theme = {
    "sadness":  {"accent": "#5B7DB1", "tint": "#E6EDF8"},
    "anger":    {"accent": "#D1495B", "tint": "#FAE6E9"},
    "love":     {"accent": "#D6619A", "tint": "#FAE6F0"},
    "surprise": {"accent": "#2E9F9A", "tint": "#DFF2F1"},
    "fear":     {"accent": "#7B61B5", "tint": "#ECE7F7"},
    "joy":      {"accent": "#E0A112", "tint": "#FDF1CF"},
}


# ==============================
# Custom CSS
# ==============================

st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@400;500;600&display=swap');

    :root {
        --ink: #1d2036;
        --muted: #6a6f85;
        --line: #e2e3ec;
        --paper: #f7f7fb;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer, header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0;
    }

    /* Base */
    html, body, .stApp, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }

    .stApp {
        background: var(--paper);
        transition: background 0.6s ease;
    }

    .block-container {
        max-width: 720px;
        padding-top: 4.5rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-title {
        font-family: 'Instrument Serif', serif;
        font-size: 64px;
        line-height: 1.02;
        letter-spacing: -0.02em;
        color: var(--ink);
        margin: 0 0 14px 0;
    }

    .subtitle {
        font-size: 17px;
        line-height: 1.55;
        color: var(--muted);
        max-width: 460px;
        margin-bottom: 40px;
    }

    /* Input */
    .input-label {
        font-size: 15px;
        font-weight: 600;
        color: var(--ink);
        margin-bottom: 10px;
    }

    /* Text area: forced light so it stays readable in dark mode */
    div[data-baseweb="textarea"],
    div[data-baseweb="base-input"],
    div[data-baseweb="textarea"] > div {
        background-color: #ffffff !important;
    }

    div[data-baseweb="textarea"] {
        border: 1px solid var(--line) !important;
        border-radius: 16px !important;
        box-shadow: 0 1px 2px rgba(29, 32, 54, 0.04);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-baseweb="textarea"]:focus-within {
        border-color: var(--ink) !important;
        box-shadow: 0 0 0 4px rgba(29, 32, 54, 0.08);
    }

    .stTextArea textarea {
        font-family: 'DM Sans', sans-serif;
        font-size: 17px;
        line-height: 1.6;
        padding: 18px 20px;
        background-color: #ffffff !important;
        color: #1d2036 !important;
        -webkit-text-fill-color: #1d2036 !important;
        caret-color: #1d2036;
    }

    .stTextArea textarea::placeholder {
        color: #a3a7b9 !important;
        -webkit-text-fill-color: #a3a7b9 !important;
        opacity: 1;
    }

    /* Button: dark with white text in every state */
    .stButton button,
    button[data-testid="stBaseButton-secondary"] {
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        font-weight: 600;
        background-color: #1d2036 !important;
        border: 1px solid #1d2036 !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.5rem;
        margin-top: 6px;
        transition: transform 0.15s ease, background-color 0.2s ease;
    }

    .stButton button p,
    .stButton button span,
    button[data-testid="stBaseButton-secondary"] p {
        color: #ffffff !important;
        font-weight: 600;
    }

    .stButton button:hover,
    .stButton button:focus,
    .stButton button:focus:not(:active),
    .stButton button:active {
        background-color: #30345a !important;
        border-color: #30345a !important;
        transform: translateY(-1px);
    }

    .stButton button:focus-visible {
        outline: 3px solid rgba(29, 32, 54, 0.3) !important;
        outline-offset: 2px;
    }

    /* Keep body text dark even when the browser is in dark mode */
    .stApp .stMarkdown,
    .stApp .stMarkdown p,
    .stApp .stMarkdown li,
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary p {
        color: #1d2036 !important;
    }

    /* Result */
    .result-card {
        border-radius: 24px;
        padding: 36px 32px;
        margin: 36px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 28px;
        background: #ffffff;
        border: 1px solid var(--line);
    }

    .result-emoji {
        flex: 0 0 auto;
        width: 96px;
        height: 96px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
    }

    .result-label {
        font-size: 14px;
        color: var(--muted);
        margin-bottom: 2px;
    }

    .emotion {
        font-family: 'Instrument Serif', serif;
        font-size: 56px;
        line-height: 1.05;
        letter-spacing: -0.01em;
        color: var(--ink);
    }

    .confidence {
        font-size: 16px;
        color: var(--muted);
        margin-top: 6px;
    }

    .confidence strong {
        color: var(--ink);
        font-weight: 600;
    }

    .interpretation {
        font-size: 16px;
        line-height: 1.6;
        color: var(--ink);
        margin: 18px 4px 36px 4px;
    }

    /* Probabilities */
    .section-title {
        font-family: 'Instrument Serif', serif;
        font-size: 28px;
        color: var(--ink);
        margin-bottom: 16px;
    }

    .prob-row {
        display: grid;
        grid-template-columns: 130px 1fr 60px;
        align-items: center;
        gap: 14px;
        margin-bottom: 14px;
        font-size: 15px;
    }

    .prob-name {
        font-weight: 500;
    }

    .prob-track {
        height: 10px;
        border-radius: 999px;
        background: #ebecf3;
        overflow: hidden;
    }

    .prob-fill {
        height: 100%;
        border-radius: 999px;
        animation: grow 0.9s ease-out both;
        transform-origin: left;
    }

    .prob-value {
        text-align: right;
        color: var(--muted);
        font-variant-numeric: tabular-nums;
    }

    @keyframes grow {
        from { transform: scaleX(0); }
        to   { transform: scaleX(1); }
    }

    @media (prefers-reduced-motion: reduce) {
        .prob-fill { animation: none; }
        .stApp, .stButton > button { transition: none; }
    }

    /* Warning */
    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* About section */
    div[data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 16px;
    }

    hr {
        border-color: var(--line);
        margin: 2.5rem 0 1.5rem 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 14px;
        margin-top: 32px;
    }

    /* Mobile */
    @media (max-width: 600px) {
        .main-title { font-size: 48px; }
        .result-card { flex-direction: column; text-align: center; padding: 28px 20px; }
        .emotion { font-size: 46px; }
        .prob-row { grid-template-columns: 105px 1fr 52px; gap: 10px; }
    }

</style>
""", unsafe_allow_html=True)


# ==============================
# Load Model & Vectorizer
# ==============================

BASE_DIR = Path(__file__).resolve().parent


@st.cache_resource
def load_model():

    model = joblib.load(
        BASE_DIR / "emotions_tuned_rf_model.pkl"
    )

    vectorizer = joblib.load(
        BASE_DIR / "emotion_tfidf_vectorizer.pkl"
    )

    return model, vectorizer


model, vectorizer = load_model()


# ==============================
# Header
# ==============================

st.markdown(
    '<div class="main-title">Emotion AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Paste a sentence or a short paragraph and find out which emotion '
    'it carries. Built with TF-IDF and Random Forest.'
    '</div>',
    unsafe_allow_html=True
)


# ==============================
# Input
# ==============================

st.markdown(
    '<div class="input-label">Enter your text</div>',
    unsafe_allow_html=True
)

text = st.text_area(
    "Write something below:",
    placeholder="Example: I am really happy with the results!",
    height=150,
    label_visibility="collapsed"
)

analyze = st.button(
    "Analyze emotion",
    use_container_width=True
)


# ==============================
# Prediction
# ==============================

if analyze:

    if not text.strip():

        st.warning("Please enter some text first.")

    else:

        # Convert text using trained TF-IDF vectorizer
        text_vectorized = vectorizer.transform([text])

        # Prediction
        prediction = model.predict(text_vectorized)[0]

        emotion = emotion_mapping[prediction]

        emoji = emotion_emoji[emotion]

        # Confidence / probabilities
        probabilities = model.predict_proba(text_vectorized)[0]

        confidence = max(probabilities) * 100

        theme = emotion_theme[emotion]

        # Tint the whole page with the predicted emotion's color
        st.markdown(
            f"""
<style>
    .stApp {{
        background: radial-gradient(
            ellipse at 50% 0%,
            {theme["tint"]} 0%,
            var(--paper) 70%
        );
    }}
</style>
""",
            unsafe_allow_html=True
        )


        # ==============================
        # Result Card
        # ==============================

        st.markdown(
            f"""
<div class="result-card" style="border-color:{theme["accent"]}33;">
<div class="result-emoji" style="background:{theme["tint"]};">{emoji}</div>
<div>
<div class="result-label">Predicted emotion</div>
<div class="emotion">{emotion.capitalize()}</div>
<div class="confidence">Confidence: <strong>{confidence:.2f}%</strong></div>
</div>
</div>
""",
            unsafe_allow_html=True
        )


        # ==============================
        # Description
        # ==============================

        st.markdown(
            f'<div class="interpretation">{emotion_description[emotion]}</div>',
            unsafe_allow_html=True
        )


        # ==============================
        # Probability Breakdown
        # ==============================

        st.markdown(
            '<div class="section-title">Emotion probabilities</div>',
            unsafe_allow_html=True
        )

        probability_data = []

        for class_index, probability in enumerate(probabilities):

            emotion_name = emotion_mapping[class_index]

            probability_data.append({
                "Emotion": emotion_name.capitalize(),
                "Probability": probability
            })

        probability_df = pd.DataFrame(probability_data)

        probability_df = probability_df.sort_values(
            by="Probability",
            ascending=False
        )

        rows_html = ""

        for _, row in probability_df.iterrows():

            emotion_name = row["Emotion"]
            probability = float(row["Probability"])
            key = emotion_name.lower()

            rows_html += (
                f'<div class="prob-row">'
                f'<div class="prob-name">{emotion_emoji[key]} {emotion_name}</div>'
                f'<div class="prob-track">'
                f'<div class="prob-fill" style="width:{probability * 100:.2f}%;'
                f'background:{emotion_theme[key]["accent"]};"></div>'
                f'</div>'
                f'<div class="prob-value">{probability * 100:.2f}%</div>'
                f'</div>'
            )

        st.markdown(rows_html, unsafe_allow_html=True)


# ==============================
# Information Section
# ==============================

st.markdown("---")

with st.expander("About this project"):

    st.write("""
    This application uses a machine learning pipeline for emotion
    classification from text.

    **Text Representation:** TF-IDF

    **Machine Learning Model:** Tuned Random Forest Classifier

    **Supported Emotions:**
    - 😢 Sadness
    - 😡 Anger
    - ❤️ Love
    - 😮 Surprise
    - 😨 Fear
    - 😊 Joy
    """)


# ==============================
# Footer
# ==============================

st.markdown(
    """
    <div class="footer">
        Built with ❤️ using Python, Scikit-learn & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)