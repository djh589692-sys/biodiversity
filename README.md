# 🌿 全球生物多样性探索

## 项目结构

```
biodiversity_app/
├── app.py                  # 主入口
├── requirements.txt
├── data/
│   └── region_data.py      # 共享数据（地区、物种数据库）
└── modules/
    ├── module1_map.py      # 世界多样性地图
    ├── module2_detail.py   # 地区详情面板
    ├── module3_filter.py   # 物种筛选 & 探索
    └── module5_funfacts.py # 科普趣味卡片
```

## 快速启动

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 功能模块

| 模块 | 功能说明 |
|------|----------|
| 世界多样性地图 | Plotly 全球地图，颜色热力图，点击查看国家数据 |
| 地区详情面板 | 下拉选择地区，展示 IUCN 等级饼图、类群柱状图、威胁指数 |
| 筛选 & 探索 | 侧边栏多维筛选，按类型/等级/地区/威胁过滤 30 种代表性物种 |
| 科普趣味卡片 | 冷知识、五题小测验（支持进度保存）、你知道吗 |

## 扩展建议

- 接入 GBIF API 替换静态数据（需要网络请求）
- 接入 iNaturalist API 加载真实物种图片
- 添加模块四：地区对比功能（两地并排对比）
- 部署到 Streamlit Community Cloud（免费）
