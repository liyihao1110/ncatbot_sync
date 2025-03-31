# ncatbot_sync

[中文文档](README.md) | [License](LICENSE)

A lightweight QQ bot framework based on OneBot v11 protocol

## Features
- Support group/private message handling
- Event-driven architecture
- Built-in WebSocket client
- API wrapper for OneBot v11
- Configurable message intents
- Logging with rotation and color output

## Installation
```bash
git clone https://gitee.com/li-yihao0328/ncatbot_sync.git
cd ncatbot_sync
pip install -r requirements.txt
```

## Configuration
1. Create `config.yaml` in project root:
```yaml
url: "ws://your-onebot-server:port"
token: "your-access-token"
```

## Usage
```python
from ncatbot_sync import BotClient, Intents

intents = Intents(group_message=True)
bot = BotClient(intents=intents)

@bot.on_message(GroupMessage, group_id=123456)
async def handler(message):
    bot.onebot11.send_msg("Hello World!", group_id=message.group_id)

bot.run()
```

## API Support
✅ Message sending  
✅ Group management  
✅ Event handling  
✅ File operations  
✅ System status  
✅ Friend requests

## License
MIT License