import subprocess
import sys

# ── Auto-install missing packages ────────────────────────────────────────────
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

required = {
    "nltk": "nltk",
    "pandas": "pandas",
    "plotly": "plotly",
    "matplotlib": "matplotlib",
    "wordcloud": "wordcloud",
}

for module, pkg in required.items():
    try:
        __import__(module)
    except ImportError:
        install(pkg)

# ── Imports ───────────────────────────────────────────────────────────────────
import streamlit as st
import nltk
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StopLens · NLP Stop Word Analyser",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Download NLTK data (safe) ─────────────────────────────────────────────────
@st.cache_resource
def download_nltk():
    for pkg in ["punkt", "stopwords", "punkt_tab"]:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass

download_nltk()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Fraunces:ital,wght@0,400;0,700;1,400&display=swap');

html, body, [class*="css"] {
    font-family: 'Fraunces', Georgia, serif;
    background-color: #f5f0e8;
    color: #1a1208;
}
.stApp { background: #f5f0e8; }

[data-testid="stSidebar"] { background: #1a1208 !important; border-right: 2px solid #c8a96e; }
[data-testid="stSidebar"] * { color: #f5f0e8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextArea label,
[data-testid="stSidebar"] .stSlider label { color: #c8a96e !important; }

h1 { font-size: 2.8rem !important; font-weight: 700 !important; color: #1a1208 !important; letter-spacing: -1px; }
h2 { font-size: 1.5rem !important; color: #3d2b00 !important; border-bottom: 2px solid #c8a96e; padding-bottom: 6px; }
h3 { font-size: 1.1rem !important; color: #5a3e00 !important; }

[data-testid="stMetric"] {
    background: #fff9f0; border: 1px solid #c8a96e;
    border-left: 4px solid #c8a96e; border-radius: 8px; padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: #5a3e00 !important; font-family: 'DM Mono', monospace !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #1a1208 !important; font-size: 2rem !important; }

.stButton > button {
    background: #1a1208 !important; color: #f5f0e8 !important;
    border: 2px solid #c8a96e !important; border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.85rem !important;
    letter-spacing: 1px !important; padding: 8px 24px !important;
}
.stButton > button:hover { background: #c8a96e !important; color: #1a1208 !important; }

.stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid #c8a96e; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace; font-size: 0.8rem;
    letter-spacing: 1px; color: #5a3e00; background: transparent;
    border-radius: 4px 4px 0 0; padding: 8px 20px;
}
.stTabs [aria-selected="true"] { background: #1a1208 !important; color: #c8a96e !important; }

.stTextArea textarea {
    background: #fff9f0 !important; border: 1px solid #c8a96e !important;
    border-radius: 6px !important; font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important; color: #1a1208 !important;
}
.stAlert { border-radius: 6px !important; font-family: 'DM Mono', monospace !important; font-size: 0.82rem !important; }

.highlight-box {
    background: #fff9f0; border: 1px solid #c8a96e;
    border-radius: 8px; padding: 20px 24px; line-height: 2.4; font-size: 1rem;
}
.sw { background: #c8a96e66; border-radius: 3px; padding: 2px 5px; font-weight: 700; color: #7a4f00; }
.kw { color: #1a1208; }
</style>
""", unsafe_allow_html=True)

# ── Supported Languages ───────────────────────────────────────────────────────
SUPPORTED_LANGS = {
    "English":    "english",
    "French":     "french",
    "German":     "german",
    "Spanish":    "spanish",
    "Italian":    "italian",
    "Portuguese": "portuguese",
    "Dutch":      "dutch",
    "Russian":    "russian",
    "Arabic":     "arabic",
}

# ── Helper Functions ──────────────────────────────────────────────────────────
@st.cache_data
def get_stopwords(lang: str) -> set:
    try:
        return set(stopwords.words(lang))
    except Exception:
        return set()

def safe_tokenize(text: str) -> list:
    try:
        tokens = word_tokenize(text.lower())
    except Exception:
        tokens = text.lower().split()
    return [t for t in tokens if re.match(r'^[a-záéíóúàâäèêëîïôùûüçñ]+$', t)]

def analyse(text: str, lang: str, custom_sw: set, apply_custom: bool) -> dict:
    sw_set = get_stopwords(lang)
    if apply_custom:
        sw_set = sw_set | custom_sw

    tokens        = safe_tokenize(text)
    stop_tokens   = [t for t in tokens if t in sw_set]
    content_tokens = [t for t in tokens if t not in sw_set]

    return {
        "all_tokens":     tokens,
        "stop_tokens":    stop_tokens,
        "content_tokens": content_tokens,
        "sw_set":         sw_set,
        "stop_freq":      Counter(stop_tokens),
        "content_freq":   Counter(content_tokens),
    }

def highlight_html(text: str, sw_set: set) -> str:
    parts = []
    for word in text.split():
        clean = re.sub(r'[^a-zA-Z]', '', word).lower()
        if clean in sw_set:
            parts.append(f'<span class="sw" title="stop word">{word}</span>')
        else:
            parts.append(f'<span class="kw">{word}</span>')
    return " ".join(parts)

def make_wordcloud(freq: Counter, colormap: str):
    if not freq:
        return None
    wc = WordCloud(
        width=860, height=380,
        background_color="#fff9f0",
        colormap=colormap,
        max_words=80,
    ).generate_from_frequencies(freq)
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor("#fff9f0")
    plt.tight_layout(pad=0)
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 StopLens")
    st.markdown("*NLP Stop Word Analyser*")
    st.divider()

    lang_name = st.selectbox("Language", list(SUPPORTED_LANGS.keys()))
    lang      = SUPPORTED_LANGS[lang_name]

    st.markdown("### ➕ Custom Stop Words")
    custom_raw = st.text_area(
        "Add words (comma-separated)",
        placeholder="e.g. also, however, therefore",
        height=80,
    )
    custom_sw    = {w.strip().lower() for w in custom_raw.split(",") if w.strip()}
    apply_custom = st.checkbox("Apply custom stop words", value=True)

    st.divider()
    top_n      = st.slider("Top N words in charts", 5, 30, 15)
    show_cloud = st.checkbox("Show Word Clouds", value=True)

    st.divider()
    sw_count = len(get_stopwords(lang))
    st.info(f"📚 {sw_count} stop words loaded for {lang_name}")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🔬 StopLens")
st.markdown("**Analyse, visualise, and understand stop words in your text using NLP.**")
st.markdown("---")

# ── Sample Texts ──────────────────────────────────────────────────────────────
SAMPLES = {
    "Custom": "",
    "News excerpt": (
        "The government announced on Wednesday that it would be implementing new policies "
        "to address the rising cost of living. Officials said the measures are expected to "
        "take effect within the next few months and will benefit millions of citizens across "
        "the country. However, critics argued that the plan does not go far enough to help "
        "the most vulnerable members of society."
    ),
    "Scientific abstract": (
        "In this study, we investigated the effects of temperature on enzymatic activity "
        "of protease extracted from Bacillus subtilis. The results demonstrated a significant "
        "increase in catalytic efficiency at 45 degrees compared to standard conditions. "
        "These findings suggest that thermostable enzymes could be effectively utilized in "
        "industrial biotechnology applications."
    ),
    "Literary prose": (
        "It was the best of times, it was the worst of times, it was the age of wisdom, "
        "it was the age of foolishness, it was the epoch of belief, it was the epoch of "
        "incredulity, it was the season of Light, it was the season of Darkness, it was "
        "the spring of hope, it was the winter of despair."
    ),
}

col1, col2 = st.columns([3, 1])
with col1:
    sample_choice = st.selectbox("Load a sample text", list(SAMPLES.keys()))
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.success(f"✅ NLTK ready · {sw_count} stop words")

text_input = st.text_area(
    "Paste or type your text here",
    value=SAMPLES[sample_choice],
    height=160,
    placeholder="Enter any text to analyse its stop words…",
)

_, btn_col, _ = st.columns([1, 1, 3])
with btn_col:
    run = st.button("▶  Analyse Text", use_container_width=True)

# ── Run Analysis ──────────────────────────────────────────────────────────────
if run or (text_input and text_input != SAMPLES.get("Custom", "")):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text to analyse.")
        st.stop()

    with st.spinner("Analysing…"):
        res = analyse(text_input, lang, custom_sw, apply_custom)

    total  = len(res["all_tokens"])
    n_stop = len(res["stop_tokens"])
    n_cont = len(res["content_tokens"])
    ratio  = round(n_stop / total * 100, 1) if total else 0

    if total == 0:
        st.error("No tokens found. Please enter valid text.")
        st.stop()

    # ── Metrics ───────────────────────────────────────────────────────────────
    st.markdown("## 📊 Overview")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Tokens",        total)
    m2.metric("Stop Words",          n_stop,               f"{ratio}%")
    m3.metric("Content Words",       n_cont,               f"{100 - ratio}%")
    m4.metric("Unique Stop Words",   len(res["stop_freq"]))
    m5.metric("Unique Content Words", len(res["content_freq"]))

    st.markdown("---")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎨 Highlighted Text",
        "📈 Frequency Charts",
        "☁️ Word Clouds",
        "📋 Data Tables",
        "⚙️ Stop Word List",
    ])

    # ── Tab 1: Highlighted Text ───────────────────────────────────────────────
    with tab1:
        st.markdown("### Text with Stop Words Highlighted")
        st.markdown(
            "<small>🟡 <b>highlighted</b> = stop word &nbsp;|&nbsp; plain = content word</small>",
            unsafe_allow_html=True,
        )
        html = highlight_html(text_input, res["sw_set"])
        st.markdown(f'<div class="highlight-box">{html}</div>', unsafe_allow_html=True)

        st.markdown("### 🧹 Cleaned Text (stop words removed)")
        cleaned = " ".join(
            w for w in text_input.split()
            if re.sub(r'[^a-zA-Z]', '', w).lower() not in res["sw_set"]
        )
        st.text_area("", value=cleaned, height=120, key="cleaned_out")

    # ── Tab 2: Charts ─────────────────────────────────────────────────────────
    with tab2:
        # Stop word bar chart
        st.markdown(f"### Top {top_n} Stop Words")
        sw_df = pd.DataFrame(res["stop_freq"].most_common(top_n), columns=["Word", "Count"])
        if not sw_df.empty:
            fig1 = go.Figure(go.Bar(
                x=sw_df["Count"], y=sw_df["Word"], orientation="h",
                marker=dict(color=sw_df["Count"], colorscale=[[0,"#e8d5b0"],[1,"#7a4f00"]]),
                text=sw_df["Count"], textposition="outside",
            ))
            fig1.update_layout(
                height=420, yaxis=dict(autorange="reversed"),
                paper_bgcolor="#fff9f0", plot_bgcolor="#fff9f0",
                font=dict(family="DM Mono, monospace", color="#1a1208"),
                margin=dict(l=10, r=50, t=10, b=10),
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No stop words detected.")

        # Content word bar chart
        st.markdown(f"### Top {top_n} Content Words")
        cw_df = pd.DataFrame(res["content_freq"].most_common(top_n), columns=["Word", "Count"])
        if not cw_df.empty:
            fig2 = go.Figure(go.Bar(
                x=cw_df["Count"], y=cw_df["Word"], orientation="h",
                marker=dict(color=cw_df["Count"], colorscale=[[0,"#b0c4e8"],[1,"#003060"]]),
                text=cw_df["Count"], textposition="outside",
            ))
            fig2.update_layout(
                height=420, yaxis=dict(autorange="reversed"),
                paper_bgcolor="#fff9f0", plot_bgcolor="#fff9f0",
                font=dict(family="DM Mono, monospace", color="#1a1208"),
                margin=dict(l=10, r=50, t=10, b=10),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No content words detected.")

        # Donut chart
        st.markdown("### Composition Breakdown")
        fig3 = go.Figure(go.Pie(
            labels=["Stop Words", "Content Words"],
            values=[n_stop, n_cont],
            hole=0.55,
            marker=dict(colors=["#c8a96e", "#1a1208"]),
            textfont=dict(family="DM Mono, monospace", size=13),
        ))
        fig3.update_layout(
            height=320, paper_bgcolor="#fff9f0",
            font=dict(family="DM Mono, monospace", color="#1a1208"),
            legend=dict(orientation="h", y=-0.1),
            margin=dict(l=20, r=20, t=10, b=20),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tab 3: Word Clouds ────────────────────────────────────────────────────
    with tab3:
        if show_cloud:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### Stop Word Cloud")
                fig_sw = make_wordcloud(res["stop_freq"], "YlOrBr")
                if fig_sw:
                    st.pyplot(fig_sw)
                else:
                    st.info("No stop words found.")
            with c2:
                st.markdown("### Content Word Cloud")
                fig_cw = make_wordcloud(res["content_freq"], "Blues")
                if fig_cw:
                    st.pyplot(fig_cw)
                else:
                    st.info("No content words found.")
        else:
            st.info("Enable **Show Word Clouds** in the sidebar.")

    # ── Tab 4: Data Tables ────────────────────────────────────────────────────
    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Stop Word Frequencies")
            sw_tbl = pd.DataFrame(res["stop_freq"].most_common(), columns=["Word", "Count"])
            if n_stop:
                sw_tbl["% of Stop Words"] = (sw_tbl["Count"] / n_stop * 100).round(1)
            st.dataframe(sw_tbl, use_container_width=True, height=340)

        with c2:
            st.markdown("### Content Word Frequencies")
            cw_tbl = pd.DataFrame(res["content_freq"].most_common(), columns=["Word", "Count"])
            if n_cont:
                cw_tbl["% of Content"] = (cw_tbl["Count"] / n_cont * 100).round(1)
            st.dataframe(cw_tbl, use_container_width=True, height=340)

        st.markdown("### ⬇️ Export")
        export_df = pd.DataFrame({
            "Token":        res["all_tokens"],
            "Is Stop Word": [t in res["sw_set"] for t in res["all_tokens"]],
        })
        csv_bytes = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Token Data (CSV)",
            data=csv_bytes,
            file_name="stopword_analysis.csv",
            mime="text/csv",
        )

    # ── Tab 5: Stop Word List ─────────────────────────────────────────────────
    with tab5:
        st.markdown(f"### NLTK Stop Words — {lang_name} ({sw_count} words)")
        cols = st.columns(6)
        for i, w in enumerate(sorted(res["sw_set"])):
            cols[i % 6].markdown(
                f"<code style='font-size:0.76rem'>{w}</code>",
                unsafe_allow_html=True,
            )
        if custom_sw:
            st.markdown("### Your Custom Stop Words")
            st.write(", ".join(sorted(custom_sw)))