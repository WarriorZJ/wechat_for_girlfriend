# WeChat For Girlfriend ❤️

一个用 Python + 微信测试号，每天定时给女朋友（以及自己）推送暖心消息的小项目。
除了主程序 `main.py`，仓库里还收集了大量表白 / 浪漫向的小动画代码（爱心、玫瑰花、圣诞树等），持续更新中。

---

## ✨ 功能特性

`main.py` 每次运行会生成并推送一条「每日关怀」消息，内容包含：

- 📅 当前日期、星期、农历日期
- 🌤️ 两个城市的实时天气、温度与贴心穿衣建议（高德天气 API）
- 💞 在一起天数（从 `start_date` 算起）
- 🎂 距离双方生日、元旦、春节还有多少天
- 📺 豆瓣热门国产剧 / 电影随机推荐
- 💌 随机早安 / 午安 / 下午好 / 晚安问候语（按运行时段自动切换）
- 🌟 每日一句情话（优先调用在线 API，失败则回退本地句库）
- ⏰ 上班 / 下班打卡提醒

消息通过微信测试号的**模板消息**推送到指定用户（支持多个 `user_id`）。

> 其余脚本（`seven_stars.py`、`test.py`、各 `代码合集` / `html爱心代码` / `shengds`）为独立的可运行小动画，不属于定时推送主流程，按需取用即可。

---

## 📁 目录结构

```
wechat_for_girfriend/
├── main.py                 # 主程序：每日微信推送（数据获取 + 模板消息）
├── config.conf             # 配置文件（含私密信息，请勿提交到公开仓库）
├── requirements.txt        # Python 依赖
├── seven_stars.py          # 🐢 turtle 绘制的「七星连珠」星空动画
├── test.py                 # 💗 tkinter 绘制的动态爱心动画
├── code合集(持续更新中)/     # 各类 Python 爱心 / 玫瑰花 / 表白代码（含效果图）
│   ├── 玫瑰花/
│   ├── 漂浮爱心/
│   ├── 满屏飘字表白代码/
│   ├── 无限弹窗表白代码/
│   ├── python红粉爱心/  python彩色爱心代码/  python粒子组成爱心代码/ ...
│   └── ...
├── html爱心代码/            # 网页版爱心动画（HTML/CSS/JS）
│   ├── 魔方爱心和文字/  蓝色粒子爱心/  蓝色变化钻石爱心/  红色爱心 i love you/  爱情表白信/ ...
└── shengds/                # 圣诞树主题网页动画（HTML/CSS/JS/素材）
    ├── 银色圣诞树/  线条圣诞树/  白色圣诞树/  旋转圣诞树/  彩带圣诞树/  小塔圣诞树/
```

---

## 🔧 环境要求

- Python 3.8+
- 一个**微信测试号**（用于模板消息推送）：<https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login>

---

## 🚀 安装与配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 `config.conf`

复制 / 编辑根目录下的 `config.conf`，按注释填写你自己的信息：

```ini
[info]
# 元旦、春节日期（用于倒计时）
yd=01-01
sp=02-06

# 在一起的起始日期，格式 YYYY-MM-DD
start_date=2026-04-06

# 女朋友所在城市（可写省/市/区，用于天气匹配）
city1=石家庄
# 女朋友的家乡（用于天气匹配）
city2=北京

# 双方生日，只写 月-日
birthday_lover=03-22
birthday_my=11-26

# 以下为微信测试号参数（在测试号后台申请时自动生成）
app_id=你的_app_id
app_secret=你的_app_secret

# 模板消息 ID（在测试号后台「模板消息接口」中新增并复制）
template_id=你的_template_id

# 接收消息的用户 OpenID，多个用逗号分隔
# 让你的女朋友扫描测试号二维码关注后，在后台「用户列表」复制其 OpenID
user_id=oiIRR7xxxxxxxxxx,oiIRR7yyyyyyyyyy
```

> 📌 天气功能默认使用代码中内置的高德 `api_key`。如需更换，可修改 `main.py` 里 `get_weather()` 的 `api_key` 参数（自行申请：<https://lbs.amap.com/>）。

### 3. 创建微信推送模板

在测试号后台「模板消息接口」新建一个模板，字段需与 `main.py` 中的 `data` 字典一一对应：

| 模板变量 | 含义 |
|---|---|
| `{{m_n_a}}` | 时段问候（早/上/中/下/傍晚好） |
| `{{eat}}` | 随机祝福语 |
| `{{city1}}` / `{{city2}}` | 两个城市名 |
| `{{daytime}}` | 公历日期 + 星期 |
| `{{nongli}}` | 农历日期 |
| `{{weather1}}` / `{{weather2}}` | 天气状况 |
| `{{temperature1}}` / `{{temperature2}}` | 温度 |
| `{{sid}}` / `{{sid2}}` | 穿衣 / 天气建议 |
| `{{birthday_lover}}` / `{{birthday_my}}` | 距双方生日天数 |
| `{{yd}}` / `{{cj}}` | 距元旦 / 春节天数 |
| `{{tv}}` / `{{mv}}` | 今日剧 / 影推荐 |
| `{{love_days}}` | 在一起天数 |
| `{{words}}` | 每日情话 |
| `{{punch}}` | 打卡提醒（上班 / 下班） |

---

## ▶️ 运行

```bash
python main.py
```

程序会读取 `config.conf`、拉取各项数据，并把消息推送到 `user_id` 对应的用户。
（推送逻辑在 `main.py` 步骤 5 中，正式发送请取消 `wm.send_template(...)` 那行的注释。）

### 其他小动画

```bash
python seven_stars.py   # 七星连珠星空动画（需图形界面）
python test.py          # 动态爱心动画（需图形界面）
```

HTML 类动画（如 `html爱心代码/`、`shengds/`）直接用浏览器打开对应的 `index.html` / `*.html` 即可。

---

## ⏰ 定时推送（建议）

让机器人每天自动跑，推荐用系统的定时任务（下面以 macOS / Linux 的 `crontab` 为例）：

```bash
# 每天早 8:00 推送
0 8 * * * /usr/bin/python3 /绝对路径/wechat_for_girfriend/main.py >> push.log 2>&1
```

> 部署到云服务器时同理，注意服务器时区设为 `Asia/Shanghai`（程序内部已按东八区计算）。

---

## 🔒 安全提醒

- `config.conf` 含有 `app_secret`、`user_id` 等**私密信息**。当前仓库未配置 `.gitignore`，若推送到公开仓库，请务必：
  1. 将 `config.conf` 加入 `.gitignore`；
  2. 用 `config.conf.example` 提供脱敏模板；
  3. 如已泄露 `app_secret`，请到测试号后台**重置密钥**。
- 切勿把真实 `app_id` / `app_secret` / `user_id` 提交进版本库。

---

## 📝 说明

- 本项目为个人情感向小工具，代码风格偏向「能跑就行」，欢迎按需改造。
- `代码合集(持续更新中)` 持续补充新的表白 / 浪漫动画，欢迎一起丰富。
