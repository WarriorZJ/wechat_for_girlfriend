import configparser
import os
import random
import time
from datetime import datetime, timedelta, timezone

import requests
import zhdate
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

"""
1、从配置文件中获取变量
"""
# 若明文 config.conf 不存在，则尝试由加密文件 config.conf.enc 解密还原
# 解密密钥来自环境变量 WECHAT_CONF_KEY（本地开发保留明文 config.conf 时此步会被跳过）
try:
    from crypto_config import decrypt_config
    if not os.path.exists("config.conf"):
        decrypt_config()
except Exception as e:
    print(f"读取配置失败：{e}")

conf = configparser.ConfigParser()
config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf.read('config.conf', 'utf8')
start_date = conf.get("info", "start_date")  # 在一起开始日期,格式 ****-**-**
city1 = conf.get("info", "city1")  # 所在的城市(请写具体城市，如昆明)，用于匹配天气预报和热点新闻
city2 = conf.get("info", "city2")
birthday_lover = conf.get("info", "birthday_lover")  # 生日 格式**-**
birthday_my = conf.get("info", "birthday_my")
app_id = conf.get("info", "app_id")  # 微信测试号ID（开通以后自动生成）
app_secret = conf.get("info", "app_secret")  # 微信测试号密钥（开通以后自动生成）
template_id = conf.get("info", "template_id")
# 接收消息的用户ID，让你的女朋友扫微信测试号的二维码，获取微信用户ID
user_id = conf.get("info", "user_id")  # 接收消息的微信号，注意这个不是普通微信号，需要扫微信测试号后台的二维码来获取
yd = conf.get("info", "yd")
sp = conf.get("info", "sp")
user_id1 = user_id.split(",")

"""
2、定义获取数据的函数
"""


def get_morning_words():
    """早安/上午祝福语（共60条，无重复）"""
    morning_inspirations = [
        "今天会是美好的一天！",
        "早晨的阳光是新的开始。",
        "新的挑战，新的机遇。",
        "早起一小时，赢得一天。",
        "每天进步一点点，成功就不远。",
        "相信自己，未来无限可能。",
        "你比你想象的更强大。",
        "保持微笑，迎接新的一天。",
        "今天是你改变的最佳时机。",
        "让今天成为最棒的一天！",
        "不畏将来，不念过往。",
        "做自己，做最好的自己。",
        "每天都是新的机会。",
        "努力不一定会成功，但放弃一定会失败。",
        "勇敢面对每一个晨曦。",
        "新的一天，新的开始。",
        "人生没有彩排，每一天都是现场直播。",
        "保持信念，迎接每个晨光。",
        "未来属于那些努力的人。",
        "阳光明媚，心情也跟着好！",
        "清晨就是新的开始，勇敢去追逐梦想。",
        "每天醒来，都是新的机会。",
        "新的一天，新的希望，继续加油！",
        "给自己一个微笑，开始新的一天。",
        "挑战自己，迎接美好的一天。",
        "从早晨开始，做最好的自己。",
        "每天都是全新的机会，抓住它！",
        "今天做更好的自己，明天更精彩。",
        "每一天都充满可能性，加油！",
        "勇敢向前，未来属于你。",
        "梦想从清晨开始，努力就不晚。",
        "你今天的努力，决定明天的精彩。",
        "从晨曦中汲取力量，迎接每一天。",
        "为美好的明天而努力，今天开始！",
        "新的开始，新的挑战，新的胜利！",
        "迎接新的一天，充满正能量。",
        "今天的努力，给明天铺路。",
        "每天都是新的希望，做最好的自己。",
        "无论如何，早起的鸟儿有虫吃！",
        "晨光正好，你也正好。",
        "推开窗，世界都在对你微笑。",
        "今天的风，都是甜的。",
        "新的一天，愿你被温柔以待。",
        "每一个清晨，都是生命给你的礼物。",
        "早安，愿你今天比昨天更快乐。",
        "太阳升起，好运也随之而来。",
        "用一杯热咖啡，开启元气满满的一天。",
        "清晨的第一缕阳光，专属于你。",
        "今天也要做闪闪发光的自己呀。",
        "起床啦！美好的事情正在等你。",
        "每一个早晨，都是重新出发的机会。",
        "早安，今天也要开心哦！",
        "新的一天，愿所有美好不期而遇。",
        "睁开眼，就是崭新的世界。",
        "晨风轻拂，愿你心情如花绽放。",
        "今天是值得期待的一天！",
        "早起的你，已经赢了全世界一半。",
        "清晨好，愿你的一天充满小确幸。",
        "早安！记得吃早餐，照顾好自己。",
    ]

    return random.choice(morning_inspirations)


def get_eatmorning_words():
    """午间祝福语（共30条，无重复）"""
    noon_words = [
        "中午好！愿你今日心情超棒",
        "午安，祝你午餐美味又开心",
        "中午到啦，愿你生活甜如蜜",
        "中午好呀，愿幸运时刻相随",
        "午间愉快，愿身心自在轻松",
        "中午安好，愿工作一切顺利",
        "中午好，愿午后时光很惬意",
        "午安！愿你享受惬意中午",
        "中午时分，愿快乐常围绕你",
        "中午好，愿笑容时刻挂嘴边",
        "中午好，休息一下，放松心情！",
        "中午愉快，享受美好的午餐！",
        "中午好，午休时间，放松一下！",
        "中午好，保持元气，继续奋斗！",
        "中午好，午饭吃好，下午精神更好！",
        "中午好，享受美好的午餐时光！",
        "中午好，愿你的每一天都充满阳光！",
        "中午愉快，笑容可掬，心情美好！",
        "中午好，愿你的事业蒸蒸日上！",
        "午安，忙了一上午，犒劳一下自己吧。",
        "中午好，记得好好吃饭哦！",
        "午间时光，愿你吃得开心，笑得灿烂。",
        "中午好呀，给自己充充电再出发。",
        "午安！愿你午后一切顺顺利利。",
        "中午好，吃饱了才有力气继续追梦。",
        "午间小憩，愿你精力充沛。",
        "中午好，今天也要元气满满哦！",
        "午安，愿你午餐时光温暖又美好。",
        "中午好，别忘了喝水，保持好状态！",
        "午间好，愿你下午好运连连。",
    ]

    return random.choice(noon_words)


def get_afternoon_words():
    """下午祝福语（共30条，无重复）"""
    afternoon_words = [
        "期待下午的阳光洒满心田。",
        "下午的时间，总是充满希望。",
        "盼望下午能有一个小小的休息。",
        "希望下午的时光如诗如画。",
        "下午，期待着美好的一切到来。",
        "下午的宁静，给了我满满的动力。",
        "期待下午有更多的美好发现。",
        "下午的阳光，洒进了我的心房。",
        "期待下午的时间更加充实。",
        "下午，是放松心情的时刻。",
        "下午的风，吹动了我的心情。",
        "下午，感受每一缕温暖的阳光。",
        "下午的空气，格外清新。",
        "期待下午的每一个小惊喜。",
        "午后的光线洒满每个角落。",
        "下午的时光，适合放慢脚步。",
        "期待下午可以有一个小小的冒险。",
        "午后的闲暇，时间悄悄流逝。",
        "下午的世界，充满了安静与美好。",
        "下午的光景是一天中最温暖的时光。",
        "下午好呀，愿你效率翻倍，早点下班！",
        "午后时光，愿你一切顺利。",
        "下午好，离下班又近了一步，加油！",
        "午后的阳光，照亮你的好心情。",
        "下午好，愿你手头的工作都顺顺利利。",
        "下午时光，愿你收获满满的成就感。",
        "下午好，坚持一下，胜利就在眼前！",
        "午后微风，愿你心旷神怡。",
        "下午好，今天也要努力鸭！",
        "下午时光，愿你被好运眷顾。",
    ]

    return random.choice(afternoon_words)


def get_goodnight_words():
    """傍晚/晚安祝福语（共50条，无重复）"""
    night_words = [
        '傍晚愉快，愿你收获美好时光！',
        '夕阳西下，愿你心情如霞光灿烂！',
        '傍晚微风轻拂，愿你惬意自在！',
        '祝你傍晚温馨，夜晚安然入梦！',
        '黄昏美好，愿你放松身心，快乐相伴！',
        '夕阳无限美，愿你笑颜常在！',
        '傍晚安好，愿你享受宁静时光！',
        '夜幕降临，愿你温暖不减，幸福依然！',
        '晚霞如诗，愿你的心情也如诗般美好！',
        '傍晚微凉，愿你温暖如初，幸福绵长！',
        '傍晚好，愿你收获一天的温暖！',
        '夕阳西沉，愿你的烦恼随风而去！',
        '傍晚微风轻拂，带来幸福与宁静！',
        '夜色将至，愿你心安自在！',
        '晚霞绚烂，愿你的生活同样精彩！',
        '傍晚时光，愿你享受片刻宁静！',
        '日落美好，愿你心中充满暖意！',
        '夜幕降临，愿你放松身心，好梦相随！',
        '愿晚风吹走疲惫，带来温暖与希望！',
        '夕阳虽落，幸福却不会散去！',
        '傍晚的霞光，映照出你的美好人生！',
        '祝你傍晚惬意，夜晚甜美入梦！',
        '星辰初上，愿你的世界依旧光亮！',
        '晚风轻拂，愿你的心境如湖水般平静！',
        '夕阳西下，愿你的梦想依旧熠熠生辉！',
        '愿这傍晚的温柔，治愈你一天的疲惫！',
        '夜色渐浓，愿你的心田洒满星光！',
        '傍晚的微光，愿它点亮你的美好心情！',
        '愿你在傍晚的余晖里，找到生活的温暖！',
        '夜幕轻柔降临，愿你收获满满的幸福！',
        '傍晚安宁，愿你快乐相随！',
        '夕阳余晖，温暖你的心田！',
        '夜风轻拂，愿你舒心惬意！',
        '霞光漫天，愿你的世界灿烂！',
        '星光闪烁，愿你幸福满怀！',
        '傍晚微凉，愿温暖常伴！',
        '落日余晖，映照美好心情！',
        '晚霞如诗，愿你笑靥如花！',
        '夜幕降临，愿你安心入眠！',
        '傍晚好，愿你远离烦恼！',
        '日落虽晚，幸福不散！',
        '黄昏静美，愿你安然自得！',
        '星夜温柔，愿你心境宁静！',
        '愿傍晚的微风，吹散你的疲惫！',
        '夕阳温暖，愿你的心也温暖！',
        '夜色如画，愿你美梦成真！',
        '晚风送爽，愿你悠然自在！',
        '傍晚的时光，愿你尽享宁静！',
        '夕阳虽落，幸福常在！',
        '夜色朦胧，愿你安心入梦！',
        '辛苦了一天，晚上好好犒劳自己吧！',
        '傍晚好，愿你有个愉快的夜晚！',
    ]

    return random.choice(night_words)


def get_beijing_time():
    # 使用 timezone 正确处理东八区时间
    bj_tz = timezone(timedelta(hours=8))
    return datetime.now(bj_tz)


# 自定义函数：将数字转换为中文
def number_to_chinese(num):
    chinese_digits = {
        '0': '零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五',
        '6': '六', '7': '七', '8': '八', '9': '九'
    }
    return ''.join(chinese_digits[digit] for digit in str(num))


# 自定义函数：将农历日期转换为中文格式
def convert_date_to_chinese(nongli_date):
    year_chinese = number_to_chinese(nongli_date.lunar_year)
    month_chinese = number_to_chinese(nongli_date.lunar_month)
    day_chinese = number_to_chinese(nongli_date.lunar_day).replace('一零', '十').replace('零', '十')

    # 根据农历月份的特殊情况，处理正月和腊月
    month_chinese = '正' if month_chinese == '一' else month_chinese
    month_chinese = '腊' if month_chinese == '十二' else month_chinese
    if len(day_chinese) == 2 and day_chinese[0] == '二':
        day_chinese = str(day_chinese[0]).replace('二', '廿') + day_chinese[1]
    elif len(day_chinese) == 1:
        day_chinese = day_chinese
    if len(day_chinese) == 1:
        day_chinese = '初' + str(day_chinese)
    else:
        if day_chinese[0] == '一':
            day_chinese = str(day_chinese[0]).replace('一', '十') + day_chinese[1]
        else:
            day_chinese = day_chinese

    return f"{year_chinese}年{month_chinese}月{day_chinese}"


def get_weekday():
    """获取当前日期、星期和农历日期"""
    now = get_beijing_time()
    date_str = now.strftime("%Y-%m-%d %X")

    # 农历日期（zhdate 不支持 aware datetime，需去掉时区信息）
    nongli_date = zhdate.ZhDate.from_datetime(now.replace(tzinfo=None))
    nongli_date_chinese = convert_date_to_chinese(nongli_date)

    # 星期映射
    weekday_map = {
        0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四",
        4: "星期五", 5: "星期六", 6: "星期日"
    }
    weekd = f"{date_str}  {weekday_map[now.weekday()]}"

    return weekd, nongli_date_chinese


# 获取天气
def get_weather(city, api_key='7c75b7045984a1ffc81b7bf751b783c1'):
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={api_key}"

    try:
        # 发送请求，设置超时时间
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 检查HTTP响应状态码

        data = response.json()

        # 判断API返回的状态
        if data.get('status') == '1' and 'lives' in data and data['lives']:
            weather_info = data['lives'][0]  # 取第一个天气信息
            weather = weather_info.get('weather', '微风')
            temperature = int(weather_info.get('temperature', 28))
        else:
            weather, temperature = "微风", 28

    except (requests.RequestException, ValueError, KeyError):
        weather, temperature = "微风", 28

    return weather, temperature


# 计算在一起的日期
def get_count():
    now = get_beijing_time()
    # 让 strptime 结果带上时区，避免 aware-naive 比较报错
    bj_tz = timezone(timedelta(hours=8))
    start = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=bj_tz)
    delta = now - start
    return delta.days + 1


# 计算距离下一次生日多少天
def get_birthday(birthday):
    now = get_beijing_time()
    today = now.date()
    bj_tz = timezone(timedelta(hours=8))
    next_birthday = datetime.strptime(str(today.year) + "-" + birthday, "%Y-%m-%d").replace(tzinfo=bj_tz)

    # 如果生日已经过了，则计算明年的生日
    if next_birthday < now:
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)

    days_until_birthday = (next_birthday.date() - today).days
    return days_until_birthday


# 计算到元旦、春节的日期
def get_spr(yd, sp):
    """计算距离元旦和春节的天数"""
    now = get_beijing_time()
    today = now.date()
    bj_tz = timezone(timedelta(hours=8))

    # 计算元旦的天数
    next_yd = datetime.strptime(str(today.year) + "-" + yd, "%Y-%m-%d").replace(tzinfo=bj_tz)
    if next_yd < now:
        next_yd = next_yd.replace(year=next_yd.year + 1)
    j_yd = (next_yd.date() - today).days

    # 计算春节的天数（修复：不再无条件+1年）
    next_cj = datetime.strptime(str(today.year) + "-" + sp, "%Y-%m-%d").replace(tzinfo=bj_tz)
    if next_cj < now:
        next_cj = next_cj.replace(year=next_cj.year + 1)
    j_cj = (next_cj.date() - today).days

    return j_yd, j_cj


# 每日金句
def get_words():
    """获取每日情话金句，API失败时使用本地备用句库"""
    words_list = [
        "我的世界，因你而暖。",
        "愿陪你走过每个春夏秋冬。",
        "星光不及你眼眸温柔。",
        "遇见你，是我最大的幸运。",
        "每天都想和你腻在一起。",
        "有你在，生活才浪漫。",
        "爱你，从未改变。",
        "风再大，也吹不走我的思念。",
        "牵着你的手，一生不放开。",
        "你是我心头的朱砂痣。",
        "一想到你，嘴角就会不自觉上扬。",
        "余生很长，我只想陪你慢慢走。",
        "夜空再美，不及你的笑颜。",
        "我的世界，只有你最耀眼。",
        "你是我生命里最美的风景。",
        "思念如影随形，一刻也不曾停。",
        "你的名字，是我心中最温柔的诗。",
        "每天醒来，第一件事就是想你。",
        "爱你，从晨曦到暮色四合。",
        "我的心里，住着一个可爱的你。",
        "你笑起来真好看，像春天的花一样。",
        "想把所有的温柔都给你。",
        "你是我的例外，也是我的偏爱。",
        "世界那么大，我的眼里只有你。",
        "你的存在，就是我最大的安心。",
        "喜欢你，是我做过最对的事。",
        "愿往后余生，都有你相伴。",
        "你是我写不完的温柔诗篇。",
        "和你在一起，连空气都是甜的。",
        "你是我所有不安的解药。",
    ]
    # 循环尝试最多3次，避免递归导致栈溢出
    for _ in range(3):
        try:
            response = requests.get("https://api.shadiao.pro/chp", timeout=5)
            response.raise_for_status()
            text = response.json().get('data', {}).get('text', '')
            if len(text) <= 20:
                return text
        except (requests.RequestException, ValueError):
            break
    return random.choice(words_list)


# 每日宜忌（本地词库随机拼，稳定不依赖外部接口）
_YI = ["出行", "约会", "表白", "观影", "散步", "做饭", "读书", "健身",
       "拍照", "逛街", "喝奶茶", "写日记", "早睡", "撸猫", "种花"]
_JI = ["熬夜", "生气", "拖延", "暴饮暴食", "久坐", "内耗", "挑食",
       "错过晚安", "忘带钥匙", "喝太多冰的"]
def get_yi_ji():
    yi = random.sample(_YI, 2)          # 随机宜 2 项
    ji = random.sample(_JI, 1)          # 随机忌 1 项
    return f"宜{yi[0]}、{yi[1]}；忌{ji[0]}"


# 美食推荐（本地菜库随机，稳定不依赖外部接口）
_FOOD = ["番茄牛腩", "可乐鸡翅", "酸菜鱼", "红烧肉", "糖醋排骨",
         "麻辣香锅", "日式咖喱饭", "芝士焗饭", "皮蛋瘦肉粥", "葱油拌面",
         "螺蛳粉", "羊肉串", "小笼包", "提拉米苏", "芒果班戟", "草莓大福"]
def get_food():
    return random.choice(_FOOD) + "（今天试试这个？）"


def get_weibo_hot():
    """获取百度热搜第一条（原微博热搜源 60s.viki.moe 已被 Cloudflare 拦截，改用百度热搜），失败回退本地"""
    try:
        r = requests.get("https://v.api.aa1.cn/api/topbaidu/index.php",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if r.status_code == 200:
            items = r.json().get("newslist", [])
            if items:
                return items[0].get("title", "")
    except (requests.RequestException, ValueError, KeyError):
        pass
    return "今天热搜有点害羞，躲起来了"


# 字体颜色，随机 每次不一样
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 豆瓣通用请求头
DOUBAN_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    ),
    "Referer": "https://movie.douban.com/",
}


def _fetch_douban_hot(media_type, fallback_name, tag="热门"):
    """
    从豆瓣热门 API 获取最新热门电视剧/电影
    :param media_type: 'tv' 或 'movie'
    :param fallback_name: 获取失败时的提示文字
    :param tag: 筛选标签，如 '热门'、'国产剧'
    :return: 格式化的推荐字符串
    """
    url = "https://movie.douban.com/j/search_subjects"
    params = {
        "type": media_type,
        "tag": tag,
        "page_limit": 10,
        "page_start": 0,
    }

    time.sleep(random.uniform(0.5, 1.5))

    for attempt in range(3):
        try:
            res = requests.get(url, params=params, headers=DOUBAN_HEADERS, timeout=5)
            if res.status_code == 200:
                subjects = res.json().get("subjects", [])
                if subjects:
                    # 只保留有评分的，优先推荐高分
                    rated = [s for s in subjects if s.get("rate")]
                    pick = random.choice(rated) if rated else random.choice(subjects)
                    name = pick["title"]
                    score = pick.get("rate", "暂无")
                    return f"《{name}》{score}分"
                break
            else:
                time.sleep(2)
        except (requests.RequestException, ValueError, KeyError):
            time.sleep(2)

    return f"暂时无法获取{fallback_name}信息"


def top_tv():
    """从豆瓣获取最新热门国产剧推荐"""
    return _fetch_douban_hot("tv", "电视剧", tag="国产剧")


def top_mv():
    """从豆瓣获取最新热门电影推荐"""
    return _fetch_douban_hot("movie", "电影")


"""
3、调用函数，获取数据，保存为字典格式数据
"""
# 获取天气和温度
wea1, temperature1 = get_weather(city1)
wea2, temperature2 = get_weather(city2)

# 计算到春节的天数
j_yd, j_cj = get_spr(yd, sp)


# 根据天气和温度生成生活建议
def get_weather_advice(weather, temperature):
    """根据天气状况和温度给出贴心建议"""
    # 特殊天气优先
    if "雨" in weather:
        return "今天有雨，出门记得带伞哦"
    if "雪" in weather:
        return "今天有雪，路滑注意安全，多穿点"
    if "雾" in weather or "霾" in weather:
        return "今天有雾霾，出门记得戴口罩"
    if "风" in weather:
        return "今天风大，注意防风保暖"
    # 温度建议
    if temperature >= 35:
        return "高温预警！尽量减少外出，注意防暑降温"
    if temperature >= 28:
        return "天气较热，注意多喝水防中暑"
    if temperature >= 23:
        return "温度适宜，适合外出活动"
    if temperature >= 10:
        return "天气微凉，记得添件外套"
    if temperature >= 0:
        return "天气较冷，注意保暖防寒"
    return "天气很冷，出门务必穿厚衣服"


sid1 = get_weather_advice(wea1, temperature1)
sid2 = get_weather_advice(wea2, temperature2)

# 提醒吃饭
now_time = get_beijing_time().hour
eat = ""
m_n_a = ""
if 9 > now_time >= 0:       # 凌晨0点~早9点前（含0点，深夜/清晨统一问候）
    eat = get_morning_words()
    m_n_a = "早上好吖！"
if 12 > now_time >= 9:
    eat = get_morning_words()
    m_n_a = "上午好吖！"
if 14 > now_time >= 12:
    eat = get_eatmorning_words()
    m_n_a = "中午好吖！"
if 18 > now_time >= 14:
    eat = get_afternoon_words()
    m_n_a = "下午好吖！"
if 24 >= now_time >= 18:
    eat = get_goodnight_words()
    m_n_a = "傍晚时分！"


# 打卡提醒
def check_time():
    # 获取当前北京时间
    current_time = get_beijing_time()

    # 判断当前时间是否已经过了中午12点
    if current_time.hour >= 12:
        return "下班打卡"
    else:
        return "上班打卡"


# 数据整理
data = {"m_n_a": {"value": m_n_a, "color": get_random_color()},
        "eat": {"value": eat, "color": get_random_color()},
        "city1": {"value": city1, "color": get_random_color()},
        "daytime": {"value": get_weekday()[0], "color": get_random_color()},
        "nongli": {"value": get_weekday()[1], "color": get_random_color()},
        "weather1": {"value": wea1, "color": get_random_color()},
        "temperature1": {"value": str(temperature1) + "摄氏度", "color": get_random_color()},
        "sid": {"value": sid1, "color": get_random_color()},
        "sid2": {"value": sid2, "color": get_random_color()},
        "birthday_lover": {"value": get_birthday(birthday_lover), "color": get_random_color()},
        "birthday_my": {"value": get_birthday(birthday_my), "color": get_random_color()},
        "yd": {"value": j_yd, "color": get_random_color()},
        "cj": {"value": j_cj, "color": get_random_color()},
        "city2": {"value": city2, "color": get_random_color()},
        "weather2": {"value": wea2, "color": get_random_color()},
        "temperature2": {"value": str(temperature2) + "摄氏度", "color": get_random_color()},
        "tv": {"value": top_tv(), "color": get_random_color()},
        "mv": {"value": top_mv(), "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()},
        "yiji": {"value": get_yi_ji(), "color": get_random_color()},
        "food": {"value": get_food(), "color": get_random_color()},
        "weibo": {"value": get_weibo_hot(), "color": get_random_color()},
        "punch": {"value": check_time(), "color": get_random_color()}
        }

"""
4、实例化微信客户端
"""
# 模拟登录微信客户端
client = WeChatClient(app_id, app_secret)
# 实例化微信客户端
wm = WeChatMessage(client)

"""
5、发送消息
"""
# 参数 接收对象、消息模板ID、数据（消息模板里面的的变量与字典数据做匹配）
for i in range(0, len(user_id1)):
    res = wm.send_template(user_id1[i], template_id, data)
    # 取出本次要发送的字段值
    v = {k: data[k]["value"] for k in data}
    v["daytime"] = v["daytime"].strip()
    v["nongli"] = v["nongli"].strip()
    v["words"] = v["words"].strip()

    message = f"""
{'=' * 40}
消息已推送至ID为 {user_id1[i]} 的微信用户
{'=' * 40}
💬 {v['m_n_a']}
🎊 {v['eat']}

⏰ 记得{v['punch']}哦！
📅 {v['daytime']}　
农历：{v['nongli']}

🌤️ To 噜妹～
城市：{v['city1']}
天气：{v['weather1']}　{v['temperature1']}
距离生日还有 {v['birthday_lover']} 天
提醒：{v['sid']}

🌤️ To 噜哥～
城市：{v['city2']}
天气：{v['weather2']}　{v['temperature2']}
距离生日还有 {v['birthday_my']} 天
提醒：{v['sid2']}

💞 这是我们在一起的第 {v['love_days']} 天
🎉 距离元旦 {v['yd']} 天，距离春节 {v['cj']} 天

📜 今日宜忌：{v['yiji']}
🍜 美食推荐：{v['food']}
🔥 微博热搜：{v['weibo']}

📺 今日剧：{v['tv']}
🎬 今日影：{v['mv']}
♥️ 每日一句：{v['words']}
"""
    print(message)


