import configparser
import os
import random
import time
from datetime import datetime, timedelta

import requests
import zhdate
from bs4 import BeautifulSoup
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

"""
1、从配置文件中获取变量
"""
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
        "阳光明媚，心情也跟着明亮。",
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
        "无论如何，早起的鸟儿有虫吃！"
    ]

    # 随机选择一句话
    random_inspiration = random.choice(morning_inspirations)
    return random_inspiration


def get_eatmorning_words():
    list = [
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
        "中午好，愿你的事业蒸蒸日上！"
    ]

    return list[random.randint(0, len(list) - 1)]


def get_afternoon_words():
    list = [
        "期待下午的阳光洒满心田。",
        "下午的时间，总是充满希望。",
        "盼望下午能有一个小小的休息。",
        "希望下午的时光如诗如画。",
        "下午，期待着美好的一切到来。",
        "下午的宁静，给了我满满的动力。",
        "期待下午有更多的美好发现。",
        "下午的阳光，洒进了我的心房。",
        "期待下午的时间更加充实。",
        "下午，是放松心情的时刻。"
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
        "下午的光景是一天中最温暖的时光。"
    ]

    return list[random.randint(0, len(list) - 1)]


def get_goodnight_words():
    list = [
        '傍晚愉快，愿你收获美好时光！',
        '夕阳西下，愿你心情如霞光灿烂！',
        '傍晚微风轻拂，愿你惬意自在！',
        '祝你傍晚温馨，夜晚安然入梦！',
        '黄昏美好，愿你放松身心，快乐相伴！',
        '夕阳无限美，愿你笑颜常在！',
        '傍晚安好，愿你享受宁静时光！',
        '夜幕降临，愿你温暖不减，幸福依然！',
        '晚霞如诗，愿你的心情也如诗般美好！',
        '傍晚微凉，愿你温暖如初，幸福绵长！'
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
        '夜色朦胧，愿你安心入梦！'
    ]

    return list[random.randint(0, len(list) - 1)]


def get_beijing_time():
    return datetime.now() + timedelta(hours=8)
    # return datetime.now() + timedelta()


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
    weekd = ''
    # 日期时间
    date = (get_beijing_time()).strftime("%Y-%m-%d %X")
    # 农历日期
    now = get_beijing_time()

    # 获取农历日期
    nongli_date = zhdate.ZhDate.from_datetime(now)  # 使用北京时间获取农历日期
    # 获取农历日期的中文大写格式
    nongli_date_chinese = convert_date_to_chinese(nongli_date)
    # 星期
    dayOfWeek = (get_beijing_time()).weekday()
    if dayOfWeek == 0:
        weekd = date + "  星期一"
    if dayOfWeek == 1:
        weekd = date + "  星期二"
    if dayOfWeek == 2:
        weekd = date + "  星期三"
    if dayOfWeek == 3:
        weekd = date + "  星期四"
    if dayOfWeek == 4:
        weekd = date + "  星期五"
    if dayOfWeek == 5:
        weekd = date + "  星期六"
    if dayOfWeek == 6:
        weekd = date + "  星期日"
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
    delta = get_beijing_time() - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days + 1


# 计算距离下一次生日多少天
def get_birthday(birthday):
    today = get_beijing_time().date()  # 获取当前北京时间的日期
    next_birthday = datetime.strptime(str(today.year) + "-" + birthday, "%Y-%m-%d")

    # 如果生日已经过了，则计算明年的生日
    if next_birthday < get_beijing_time():
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)

    days_until_birthday = (next_birthday.date() - today).days  # 计算距离生日的天数
    return days_until_birthday


# 计算到元旦、春节的日期
def get_spr(yd, sp):
    today = get_beijing_time().date()  # 使用北京时间的当前日期

    # 计算元旦的日期
    next1 = datetime.strptime(str(today.year) + "-" + yd, "%Y-%m-%d")
    if next1 < get_beijing_time():
        next1 = next1.replace(year=next1.year + 1)
        j_yd = (next1.date() - today).days  # 计算元旦距离今天的天数
    else:
        j_yd = (next1.date() - today).days  # 计算元旦距离今天的天数

    # 计算春节的日期
    next2 = datetime.strptime(str(today.year) + "-" + sp, "%Y-%m-%d")
    if next2 < get_beijing_time():
        next2 = next2.replace(year=next2.year + 1)
        j_cj = (next2.date() - today).days  # 计算春节距离今天的天数
    else:
        next2 = next2.replace(year=next2.year + 1)
        j_cj = (next2.date() - today).days  # 计算春节距离今天的天数

    return j_yd, j_cj


# 每日金句
def get_words():
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
        "我的心里，住着一个可爱的你。"
    ]
    try:
        response = requests.get("https://api.shadiao.pro/chp", timeout=5)  # 设置超时时间
        response.raise_for_status()  # 如果状态码不是 200，会抛出 HTTPError
        text = response.json().get('data', {}).get('text', '')

        # 如果文本的长度大于 20 个字，则重新请求
        if len(text) > 20:
            return get_words()
        return text
    except (requests.RequestException, ValueError):  # 捕获请求异常和 JSON 解析异常
        return random.choice(words_list)  # 返回备用句子


# 字体颜色，随机 每次不一样
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 电影
def top_mv():
    url = "https://movie.douban.com/chart"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        ),
        "Referer": "https://movie.douban.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": (
            "bid=gBOB68qc6u4; "
            "_pk_id.100001.4cf6=a839b0f6b22f3b72.1754645362.; "
            "_pk_ses.100001.4cf6=1; ap_v=0,6.0; "
            "__utma=30149280.695913436.1754645363.1754645363.1754645363.1; "
            "__utmb=30149280.0.10.1754645363; __utmc=30149280; "
            "__utmz=30149280.1754645363.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); "
            "__utma=223695111.1773430490.1754645363.1754645363.1754645363.1; "
            "__utmc=223695111; "
            "__utmz=223695111.1754645363.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); "
            "__utmt=1; __utmb=223695111.1.10.1754645363"
        )
    }

    # 随机延时，降低被反爬概率
    time.sleep(random.uniform(1, 3))

    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                break
            else:
                time.sleep(2)
        except requests.RequestException:
            time.sleep(2)
    else:
        return "暂时无法获取电影信息"

    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select('.pl2')

    movie_list = []
    for item in items:
        full_title = item.a.get_text(strip=True)
        name = full_title.split('/')[0].strip()
        rating = item.find_next('span', class_='rating_nums')
        score = rating.text.strip() if rating else "暂无评分"
        movie_list.append((name, score))

    if movie_list:
        movie_name, rating = random.choice(movie_list)
        return f"《{movie_name}》{rating}分"
    else:
        return "暂时无法获取电影信息"


"""
3、调用函数，获取数据，保存为字典格式数据
"""
# 获取天气和温度
wea1, temperature1 = get_weather(city1)
wea2, temperature2 = get_weather(city2)

# 计算到春节的天数
j_yd, j_cj = get_spr(yd, sp)
# 如果温度过高，提示语
sid = ""
if temperature1 >= 23:
    sid = "室外温度较高，注意喝水哦"
elif temperature1 <= 17:
    sid = "室外温度过低，记得多穿点衣服保暖"
else:
    sid = "温度不高不低，但也要注意及时补水哦"

# 提醒吃饭
now_time = get_beijing_time().hour
eat = ""
m_n_a = ""
if 9 > now_time > 0:
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
        "sid": {"value": sid, "color": get_random_color()},
        "birthday_lover": {"value": get_birthday(birthday_lover), "color": get_random_color()},
        "yd": {"value": j_yd, "color": get_random_color()},
        "cj": {"value": j_cj, "color": get_random_color()},
        "city2": {"value": city2, "color": get_random_color()},
        "weather2": {"value": wea2, "color": get_random_color()},
        "temperature2": {"value": str(temperature2) + "摄氏度", "color": get_random_color()},
        "mv": {"value": top_mv(), "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()},
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
    print(f"\n消息已推送至ID为{user_id1[i]}的微信用户，推送内容如下：\n"
          f"  {data['m_n_a']['value']}\n"
          f"  {data['eat']['value']}\n"
          f"  所在城市：{data['city1']['value']}\n"
          f"  当前时间：{data['daytime']['value'].strip()}\n"
          f"  农历：{data['nongli']['value'].strip()}\n"
          f"  今日天气：{data['weather1']['value']}\n"
          f"  当前温度：{data['temperature1']['value']}\n"
          f"  {data['sid']['value']}\n"
          f"  距离生日还有{data['birthday_lover']['value']}天\n"
          f"  距离元旦还有{data['yd']['value']}天\n"
          f"  距离春节还有{data['cj']['value']}天\n"
          f"  我们已经在一起{data['love_days']['value']}天啦\n"
          f"  ===家乡:{data['city2']['value']} 天气:{data['weather2']['value']} 气温:{data['temperature2']['value']}===\n"
          f"  今日电影推荐：{data['mv']['value']}\n"
          f"  每日一句：{data['words']['value'].strip()}\n")
