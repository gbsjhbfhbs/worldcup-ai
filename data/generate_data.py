"""生成 2026 世界杯完整数据 JSON（北京时间）
运行: D:/py/python.exe data/generate_data.py
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

# ============================================================
# 1. 48 支球队
# ============================================================
TEAMS = {
    "MEX": {"name":"墨西哥","name_en":"Mexico","fifa_rank":15,"elo_rating":1880,"confederation":"CONCACAF","group":"A","coach":"哈维尔·阿吉雷","key_players":["洛萨诺","希门尼斯","阿尔瓦雷斯","奥乔亚","埃雷拉"],"recent_form":["W","W","D","L","W"],"avg_goals":1.8,"avg_conceded":0.9,"world_cup_titles":0},
    "RSA": {"name":"南非","name_en":"South Africa","fifa_rank":58,"elo_rating":1610,"confederation":"CAF","group":"A","coach":"雨果·布鲁斯","key_players":["佩尔西·陶","莱尔·福斯特","莫科纳","威廉姆斯","兹瓦内"],"recent_form":["W","D","L","W","D"],"avg_goals":1.2,"avg_conceded":1.1,"world_cup_titles":0},
    "KOR": {"name":"韩国","name_en":"South Korea","fifa_rank":22,"elo_rating":1820,"confederation":"AFC","group":"A","coach":"洪明甫","key_players":["孙兴慜","金玟哉","李刚仁","黄喜灿","曹圭成"],"recent_form":["W","W","W","D","W"],"avg_goals":2.0,"avg_conceded":0.7,"world_cup_titles":0},
    "CZE": {"name":"捷克","name_en":"Czechia","fifa_rank":35,"elo_rating":1750,"confederation":"UEFA","group":"A","coach":"伊万·哈谢克","key_players":["希克","绍切克","库法尔","赫洛泽克","巴拉克"],"recent_form":["W","D","W","L","W"],"avg_goals":1.6,"avg_conceded":0.8,"world_cup_titles":0},
    "CAN": {"name":"加拿大","name_en":"Canada","fifa_rank":30,"elo_rating":1770,"confederation":"CONCACAF","group":"B","coach":"杰西·马什","key_players":["阿方索·戴维斯","乔纳森·戴维","拉林","布坎南","欧斯塔基奥"],"recent_form":["W","D","W","W","L"],"avg_goals":1.7,"avg_conceded":1.0,"world_cup_titles":0},
    "BIH": {"name":"波黑","name_en":"Bosnia and Herzegovina","fifa_rank":42,"elo_rating":1700,"confederation":"UEFA","group":"B","coach":"塞尔吉·巴尔巴雷兹","key_players":["哲科","皮亚尼奇","克鲁尼奇","德米罗维奇","科拉希纳茨"],"recent_form":["W","W","D","L","W"],"avg_goals":1.4,"avg_conceded":1.1,"world_cup_titles":0},
    "QAT": {"name":"卡塔尔","name_en":"Qatar","fifa_rank":48,"elo_rating":1650,"confederation":"AFC","group":"B","coach":"巴特·卡塞雷斯","key_players":["阿菲夫","阿里","海多斯","布迪亚夫","巴沙姆"],"recent_form":["W","W","D","W","L"],"avg_goals":1.5,"avg_conceded":1.2,"world_cup_titles":0},
    "SUI": {"name":"瑞士","name_en":"Switzerland","fifa_rank":14,"elo_rating":1900,"confederation":"UEFA","group":"B","coach":"穆拉特·雅金","key_players":["扎卡","阿坎吉","恩博洛","沙奇里","奥卡福"],"recent_form":["W","D","W","W","D"],"avg_goals":1.9,"avg_conceded":0.6,"world_cup_titles":0},
    "BRA": {"name":"巴西","name_en":"Brazil","fifa_rank":3,"elo_rating":2060,"confederation":"CONMEBOL","group":"C","coach":"多里瓦尔","key_players":["维尼修斯","罗德里戈","阿利松","马尔基尼奥斯","吉马良斯"],"recent_form":["W","W","W","L","W"],"avg_goals":2.3,"avg_conceded":0.7,"world_cup_titles":5},
    "MAR": {"name":"摩洛哥","name_en":"Morocco","fifa_rank":13,"elo_rating":1810,"confederation":"CAF","group":"C","coach":"雷格拉吉","key_players":["阿什拉夫","齐耶赫","恩内斯里","马兹拉维","阿姆拉巴特"],"recent_form":["W","D","W","W","D"],"avg_goals":1.5,"avg_conceded":0.7,"world_cup_titles":0},
    "HAI": {"name":"海地","name_en":"Haiti","fifa_rank":87,"elo_rating":1480,"confederation":"CONCACAF","group":"C","coach":"塞巴斯蒂安·米涅","key_players":["纳宗","皮埃罗","阿德","普吕尼耶","克里斯蒂安"],"recent_form":["D","W","L","L","W"],"avg_goals":1.0,"avg_conceded":1.6,"world_cup_titles":0},
    "SCO": {"name":"苏格兰","name_en":"Scotland","fifa_rank":28,"elo_rating":1780,"confederation":"UEFA","group":"C","coach":"史蒂夫·克拉克","key_players":["罗伯逊","麦克托米奈","蒂尔尼","麦金","亚当斯"],"recent_form":["W","W","D","W","L"],"avg_goals":1.6,"avg_conceded":0.9,"world_cup_titles":0},
    "USA": {"name":"美国","name_en":"United States","fifa_rank":12,"elo_rating":1860,"confederation":"CONCACAF","group":"D","coach":"波切蒂诺","key_players":["普利西奇","麦肯尼","雷纳","巴洛贡","罗宾逊"],"recent_form":["W","W","W","D","W"],"avg_goals":2.0,"avg_conceded":0.6,"world_cup_titles":0},
    "PAR": {"name":"巴拉圭","name_en":"Paraguay","fifa_rank":52,"elo_rating":1660,"confederation":"CONMEBOL","group":"D","coach":"吉列尔莫·巴罗斯","key_players":["阿尔米隆","恩西索","桑纳夫里亚","戈麦斯","阿尔德雷特"],"recent_form":["D","L","W","D","W"],"avg_goals":1.1,"avg_conceded":1.2,"world_cup_titles":0},
    "AUS": {"name":"澳大利亚","name_en":"Australia","fifa_rank":24,"elo_rating":1790,"confederation":"AFC","group":"D","coach":"格雷厄姆·阿诺德","key_players":["苏塔尔","古德温","杜克","莱基","欧文"],"recent_form":["W","W","L","W","D"],"avg_goals":1.7,"avg_conceded":0.9,"world_cup_titles":0},
    "TUR": {"name":"土耳其","name_en":"Turkiye","fifa_rank":32,"elo_rating":1760,"confederation":"UEFA","group":"D","coach":"温琴佐·蒙特拉","key_players":["恰尔汗奥卢","居莱尔","伊尔马兹","德米拉尔","切利克"],"recent_form":["W","W","W","L","W"],"avg_goals":1.9,"avg_conceded":0.8,"world_cup_titles":0},
    "GER": {"name":"德国","name_en":"Germany","fifa_rank":11,"elo_rating":1940,"confederation":"UEFA","group":"E","coach":"纳格尔斯曼","key_players":["穆夏拉","维尔茨","基米希","哈弗茨","吕迪格"],"recent_form":["W","W","W","D","W"],"avg_goals":2.0,"avg_conceded":0.8,"world_cup_titles":4},
    "CUW": {"name":"库拉索","name_en":"Curacao","fifa_rank":91,"elo_rating":1420,"confederation":"CONCACAF","group":"E","coach":"迪克·阿德沃卡特","key_players":["巴库纳","容","范埃维克","霍伊","安东尼"],"recent_form":["W","D","L","W","L"],"avg_goals":1.0,"avg_conceded":1.5,"world_cup_titles":0},
    "CIV": {"name":"科特迪瓦","name_en":"Cote d'Ivoire","fifa_rank":38,"elo_rating":1730,"confederation":"CAF","group":"E","coach":"埃默斯·法埃","key_players":["阿莱","凯西","佩佩","福法纳","迪奥曼德"],"recent_form":["W","W","W","D","W"],"avg_goals":1.6,"avg_conceded":0.8,"world_cup_titles":0},
    "ECU": {"name":"厄瓜多尔","name_en":"Ecuador","fifa_rank":31,"elo_rating":1760,"confederation":"CONMEBOL","group":"E","coach":"塞巴斯蒂安·贝卡塞斯","key_players":["凯塞多","恩纳·瓦伦西亚","埃斯图皮尼安","因卡皮耶","派斯"],"recent_form":["W","D","W","W","L"],"avg_goals":1.5,"avg_conceded":0.8,"world_cup_titles":0},
    "NED": {"name":"荷兰","name_en":"Netherlands","fifa_rank":7,"elo_rating":2000,"confederation":"UEFA","group":"F","coach":"罗纳德·科曼","key_players":["范戴克","加克波","德容","西蒙斯","阿克"],"recent_form":["W","W","W","D","W"],"avg_goals":2.3,"avg_conceded":0.5,"world_cup_titles":0},
    "JPN": {"name":"日本","name_en":"Japan","fifa_rank":16,"elo_rating":1830,"confederation":"AFC","group":"F","coach":"森保一","key_players":["三笘薫","久保建英","远藤航","富安健洋","堂安律"],"recent_form":["W","W","W","W","L"],"avg_goals":1.9,"avg_conceded":0.6,"world_cup_titles":0},
    "SWE": {"name":"瑞典","name_en":"Sweden","fifa_rank":26,"elo_rating":1800,"confederation":"UEFA","group":"F","coach":"容·达尔·托马森","key_players":["伊萨克","库卢塞夫斯基","埃兰加","林德洛夫","福斯贝里"],"recent_form":["W","W","L","W","D"],"avg_goals":1.8,"avg_conceded":0.7,"world_cup_titles":0},
    "TUN": {"name":"突尼斯","name_en":"Tunisia","fifa_rank":41,"elo_rating":1690,"confederation":"CAF","group":"F","coach":"蒙特塞·卢比斯","key_players":["姆萨克尼","斯里蒂","莱杜尼","塔尔比","杰巴利"],"recent_form":["W","D","W","L","W"],"avg_goals":1.2,"avg_conceded":1.0,"world_cup_titles":0},
    "BEL": {"name":"比利时","name_en":"Belgium","fifa_rank":5,"elo_rating":1980,"confederation":"UEFA","group":"G","coach":"多梅尼科·特德斯科","key_players":["德布劳内","卢卡库","多库","奥纳纳","特罗萨德"],"recent_form":["W","W","D","W","W"],"avg_goals":2.2,"avg_conceded":0.5,"world_cup_titles":0},
    "EGY": {"name":"埃及","name_en":"Egypt","fifa_rank":33,"elo_rating":1740,"confederation":"CAF","group":"G","coach":"鲁伊·维多利亚","key_players":["萨拉赫","埃尔内尼","马尔穆什","特雷泽盖","赫加齐"],"recent_form":["W","W","W","D","W"],"avg_goals":1.8,"avg_conceded":0.7,"world_cup_titles":0},
    "IRN": {"name":"伊朗","name_en":"Iran","fifa_rank":20,"elo_rating":1840,"confederation":"AFC","group":"G","coach":"阿米尔·加莱诺埃","key_players":["塔雷米","阿兹蒙","贾汉巴赫什","戈利扎德","贝兰万德"],"recent_form":["W","W","W","W","D"],"avg_goals":2.1,"avg_conceded":0.5,"world_cup_titles":0},
    "NZL": {"name":"新西兰","name_en":"New Zealand","fifa_rank":94,"elo_rating":1510,"confederation":"OFC","group":"G","coach":"达伦·贝兹利","key_players":["伍德","卡卡塞","托马斯","辛格","博克索尔"],"recent_form":["W","W","D","W","L"],"avg_goals":1.4,"avg_conceded":1.0,"world_cup_titles":0},
    "ESP": {"name":"西班牙","name_en":"Spain","fifa_rank":8,"elo_rating":1990,"confederation":"UEFA","group":"H","coach":"德拉富恩特","key_players":["罗德里","佩德里","亚马尔","莫拉塔","奥尔莫"],"recent_form":["W","W","W","D","W"],"avg_goals":2.2,"avg_conceded":0.5,"world_cup_titles":1},
    "CPV": {"name":"佛得角","name_en":"Cape Verde","fifa_rank":65,"elo_rating":1570,"confederation":"CAF","group":"H","coach":"布比斯塔","key_players":["塔瓦雷斯","门德斯","罗沙","福特斯","瓦雷拉"],"recent_form":["W","D","W","L","W"],"avg_goals":1.1,"avg_conceded":1.2,"world_cup_titles":0},
    "KSA": {"name":"沙特阿拉伯","name_en":"Saudi Arabia","fifa_rank":53,"elo_rating":1640,"confederation":"AFC","group":"H","coach":"赫维·勒纳尔","key_players":["多萨里","布莱希","谢赫里","卡努","奥韦斯"],"recent_form":["W","L","W","D","W"],"avg_goals":1.3,"avg_conceded":1.1,"world_cup_titles":0},
    "URU": {"name":"乌拉圭","name_en":"Uruguay","fifa_rank":9,"elo_rating":1960,"confederation":"CONMEBOL","group":"H","coach":"贝尔萨","key_players":["巴尔韦德","努涅斯","阿劳霍","乌加特","佩利斯特里"],"recent_form":["W","W","W","L","W"],"avg_goals":2.0,"avg_conceded":0.6,"world_cup_titles":2},
    "FRA": {"name":"法国","name_en":"France","fifa_rank":2,"elo_rating":2080,"confederation":"UEFA","group":"I","coach":"德尚","key_players":["姆巴佩","格列兹曼","楚阿梅尼","特奥","萨利巴"],"recent_form":["W","W","D","W","L"],"avg_goals":2.4,"avg_conceded":0.9,"world_cup_titles":2},
    "SEN": {"name":"塞内加尔","name_en":"Senegal","fifa_rank":17,"elo_rating":1820,"confederation":"CAF","group":"I","coach":"阿利乌·西塞","key_players":["马内","库利巴利","杰克逊","萨尔","门迪"],"recent_form":["W","W","W","D","W"],"avg_goals":1.7,"avg_conceded":0.6,"world_cup_titles":0},
    "IRQ": {"name":"伊拉克","name_en":"Iraq","fifa_rank":67,"elo_rating":1580,"confederation":"AFC","group":"I","coach":"赫苏斯·卡萨斯","key_players":["哈马迪","纳提克","阿马里","齐丹","哈希姆"],"recent_form":["W","D","W","W","L"],"avg_goals":1.3,"avg_conceded":1.0,"world_cup_titles":0},
    "NOR": {"name":"挪威","name_en":"Norway","fifa_rank":43,"elo_rating":1720,"confederation":"UEFA","group":"I","coach":"斯托尔·索尔巴肯","key_players":["哈兰德","厄德高","博格","索尔洛特","阿耶尔"],"recent_form":["W","W","W","W","D"],"avg_goals":2.5,"avg_conceded":0.8,"world_cup_titles":0},
    "ARG": {"name":"阿根廷","name_en":"Argentina","fifa_rank":1,"elo_rating":2100,"confederation":"CONMEBOL","group":"J","coach":"斯卡洛尼","key_players":["梅西","阿尔瓦雷斯","恩佐","C·罗梅罗","E·马丁内斯"],"recent_form":["W","W","W","W","D"],"avg_goals":2.6,"avg_conceded":0.4,"world_cup_titles":3},
    "ALG": {"name":"阿尔及利亚","name_en":"Algeria","fifa_rank":44,"elo_rating":1710,"confederation":"CAF","group":"J","coach":"弗拉基米尔·佩特科维奇","key_players":["马赫雷斯","本纳赛尔","阿明·古伊里","奥亚尔","本塞拜尼"],"recent_form":["W","W","L","W","D"],"avg_goals":1.5,"avg_conceded":0.9,"world_cup_titles":0},
    "AUT": {"name":"奥地利","name_en":"Austria","fifa_rank":25,"elo_rating":1810,"confederation":"UEFA","group":"J","coach":"朗尼克","key_players":["阿拉巴","萨比策","鲍姆加特纳","莱默尔","施拉格尔"],"recent_form":["W","W","W","D","W"],"avg_goals":1.9,"avg_conceded":0.7,"world_cup_titles":0},
    "JOR": {"name":"约旦","name_en":"Jordan","fifa_rank":71,"elo_rating":1540,"confederation":"AFC","group":"J","coach":"侯赛因·阿穆塔","key_players":["塔马里","纳伊马特","奥尔万","哈达德","阿布-莱拉"],"recent_form":["W","W","L","D","W"],"avg_goals":1.2,"avg_conceded":1.3,"world_cup_titles":0},
    "POR": {"name":"葡萄牙","name_en":"Portugal","fifa_rank":6,"elo_rating":1970,"confederation":"UEFA","group":"K","coach":"罗伯托·马丁内斯","key_players":["C罗","B费","莱奥","B席","迪亚斯"],"recent_form":["W","W","W","W","W"],"avg_goals":2.8,"avg_conceded":0.3,"world_cup_titles":0},
    "COD": {"name":"刚果民主共和国","name_en":"DR Congo","fifa_rank":60,"elo_rating":1600,"confederation":"CAF","group":"K","coach":"塞巴斯蒂安·德萨布雷","key_players":["巴坎布","姆本巴","维萨","马苏亚库","马约罗"],"recent_form":["W","D","W","L","W"],"avg_goals":1.3,"avg_conceded":1.0,"world_cup_titles":0},
    "UZB": {"name":"乌兹别克斯坦","name_en":"Uzbekistan","fifa_rank":68,"elo_rating":1570,"confederation":"AFC","group":"K","coach":"斯雷奇科·卡塔内茨","key_players":["肖穆罗多夫","马沙里波夫","哈姆罗别科夫","阿利库洛夫","尤苏波夫"],"recent_form":["W","W","D","W","L"],"avg_goals":1.4,"avg_conceded":0.9,"world_cup_titles":0},
    "COL": {"name":"哥伦比亚","name_en":"Colombia","fifa_rank":10,"elo_rating":1920,"confederation":"CONMEBOL","group":"K","coach":"内斯托尔·洛伦索","key_players":["路易斯·迪亚斯","J罗","阿里亚斯","穆尼奥斯","博雷"],"recent_form":["W","W","W","D","W"],"avg_goals":2.0,"avg_conceded":0.5,"world_cup_titles":0},
    "ENG": {"name":"英格兰","name_en":"England","fifa_rank":4,"elo_rating":2020,"confederation":"UEFA","group":"L","coach":"图赫尔","key_players":["凯恩","贝林厄姆","萨卡","赖斯","福登"],"recent_form":["W","W","D","W","W"],"avg_goals":2.1,"avg_conceded":0.6,"world_cup_titles":1},
    "CRO": {"name":"克罗地亚","name_en":"Croatia","fifa_rank":18,"elo_rating":1850,"confederation":"UEFA","group":"L","coach":"达利奇","key_players":["莫德里奇","格瓦迪奥尔","科瓦契奇","布罗佐维奇","佩里西奇"],"recent_form":["W","D","W","W","L"],"avg_goals":1.6,"avg_conceded":0.7,"world_cup_titles":0},
    "GHA": {"name":"加纳","name_en":"Ghana","fifa_rank":55,"elo_rating":1630,"confederation":"CAF","group":"L","coach":"奥托·阿多","key_players":["库杜斯","托马斯","塞梅尼奥","乔丹·阿尤","兰普泰"],"recent_form":["W","L","W","D","W"],"avg_goals":1.4,"avg_conceded":1.1,"world_cup_titles":0},
    "PAN": {"name":"巴拿马","name_en":"Panama","fifa_rank":50,"elo_rating":1620,"confederation":"CONCACAF","group":"L","coach":"托马斯·克里斯蒂安森","key_players":["卡拉斯基利亚","穆里略","巴塞纳斯","法哈多","戴维斯"],"recent_form":["W","D","W","L","W"],"avg_goals":1.2,"avg_conceded":1.2,"world_cup_titles":0},
}

GROUPS = {
    "A": ["MEX","RSA","KOR","CZE"], "B": ["CAN","BIH","QAT","SUI"],
    "C": ["BRA","MAR","HAI","SCO"], "D": ["USA","PAR","AUS","TUR"],
    "E": ["GER","CUW","CIV","ECU"], "F": ["NED","JPN","SWE","TUN"],
    "G": ["BEL","EGY","IRN","NZL"], "H": ["ESP","CPV","KSA","URU"],
    "I": ["FRA","SEN","IRQ","NOR"], "J": ["ARG","ALG","AUT","JOR"],
    "K": ["POR","COD","UZB","COL"], "L": ["ENG","CRO","GHA","PAN"],
}

# ============================================================
# 2. 赛程（北京时间 UTC+8）
#    格式: (北京日期, [(match_id, 主队, 客队, 小组, 球场, 城市, 北京开球时间), ...])
# ============================================================
GROUP_FIXTURES_BEIJING = [
    # ── 6/12 (周五) 揭幕战 ──
    ("2026-06-12", [
        ("G-A-1","MEX","RSA","A","墨西哥城体育场","墨西哥城","03:00"),
        ("G-A-2","KOR","CZE","A","瓜达拉哈拉体育场","瓜达拉哈拉","10:00"),
    ]),
    # ── 6/13 (周六) ──
    ("2026-06-13", [
        ("G-B-1","CAN","BIH","B","BMO球场","多伦多","03:00"),
        ("G-D-1","USA","PAR","D","SoFi体育场","洛杉矶","09:00"),
    ]),
    # ── 6/14 (周日) ──
    ("2026-06-14", [
        ("G-B-2","QAT","SUI","B","李维斯体育场","旧金山","03:00"),
        ("G-C-2","BRA","MAR","C","大都会体育场","纽约/新泽西","06:00"),
        ("G-C-1","HAI","SCO","C","吉列体育场","波士顿","09:00"),
        ("G-D-2","AUS","TUR","D","BC广场","温哥华","12:00"),
    ]),
    # ── 6/15 (周一) ──
    ("2026-06-15", [
        ("G-E-2","GER","CUW","E","NRG体育场","休斯顿","01:00"),
        ("G-F-1","NED","JPN","F","AT&T体育场","达拉斯","04:00"),
        ("G-E-1","CIV","ECU","E","林肯金融体育场","费城","07:00"),
        ("G-F-2","SWE","TUN","F","BBVA体育场","蒙特雷","10:00"),
    ]),
    # ── 6/16 (周二) ──
    ("2026-06-16", [
        ("G-H-2","ESP","CPV","H","奔驰体育场","亚特兰大","00:00"),
        ("G-G-2","BEL","EGY","G","流明体育场","西雅图","03:00"),
        ("G-H-1","KSA","URU","H","硬石体育场","迈阿密","06:00"),
        ("G-G-1","IRN","NZL","G","SoFi体育场","洛杉矶","09:00"),
    ]),
    # ── 6/17 (周三) ──
    ("2026-06-17", [
        ("G-I-1","FRA","SEN","I","大都会体育场","纽约/新泽西","03:00"),
        ("G-I-2","IRQ","NOR","I","吉列体育场","波士顿","06:00"),
        ("G-J-1","ARG","ALG","J","儿童慈善公园","堪萨斯城","09:00"),
        ("G-J-2","AUT","JOR","J","李维斯体育场","旧金山","12:00"),
    ]),
    # ── 6/18 (周四) ──
    ("2026-06-18", [
        ("G-K-1","POR","COD","K","NRG体育场","休斯顿","01:00"),
        ("G-L-2","ENG","CRO","L","AT&T体育场","达拉斯","04:00"),
        ("G-L-1","GHA","PAN","L","BMO球场","多伦多","07:00"),
        ("G-K-2","UZB","COL","K","墨西哥城体育场","墨西哥城","10:00"),
    ]),
    # ── 6/19 (周五) 第2轮 ──
    ("2026-06-19", [
        ("G-A-3","CZE","RSA","A","奔驰体育场","亚特兰大","00:00"),
        ("G-B-3","SUI","BIH","B","SoFi体育场","洛杉矶","03:00"),
        ("G-B-4","CAN","QAT","B","BC广场","温哥华","06:00"),
        ("G-A-4","MEX","KOR","A","瓜达拉哈拉体育场","瓜达拉哈拉","09:00"),
    ]),
    # ── 6/20 (周六) ──
    ("2026-06-20", [
        ("G-D-4","USA","AUS","D","流明体育场","西雅图","03:00"),
        ("G-C-4","SCO","MAR","C","吉列体育场","波士顿","06:00"),
        ("G-C-3","BRA","HAI","C","林肯金融体育场","费城","09:00"),
        ("G-D-3","TUR","PAR","D","李维斯体育场","旧金山","12:00"),
    ]),
    # ── 6/21 (周日) ──
    ("2026-06-21", [
        ("G-F-3","NED","SWE","F","NRG体育场","休斯顿","01:00"),
        ("G-E-3","GER","CIV","E","BMO球场","多伦多","04:00"),
        ("G-E-4","ECU","CUW","E","儿童慈善公园","堪萨斯城","08:00"),
        ("G-F-4","TUN","JPN","F","BBVA体育场","蒙特雷","12:00"),
    ]),
    # ── 6/22 (周一) ──
    ("2026-06-22", [
        ("G-H-4","ESP","KSA","H","奔驰体育场","亚特兰大","00:00"),
        ("G-G-3","BEL","IRN","G","SoFi体育场","洛杉矶","03:00"),
        ("G-H-3","URU","CPV","H","硬石体育场","迈阿密","06:00"),
        ("G-G-4","NZL","EGY","G","BC广场","温哥华","09:00"),
    ]),
    # ── 6/23 (周二) ──
    ("2026-06-23", [
        ("G-J-3","ARG","AUT","J","AT&T体育场","达拉斯","01:00"),
        ("G-I-4","FRA","IRQ","I","林肯金融体育场","费城","05:00"),
        ("G-I-3","NOR","SEN","I","大都会体育场","纽约/新泽西","08:00"),
        ("G-J-4","JOR","ALG","J","李维斯体育场","旧金山","11:00"),
    ]),
    # ── 6/24 (周三) ──
    ("2026-06-24", [
        ("G-K-3","POR","UZB","K","NRG体育场","休斯顿","01:00"),
        ("G-L-3","ENG","GHA","L","吉列体育场","波士顿","04:00"),
        ("G-L-4","PAN","CRO","L","BMO球场","多伦多","07:00"),
        ("G-K-4","COL","COD","K","瓜达拉哈拉体育场","瓜达拉哈拉","10:00"),
    ]),
    # ── 6/25 (周四) 第3轮 B+C组 ──
    ("2026-06-25", [
        ("G-B-5","SUI","CAN","B","BC广场","温哥华","03:00"),
        ("G-B-6","BIH","QAT","B","流明体育场","西雅图","03:00"),
        ("G-C-5","SCO","BRA","C","硬石体育场","迈阿密","06:00"),
        ("G-C-6","MAR","HAI","C","奔驰体育场","亚特兰大","06:00"),
        ("G-A-5","CZE","MEX","A","墨西哥城体育场","墨西哥城","09:00"),
        ("G-A-6","RSA","KOR","A","BBVA体育场","蒙特雷","09:00"),
    ]),
    # ── 6/26 (周五) 第3轮 E+F+D组 ──
    ("2026-06-26", [
        ("G-E-6","ECU","GER","E","大都会体育场","纽约/新泽西","04:00"),
        ("G-E-5","CUW","CIV","E","林肯金融体育场","费城","04:00"),
        ("G-F-5","JPN","SWE","F","AT&T体育场","达拉斯","07:00"),
        ("G-F-6","TUN","NED","F","儿童慈善公园","堪萨斯城","07:00"),
        ("G-D-5","TUR","USA","D","SoFi体育场","洛杉矶","10:00"),
        ("G-D-6","PAR","AUS","D","李维斯体育场","旧金山","10:00"),
    ]),
    # ── 6/27 (周六) 第3轮 I+H+G组 ──
    ("2026-06-27", [
        ("G-I-5","NOR","FRA","I","吉列体育场","波士顿","03:00"),
        ("G-I-6","SEN","IRQ","I","BMO球场","多伦多","03:00"),
        ("G-H-5","CPV","KSA","H","NRG体育场","休斯顿","08:00"),
        ("G-H-6","URU","ESP","H","瓜达拉哈拉体育场","瓜达拉哈拉","08:00"),
        ("G-G-5","EGY","IRN","G","流明体育场","西雅图","11:00"),
        ("G-G-6","NZL","BEL","G","BC广场","温哥华","11:00"),
    ]),
    # ── 6/28 (周日) 第3轮 L+K+J组 ──
    ("2026-06-28", [
        ("G-L-5","PAN","ENG","L","大都会体育场","纽约/新泽西","05:00"),
        ("G-L-6","CRO","GHA","L","林肯金融体育场","费城","05:00"),
        ("G-K-5","COL","POR","K","硬石体育场","迈阿密","07:30"),
        ("G-K-6","COD","UZB","K","奔驰体育场","亚特兰大","07:30"),
        ("G-J-5","ALG","AUT","J","儿童慈善公园","堪萨斯城","10:00"),
        ("G-J-6","JOR","ARG","J","AT&T体育场","达拉斯","10:00"),
    ]),
]

# ============================================================
# 3. 淘汰赛（北京时间）
# ============================================================
KNOCKOUT_FIXTURES_BEIJING = [
    # Round of 32 (6/29-7/4)
    ("2026-06-29", [("KO-R32-1","TBD","TBD","round_of_32",None,"洛杉矶","03:00")]),
    ("2026-06-30", [
        ("KO-R32-2","TBD","TBD","round_of_32",None,"休斯顿","01:00"),
        ("KO-R32-3","TBD","TBD","round_of_32",None,"波士顿","04:30"),
        ("KO-R32-4","TBD","TBD","round_of_32",None,"蒙特雷","09:00"),
    ]),
    ("2026-07-01", [
        ("KO-R32-5","TBD","TBD","round_of_32",None,"达拉斯","01:00"),
        ("KO-R32-6","TBD","TBD","round_of_32",None,"纽约/新泽西","05:00"),
        ("KO-R32-7","TBD","TBD","round_of_32",None,"墨西哥城","09:00"),
    ]),
    ("2026-07-02", [
        ("KO-R32-8","TBD","TBD","round_of_32",None,"亚特兰大","00:00"),
        ("KO-R32-9","TBD","TBD","round_of_32",None,"西雅图","04:00"),
        ("KO-R32-10","TBD","TBD","round_of_32",None,"旧金山","08:00"),
    ]),
    ("2026-07-03", [
        ("KO-R32-11","TBD","TBD","round_of_32",None,"洛杉矶","03:00"),
        ("KO-R32-12","TBD","TBD","round_of_32",None,"多伦多","07:00"),
        ("KO-R32-13","TBD","TBD","round_of_32",None,"温哥华","11:00"),
        ("KO-R32-14","TBD","TBD","round_of_32",None,"达拉斯","02:00"),
    ]),
    ("2026-07-04", [
        ("KO-R32-15","TBD","TBD","round_of_32",None,"迈阿密","06:00"),
        ("KO-R32-16","TBD","TBD","round_of_32",None,"堪萨斯城","09:30"),
    ]),
    # Round of 16 (7/5-7/8)
    ("2026-07-05", [("KO-R16-1","TBD","TBD","round_of_16",None,"费城","01:00"),("KO-R16-2","TBD","TBD","round_of_16",None,"纽约/新泽西","05:00")]),
    ("2026-07-06", [("KO-R16-3","TBD","TBD","round_of_16",None,"休斯顿","04:00"),("KO-R16-4","TBD","TBD","round_of_16",None,"墨西哥城","08:00")]),
    ("2026-07-07", [("KO-R16-5","TBD","TBD","round_of_16",None,"达拉斯","03:00"),("KO-R16-6","TBD","TBD","round_of_16",None,"西雅图","08:00")]),
    ("2026-07-08", [("KO-R16-7","TBD","TBD","round_of_16",None,"亚特兰大","00:00"),("KO-R16-8","TBD","TBD","round_of_16",None,"温哥华","04:00")]),
    # Quarter-finals (7/10-7/12)
    ("2026-07-10", [("KO-QF-1","TBD","TBD","quarter_final",None,"波士顿","04:00")]),
    ("2026-07-11", [("KO-QF-2","TBD","TBD","quarter_final",None,"洛杉矶","03:00")]),
    ("2026-07-12", [("KO-QF-3","TBD","TBD","quarter_final",None,"迈阿密","05:00"),("KO-QF-4","TBD","TBD","quarter_final",None,"堪萨斯城","09:00")]),
    # Semi-finals (7/15-7/16)
    ("2026-07-15", [("KO-SF-1","TBD","TBD","semi_final",None,"达拉斯","03:00")]),
    ("2026-07-16", [("KO-SF-2","TBD","TBD","semi_final",None,"亚特兰大","03:00")]),
    # Third place (7/19)
    ("2026-07-19", [("KO-3RD-1","TBD","TBD","third_place",None,"迈阿密","05:00")]),
    # Final (7/20)
    ("2026-07-20", [("KO-F-1","TBD","TBD","final",None,"大都会体育场, 纽约/新泽西","03:00")]),
]

# ============================================================
# 4. 已知赛果（截至 6/18 北京）
# ============================================================
KNOWN_RESULTS = {
    "G-A-1":(2,0), "G-A-2":(2,1),
    "G-B-1":(1,1), "G-D-1":(4,1),
    "G-B-2":(1,1), "G-C-2":(1,1), "G-C-1":(0,1), "G-D-2":(2,0),
    "G-E-2":(7,1), "G-F-1":(2,2), "G-E-1":(1,0), "G-F-2":(5,1),
    "G-H-2":(0,0), "G-G-2":(1,1), "G-H-1":(1,1), "G-G-1":(2,2),
    "G-I-1":(3,1), "G-I-2":(1,4), "G-J-1":(3,0), "G-J-2":(3,1),
    "G-K-1":(1,1), "G-L-2":(4,2), "G-L-1":(1,0), "G-K-2":(1,3),
}

H2H = {
    "MEX_RSA":{"total":2,"wins_team1":1,"draws":1,"wins_team2":0},
    "ARG_ALG":{"total":2,"wins_team1":1,"draws":1,"wins_team2":0},
    "BRA_MAR":{"total":2,"wins_team1":2,"draws":0,"wins_team2":0},
    "ENG_CRO":{"total":6,"wins_team1":3,"draws":1,"wins_team2":2},
    "FRA_SEN":{"total":1,"wins_team1":1,"draws":0,"wins_team2":0},
    "GER_CUW":{"total":0,"wins_team1":0,"draws":0,"wins_team2":0},
    "NED_JPN":{"total":2,"wins_team1":1,"draws":1,"wins_team2":0},
    "ESP_URU":{"total":4,"wins_team1":2,"draws":2,"wins_team2":0},
    "POR_COL":{"total":2,"wins_team1":1,"draws":0,"wins_team2":1},
    "USA_PAR":{"total":5,"wins_team1":3,"draws":1,"wins_team2":1},
    "CAN_BIH":{"total":1,"wins_team1":0,"draws":1,"wins_team2":0},
    "KOR_CZE":{"total":3,"wins_team1":1,"draws":1,"wins_team2":1},
}


# ============================================================
# 5. 生成并写入
# ============================================================
def generate_all_matches():
    all_matches = []

    for date_str, fixtures in GROUP_FIXTURES_BEIJING:
        for (mid, home, away, group, stadium, city, kickoff) in fixtures:
            score = KNOWN_RESULTS.get(mid)
            all_matches.append({
                "match_id": mid, "home_team": home, "away_team": away,
                "stage": "group", "group": group,
                "match_date": f"{date_str}T{kickoff}:00",
                "stadium": stadium, "city": city,
                "home_score": score[0] if score else None,
                "away_score": score[1] if score else None,
            })

    for date_str, fixtures in KNOCKOUT_FIXTURES_BEIJING:
        for (mid, home, away, stage, group, stadium, kickoff) in fixtures:
            all_matches.append({
                "match_id": mid, "home_team": home, "away_team": away,
                "stage": stage, "group": group,
                "match_date": f"{date_str}T{kickoff}:00",
                "stadium": stadium, "city": "",
                "home_score": None, "away_score": None,
            })

    return all_matches


def write_json(filename, data):
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> {filename}")


def main():
    print("生成 2026 世界杯数据（北京时间）...\n")

    write_json("teams.json", TEAMS)
    write_json("groups.json", GROUPS)

    matches = generate_all_matches()
    group_n = sum(1 for m in matches if m["stage"] == "group")
    ko_n = sum(1 for m in matches if m["stage"] != "group")
    played = sum(1 for m in matches if m["home_score"] is not None)

    schedule = {
        "tournament": "2026 FIFA 世界杯",
        "host": "美国 / 加拿大 / 墨西哥",
        "date_range": "2026-06-12 ~ 2026-07-20 (北京时间)",
        "total_matches": len(matches),
        "matches": matches,
    }
    write_json("schedule.json", schedule)
    print(f"  小组赛 {group_n} 场 + 淘汰赛 {ko_n} 场 = {len(matches)} 场 | 已结束 {played} 场")

    write_json("historical/head_to_head.json", H2H)
    print(f"\n完成!")


if __name__ == "__main__":
    main()
