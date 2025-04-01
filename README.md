<div align="center">

# 🚀 ncatbot_sync

![background](assets/background.png)

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OneBot v11](https://img.shields.io/badge/OneBot-v11-black.svg)](https://github.com/botuniverse/onebot)
[![PyPI](https://img.shields.io/pypi/v/ncatbot-sync.svg)](https://pypi.org/project/ncatbot-sync/)
[![访问量统计](https://visitor-badge.laobi.icu/badge?page_id=li-yihao0328.ncatbot_sync)](https://gitee.com/li-yihao0328/ncatbot_sync)

基于OneBot v11协议的轻量级QQ机器人框架

[文档](docs/) | [许可证](LICENSE) | [QQ群](https://qm.qq.com/q/AmdNUkSxFY)

</div>

## 🌟 核心特性
- **多协议支持**：完整实现OneBot v11规范并支持`Napcat`、`LLonebot`、`Lagrange`多协议。
- **事件驱动架构**：支持群聊/私聊消息处理，让你可以根据不同事件灵活编写机器人逻辑。
- **高效通信**：内置高性能WebSocket客户端，确保消息的快速稳定传输。
- **模块化设计**：拥有可扩展的消息订阅机制，方便你根据需求定制功能。
- **开发者友好**：简洁直观的API设计，降低开发门槛，让开发QQ机器人变得轻松。
- **丰富功能**：支持消息发送、群组管理、文件操作等多种功能，满足多样化的使用场景。
- **专业日志**：带轮转机制的彩色日志系统，方便你查看和管理日志信息。

## ⚙️ 配置说明
在项目根目录创建 `config.yaml` 文件，配置如下：
```yaml
# 必填配置
url: "ws://your-onebot-server:port"  # 服务地址
token: "your-access-token"          # 访问令牌
```

## 🚀 快速开始

### 基础示例
```python
from ncatbot_sync import BotClient, Intents, GroupMessage

# 初始化机器人
intents = Intents(group_message=True)
bot = BotClient(intents=intents)

@bot.on_message(GroupMessage, group_id=123456)  # 监听指定群聊消息
async def handle_group_message(message: GroupMessage):
    """处理群组消息"""
    bot.onebot11.send_msg("收到消息！", group_id=message.group_id)

bot.run()
```

### 高级功能示例
```python
# 发送复合消息
diy_message = [
    bot.onebot11.face(id=1),
    bot.onebot11.text("带表情的消息"),
    bot.onebot11.image(file="http://example.com/image.png")
]
bot.onebot11.send_msg(diy_message, group_id=123456)

# 处理好友请求
from ncatbot_sync import RequestMessage

@bot.on_message(RequestMessage)
def handle_friend_request(message: RequestMessage):
    if message.sub_type == "friend":
        bot.onebot11.set_friend_add_request(flag=message.flag, approve=True)
```

## 📚 功能矩阵
| 功能类别       | 已实现接口                   | 状态  |
|----------------|-----------------------------|-------|
| **消息管理**   | 发送消息/图片/表情           | ✅    |
| **群组操作**   | 禁言/踢人/设置管理员         | ✅    |
| **文件管理**   | 上传/下载群文件              | ✅    |
| **系统监控**   | 获取状态/扩展数据            | ✅    |
| **事件处理**   | 加好友/加群请求处理          | ✅    |
| **高级功能**   | 转发消息/在线状态设置        | ✅    |

## 🧩 开发指南

### 定时任务(待开发，后续实现)
```python
from ncatbot_sync.tools import schedule_task

@schedule_task(hours=1)
def hourly_task():
    """每小时执行的定时任务"""
    bot.onebot11.send_group_msg("整点报时！", group_id=123456)
```

### 事件处理
项目支持多种事件处理，包括群消息、私聊消息、通知消息和请求消息。可以通过 `Intents` 类来选择需要处理的事件类型，例如：
```python
from ncatbot_sync import BotClient, Intents, GroupMessage, PrivateMessage

# 监听群消息和私聊消息
intents = Intents(group_message=True, private_message=True)
bot = BotClient(intents=intents)

@bot.on_message(GroupMessage, group_id=123456)
def handle_group_message(message: GroupMessage):
    """处理群组消息"""
    bot.onebot11.send_msg("收到群消息！", group_id=message.group_id)

@bot.on_message(PrivateMessage, user_id=456789)
def handle_private_message(message: PrivateMessage):
    """处理私聊消息"""
    bot.onebot11.send_msg("收到私聊消息！", user_id=message.user_id)

bot.run()
```

### 消息构造
可以使用 `api.py` 中提供的方法来构造不同类型的消息段，例如：
```python
# 构造回复消息段
reply_msg = bot.onebot11.reply(message_id=123)

# 构造戳一戳消息段
poke_msg = bot.onebot11.poke(type=1, id=2)

# 构造XML消息段
xml_msg = bot.onebot11.xml(data="<xml>...</xml>")
```

### 文件操作
支持上传和下载群文件，示例如下：
```python
# 上传群文件
bot.onebot11.upload_group_file(group_id=123456, file="path/to/your/file.txt", name="file.txt")

# 下载文件
file = bot.onebot11.get_file(file_id="file_id")
```

## 😃 开发进度
- [ ] 插件系统搭建
- [ ] 插件市场
- [ ] markdown实现发送

## 🤝 参与贡献
欢迎通过 Issue 或 Pull Request 参与项目开发！请先阅读 [贡献指南](CONTRIBUTING.md)。

### 贡献者
<a href="https://github.com/eryajf/learn-github/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=liyihao1110/ncatbot_sync" />
</a>

---

<div align="center">

如果你在使用过程中遇到任何问题，欢迎在 [GitHub Issues](https://github.com/liyihao1110/ncatbot_sync/issues) 中反馈。感谢你的支持！
![image](https://uapis.cn/api/imgapi/acg/pc.php)
</div>