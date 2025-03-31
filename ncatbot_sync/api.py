import json
from ncatbot_sync.logger import get_logger

log = get_logger()

class Onebot11API:
    def __init__(self, client):
        self.client = client

    def _send_request(self, action, params=None, expect_data=True):
        """统一发送请求并处理响应"""
        if params is None:
            params = {}
        message = {
            "action": action,
            "params": params
        }
        try:
            response = self.client.websocket_client._send(json.dumps(message))
            
        except json.JSONDecodeError as e:
            log.error(f"JSON解析失败: {e}")
            return None
        except Exception as e:
            log.error(f"请求发送失败: {e}")
            return None
        
        if response.get("status") == "ok":
            return response.get("data") if expect_data else True
        else:
            log.warning(f"API调用失败: {action}, 错误信息: {response}")
            return None

    # region 消息相关API
    def send_private_msg(self, user_id, message, auto_escape=False):
        params = {
            "user_id": user_id,
            "message": message,
            "auto_escape": auto_escape
        }
        data = self._send_request("send_private_msg", params)
        return data.get("message_id") if data else None

    def send_group_msg(self, group_id, message, auto_escape=False):
        params = {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        }
        data = self._send_request("send_group_msg", params)
        return data.get("message_id") if data else None

    def send_msg(self, message, message_type=None, group_id=None, user_id=None, auto_escape=False):
        params = {
            "message": message,
            "auto_escape": auto_escape
        }
        if message_type:
            params["message_type"] = message_type
        elif group_id is not None:
            params.update({"group_id": group_id, "message_type": "group"})
        elif user_id is not None:
            params.update({"user_id": user_id, "message_type": "private"})
        else:
            raise ValueError("需指定group_id、user_id或message_type")
        data = self._send_request("send_msg", params)
        return data.get("message_id") if data else None

    def delete_msg(self, message_id):
        return self._send_request("delete_msg", {"message_id": message_id}, False)

    def get_msg(self, message_id):
        return self._send_request("get_msg", {"message_id": message_id})

    def get_forward_msg(self, forward_id):
        return self._send_request("get_forward_msg", {"id": forward_id})
    # endregion

    # region 群组管理API
    def set_group_kick(self, group_id, user_id, reject_add=False):
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add
        }
        return self._send_request("set_group_kick", params, False)

    def set_group_ban(self, group_id, user_id, duration=1800):
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        return self._send_request("set_group_ban", params, False)

    def set_group_anonymous_ban(self, group_id, anonymous=None, flag=None, duration=1800):
        params = {"group_id": group_id, "duration": duration}
        if anonymous:
            params["anonymous"] = anonymous
        elif flag:
            params["anonymous_flag"] = flag
        else:
            raise ValueError("需提供anonymous或flag参数")
        return self._send_request("set_group_anonymous_ban", params, False)

    def set_group_whole_ban(self, group_id, enable=True):
        return self._send_request("set_group_whole_ban", {
            "group_id": group_id,
            "enable": enable
        }, False)

    def set_group_admin(self, group_id, user_id, enable=True):
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        }
        return self._send_request("set_group_admin", params, False)

    def set_group_anonymous(self, group_id, enable=True):
        return self._send_request("set_group_anonymous", {
            "group_id": group_id,
            "enable": enable
        }, False)

    def set_group_card(self, group_id, user_id, card=""):
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        }
        return self._send_request("set_group_card", params, False)

    def set_group_name(self, group_id, group_name):
        return self._send_request("set_group_name", {
            "group_id": group_id,
            "group_name": group_name
        }, False)

    def set_group_leave(self, group_id, dismiss=False):
        return self._send_request("set_group_leave", {
            "group_id": group_id,
            "is_dismiss": dismiss
        }, False)

    def set_group_special_title(self, group_id, user_id, title="", duration=-1):
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": title,
            "duration": duration
        }
        return self._send_request("set_group_special_title", params, False)
    # endregion

    # region 请求处理API
    def set_friend_add_request(self, flag, approve=True, remark=""):
        params = {
            "flag": flag,
            "approve": approve,
            "remark": remark
        }
        return self._send_request("set_friend_add_request", params, False)

    def set_group_add_request(self, flag, req_type, approve=True, reason=""):
        params = {
            "flag": flag,
            "type": req_type,
            "approve": approve,
            "reason": reason
        }
        return self._send_request("set_group_add_request", params, False)
    # endregion

    # region 信息获取API
    def get_login_info(self):
        return self._send_request("get_login_info")

    def get_stranger_info(self, user_id, no_cache=False):
        return self._send_request("get_stranger_info", {
            "user_id": user_id,
            "no_cache": no_cache
        })

    def get_friend_list(self):
        return self._send_request("get_friend_list")

    def get_group_info(self, group_id, no_cache=False):
        return self._send_request("get_group_info", {
            "group_id": group_id,
            "no_cache": no_cache
        })

    def get_group_list(self):
        return self._send_request("get_group_list")

    def get_group_member_info(self, group_id, user_id, no_cache=False):
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache
        }
        return self._send_request("get_group_member_info", params)

    def get_group_member_list(self, group_id):
        return self._send_request("get_group_member_list", {"group_id": group_id})

    def get_group_honor_info(self, group_id, honor_type):
        return self._send_request("get_group_honor_info", {
            "group_id": group_id,
            "type": honor_type
        })
    # endregion

    # region 实用功能API
    def send_like(self, user_id, times=1):
        return self._send_request("send_like", {
            "user_id": user_id,
            "times": times
        }, False)

    def get_cookies(self, domain=""):
        data = self._send_request("get_cookies", {"domain": domain})
        return data.get("cookies") if data else None

    def get_csrf_token(self):
        data = self._send_request("get_csrf_token")
        return data.get("token") if data else None

    def get_credentials(self, domain=""):
        return self._send_request("get_credentials", {"domain": domain})

    def get_record(self, file_id, format):
        data = self._send_request("get_record", {
            "file": file_id,
            "out_format": format
        })
        return data.get("file") if data else None

    def get_image(self, file_id):
        data = self._send_request("get_image", {"file": file_id})
        return data.get("file") if data else None

    def can_send_image(self):
        data = self._send_request("can_send_image")
        return data.get("yes") if data else False

    def can_send_record(self):
        data = self._send_request("can_send_record")
        return data.get("yes") if data else False
    # endregion

    # region 系统相关API
    def get_status(self):
        return self._send_request("get_status")

    def get_version_info(self):
        return self._send_request("get_version_info")

    def set_restart(self, delay=0):
        return self._send_request("set_restart", {"delay": delay}, False)

    def clean_cache(self):
        return self._send_request("clean_cache", expect_data=False)
    # endregion
