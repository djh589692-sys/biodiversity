import streamlit as st

st.set_page_config(
    page_title="全球生物多样性探索",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

from modules.module1_map import render_map
from modules.module3_filter import render_filter
from modules.module5_funfacts import render_funfacts
from modules.module6_ai_guide import render_ai_guide

st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #f8faf6; }
.block-container { padding-top: 1.5rem; }
.stMetric label { font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)

PAGES = [
    "🗺️ 世界多样性地图",
    " 🔍 筛选 & 探索",
    "💡 科普趣味卡片",
    "🤖 AI 讲解员",
]

# 支持从地图页跳转到详情页
if "current_page" in st.session_state:
    default_idx = PAGES.index(st.session_state["current_page"])
    del st.session_state["current_page"]
else:
    default_idx = 0

with st.sidebar:
    st.markdown("## 🌿 生物多样性探索")
    st.markdown("---")
    page = st.radio(
        "选择模块",
        PAGES,
        index=default_idx,
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("数据来源：GBIF · IUCN Red List · WWF")
    

if page == "🗺️ 世界多样性地图":
    render_map()
elif page == " 🔍 筛选 & 探索":
    render_filter()
elif page == "💡 科普趣味卡片":
    render_funfacts()
elif page == "🤖 AI 讲解员":
    render_ai_guide()
