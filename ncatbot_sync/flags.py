from ncatbot_sync.message import GroupMessage, PrivateMessage, NoticeMessage, RequestMessage

class Intents:
    def __init__(self, **kwargs):
        self.group_message = kwargs.get("group_message", False)
        self.private_message = kwargs.get("private_message", False)
        self.notice_message = kwargs.get("notice_message", False)
        self.request_message = kwargs.get("request_message", False)

    @classmethod
    def public(self):
        return self(group_message=True, private_message=True, notice_message=False, request_message=False)

    def all(self):
        return self(group_message=True, private_message=True, notice_message=True, request_message=True)
    
    def group(self):
        return self(group_message=True, private_message=False, notice_message=False, request_message=False)
    
    def private(self):
        return self(group_message=False, private_message=True, notice_message=False, request_message=False)
    
    def notice(self):
        return self(group_message=False, private_message=False, notice_message=True, request_message=False)
    
    def request(self):
        return self(group_message=False, private_message=False, notice_message=False, request_message=True)
    
    
def should_handle(message, intents):
    if isinstance(message, GroupMessage):
        return intents.group_message
    if isinstance(message, PrivateMessage):
        return intents.private_message
    if isinstance(message, NoticeMessage):
        return intents.notice_message
    if isinstance(message, RequestMessage):
        return intents.request_message
    return False
