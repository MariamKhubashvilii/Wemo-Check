import streamlit as st
import os

st.set_page_config(
    page_title="Wemo Check",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - editorial / luxury minimal aesthetic
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --cream: #F5F0E8;
    --charcoal: #1C1C1E;
    --warm-gray: #8C8C8C;
    --accent: #C8A882;
    --light-border: #E8E2D9;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream) !important;
    color: var(--charcoal) !important;
}

.stApp {
    background-color: var(--cream) !important;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--charcoal) !important;
    letter-spacing: -0.02em;
}

.stButton > button {
    background-color: var(--charcoal) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: var(--accent) !important;
    color: var(--charcoal) !important;
}

.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    color: var(--charcoal) !important;
    border: 1px solid var(--charcoal) !important;
}

.stButton > button[kind="secondary"]:hover {
    background-color: var(--charcoal) !important;
    color: var(--cream) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: white !important;
    border: 1px solid var(--light-border) !important;
    border-radius: 0 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--charcoal) !important;
}

.stSelectbox > div > div:hover,
.stTextInput > div > div > input:focus {
    border-color: var(--charcoal) !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] {
    background-color: var(--charcoal) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: var(--cream) !important;
}

[data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    color: var(--cream) !important;
    border: 1px solid rgba(245,240,232,0.2) !important;
    width: 100% !important;
    text-align: left !important;
    padding: 0.5rem 1rem !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    color: var(--charcoal) !important;
}

[data-testid="stSidebar"] .stTextInput > div > div > input {
    background-color: rgba(245,240,232,0.05) !important;
    border: 1px solid rgba(245,240,232,0.15) !important;
    color: var(--cream) !important;
}

.stSlider > div > div > div {
    color: var(--charcoal) !important;
}

div[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

.item-card {
    background: white;
    border: 1px solid var(--light-border);
    padding: 0;
    transition: all 0.2s ease;
    cursor: pointer;
}

.item-card:hover {
    border-color: var(--charcoal);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.item-label {
    padding: 0.6rem 0.8rem;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--warm-gray);
    border-top: 1px solid var(--light-border);
}

.outfit-card {
    background: white;
    border: 1px solid var(--light-border);
    padding: 1.2rem;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--warm-gray);
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--light-border);
}

.tag {
    display: inline-block;
    background: var(--cream);
    border: 1px solid var(--light-border);
    padding: 0.15rem 0.5rem;
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--warm-gray);
    margin: 0.1rem;
}

hr {
    border: none;
    border-top: 1px solid var(--light-border) !important;
    margin: 1.5rem 0 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent;
    border-bottom: 1px solid var(--light-border);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--warm-gray) !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.2rem !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}

.stTabs [aria-selected="true"] {
    color: var(--charcoal) !important;
    border-bottom: 2px solid var(--charcoal) !important;
}

.stSuccess {
    background-color: rgba(200, 168, 130, 0.1) !important;
    border-color: var(--accent) !important;
    color: var(--charcoal) !important;
}

div[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    color: var(--charcoal) !important;
}
</style>
""", unsafe_allow_html=True)

from database import init_db

init_db()

# Sidebar
with st.sidebar:
    st.markdown("## Wemo Check")
    st.markdown("<p style='font-size:0.7rem; letter-spacing:0.15em; text-transform:uppercase; opacity:0.5; margin-top:-0.5rem; margin-bottom:1.5rem;'>Your wardrobe, styled. 🧥</p>", unsafe_allow_html=True)

    st.markdown("---")

    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    if api_key:
        st.session_state["api_key"] = api_key
        st.success("✓ Key saved")
    elif "api_key" not in st.session_state:
        st.warning("Add your API key to use AI features.")

    st.markdown("---")
    st.markdown("<p class='section-title' style='color:rgba(245,240,232,0.4);'>Navigation</p>", unsafe_allow_html=True)

    if st.button("🧥  Wardrobe"):
        st.session_state["page"] = "wardrobe"
        st.rerun()
    if st.button("✨  Get Dressed"):
        st.session_state["page"] = "suggest"
        st.rerun()
    if st.button("📁  Saved Outfits"):
        st.session_state["page"] = "saved"
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size:0.65rem; opacity:0.3; letter-spacing:0.05em;'>v1.0 — local storage</p>", unsafe_allow_html=True)

# Page routing
page = st.session_state.get("page", "wardrobe")

if page == "wardrobe":
    from views.wardrobe import show
    show()
elif page == "suggest":
    from views.suggest import show
    show()
elif page == "saved":
    from views.saved import show
    show()
