import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data.region_data import REGION_DB, STATUS_COLOR_HEX, STATUS_LABEL

MAP_DATA = pd.DataFrame([
    {"country":"Brazil",             "name":"巴西",           "score":95,"species_num":116000,"endemic_pct":43,"endangered_num":1173,"protected_pct":29.4,"biome":"热带雨林","rep":"美洲豹、金刚鹦鹉、巨嘴鸟","rep_latin":"Panthera onca, Ara ararauna, Ramphastos toco"},
    {"country":"Indonesia",          "name":"印度尼西亚",     "score":92,"species_num":28000, "endemic_pct":39,"endangered_num":920, "protected_pct":21.8,"biome":"热带雨林/珊瑚礁","rep":"苏门答腊虎、红毛猩猩、科莫多龙","rep_latin":"Panthera tigris sumatrae, Pongo pygmaeus, Varanus komodoensis"},
    {"country":"Madagascar",         "name":"马达加斯加",     "score":93,"species_num":25000, "endemic_pct":92,"endangered_num":701, "protected_pct":10.5,"biome":"热带干燥森林","rep":"环尾狐猴、变色龙、指猴","rep_latin":"Lemur catta, Furcifer pardalis, Daubentonia madagascariensis"},
    {"country":"Colombia",           "name":"哥伦比亚",       "score":90,"species_num":56000, "endemic_pct":28,"endangered_num":678, "protected_pct":14.2,"biome":"安第斯山/雨林","rep":"眼镜熊、毒箭蛙、安第斯神鹰","rep_latin":"Tremarctos ornatus, Dendrobates tinctorius, Vultur gryphus"},
    {"country":"Australia",          "name":"澳大利亚",       "score":85,"species_num":166000,"endemic_pct":84,"endangered_num":511, "protected_pct":19.4,"biome":"干旱地带/珊瑚礁","rep":"考拉、鸭嘴兽、塔斯马尼亚魔鬼","rep_latin":"Phascolarctos cinereus, Ornithorhynchus anatinus, Sarcophilus harrisii"},
    {"country":"Peru",               "name":"秘鲁",           "score":87,"species_num":25000, "endemic_pct":27,"endangered_num":422, "protected_pct":17.3,"biome":"亚马逊/安第斯山","rep":"安第斯神鹰、美洲狮、亚马逊河豚","rep_latin":"Vultur gryphus, Puma concolor, Inia geoffrensis"},
    {"country":"Mexico",             "name":"墨西哥",         "score":82,"species_num":64000, "endemic_pct":52,"endangered_num":556, "protected_pct":11.6,"biome":"热带森林/沙漠","rep":"美洲豹、粉红火烈鸟、墨西哥钝口螈","rep_latin":"Panthera onca, Phoenicopterus roseus, Ambystoma mexicanum"},
    {"country":"Papua New Guinea",   "name":"巴布亚新几内亚", "score":89,"species_num":20000, "endemic_pct":55,"endangered_num":256, "protected_pct":3.6, "biome":"热带雨林","rep":"极乐鸟、树袋鼠、天堂翠鸟","rep_latin":"Paradisaea apoda, Dendrolagus goodfellowi, Tanysiptera sylvia"},
    {"country":"India",              "name":"印度",           "score":78,"species_num":91000, "endemic_pct":33,"endangered_num":683, "protected_pct":5.0, "biome":"热带森林/草原","rep":"孟加拉虎、亚洲象、印度犀牛","rep_latin":"Panthera tigris tigris, Elephas maximus, Rhinoceros unicornis"},
    {"country":"China",              "name":"中国",           "score":72,"species_num":34000, "endemic_pct":19,"endangered_num":812, "protected_pct":18.0,"biome":"温带森林/高原","rep":"大熊猫、金丝猴、扬子鳄","rep_latin":"Ailuropoda melanoleuca, Rhinopithecus roxellana, Alligator sinensis"},
    {"country":"South Africa",       "name":"南非",           "score":76,"species_num":95000, "endemic_pct":67,"endangered_num":567, "protected_pct":8.1, "biome":"开普植物区","rep":"非洲象、猎豹、开普企鹅","rep_latin":"Loxodonta africana, Acinonyx jubatus, Spheniscus demersus"},
    {"country":"Kenya",              "name":"肯尼亚",         "score":73,"species_num":35000, "endemic_pct":15,"endangered_num":345, "protected_pct":12.4,"biome":"稀树草原","rep":"非洲象、狮子、长颈鹿","rep_latin":"Loxodonta africana, Panthera leo, Giraffa camelopardalis"},
    {"country":"Democratic Republic of the Congo","name":"刚果民主共和国","score":88,"species_num":10000,"endemic_pct":31,"endangered_num":433,"protected_pct":10.5,"biome":"热带雨林","rep":"山地大猩猩、倭黑猩猩、奥卡皮鹿","rep_latin":"Gorilla beringei, Pan paniscus, Okapia johnstoni"},
    {"country":"Japan",              "name":"日本",           "score":70,"species_num":90000, "endemic_pct":41,"endangered_num":312, "protected_pct":20.5,"biome":"温带森林","rep":"日本猕猴、朱鹮、儒艮","rep_latin":"Macaca fuscata, Nipponia nippon, Dugong dugon"},
    {"country":"United States of America","name":"美国",      "score":65,"species_num":432000,"endemic_pct":29,"endangered_num":1341,"protected_pct":12.0,"biome":"温带/草原/沙漠","rep":"美洲野牛、秃鹰、加州神鹫","rep_latin":"Bison bison, Haliaeetus leucocephalus, Gymnogyps californianus"},
    {"country":"Germany",            "name":"德国",           "score":58,"species_num":72000, "endemic_pct":6, "endangered_num":812, "protected_pct":38.2,"biome":"温带落叶林","rep":"欧亚猞猁、白尾海雕、欧洲野牛","rep_latin":"Lynx lynx, Haliaeetus albicilla, Bison bonasus"},
    {"country":"Canada",             "name":"加拿大",         "score":55,"species_num":140000,"endemic_pct":8, "endangered_num":567, "protected_pct":12.5,"biome":"北方针叶林","rep":"北极熊、驯鹿、美洲貂","rep_latin":"Ursus maritimus, Rangifer tarandus, Martes americana"},
    {"country":"Russia",             "name":"俄罗斯",         "score":48,"species_num":22000, "endemic_pct":6, "endangered_num":423, "protected_pct":11.4,"biome":"泰加林/苔原","rep":"西伯利亚虎、雪豹、北极熊","rep_latin":"Panthera tigris altaica, Panthera uncia, Ursus maritimus"},
    {"country":"Norway",             "name":"挪威",           "score":38,"species_num":44000, "endemic_pct":2, "endangered_num":89,  "protected_pct":17.1,"biome":"北极/峡湾","rep":"驯鹿、北极狐、麝牛","rep_latin":"Rangifer tarandus, Vulpes lagopus, Ovibos moschatus"},
    {"country":"Venezuela",          "name":"委内瑞拉",       "score":84,"species_num":21000, "endemic_pct":23,"endangered_num":312, "protected_pct":53.9,"biome":"热带雨林/大草原","rep":"美洲鳄、大食蚁兽、鹦鹉","rep_latin":"Crocodylus intermedius, Myrmecophaga tridactyla, Amazona ochrocephala"},
    {"country":"Ecuador",            "name":"厄瓜多尔",       "score":86,"species_num":17000, "endemic_pct":30,"endangered_num":298, "protected_pct":19.4,"biome":"热带雨林/加拉帕戈斯","rep":"加拉帕戈斯象龟、海鬣蜥、蓝脚鲣鸟","rep_latin":"Chelonoidis nigra, Amblyrhynchus cristatus, Sula nebouxii"},
    {"country":"Bolivia",            "name":"玻利维亚",       "score":80,"species_num":17000, "endemic_pct":22,"endangered_num":204, "protected_pct":22.0,"biome":"热带雨林/高原草甸","rep":"眼镜熊、美洲豹、安第斯火烈鸟","rep_latin":"Tremarctos ornatus, Panthera onca, Phoenicoparrus andinus"},
    {"country":"Tanzania",           "name":"坦桑尼亚",       "score":75,"species_num":14000, "endemic_pct":19,"endangered_num":288, "protected_pct":38.0,"biome":"稀树草原/高山","rep":"非洲象、狮子、山地大猩猩","rep_latin":"Loxodonta africana, Panthera leo, Gorilla beringei"},
    {"country":"Cameroon",           "name":"喀麦隆",         "score":79,"species_num":9000,  "endemic_pct":16,"endangered_num":198, "protected_pct":18.3,"biome":"热带雨林/草原","rep":"西部大猩猩、非洲象、黑猩猩","rep_latin":"Gorilla gorilla, Loxodonta africana, Pan troglodytes"},
    {"country":"Myanmar",            "name":"缅甸",           "score":74,"species_num":12000, "endemic_pct":25,"endangered_num":321, "protected_pct":6.4, "biome":"热带雨林/红树林","rep":"印支虎、亚洲象、绿孔雀","rep_latin":"Panthera tigris corbetti, Elephas maximus, Pavo muticus"},
    {"country":"Philippines",        "name":"菲律宾",         "score":83,"species_num":13500, "endemic_pct":65,"endangered_num":389, "protected_pct":7.8, "biome":"热带雨林/珊瑚礁","rep":"菲律宾鹰、眼镜猴、儒艮","rep_latin":"Pithecophaga jefferyi, Tarsius syrichta, Dugong dugon"},
    {"country":"Malaysia",           "name":"马来西亚",       "score":81,"species_num":15000, "endemic_pct":34,"endangered_num":445, "protected_pct":18.3,"biome":"热带雨林/红树林","rep":"马来虎、长鼻猴、马来貘","rep_latin":"Panthera tigris jacksoni, Nasalis larvatus, Tapirus indicus"},
    {"country":"Ethiopia",           "name":"埃塞俄比亚",     "score":69,"species_num":6500,  "endemic_pct":29,"endangered_num":176, "protected_pct":14.9,"biome":"高地草甸/热带森林","rep":"山地猩猩、非洲野驴、格雷维斑马","rep_latin":"Gorilla beringei, Equus africanus, Equus grevyi"},
    {"country":"Argentina",          "name":"阿根廷",         "score":71,"species_num":9400,  "endemic_pct":18,"endangered_num":224, "protected_pct":6.8, "biome":"潘帕斯草原/巴塔哥尼亚","rep":"美洲鸵、美洲狮、南美海狮","rep_latin":"Rhea americana, Puma concolor, Otaria flavescens"},
    {"country":"Thailand",           "name":"泰国",           "score":72,"species_num":10500, "endemic_pct":20,"endangered_num":259, "protected_pct":19.7,"biome":"热带雨林/红树林","rep":"印支虎、亚洲象、马来熊","rep_latin":"Panthera tigris corbetti, Elephas maximus, Helarctos malayanus"},
    {"country":"Vietnam",            "name":"越南",           "score":71,"species_num":13000, "endemic_pct":25,"endangered_num":289, "protected_pct":6.4, "biome":"热带雨林/珊瑚礁","rep":"越南豹猫、白臀叶猴、湾鳄","rep_latin":"Prionailurus bengalensis, Pygathrix nemaeus, Crocodylus porosus"},
    {"country":"Cambodia",           "name":"柬埔寨",         "score":65,"species_num":7000,  "endemic_pct":12,"endangered_num":155, "protected_pct":25.0,"biome":"热带雨林/湿地","rep":"印支虎、亚洲象、伊洛瓦底江海豚","rep_latin":"Panthera tigris corbetti, Elephas maximus, Orcaella brevirostris"},
    {"country":"New Zealand",        "name":"新西兰",         "score":68,"species_num":80000, "endemic_pct":80,"endangered_num":183, "protected_pct":30.1,"biome":"温带雨林/草地","rep":"几维鸟、毛利鹦鹉、白鳍豚","rep_latin":"Apteryx australis, Nestor meridionalis, Cephalorhynchus hectori"},
    {"country":"Congo",              "name":"刚果共和国",     "score":77,"species_num":7000,  "endemic_pct":14,"endangered_num":162, "protected_pct":8.5, "biome":"热带雨林","rep":"西部大猩猩、森林象、黑猩猩","rep_latin":"Gorilla gorilla, Loxodonta cyclotis, Pan troglodytes"},
    {"country":"Gabon",              "name":"加蓬",           "score":82,"species_num":8000,  "endemic_pct":20,"endangered_num":134, "protected_pct":22.0,"biome":"热带雨林","rep":"西部大猩猩、非洲森象、海牛","rep_latin":"Gorilla gorilla, Loxodonta cyclotis, Trichechus senegalensis"},
    {"country":"Mozambique",         "name":"莫桑比克",       "score":66,"species_num":5500,  "endemic_pct":8, "endangered_num":121, "protected_pct":15.5,"biome":"稀树草原/珊瑚礁","rep":"非洲象、狮子、儒艮","rep_latin":"Loxodonta africana, Panthera leo, Dugong dugon"},
    {"country":"Zambia",             "name":"赞比亚",         "score":64,"species_num":5800,  "endemic_pct":7, "endangered_num":98,  "protected_pct":31.7,"biome":"稀树草原/湿地","rep":"非洲象、尼罗鳄、鱼鹰","rep_latin":"Loxodonta africana, Crocodylus niloticus, Haliaeetus vocifer"},
    {"country":"Zimbabwe",           "name":"津巴布韦",       "score":63,"species_num":5300,  "endemic_pct":6, "endangered_num":109, "protected_pct":13.0,"biome":"稀树草原","rep":"非洲象、黑犀牛、猎豹","rep_latin":"Loxodonta africana, Diceros bicornis, Acinonyx jubatus"},
    {"country":"Botswana",           "name":"博茨瓦纳",       "score":61,"species_num":4500,  "endemic_pct":5, "endangered_num":78,  "protected_pct":17.0,"biome":"半干旱草原/湿地","rep":"非洲象、狮子、野犬","rep_latin":"Loxodonta africana, Panthera leo, Lycaon pictus"},
    {"country":"Angola",             "name":"安哥拉",         "score":67,"species_num":6200,  "endemic_pct":11,"endangered_num":143, "protected_pct":12.4,"biome":"热带雨林/稀树草原","rep":"非洲象、黑白犀牛、鸵鸟","rep_latin":"Loxodonta africana, Diceros bicornis, Struthio camelus"},
    {"country":"Namibia",            "name":"纳米比亚",       "score":60,"species_num":4200,  "endemic_pct":14,"endangered_num":88,  "protected_pct":17.1,"biome":"沙漠/半干旱草原","rep":"猎豹、非洲象、黑犀牛","rep_latin":"Acinonyx jubatus, Loxodonta africana, Diceros bicornis"},
    {"country":"France",             "name":"法国",           "score":52,"species_num":40000, "endemic_pct":4, "endangered_num":189, "protected_pct":26.0,"biome":"温带森林/地中海","rep":"狼、棕熊、欧洲野牛","rep_latin":"Canis lupus, Ursus arctos, Bison bonasus"},
    {"country":"Spain",              "name":"西班牙",         "score":56,"species_num":57000, "endemic_pct":10,"endangered_num":267, "protected_pct":27.4,"biome":"地中海/温带森林","rep":"伊比利亚猞猁、棕熊、西班牙帝雕","rep_latin":"Lynx pardinus, Ursus arctos, Aquila adalberti"},
    {"country":"Italy",              "name":"意大利",         "score":54,"species_num":58000, "endemic_pct":5, "endangered_num":198, "protected_pct":21.5,"biome":"地中海/温带森林","rep":"地中海僧侣海豹、棕熊、欧洲貂","rep_latin":"Monachus monachus, Ursus arctos, Martes martes"},
    {"country":"Sweden",             "name":"瑞典",           "score":42,"species_num":30000, "endemic_pct":2, "endangered_num":71,  "protected_pct":13.8,"biome":"北方针叶林","rep":"驼鹿、欧洲狼、棕熊","rep_latin":"Alces alces, Canis lupus, Ursus arctos"},
    {"country":"Finland",            "name":"芬兰",           "score":40,"species_num":45000, "endemic_pct":2, "endangered_num":67,  "protected_pct":13.4,"biome":"北方针叶林/苔原","rep":"棕熊、驼鹿、白尾海雕","rep_latin":"Ursus arctos, Alces alces, Haliaeetus albicilla"},
    {"country":"Poland",             "name":"波兰",           "score":50,"species_num":33000, "endemic_pct":2, "endangered_num":98,  "protected_pct":19.6,"biome":"温带混合林","rep":"欧洲野牛、狼、猞猁","rep_latin":"Bison bonasus, Canis lupus, Lynx lynx"},
    {"country":"Ukraine",            "name":"乌克兰",         "score":49,"species_num":25000, "endemic_pct":3, "endangered_num":88,  "protected_pct":6.5, "biome":"草原/温带森林","rep":"欧洲野牛、狼、棕熊","rep_latin":"Bison bonasus, Canis lupus, Ursus arctos"},
    {"country":"Kazakhstan",         "name":"哈萨克斯坦",     "score":44,"species_num":12000, "endemic_pct":5, "endangered_num":78,  "protected_pct":2.5, "biome":"草原/半荒漠","rep":"雪豹、蒙古野驴、赛加羚羊","rep_latin":"Panthera uncia, Equus hemionus, Saiga tatarica"},
    {"country":"Mongolia",           "name":"蒙古国",         "score":46,"species_num":5000,  "endemic_pct":3, "endangered_num":54,  "protected_pct":17.4,"biome":"草原/戈壁沙漠","rep":"雪豹、野双峰驼、普氏野马","rep_latin":"Panthera uncia, Camelus ferus, Equus przewalskii"},
    {"country":"Iran",               "name":"伊朗",           "score":57,"species_num":8000,  "endemic_pct":11,"endangered_num":122, "protected_pct":7.6, "biome":"山地/半干旱草原","rep":"亚洲猎豹、波斯豹、亚洲狮","rep_latin":"Acinonyx jubatus venaticus, Panthera pardus saxicolor, Panthera leo persica"},
    {"country":"Turkey",             "name":"土耳其",         "score":60,"species_num":11000, "endemic_pct":30,"endangered_num":156, "protected_pct":1.1, "biome":"地中海/温带森林","rep":"安纳托利亚豹、棕熊、地中海僧侣海豹","rep_latin":"Panthera pardus tulliana, Ursus arctos, Monachus monachus"},
    {"country":"Morocco",            "name":"摩洛哥",         "score":53,"species_num":7000,  "endemic_pct":15,"endangered_num":98,  "protected_pct":1.6, "biome":"地中海/半干旱","rep":"阿特拉斯狮、巴巴里猕猴、穿山甲","rep_latin":"Panthera leo leo, Macaca sylvanus, Manis temminckii"},
    {"country":"Algeria",            "name":"阿尔及利亚",     "score":47,"species_num":5000,  "endemic_pct":8, "endangered_num":76,  "protected_pct":6.0, "biome":"地中海/撒哈拉沙漠","rep":"撒哈拉猎豹、沙漠豪猪、弓角羚羊","rep_latin":"Acinonyx jubatus, Hystrix cristata, Addax nasomaculatus"},
    {"country":"Nigeria",            "name":"尼日利亚",       "score":68,"species_num":7500,  "endemic_pct":11,"endangered_num":167, "protected_pct":14.5,"biome":"热带雨林/草原","rep":"尼日利亚长颈鹿、黑猩猩、河马","rep_latin":"Giraffa camelopardalis, Pan troglodytes, Hippopotamus amphibius"},
    {"country":"Ghana",              "name":"加纳",           "score":65,"species_num":5200,  "endemic_pct":9, "endangered_num":134, "protected_pct":16.3,"biome":"热带雨林/草原","rep":"大象、黑猩猩、西非狮","rep_latin":"Loxodonta africana, Pan troglodytes, Panthera leo"},
    {"country":"Ivory Coast",        "name":"科特迪瓦",       "score":66,"species_num":5000,  "endemic_pct":8, "endangered_num":121, "protected_pct":22.4,"biome":"热带雨林","rep":"黑猩猩、西部大猩猩、非洲象","rep_latin":"Pan troglodytes, Gorilla gorilla, Loxodonta africana"},
    {"country":"Chile",              "name":"智利",           "score":62,"species_num":5100,  "endemic_pct":28,"endangered_num":121, "protected_pct":14.2,"biome":"地中海/温带雨林","rep":"南美洲骆马、美洲狮、Darwin狐","rep_latin":"Lama glama, Puma concolor, Lycalopex fulvipes"},
    {"country":"Paraguay",           "name":"巴拉圭",         "score":63,"species_num":7000,  "endemic_pct":8, "endangered_num":98,  "protected_pct":6.0, "biome":"热带/亚热带草原","rep":"大食蚁兽、美洲豹、大鸵鸟","rep_latin":"Myrmecophaga tridactyla, Panthera onca, Rhea americana"},
    {"country":"Uruguay",            "name":"乌拉圭",         "score":55,"species_num":3500,  "endemic_pct":4, "endangered_num":67,  "protected_pct":0.6, "biome":"潘帕斯草原","rep":"南美河狼、美洲鸵、南美海狮","rep_latin":"Chrysocyon brachyurus, Rhea americana, Otaria flavescens"},
    {"country":"United Kingdom",     "name":"英国",           "score":45,"species_num":70000, "endemic_pct":1, "endangered_num":145, "protected_pct":28.0,"biome":"温带海洋性草原","rep":"红松鼠、水獭、金雕","rep_latin":"Sciurus vulgaris, Lutra lutra, Aquila chrysaetos"},
    {"country":"Greece",             "name":"希腊",           "score":55,"species_num":23000, "endemic_pct":13,"endangered_num":167, "protected_pct":27.0,"biome":"地中海","rep":"地中海僧侣海豹、秃鹫、棕熊","rep_latin":"Monachus monachus, Gyps fulvus, Ursus arctos"},
    {"country":"Romania",            "name":"罗马尼亚",       "score":53,"species_num":33000, "endemic_pct":3, "endangered_num":98,  "protected_pct":23.7,"biome":"温带混合林/草原","rep":"棕熊、猞猁、欧洲野牛","rep_latin":"Ursus arctos, Lynx lynx, Bison bonasus"},
    {"country":"Belarus",            "name":"白俄罗斯",       "score":48,"species_num":12000, "endemic_pct":1, "endangered_num":65,  "protected_pct":7.9, "biome":"温带混合林/湿地","rep":"欧洲野牛、猞猁、狼","rep_latin":"Bison bonasus, Lynx lynx, Canis lupus"},
    {"country":"Pakistan",           "name":"巴基斯坦",       "score":55,"species_num":5000,  "endemic_pct":8, "endangered_num":109, "protected_pct":9.0, "biome":"山地/半干旱","rep":"雪豹、孟加拉虎、印度河海豚","rep_latin":"Panthera uncia, Panthera tigris tigris, Platanista gangetica"},
    {"country":"Nepal",              "name":"尼泊尔",         "score":64,"species_num":6000,  "endemic_pct":12,"endangered_num":134, "protected_pct":23.4,"biome":"喜马拉雅山地","rep":"雪豹、孟加拉虎、独角犀牛","rep_latin":"Panthera uncia, Panthera tigris tigris, Rhinoceros unicornis"},
    {"country":"Sri Lanka",          "name":"斯里兰卡",       "score":72,"species_num":4000,  "endemic_pct":55,"endangered_num":145, "protected_pct":26.9,"biome":"热带雨林/干旱区","rep":"斯里兰卡豹、亚洲象、紫脸叶猴","rep_latin":"Panthera pardus kotiya, Elephas maximus, Trachypithecus vetulus"},
    {"country":"Laos",               "name":"老挝",           "score":68,"species_num":8000,  "endemic_pct":18,"endangered_num":132, "protected_pct":16.5,"biome":"热带雨林","rep":"云豹、亚洲象、赤鹿","rep_latin":"Neofelis nebulosa, Elephas maximus, Cervus elaphus"},
])


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


def render_map():
    st.title("🗺️ 全球生物多样性热点地图")
    st.caption("点击选择国家查看详情，所有国家均可查看基本信息")

    if "selected_country" not in st.session_state:
        st.session_state.selected_country = None

    fig = px.choropleth(
        MAP_DATA,
        locations="country",
        locationmode="country names",
        color="score",
        hover_name="name",
        custom_data=["name", "species_num", "endemic_pct", "endangered_num", "protected_pct", "biome", "rep"],
        color_continuous_scale=[
            [0.0, "#EAF3DE"],
            [0.35, "#97C459"],
            [0.65, "#3B6D11"],
            [1.0, "#173404"],
        ],
        range_color=[30, 100],
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "🦋 已知物种：%{customdata[1]:,} 种<br>"
            "⚠️ 濒危物种：%{customdata[3]:,} 种<br>"
            "🌿 特有物种率：%{customdata[2]}%<br>"
            "🛡️ 保护区比例：%{customdata[4]}%<br>"
            "🌍 生态系统：%{customdata[5]}<br>"
            "🐾 代表物种：%{customdata[6]}<br>"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.5)",
            showland=True,
            landcolor="#e8ede0",
            showocean=True,
            oceancolor="#cce4f0",
            bgcolor="rgba(0,0,0,0)",
        ),
        coloraxis_colorbar=dict(
            title="多样性指数",
            tickvals=[30, 50, 70, 90, 100],
            ticktext=["低", "中低", "中", "高", "极高"],
            len=0.6,
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True, key="world_map")

    st.markdown("---")

    # 选国家 → 显示快速概览 + 跳转按钮
    all_names = ["（请选择国家）"] + sorted(MAP_DATA["name"].tolist())

    selected = st.selectbox("选择国家查看详情", all_names, index=0)

    if selected != "（请选择国家）":
        row = MAP_DATA[MAP_DATA["name"] == selected].iloc[0]
        st.markdown(f"### 📋 {row['name']} — 详细信息")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("多样性指数", row["score"])
        c2.metric("已知物种", f"{row['species_num']:,} 种")
        c3.metric("特有物种率", f"{row['endemic_pct']}%")
        c4.metric("濒危物种", f"{row['endangered_num']:,} 种")
        st.markdown(f"**主要生态系统：** {row['biome']}")
        st.markdown(f"**代表性物种：** {row['rep']}")
        st.markdown("---")

        # 所有国家都显示代表性物种图片（从 rep_latin 获取拉丁学名）
        st.markdown("**🐾 代表性物种（自动加载图片）**")
        rep_names = row['rep'].split('、')
        rep_latin_list = row.get('rep_latin', '').split(', ')
        
        cols = st.columns(3)
        for i, (name, latin) in enumerate(zip(rep_names, rep_latin_list)):
            if i >= 3:
                break
            with cols[i]:
                img_url = get_species_image(latin.strip()) if latin.strip() else None
                if img_url:
                    st.image(img_url, use_container_width=True)
                else:
                    st.markdown(
                        '<div style="height:120px;background:#f0f0e8;border-radius:8px;display:flex;'
                        'align-items:center;justify-content:center;color:#aaa;font-size:12px;">暂无图片</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f"""<div style="border:0.5px solid #e0e0d8;border-radius:10px;padding:10px;margin-top:5px;margin-bottom:15px;">
                    <p style="font-size:15px;font-weight:500;margin:0 0 2px;color:#1a2a1a;">{name}</p>
                    <p style="font-size:11px;color:#aaa;font-style:italic;margin:0;">{latin.strip()}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
        
        st.markdown("---")

        # 如果该国家在 REGION_DB 中有详细信息，则显示完整详情
        if selected in REGION_DB:
            d = REGION_DB[selected]
            
            # 四格指标
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("已知物种总数", d["total_species"])
            c2.metric("濒危物种数", f'{d["endangered"]} 种')
            c3.metric("特有物种率", f'{d["endemic_pct"]}%')
            c4.metric("保护区面积占比", f'{d["protected_pct"]}%')

            st.markdown("---")

            # 主要威胁指数（带图片）
            st.markdown("**⚠️ 主要威胁指数**")
            
            # 威胁类型对应的代表性物种拉丁学名（用于获取图片）
            threat_images = {
                "栖息地破坏": "Panthera onca",
                "偷猎": "Panthera tigris",
                "气候变化": "Ursus maritimus",
                "外来物种": "Spheniscus demersus",
                "过度捕捞": "Balaenoptera musculus",
                "水体污染": "Lutra lutra",
                "光污染": "Photinus pyralis",
                "非法贸易": "Manis temminckii",
                "开发破坏": "Rhizophora mangle",
            }
            
            for threat_name, val in d["threats"]:
                bar_color = "#E24B4A" if val >= 80 else "#EF9F27" if val >= 60 else "#97C459"
                threat_latin = threat_images.get(threat_name, "")
                threat_img_url = get_species_image(threat_latin) if threat_latin else None
                
                # 使用两列布局：左边图片，右边进度条
                threat_col1, threat_col2 = st.columns([1, 3])
                with threat_col1:
                    if threat_img_url:
                        st.image(threat_img_url, width=80)
                    else:
                        st.markdown(
                            '<div style="width:80px;height:60px;background:#f0f0e8;border-radius:8px;display:flex;'
                            'align-items:center;justify-content:center;color:#aaa;font-size:10px;">暂无图片</div>',
                            unsafe_allow_html=True,
                        )
                with threat_col2:
                    st.markdown(
                        f"""<div style="margin-bottom:5px;">
                        <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                            <span style="font-weight:500;">{threat_name}</span><span style="color:{bar_color};font-weight:500;">{val}%</span>
                        </div>
                        <div style="background:#f0f0e8;border-radius:3px;height:10px;">
                            <div style="width:{val}%;height:10px;border-radius:3px;background:{bar_color};"></div>
                        </div></div>""",
                        unsafe_allow_html=True,
                    )
        else:
            # 没有详细数据的国家也显示基本威胁信息（根据 biome 推断）
            st.markdown("**⚠️ 主要威胁评估**")
            biome = row['biome']
            
            # 根据生态系统推断主要威胁
            threat_estimates = []
            if "热带雨林" in biome:
                threat_estimates = [("栖息地破坏", 85), ("偷猎", 70), ("气候变化", 60)]
            elif "珊瑚礁" in biome:
                threat_estimates = [("气候变化", 90), ("水体污染", 75), ("过度捕捞", 65)]
            elif "草原" in biome or "稀树草原" in biome:
                threat_estimates = [("栖息地破坏", 75), ("偷猎", 60), ("气候变化", 55)]
            elif "沙漠" in biome or "半干旱" in biome:
                threat_estimates = [("气候变化", 80), ("栖息地破坏", 65), ("非法贸易", 50)]
            elif "温带" in biome or "森林" in biome:
                threat_estimates = [("栖息地破坏", 70), ("气候变化", 65), ("外来物种", 45)]
            elif "北极" in biome or "苔原" in biome:
                threat_estimates = [("气候变化", 95), ("栖息地破坏", 50), ("偷猎", 40)]
            elif "海洋" in biome:
                threat_estimates = [("过度捕捞", 85), ("气候变化", 80), ("水体污染", 70)]
            else:
                threat_estimates = [("栖息地破坏", 70), ("气候变化", 60), ("偷猎", 50)]
            
            threat_images = {
                "栖息地破坏": "Panthera onca",
                "偷猎": "Panthera tigris",
                "气候变化": "Ursus maritimus",
                "外来物种": "Spheniscus demersus",
                "过度捕捞": "Balaenoptera musculus",
                "水体污染": "Lutra lutra",
                "光污染": "Photinus pyralis",
                "非法贸易": "Manis temminckii",
                "开发破坏": "Rhizophora mangle",
            }
            
            for threat_name, val in threat_estimates:
                bar_color = "#E24B4A" if val >= 80 else "#EF9F27" if val >= 60 else "#97C459"
                threat_latin = threat_images.get(threat_name, "")
                threat_img_url = get_species_image(threat_latin) if threat_latin else None
                
                threat_col1, threat_col2 = st.columns([1, 3])
                with threat_col1:
                    if threat_img_url:
                        st.image(threat_img_url, width=80)
                    else:
                        st.markdown(
                            '<div style="width:80px;height:60px;background:#f0f0e8;border-radius:8px;display:flex;'
                            'align-items:center;justify-content:center;color:#aaa;font-size:10px;">暂无图片</div>',
                            unsafe_allow_html=True,
                        )
                with threat_col2:
                    st.markdown(
                        f"""<div style="margin-bottom:5px;">
                        <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
                            <span style="font-weight:500;">{threat_name}</span><span style="color:{bar_color};font-weight:500;">{val}%</span>
                        </div>
                        <div style="background:#f0f0e8;border-radius:3px;height:10px;">
                            <div style="width:{val}%;height:10px;border-radius:3px;background:{bar_color};"></div>
                        </div></div>""",
                        unsafe_allow_html=True,
                    )
            
            st.info(f"💡 以上威胁评估基于 {row['name']} 的主要生态系统 '{biome}' 推断，详细数据正在建设中。")

    st.markdown("---")
    st.subheader("全球多样性热点 Top 15")
    top = MAP_DATA.sort_values("score", ascending=False).head(15).reset_index(drop=True)
    top.index += 1
    st.dataframe(
        top[["name", "biome", "species_num", "endemic_pct", "endangered_num", "score", "rep"]].rename(columns={
            "name": "国家/地区", "biome": "主要生态系统",
            "species_num": "已知物种数", "endemic_pct": "特有物种率(%)",
            "endangered_num": "濒危物种数", "score": "多样性指数", "rep": "代表性物种",
        }),
        use_container_width=True,
        hide_index=False,
    )
