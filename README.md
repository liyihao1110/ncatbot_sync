<div align="center">

# 🚀 ncatbot_sync

![background](assets/background.png)

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OneBot v11](https://img.shields.io/badge/OneBot-v11-black.svg)](https://github.com/botuniverse/onebot)
[![PyPI](https://img.shields.io/pypi/v/ncatbot-sync.svg)](https://pypi.org/project/ncatbot-sync/)
[![访问量统计](https://visitor-badge.laobi.icu/badge?page_id=li-yihao0328.ncatbot_sync)](https://gitee.com/li-yihao0328/ncatbot_sync)

基于OneBot v11协议的轻量级QQ机器人框架

[文档](docs/) | [许可证](LICENSE)

</div>

## 🌟 核心特性
- **多协议支持**：完整实现OneBot v11规范并支持`Napcat`,`LLonebot`,`Lagrange`多协议
- **事件驱动架构**：支持群聊/私聊消息处理
- **高效通信**：内置高性能WebSocket客户端
- **模块化设计**：可扩展的消息订阅机制
- **开发者友好**：简洁直观的API设计
- **丰富功能**：支持消息发送、群组管理、文件操作等
- **专业日志**：带轮转机制的彩色日志系统
## 🛠️ 安装指南
### 使用pip安装
```bash
pip install ncatbot-sync
```
### 从源码安装
```bash
git clone https://github.com/liyihao1110/ncatbot_sync.git
cd ncatbot_sync
pip install -r requirements.txt
```
## ⚙️ 配置说明
在项目根目录创建 `config.yaml`：
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
@bot.on_message(GroupMessage, group_id=123456)# 监听指定群聊消息
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
### 事件监听
```python
@bot.on_message(PrivateMessage)
def handle_private_msg(message: PrivateMessage):
    """处理私聊消息"""
    if message.raw_message == "状态":
        bot.onebot11.send_msg(f"当前温度：1000℃",user_id=message.user_id)
```
### 定时任务(待开发，后续实现)
```python
from ncatbot_sync.tools import schedule_task
@schedule_task(hours=1)
def hourly_task():
    """每小时执行的定时任务"""
    bot.onebot11.send_group_msg("整点报时！", group_id=123456)
```

## 😃 开发进度

 - [ ] 插件系统搭建
 - [ ] 插件市场
 - [ ] markdown实现发送

## 🤝 参与贡献
欢迎通过 Issue 或 Pull Request 参与项目开发！
请先阅读 [贡献指南](CONTRIBUTING.md)

---

<div align="center">

## 贡献者
<a href="https://github.com/eryajf/learn-github/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=liyihao1110/ncatbot_sync" />
</a>

</div>
