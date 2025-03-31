import ncatbot_sync
from ncatbot_sync.client import BotClient
from ncatbot_sync.logger import get_logger
from ncatbot_sync.message import GroupMessage, PrivateMessage, NoticeMessage, RequestMessage

log = get_logger()
# 通过预设置的类型，设置需要监听的事件通道
# intents = ncatbot_sync.Intents.none()
# intents.group_message=True

# 通过kwargs，设置需要监听的事件通道
intents = ncatbot_sync.Intents(group_message=True, 
                               private_message=True,
                               notice_message=True)
bot = BotClient(intents=intents)

@bot.on_message(GroupMessage, group_id=322645753)  # 函数接受一个必须参数和多个可选参数*kwargs
def group_message_handler(message: GroupMessage):
    log.info(message.raw_message)
    if message.raw_message == "测试":
        bot.onebot11.send_msg("NcatBot 测试成功喵~", group_id=message.group_id)

@bot.on_message(PrivateMessage, user_id=2793415370)  # 函数接受一个必须参数和多个可选参数*kwargs
def private_message_handler(message: PrivateMessage):
    log.info(message.raw_message)
    log.info(message.user_id)
    
    # 遍历 message.message 列表
    for msg in message.message:
        log.info(f"Message Type: {msg.type}")
        log.info(f"Message Data: {msg.data}")
    
    if message.raw_message == "测试":
        bot.onebot11.send_private_msg(user_id=message.user_id, message="NcatBot 测试成功喵~")
        

@bot.on_message(NoticeMessage)
def notice_message_handler(message: NoticeMessage):
    log.info(message)
    if message.sub_type == "poke":
        bot.onebot11.send_private_msg(user_id=message.user_id, message="NcatBot 戳一戳成功喵~")

# 运行方式1：自定义配置
bot.run(url="ws://localhost:3001", token="0123456789")
# 运行方式2：使用配置文件
# bot.run()