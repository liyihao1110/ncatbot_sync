import ncatbot_sync
from ncatbot_sync.client import BotClient
from ncatbot_sync.logger import get_logger
from ncatbot_sync.message import GroupMessage, PrivateMessage, NoticeMessage, RequestMessage

log = get_logger()

# 通过预设置的类型，设置需要监听的事件通道
# intents = ncatbot_sync.Intents.public()
# intents.notice_message=True

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
    
    if message.raw_message == "测试":

        # demo1: 私聊消息发送
        # bot.onebot11.send_private_msg(user_id=message.user_id, message="NcatBot 测试成功喵~")
        
        # demo2: 自定义消息发送
        diy_message = [
            bot.onebot11.face(id=1),
            bot.onebot11.text("NcatBot 测试成功喵~")
        ]
        # bot.onebot11.send_msg(diy_message, user_id=message.user_id)

        # demo3: 转发消息发送
        diy_message_1 = [{
            "type": "node",
            "data": {
                "name": "消息节点",
                "uin": "2793415370",
                "content": "测试消息"
            }
        }]
        # bot.napcat.send_forward_msg(diy_message_1, user_id=message.user_id)

        # demo4: 戳一戳
        # bot.napcat.friend_poke(user_id=message.user_id)

        # demo5: 设置在线状态
        # 1.设置基础状态：在线
        bot.napcat.set_online_status(ncatbot_sync.StatusType.ONLINE)
        # 2. 设置扩展状态：听歌中
        # bot.napcat.set_online_status(ncatbot_sync.StatusType.LISTENING)
        # 3. 设置带电池状态
        # bot.napcat.set_online_status(ncatbot_sync.StatusType.BATTERY, battery_status=75)
        # 4. 使用离散参数
        # bot.napcat.set_online_status(10, 1000, 50)
        
        

@bot.on_message(NoticeMessage)
def notice_message_handler(message: NoticeMessage):
    log.info(message)
    if message.sub_type == "poke":
        bot.onebot11.send_private_msg(user_id=message.user_id, message="NcatBot 戳一戳成功喵~")

@bot.on_message(RequestMessage)
def request_message_handler(message: RequestMessage):
    log.info(message)
    if message.sub_type == "friend":
        bot.onebot11.send_private_msg(user_id=message.user_id, message="NcatBot 好友请求成功喵~")

if __name__ == "__main__":
    # 运行方式1：自定义配置
    bot.run(url="ws://localhost:3001", token="0123456789")
    # 运行方式2：使用配置文件
    # bot.run()