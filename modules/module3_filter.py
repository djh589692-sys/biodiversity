import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data.region_data import SPECIES_DB, STATUS_COLOR_HEX, STATUS_LABEL, STATUS_ORDER


# 用拉丁学名从 iNaturalist 获取图片
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


def render_filter():
    st.title("🔍 物种筛选 & 探索")

    # ── 页面内筛选区（不用 sidebar，避免遮住导航）────────────
    with st.container(border=True):
        st.markdown("**筛选条件**")
        row1_c1, row1_c2 = st.columns([2, 2])
        with row1_c1:
            search = st.text_input("搜索物种名称或分布地", placeholder="例如：虎、巴西...", label_visibility="visible")
        with row1_c2:
            type_opts = ["全部"] + sorted(SPECIES_DB["类型"].unique().tolist())
            type_sel = st.selectbox("物种类型", type_opts)

        row2_c1, row2_c2, row2_c3 = st.columns(3)
        with row2_c1:
            status_map = {"全部": "全部", "CR 极危": "CR", "EN 濒危": "EN", "VU 易危": "VU", "NT 近危": "NT", "LC 无危": "LC"}
            status_sel_label = st.selectbox("濒危等级", list(status_map.keys()))
            status_sel = status_map[status_sel_label]
        with row2_c2:
            region_opts = ["全部"] + sorted(SPECIES_DB["地区"].unique().tolist())
            region_sel = st.selectbox("地区", region_opts)
        with row2_c3:
            threat_opts = ["全部"] + sorted(SPECIES_DB["威胁"].unique().tolist())
            threat_sel = st.selectbox("主要威胁", threat_opts)

        sort_row_c1, sort_row_c2 = st.columns([2, 2])
        with sort_row_c1:
            sort_by = st.radio("排序方式", ["名称", "濒危程度", "地区"], horizontal=True)
        with sort_row_c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("重置所有筛选", use_container_width=False):
                st.rerun()

    # ── 过滤逻辑 ───────────────────────────────────────
    df = SPECIES_DB.copy()
    if search:
        mask = df["名称"].str.contains(search, na=False) | df["分布"].str.contains(search, na=False)
        df = df[mask]
    if type_sel != "全部":
        df = df[df["类型"] == type_sel]
    if status_sel != "全部":
        df = df[df["等级"] == status_sel]
    if region_sel != "全部":
        df = df[df["地区"] == region_sel]
    if threat_sel != "全部":
        df = df[df["威胁"] == threat_sel]

    if sort_by == "名称":
        df = df.sort_values("名称")
    elif sort_by == "濒危程度":
        df = df.copy()
        df["_rank"] = df["等级"].map(STATUS_ORDER)
        df = df.sort_values("_rank").drop(columns=["_rank"])
    elif sort_by == "地区":
        df = df.sort_values("地区")

    # ── 结果展示 ───────────────────────────────────────
    st.markdown(f"共找到 **{len(df)}** 种物种")
    st.markdown("---")

    if df.empty:
        st.info("没有符合条件的物种，请调整筛选条件。")
        return

    cols = st.columns(3)
    for i, (_, row) in enumerate(df.iterrows()):
        status = row["等级"]
        color = STATUS_COLOR_HEX.get(status, "#888")
        label = STATUS_LABEL.get(status, status)
        with cols[i % 3]:
            # 直接显示物种图片
            latin_name = row.get("拉丁名", "")
            img_url = get_species_image(latin_name) if latin_name else None
            
            if img_url:
                st.image(img_url, use_container_width=True)
            else:
                st.markdown(
                    '<div style="height:120px;background:#f0f0e8;border-radius:8px;display:flex;'
                    'align-items:center;justify-content:center;color:#aaa;font-size:12px;">暂无图片</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"""<div style="border:0.5px solid #e0e0d8;border-radius:10px;padding:12px;margin-top:5px;margin-bottom:15px;background:#fff;">
                <p style="font-size:15px;font-weight:500;margin:0 0 6px;color:#1a2a1a;">{row['名称']}</p>
                <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:5px;">
                  <span style="font-size:11px;padding:2px 7px;border-radius:4px;background:{color}22;color:{color};">{label} ({status})</span>
                  <span style="font-size:11px;padding:2px 7px;border-radius:4px;background:#f0f0e8;color:#555;">{row['类型']}</span>
                  <span style="font-size:11px;padding:2px 7px;border-radius:4px;background:#f0f0e8;color:#555;">{row['地区']}</span>
                </div>
                <p style="font-size:11px;color:#aaa;margin:0;">📍 {row['分布']}</p>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("**完整数据表**")
    st.dataframe(
        df[["名称", "类型", "等级", "地区", "威胁", "分布"]],
        use_container_width=True,
        hide_index=True,
    )
