import time

from .api import Onebot11API
from .logger import get_logger

log = get_logger()

class BotClient:
    def __init__(self, intents):
        self.intents = intents
        self.handlers = {}
        self.websocket_client = None
        self.onebot11 = None

    def on_message(self, message_type, **conditions):
        def decorator(func):
            if message_type not in self.handlers:
                self.handlers[message_type] = []
            self.handlers[message_type].append((func, conditions))
            return func
        return decorator

    def run(self, url=None, token=None):
        from .config import load_config
        from .connect import WebSocketClient
        
        if url is None or token is None:
            config = load_config()
            url = url or config.url
            token = token or config.token

        self.onebot11 = Onebot11API(self)
        
        self.websocket_client = WebSocketClient(
            url=url,
            token=token,
            on_message=self._handle_message
        )
        self.websocket_client.connect()
        is_record = self.onebot11.can_send_record()
        is_image = self.onebot11.can_send_image()
        status = self.onebot11.get_status()
        version_info = self.onebot11.get_version_info()
        log.info("连接检查：%s;%s;机器人QQ状态：%s;客户端版本信息：%s", "可以发送语音" if is_record else "不可以发送语音", "可以发送图片" if is_image else "不可以发送图片", "在线" if status["online"]==True else "不在线", version_info['app_name']+version_info['app_version'])
        try:
            while True:
                time.sleep(1)
                if self.websocket_client.is_quit:
                    self.websocket_client._close()
                    break
        except KeyboardInterrupt:
            self.websocket_client._close()

    def _handle_message(self, message):
        from .message import parse_message
        from .flags import should_handle
        
        parsed = parse_message(message)
        if not parsed or not should_handle(parsed, self.intents):
            return

        handlers = self.handlers.get(type(parsed), [])
        for handler, conditions in handlers:
            if all(
                getattr(parsed, key, None) == value if value != all else True
                for key, value in conditions.items()
            ):
                handler(parsed)
