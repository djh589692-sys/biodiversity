import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data.region_data import REGION_DB, STATUS_COLOR_HEX, STATUS_LABEL

# 用拉丁学名从 iNaturalist 获取图片，显示中文名
def get_species_image(latin_name):
    try:
        url = f"https://api.inaturalist.org/v1/taxa/autocomplete?q={latin_name}&per_page=1"
        res = requests.get(url, timeout=5).json()
        if res.get("results"):
            photo = res["results"][0].get("default_photo", {})
            return photo.get("medium_url")
    except Exception:
        pass
    return None

def render_detail():
    st.title("📊 地区详情面板")

    # 支持从地图页跳转过来时自动选中地区
    default_region = st.session_state.pop("detail_region", list(REGION_DB.keys())[0])
    if default_region not in REGION_DB:
        default_region = list(REGION_DB.keys())[0]
    default_idx = list(REGION_DB.keys()).index(default_region)

    region_name = st.selectbox("选择地区", list(REGION_DB.keys()), index=default_idx)
    d = REGION_DB[region_name]

    # ── 基本信息 ───────────────────────────────────────
    st.markdown(f"**生态系统：** {d['biome']}")
    badge_color = "#27500A" if d["score"] >= 80 else "#633806" if d["score"] >= 60 else "#791F1F"
    st.markdown(
        f'<span style="background:#EAF3DE;color:{badge_color};padding:3px 12px;border-radius:20px;font-size:13px;">'
        f'{d["score_label"]}（多样性指数 {d["score"]}）</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    # ── 四格指标 ───────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("已知物种总数", d["total_species"])
    c2.metric("濒危物种数", f'{d["endangered"]} 种')
    c3.metric("特有物种率", f'{d["endemic_pct"]}%')
    c4.metric("保护区面积占比", f'{d["protected_pct"]}%')

    st.markdown("---")

    # ── 双图表 ─────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**濒危等级分布**")
        iucn = {k: v for k, v in d["iucn"].items() if v > 0}
        colors = ["#E24B4A", "#EF9F27", "#FAC775", "#97C459"]
        fig_iucn = go.Figure(go.Pie(
            labels=list(iucn.keys()),
            values=list(iucn.values()),
            hole=0.55,
            marker_colors=colors[:len(iucn)],
            textinfo="label+percent",
            textfont_size=12,
        ))
        fig_iucn.update_layout(
            showlegend=False, margin=dict(l=0, r=0, t=10, b=10),
            height=240, paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_iucn, use_container_width=True)

    with col_right:
        st.markdown("**物种类群分布**")
        taxa = d["taxa"]
        fig_taxa = px.bar(
            x=list(taxa.keys()), y=list(taxa.values()),
            color=list(taxa.keys()),
            color_discrete_sequence=["#5DCAA5", "#1D9E75", "#085041", "#9FE1CB"],
            labels={"x": "", "y": "物种数"},
        )
        fig_taxa.update_layout(
            showlegend=False, margin=dict(l=0, r=0, t=10, b=10),
            height=240, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        fig_taxa.update_yaxes(gridcolor="rgba(0,0,0,0.06)")
        st.plotly_chart(fig_taxa, use_container_width=True)

    st.markdown("---")

    # ── 代表性物种（含图片 + 中文名标注）──────────────────
    st.markdown("**代表性物种**")
    type_filter = st.radio(
        "按类型筛选", ["全部", "哺乳类", "鸟类", "爬行类"],
        horizontal=True, label_visibility="collapsed",
    )
    species_list = d["species"]
    if type_filter != "全部":
        species_list = [s for s in species_list if s["type"] == type_filter]

    load_images = st.toggle("加载物种图片（需要网络）", value=False)

    cols = st.columns(3)
    for i, s in enumerate(species_list):
        status = s["status"]
        label = STATUS_LABEL.get(status, status)
        color = STATUS_COLOR_HEX.get(status, "#888")
        with cols[i % 3]:
            if load_images:
                img_url = get_species_image(s["latin"])
                if img_url:
                    st.image(img_url, use_container_width=True)
                else:
                    st.markdown(
                        '<div style="height:80px;background:#f0f0e8;border-radius:8px;display:flex;'
                        'align-items:center;justify-content:center;color:#aaa;font-size:12px;">暂无图片</div>',
                        unsafe_allow_html=True,
                    )
            # 中文名（大字）+ 拉丁名（小字灰色）
            st.markdown(
                f"""<div style="border:0.5px solid #e0e0d8;border-radius:10px;padding:10px;margin-bottom:8px;">
                <p style="font-size:15px;font-weight:500;margin:0 0 2px;color:#1a2a1a;">{s['name']}</p>
                <p style="font-size:11px;color:#aaa;font-style:italic;margin:0 0 6px;">{s['latin']}</p>
                <span style="font-size:11px;padding:2px 8px;border-radius:4px;background:{color}22;color:{color};">{label} ({status})</span>
                <span style="font-size:11px;padding:2px 8px;border-radius:4px;background:#f0f0e8;color:#555;margin-left:4px;">{s['type']}</span>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── 威胁指数 ───────────────────────────────────────
    st.markdown("**主要威胁指数**")
    for threat_name, val in d["threats"]:
        bar_color = "#E24B4A" if val >= 80 else "#EF9F27" if val >= 60 else "#97C459"
        st.markdown(
            f"""<div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                <span>{threat_name}</span><span style="color:#888;">{val}%</span>
            </div>
            <div style="background:#f0f0e8;border-radius:3px;height:7px;">
                <div style="width:{val}%;height:7px;border-radius:3px;background:{bar_color};"></div>
            </div></div>""",
            unsafe_allow_html=True,
        )
