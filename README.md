# ncatbot_sync

[English Docs](README.en.md) | [许可证](LICENSE)

基于 OneBot v11 协议的轻量级QQ机器人框架

## 特性
- 支持群聊/私聊消息处理
- 事件驱动架构
- 内置 WebSocket 客户端
- OneBot v11 API 封装
- 可配置的消息订阅机制
- 带日志轮转和彩色输出的日志系统

## 安装
```bash
git clone https://gitee.com/li-yihao0328/ncatbot_sync.git
cd ncatbot_sync
pip install -r requirements.txt
```

## 配置
1. 在项目根目录创建 `config.yaml`:
```yaml
url: "ws://你的OneBot服务地址:端口"
token: "你的访问令牌"
```

## 使用示例
```python
from ncatbot_sync import BotClient, Intents

# 配置需要处理的消息类型
intents = Intents(group_message=True)
bot = BotClient(intents=intents)

@bot.on_message(GroupMessage, group_id=123456)
async def 消息处理器(message):
    bot.onebot11.send_msg("你好世界！", group_id=message.group_id)

bot.run()
```

## 已实现功能
✅ 消息发送  
✅ 群组管理  
✅ 事件处理  
✅ 文件操作  
✅ 系统状态  
✅ 好友请求处理

## 许可证
MIT 许可证