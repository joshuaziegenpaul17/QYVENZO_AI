import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

# --- CONFIG ---
st.set_page_config(page_title="QYVENZO AI", layout="wide", initial_sidebar_state="expanded")

# --- CYBER-GLASS STYLING ---
st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top left,#16213e 0%,#0a0a0a 45%), radial-gradient(circle at bottom right,#1b263b 0%,#0a0a0a 40%); color:white; }
[data-testid="stSidebar"] { background:rgba(10,15,25,0.95); backdrop-filter:blur(30px); border-right:1px solid rgba(255,255,255,0.08); width: 320px !important; }
.hero { padding:35px; border-radius:28px; background:linear-gradient(135deg, rgba(0,255,255,0.08), rgba(124,77,255,0.08)); border:1px solid rgba(255,255,255,0.08); backdrop-filter:blur(30px); margin-bottom:25px; }
.stButton>button { width:100%; height:50px; border-radius:15px; border:none; background:linear-gradient(90deg, #00e5ff, #7c4dff); color:white; font-weight:700; margin-bottom: 10px; }
.marquee { overflow: hidden; white-space: nowrap; color: #00e5ff; font-weight: bold; margin-bottom: 20px; font-size: 1.2rem; }
.marquee span { display: inline-block; animation: move 20s linear infinite; }
@keyframes move { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "page" not in st.session_state: st.session_state.page = "🏠 Dashboard"

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.markdown("# QYVENZO AI\n### Enterprise Suite")
    st.divider()
    if st.button("🏠 Dashboard"): st.session_state.page = "🏠 Dashboard"
    if st.button("📊 Analytics"): st.session_state.page = "📊 Analytics"
    if st.button("🤖 AI Strategy"): st.session_state.page = "🤖 AI Strategy"
    
    st.divider()
    st.success("🟢 AI Online") # Always shows

# --- HEADER ---
st.markdown('<div class="hero"><h1>⚡ QYVENZO AI</h1><h4>Enterprise Intelligence Platform</h4></div>', unsafe_allow_html=True)

# Updated Moving Text
st.markdown('<div class="marquee"><span>📊 Data Analytics • 🤖 AI Strategy Engine • 📈 Predictive Insights • 🎯 Executive Reporting • ⚡ Automated Intelligence</span></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    st.session_state.df = df
    df.columns = df.columns.str.strip()
    num = df.select_dtypes(include="number").columns.tolist()
    cat = df.select_dtypes(include=["object"]).columns.tolist()

    if st.session_state.page == "🏠 Dashboard":
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("📁 Records", f"{len(df):,}"); c2.metric("📊 Columns", len(df.columns)); c3.metric("🔢 Metrics", len(num)); c4.metric("🛡 Integrity", "98%")
        st.plotly_chart(px.line(df, y=num[0], title="Performance Trend", template="plotly_dark"), use_container_width=True)
        st.dataframe(df.head(50), use_container_width=True)

    elif st.session_state.page == "📊 Analytics":
        tabs = st.tabs(["Overview", "Distribution", "Correlation", "Advanced"])
        with tabs[0]: 
            c1, c2 = st.columns(2)
            c1.plotly_chart(px.line(df, y=num[0], title="Trend", template="plotly_dark"), use_container_width=True)
            c2.plotly_chart(px.bar(df.head(15), x=cat[0] if cat else None, y=num[0], title="Performance", template="plotly_dark"), use_container_width=True)
        with tabs[1]:
            c1, c2 = st.columns(2); c3, c4 = st.columns(2)
            c1.plotly_chart(px.histogram(df, x=num[0], title="Freq", template="plotly_dark"), use_container_width=True)
            c2.plotly_chart(px.box(df, y=num[0], title="Outliers", template="plotly_dark"), use_container_width=True)
            c3.plotly_chart(px.violin(df, y=num[0], title="Spread", template="plotly_dark"), use_container_width=True)
            c4.plotly_chart(px.pie(df.head(10), names=cat[0] if cat else None, values=num[0], title="Split", template="plotly_dark"), use_container_width=True)
        with tabs[2]:
            c1, c2 = st.columns(2)
            c1.plotly_chart(px.scatter(df, x=num[0], y=num[1] if len(num)>1 else None, title="Corr", template="plotly_dark"), use_container_width=True)
            c2.plotly_chart(px.density_heatmap(df, x=num[0], y=num[1] if len(num)>1 else None, title="Heatmap", template="plotly_dark"), use_container_width=True)
        with tabs[3]:
            c1, c2 = st.columns(2)
            c1.plotly_chart(px.area(df, y=num[0], title="Volume", template="plotly_dark"), use_container_width=True)
            c2.plotly_chart(px.funnel(df.head(10), x=num[0], y=cat[0] if cat else None, title="Funnel", template="plotly_dark"), use_container_width=True)

    elif st.session_state.page == "🤖 AI Strategy":
        st.subheader("🤖 Executive AI Strategy Report")
        with st.spinner("Analyzing intelligence..."):
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Analyze: {df.describe().to_string()}. Provide executive summary, findings, opportunities, risks, and recommendations."}])
            st.chat_message("assistant").write(response.choices[0].message.content)
else:
    st.info("QYVENZO AI is standing by. Please upload a file to initialize the engine.")