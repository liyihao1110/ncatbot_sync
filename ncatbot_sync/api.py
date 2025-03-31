import json
from typing import Union, List, Dict, Optional
from ncatbot_sync.status import Status
from ncatbot_sync.logger import get_logger

log = get_logger("api")

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
        
    # 自定义API方法
    def build_diy_api(self, action: str, params: Dict = None):
        """
        发送自定义API请求
        
        :param action: API名称
        :param params: 请求参数(可选)
        :return: 响应数据或True(如果expect_data为False)
        """
        return self._send_request(action, params, expect_data=True)

    # region 消息段构造方法
    @staticmethod
    def text(text: str) -> Dict:
        """
        构造纯文本消息段
        
        :param text: 文本内容
        :return: 消息段字典
        """
        return {
            "type": "text",
            "data": {
                "text": text
            }
        }
    @staticmethod
    def face(id: Union[int, str]) -> Dict:
        """
        构造QQ表情消息段
        
        :param id: 表情ID
        :return: 消息段字典
        """
        return {
            "type": "face",
            "data": {
                "id": str(id)
            }
        }
    @staticmethod
    def image(
        file: str,
        image_type: Optional[str] = None,
        cache: bool = True,
        proxy: bool = True,
        timeout: Optional[int] = None
    ) -> Dict:
        """
        构造图片消息段
        
        :param file: 图片文件名/URL/Base64
        :param image_type: 图片类型，flash表示闪照
        :param cache: 是否使用缓存
        :param proxy: 是否通过代理
        :param timeout: 超时时间(秒)
        :return: 消息段字典
        """
        data = {"file": file}
        if image_type:
            data["type"] = image_type
        data["cache"] = "1" if cache else "0"
        data["proxy"] = "1" if proxy else "0"
        if timeout is not None:
            data["timeout"] = str(timeout)
        return {
            "type": "image",
            "data": data
        }
    @staticmethod
    def record(
        file: str,
        magic: bool = False,
        cache: bool = True,
        proxy: bool = True,
        timeout: Optional[int] = None
    ) -> Dict:
        """
        构造语音消息段
        
        :param file: 语音文件名/URL/Base64
        :param magic: 是否变声
        :param cache: 是否使用缓存
        :param proxy: 是否通过代理
        :param timeout: 超时时间(秒)
        :return: 消息段字典
        """
        data = {"file": file}
        data["magic"] = "1" if magic else "0"
        data["cache"] = "1" if cache else "0"
        data["proxy"] = "1" if proxy else "0"
        if timeout is not None:
            data["timeout"] = str(timeout)
        return {
            "type": "record",
            "data": data
        }
    @staticmethod
    def video(
        file: str,
        cache: bool = True,
        proxy: bool = True,
        timeout: Optional[int] = None
    ) -> Dict:
        """
        构造短视频消息段
        
        :param file: 视频文件名/URL/Base64
        :param cache: 是否使用缓存
        :param proxy: 是否通过代理
        :param timeout: 超时时间(秒)
        :return: 消息段字典
        """
        data = {"file": file}
        data["cache"] = "1" if cache else "0"
        data["proxy"] = "1" if proxy else "0"
        if timeout is not None:
            data["timeout"] = str(timeout)
        return {
            "type": "video",
            "data": data
        }
    @staticmethod
    def at(qq: Union[int, str]) -> Dict:
        """
        构造@某人消息段
        
        :param qq: QQ号，可以是数字或"all"
        :return: 消息段字典
        """
        return {
            "type": "at",
            "data": {
                "qq": str(qq)
            }
        }
    @staticmethod
    def rps() -> Dict:
        """构造猜拳魔法表情消息段"""
        return {"type": "rps", "data": {}}
    @staticmethod
    def dice() -> Dict:
        """构造掷骰子魔法表情消息段"""
        return {"type": "dice", "data": {}}
    @staticmethod
    def shake() -> Dict:
        """构造窗口抖动消息段"""
        return {"type": "shake", "data": {}}
    @staticmethod
    def poke(type: Union[int, str], id: Union[int, str]) -> Dict:
        """
        构造戳一戳消息段
        
        :param type: 类型ID
        :param id: 动作ID
        :return: 消息段字典
        """
        return {
            "type": "poke",
            "data": {
                "type": str(type),
                "id": str(id)
            }
        }
    @staticmethod
    def anonymous(ignore: bool = False) -> Dict:
        """
        构造匿名消息段
        
        :param ignore: 无法匿名时是否继续发送
        :return: 消息段字典
        """
        return {
            "type": "anonymous",
            "data": {
                "ignore": "1" if ignore else "0"
            }
        }
    @staticmethod
    def share(
        url: str,
        title: str,
        content: Optional[str] = None,
        image: Optional[str] = None
    ) -> Dict:
        """
        构造链接分享消息段
        
        :param url: 链接地址
        :param title: 标题
        :param content: 内容描述(可选)
        :param image: 图片URL(可选)
        :return: 消息段字典
        """
        data = {"url": url, "title": title}
        if content:
            data["content"] = content
        if image:
            data["image"] = image
        return {
            "type": "share",
            "data": data
        }
    @staticmethod
    def contact_user(qq: Union[int, str]) -> Dict:
        """
        构造推荐好友消息段
        
        :param qq: 推荐好友的QQ号
        :return: 消息段字典
        """
        return {
            "type": "contact",
            "data": {
                "type": "qq",
                "id": str(qq)
            }
        }
    @staticmethod
    def contact_group(group_id: Union[int, str]) -> Dict:
        """
        构造推荐群消息段
        
        :param group_id: 推荐群的群号
        :return: 消息段字典
        """
        return {
            "type": "contact",
            "data": {
                "type": "group",
                "id": str(group_id)
            }
        }
    @staticmethod
    def location(
        lat: float,
        lon: float,
        title: Optional[str] = None,
        content: Optional[str] = None
    ) -> Dict:
        """
        构造位置消息段
        
        :param lat: 纬度
        :param lon: 经度
        :param title: 标题(可选)
        :param content: 内容描述(可选)
        :return: 消息段字典
        """
        data = {
            "lat": str(lat),
            "lon": str(lon)
        }
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        return {
            "type": "location",
            "data": data
        }
    @staticmethod
    def music(music_type: str, id: Union[int, str]) -> Dict:
        """
        构造音乐分享消息段
        
        :param music_type: 音乐类型(qq/163/xm)
        :param id: 歌曲ID
        :return: 消息段字典
        """
        return {
            "type": "music",
            "data": {
                "type": music_type,
                "id": str(id)
            }
        }
    @staticmethod
    def custom_music(
        url: str,
        audio: str,
        title: str,
        content: Optional[str] = None,
        image: Optional[str] = None
    ) -> Dict:
        """
        构造自定义音乐分享消息段
        
        :param url: 跳转URL
        :param audio: 音频URL
        :param title: 标题
        :param content: 内容描述(可选)
        :param image: 图片URL(可选)
        :return: 消息段字典
        """
        data = {
            "type": "custom",
            "url": url,
            "audio": audio,
            "title": title
        }
        if content:
            data["content"] = content
        if image:
            data["image"] = image
        return {
            "type": "music",
            "data": data
        }
    @staticmethod
    def reply(message_id: Union[int, str]) -> Dict:
        """
        构造回复消息段
        
        :param message_id: 回复的消息ID
        :return: 消息段字典
        """
        return {
            "type": "reply",
            "data": {
                "id": str(message_id)
            }
        }
    @staticmethod
    def forward_node(message_id: Union[int, str]) -> Dict:
        """
        构造合并转发节点消息段
        
        :param message_id: 消息ID
        :return: 消息段字典
        """
        return {
            "type": "node",
            "data": {
                "id": str(message_id)
            }
        }
    @staticmethod
    def custom_node(
        user_id: Union[int, str],
        nickname: str,
        content: Union[str, List[Dict]]
    ) -> Dict:
        """
        构造自定义合并转发节点
        
        :param user_id: 发送者QQ号
        :param nickname: 发送者昵称
        :param content: 消息内容(支持字符串或消息段列表)
        :return: 消息段字典
        """
        return {
            "type": "node",
            "data": {
                "user_id": str(user_id),
                "nickname": nickname,
                "content": content
            }
        }
    @staticmethod
    def xml(data: str) -> Dict:
        """
        构造XML消息段
        
        :param data: XML内容
        :return: 消息段字典
        """
        return {
            "type": "xml",
            "data": {
                "data": data
            }
        }
    @staticmethod
    def json(data: Union[str, Dict]) -> Dict:
        """
        构造JSON消息段
        
        :param data: JSON内容(字符串或字典)
        :return: 消息段字典
        """
        if isinstance(data, Dict):
            data = json.dumps(data)
        return {
            "type": "json",
            "data": {
                "data": data
            }
        }
    # endregion

    # region 消息相关API
    def send_private_msg(self, user_id: Union[int, str], message: Union[str, List[Dict]], auto_escape: bool = False) -> Optional[int]:
        params = {
            "user_id": int(user_id),
            "message": message,
            "auto_escape": auto_escape
        }
        data = self._send_request("send_private_msg", params)
        return data.get("message_id") if data else None
    def send_group_msg(self, group_id: Union[int, str], message: Union[str, List[Dict]], auto_escape: bool = False) -> Optional[int]:
        params = {
            "group_id": int(group_id),
            "message": message,
            "auto_escape": auto_escape
        }
        data = self._send_request("send_group_msg", params)
        return data.get("message_id") if data else None
    def send_msg(
        self,
        message: Union[str, List[Dict]],
        message_type: Optional[str] = None,
        group_id: Optional[Union[int, str]] = None,
        user_id: Optional[Union[int, str]] = None,
        auto_escape: bool = False
    ) -> Optional[int]:
        params = {"message": message, "auto_escape": auto_escape}
        if message_type:
            params["message_type"] = message_type
        elif group_id is not None:
            params.update({
                "group_id": int(group_id),
                "message_type": "group"
            })
        elif user_id is not None:
            params.update({
                "user_id": int(user_id),
                "message_type": "private"
            })
        else:
            raise ValueError("需指定group_id、user_id或message_type")
        data = self._send_request("send_msg", params)
        return data.get("message_id") if data else None
    def delete_msg(self, message_id: Union[int, str]) -> bool:
        return bool(self._send_request("delete_msg", {"message_id": int(message_id)}, False))
    def get_msg(self, message_id: Union[int, str]) -> Optional[Dict]:
        return self._send_request("get_msg", {"message_id": int(message_id)})
    def get_forward_msg(self, forward_id: Union[int, str]) -> Optional[Dict]:
        return self._send_request("get_forward_msg", {"id": str(forward_id)})
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


class NapcatAPI:
    def __init__(self, client):
        self.client = client

    def _send_request(self, action: str, params: Optional[Dict] = None, expect_data: bool = True) -> Union[Dict, List, bool, None]:
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
            log.warning(f"API调用失败: {action}, 错误信息: {response.get('message')}")
            return None
        
    # region NapcatAPI

    # 群签到
    def set_group_sign(self, group_id: Union[str, int]) -> bool:
        params = {"group_id": str(group_id)}
        return self._send_request("set_group_sign", params, expect_data=False)

    # 群聊戳一戳
    def group_poke(self, group_id: int, user_id: int) -> bool:
        params = {"group_id": group_id, "user_id": user_id}
        return self._send_request("group_poke", params, expect_data=False)

    # 私聊戳一戳
    def friend_poke(self, user_id: int) -> bool:
        params = {"user_id": user_id}
        return self._send_request("friend_poke", params, expect_data=False)

    # 获取推荐好友/群聊卡片
    def ark_share_peer(
        self,
        user_id: Optional[Union[str, int]] = None,
        phone_number: str = "",
        group_id: Optional[Union[str, int]] = None,
    ) -> Optional[Dict]:
        if (user_id is None) == (group_id is None):
            raise ValueError("必须提供 user_id 或 group_id 中的一个")
        params = {}
        if user_id is not None:
            params["user_id"] = str(user_id)
            params["phoneNumber"] = phone_number
        else:
            params["group_id"] = str(group_id)
        return self._send_request("ArkSharePeer", params)

    # 获取推荐群聊卡片
    def ark_share_group(self, group_id: Union[str, int]) -> Optional[str]:
        params = {"group_id": str(group_id)}
        return self._send_request("ArkShareGroup", params)

    # 获取机器人账号范围
    def get_robot_uin_range(self) -> Optional[List[Dict]]:
        return self._send_request("get_robot_uin_range")

    # 设置在线状态
    def set_online_status(
        self, 
        status: Union[int, Status], 
        ext_status: Optional[int] = None,
        battery_status: Optional[int] = None
    ) -> bool:
        """
        设置在线状态（增强版）
        
        :param status: 状态码整数或Status对象
        :param ext_status: 扩展状态码（当第一个参数为整数时必填）
        :param battery_status: 电池状态（当第一个参数为整数时必填）
        """
        if isinstance(status, Status):
            # 使用状态对象
            params = {
                "status": status.status,
                "ext_status": status.ext_status,
                "battery_status": battery_status if battery_status is not None else status.battery_status
            }
        else:
            # 使用离散参数
            if None in (ext_status, battery_status):
                raise ValueError("当使用离散参数时，ext_status和battery_status必须提供")
            params = {
                "status": status,
                "ext_status": ext_status,
                "battery_status": battery_status
            }
        
        return self._send_request("set_online_status", params, expect_data=False)


    # 获取分类好友列表
    def get_friends_with_category(self) -> Optional[List[Dict]]:
        return self._send_request("get_friends_with_category")

    # 设置QQ头像
    def set_qq_avatar(self, file: str) -> bool:
        return self._send_request("set_qq_avatar", {"file": file}, expect_data=False)

    # 获取文件信息
    def get_file(self, file_id: str) -> Optional[Dict]:
        return self._send_request("get_file", {"file_id": file_id})

    # 转发消息到私聊
    def forward_friend_single_msg(self, message_id: int, user_id: int) -> bool:
        params = {"message_id": message_id, "user_id": user_id}
        return self._send_request("forward_friend_single_msg", params, expect_data=False)

    # 转发消息到群聊
    def forward_group_single_msg(self, message_id: int, group_id: int) -> bool:
        params = {"message_id": message_id, "group_id": group_id}
        return self._send_request("forward_group_single_msg", params, expect_data=False)

    # 英译中
    def translate_en2zh(self, words: List[str]) -> Optional[List[str]]:
        return self._send_request("translate_en2zh", {"words": words})

    # 设置消息表情点赞
    def set_msg_emoji_like(self, message_id: int, emoji_id: str) -> bool:
        params = {"message_id": message_id, "emoji_id": emoji_id}
        return self._send_request("set_msg_emoji_like", params, expect_data=False)

    # 发送合并转发消息
    def send_forward_msg(
        self,
        messages: List[Dict],
        message_type: Optional[str] = None,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ) -> Optional[Dict]:
        params = {"messages": messages}
        if message_type:
            params["message_type"] = message_type
        else:
            if user_id:
                params["user_id"] = user_id
                params["message_type"] = "private"
            elif group_id:
                params["group_id"] = group_id
                params["message_type"] = "group"
            else:
                raise ValueError("未指定消息类型且缺少 user_id/group_id 参数")
        return self._send_request("send_forward_msg", params)

    # 标记私聊消息已读
    def mark_private_msg_as_read(self, user_id: int) -> bool:
        return self._send_request("mark_private_msg_as_read", {"user_id": user_id}, expect_data=False)

    # 标记群聊消息已读
    def mark_group_msg_as_read(self, group_id: int) -> bool:
        return self._send_request("mark_group_msg_as_read", {"group_id": group_id}, expect_data=False)

    # 获取私聊历史消息
    def get_friend_msg_history(
        self,
        user_id: str,
        message_seq: str = "0",
        count: int = 20,
        reverse_order: bool = False,
    ) -> Optional[Dict]:
        params = {
            "user_id": user_id,
            "message_seq": message_seq,
            "count": count,
            "reverseOrder": reverse_order,
        }
        return self._send_request("get_friend_msg_history", params)

    # 设置签名
    def set_self_longnick(self, long_nick: str) -> Optional[Dict]:
        return self._send_request("set_self_longnick", {"longNick": long_nick})

    # 获取最近联系人
    def get_recent_contact(self, count: int = 10) -> Optional[List[Dict]]:
        return self._send_request("get_recent_contact", {"count": count})

    # 标记所有消息已读 (内部接口)
    def _mark_all_as_read(self) -> bool:
        return self._send_request("_mark_all_as_read", expect_data=False)

    # 获取点赞信息
    def get_profile_like(self) -> Optional[Dict]:
        return self._send_request("get_profile_like")

    # 获取自定义表情
    def fetch_custom_face(self, count: int = 48) -> Optional[List[str]]:
        return self._send_request("fetch_custom_face", {"count": count})

    # AI文字转语音
    def get_ai_record(self, character: str, group_id: int, text: str) -> Optional[Dict]:
        params = {"character": character, "group_id": group_id, "text": text}
        return self._send_request("get_ai_record", params)

    # 获取AI语音角色列表
    def get_ai_characters(self, group_id: int, chat_type: int) -> Optional[Dict]:
        params = {"group_id": group_id, "chat_type": chat_type}
        return self._send_request("get_ai_characters", params)

    # 发送群聊AI语音
    def send_group_ai_record(self, character: str, group_id: int, text: str) -> Optional[Dict]:
        params = {"character": character, "group_id": group_id, "text": text}
        return self._send_request("send_group_ai_record", params)

    # 通用戳一戳接口
    def send_poke(self, user_id: int, group_id: Optional[int] = None) -> bool:
        params = {"user_id": user_id}
        if group_id is not None:
            params["group_id"] = group_id
        return self._send_request("send_poke", params, expect_data=False)

    # 文件直链获取
    def get_group_file_url(self, file_id: str, group_id: Union[str, int]) -> Optional[Dict]:
        """获取群文件直链"""
        params = {
            "file_id": str(file_id),
            "group": str(group_id)
        }
        return self._send_request("get_group_file_url", params)

    def get_private_file_url(self, file_id: str) -> Optional[Dict]:
        """获取私聊文件直链"""
        return self._send_request("get_private_file_url", {"file_id": str(file_id)})

    # 文件下载增强版
    def get_file(self, 
                file_id: Optional[str] = None, 
                file_path: Optional[str] = None) -> Optional[Dict]:
        """通用文件下载接口"""
        if not any([file_id, file_path]):
            raise ValueError("必须提供 file_id 或 file_path 中的一个")
        
        params = {}
        if file_id:
            params["file_id"] = str(file_id)
        else:
            params["file"] = file_path
        
        return self._send_request("get_file", params)

    # 音频文件处理
    def get_record(self, 
                file_id: Optional[str] = None,
                file_path: Optional[str] = None,
                out_format: str = "mp3") -> Optional[Dict]:
        """获取音频文件(支持格式转换)"""
        if not any([file_id, file_path]):
            raise ValueError("必须提供 file_id 或 file_path 中的一个")
        
        params = {}
        if file_id:
            params["file_id"] = str(file_id)
        else:
            params["file"] = file_path
        
        if out_format:
            params["out_format"] = out_format.lower()
        
        return self._send_request("get_record", params)

    # 图片刷新功能
    def get_rkey(self) -> Optional[Dict]:
        """获取图片刷新密钥"""
        return self._send_request("nc_get_rkey")

    def refresh_image_url(self, original_url: str) -> Optional[str]:
        """刷新过期图片链接"""
        rkey_data = self.get_rkey()
        if not rkey_data or 'rkey' not in rkey_data:
            return None
        
        # 替换URL中的rkey参数
        from urllib.parse import urlparse, parse_qs, urlunparse
        parsed = urlparse(original_url)
        query = parse_qs(parsed.query)
        query['rkey'] = rkey_data['rkey']
        new_query = '&'.join([f"{k}={v[0]}" for k,v in query.items()])
        
        return urlunparse(parsed._replace(query=new_query))

    # end region

    # region Gocqhttp API
class GocqhttpAPI:
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

    # Bot账号相关接口
    def get_login_info(self):
        return self._send_request("get_login_info")

    def set_qq_profile(self, nickname: Optional[str] = None, company: Optional[str] = None, 
                      email: Optional[str] = None, college: Optional[str] = None, 
                      personal_note: Optional[str] = None):
        params = {}
        if nickname: params['nickname'] = nickname
        if company: params['company'] = company
        if email: params['email'] = email
        if college: params['college'] = college
        if personal_note: params['personal_note'] = personal_note
        return self._send_request("set_qq_profile", params, expect_data=False)

    def qidian_get_account_info(self):
        return self._send_request("qidian_get_account_info")

    def get_model_show(self, model: str):
        return self._send_request("_get_model_show", {"model": model})

    def set_model_show(self, model: str, model_show: str):
        return self._send_request("_set_model_show", {"model": model, "model_show": model_show}, False)

    def get_online_clients(self, no_cache=False):
        return self._send_request("get_online_clients", {"no_cache": no_cache})

    # 好友信息接口
    def get_stranger_info(self, user_id: int, no_cache=False):
        return self._send_request("get_stranger_info", {"user_id": user_id, "no_cache": no_cache})

    def get_friend_list(self):
        return self._send_request("get_friend_list")

    def get_unidirectional_friend_list(self):
        return self._send_request("get_unidirectional_friend_list")

    # 好友操作接口
    def delete_friend(self, user_id: int):
        return self._send_request("delete_friend", {"user_id": user_id}, False)

    def delete_unidirectional_friend(self, user_id: int):
        return self._send_request("delete_unidirectional_friend", {"user_id": user_id}, False)

    # 消息接口
    def send_private_msg(self, user_id: int, message: Union[str, List], group_id: Optional[int]=None, auto_escape=False):
        params = {"user_id": user_id, "message": message, "auto_escape": auto_escape}
        if group_id: params["group_id"] = group_id
        return self._send_request("send_private_msg", params)

    def send_group_msg(self, group_id: int, message: Union[str, List], auto_escape=False):
        return self._send_request("send_group_msg", {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        })

    def send_msg(self, message_type: Optional[str]=None, user_id: Optional[int]=None, 
                group_id: Optional[int]=None, message: Union[str, List]=None, auto_escape=False):
        params = {"auto_escape": auto_escape}
        if message_type: params["message_type"] = message_type
        if user_id: params["user_id"] = user_id
        if group_id: params["group_id"] = group_id
        if message: params["message"] = message
        return self._send_request("send_msg", params)

    def get_msg(self, message_id: int):
        return self._send_request("get_msg", {"message_id": message_id})

    def delete_msg(self, message_id: int):
        return self._send_request("delete_msg", {"message_id": message_id}, False)

    def mark_msg_as_read(self, message_id: int):
        return self._send_request("mark_msg_as_read", {"message_id": message_id}, False)

    def get_forward_msg(self, message_id: str):
        return self._send_request("get_forward_msg", {"message_id": message_id})

    def send_group_forward_msg(self, group_id: int, messages: List):
        return self._send_request("send_group_forward_msg", {"group_id": group_id, "messages": messages})

    def send_private_forward_msg(self, user_id: int, messages: List):
        return self._send_request("send_private_forward_msg", {"user_id": user_id, "messages": messages})

    def get_group_msg_history(self, group_id: int, message_seq: int):
        return self._send_request("get_group_msg_history", {"group_id": group_id, "message_seq": message_seq})

    # 图片接口
    def get_image(self, file: str):
        return self._send_request("get_image", {"file": file})

    def can_send_image(self):
        return self._send_request("can_send_image")

    def ocr_image(self, image: str):
        return self._send_request("ocr_image", {"image": image})

    # 处理接口
    def set_friend_add_request(self, flag: str, approve=True, remark=""):
        return self._send_request("set_friend_add_request", {
            "flag": flag,
            "approve": approve,
            "remark": remark
        }, False)

    def set_group_add_request(self, flag: str, sub_type: str, approve=True, reason=""):
        return self._send_request("set_group_add_request", {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve,
            "reason": reason
        }, False)

    # 群信息接口
    def get_group_info(self, group_id: int, no_cache=False):
        return self._send_request("get_group_info", {"group_id": group_id, "no_cache": no_cache})

    def get_group_list(self, no_cache=False):
        return self._send_request("get_group_list", {"no_cache": no_cache})

    def get_group_member_info(self, group_id: int, user_id: int, no_cache=False):
        return self._send_request("get_group_member_info", {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache
        })

    def get_group_member_list(self, group_id: int, no_cache=False):
        return self._send_request("get_group_member_list", {"group_id": group_id, "no_cache": no_cache})

    def get_group_honor_info(self, group_id: int, type: str):
        return self._send_request("get_group_honor_info", {"group_id": group_id, "type": type})

    def get_group_system_msg(self):
        return self._send_request("get_group_system_msg")

    def get_essence_msg_list(self, group_id: int):
        return self._send_request("get_essence_msg_list", {"group_id": group_id})

    def get_group_at_all_remain(self, group_id: int):
        return self._send_request("get_group_at_all_remain", {"group_id": group_id})

    # 群设置接口
    def set_group_name(self, group_id: int, group_name: str):
        return self._send_request("set_group_name", {"group_id": group_id, "group_name": group_name}, False)

    def set_group_portrait(self, group_id: int, file: str, cache=1):
        return self._send_request("set_group_portrait", {
            "group_id": group_id,
            "file": file,
            "cache": cache
        }, False)

    def set_group_admin(self, group_id: int, user_id: int, enable=True):
        return self._send_request("set_group_admin", {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        }, False)

    def set_group_card(self, group_id: int, user_id: int, card=""):
        return self._send_request("set_group_card", {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        }, False)

    def set_group_special_title(self, group_id: int, user_id: int, title="", duration=-1):
        return self._send_request("set_group_special_title", {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": title,
            "duration": duration
        }, False)

    # 群操作接口
    def set_group_ban(self, group_id: int, user_id: int, duration=1800):
        return self._send_request("set_group_ban", {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }, False)

    def set_group_whole_ban(self, group_id: int, enable=True):
        return self._send_request("set_group_whole_ban", {
            "group_id": group_id,
            "enable": enable
        }, False)

    def set_group_anonymous_ban(self, group_id: int, anonymous: Optional[Dict]=None, flag: Optional[str]=None, duration=1800):
        params = {"group_id": group_id, "duration": duration}
        if anonymous: params["anonymous"] = anonymous
        elif flag: params["anonymous_flag"] = flag
        else: raise ValueError("需要提供anonymous或anonymous_flag参数")
        return self._send_request("set_group_anonymous_ban", params, False)

    def set_essence_msg(self, message_id: int):
        return self._send_request("set_essence_msg", {"message_id": message_id}, False)

    def delete_essence_msg(self, message_id: int):
        return self._send_request("delete_essence_msg", {"message_id": message_id}, False)

    def send_group_sign(self, group_id: int):
        return self._send_request("send_group_sign", {"group_id": group_id}, False)

    def set_group_anonymous(self, group_id: int, enable=True):
        return self._send_request("set_group_anonymous", {
            "group_id": group_id,
            "enable": enable
        }, False)

    def _send_group_notice(self, group_id: int, content: str, image: Optional[str]=None):
        params = {"group_id": group_id, "content": content}
        if image: params["image"] = image
        return self._send_request("_send_group_notice", params, False)

    def _get_group_notice(self, group_id: int):
        return self._send_request("_get_group_notice", {"group_id": group_id})

    def set_group_kick(self, group_id: int, user_id: int, reject_add_request=False):
        return self._send_request("set_group_kick", {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        }, False)

    def set_group_leave(self, group_id: int, is_dismiss=False):
        return self._send_request("set_group_leave", {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        }, False)

    # 文件接口
    def upload_group_file(self, group_id: int, file: str, name: str, folder: Optional[str]=None):
        params = {"group_id": group_id, "file": file, "name": name}
        if folder: params["folder"] = folder
        return self._send_request("upload_group_file", params, False)

    def delete_group_file(self, group_id: int, file_id: str, busid: int):
        return self._send_request("delete_group_file", {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        }, False)

    def create_group_file_folder(self, group_id: int, name: str, parent_id="/"):
        return self._send_request("create_group_file_folder", {
            "group_id": group_id,
            "name": name,
            "parent_id": parent_id
        }, False)

    def delete_group_folder(self, group_id: int, folder_id: str):
        return self._send_request("delete_group_folder", {
            "group_id": group_id,
            "folder_id": folder_id
        }, False)

    def get_group_file_system_info(self, group_id: int):
        return self._send_request("get_group_file_system_info", {"group_id": group_id})

    def get_group_root_files(self, group_id: int):
        return self._send_request("get_group_root_files", {"group_id": group_id})

    def get_group_files_by_folder(self, group_id: int, folder_id: str):
        return self._send_request("get_group_files_by_folder", {
            "group_id": group_id,
            "folder_id": folder_id
        })

    def get_group_file_url(self, group_id: int, file_id: str, busid: int):
        return self._send_request("get_group_file_url", {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        })

    def upload_private_file(self, user_id: int, file: str, name: str):
        return self._send_request("upload_private_file", {
            "user_id": user_id,
            "file": file,
            "name": name
        }, False)

    # 系统接口
    def get_version_info(self):
        return self._send_request("get_version_info")

    def get_status(self):
        return self._send_request("get_status")

    def reload_event_filter(self, file: str):
        return self._send_request("reload_event_filter", {"file": file}, False)

    def download_file(self, url: str, thread_count=1, headers=None):
        params = {"url": url, "thread_count": thread_count}
        if headers: params["headers"] = headers
        return self._send_request("download_file", params)

    def check_url_safely(self, url: str):
        return self._send_request("check_url_safely", {"url": url})

    # 隐藏接口
    def _get_word_slices(self, content: str):
        return self._send_request(".get_word_slices", {"content": content})

    def _handle_quick_operation(self, context: Dict, operation: Dict):
        return self._send_request(".handle_quick_operation", {
            "context": context,
            "operation": operation
        }, False)

    # end region

    # region Lagrange API
class LagrangeAPI:
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

    def fetch_custom_face(self) -> Optional[List[str]]:
        """获取收藏表情"""
        return self._send_request("fetch_custom_face")

    def get_friend_msg_history(self, user_id: int, message_id: int, count: int) -> Optional[List[Dict]]:
        """获取好友历史消息记录"""
        params = {
            "user_id": user_id,
            "message_id": message_id,
            "count": count
        }
        data = self._send_request("get_friend_msg_history", params)
        return data.get("messages") if data else None

    def get_group_msg_history(self, group_id: int, message_id: int, count: int) -> Optional[List[Dict]]:
        """获取群组历史消息记录"""
        params = {
            "group_id": group_id,
            "message_id": message_id,
            "count": count
        }
        data = self._send_request("get_group_msg_history", params)
        return data.get("messages") if data else None

    def send_forward_msg(self, messages: List[Dict]) -> Optional[str]:
        """构造合并转发消息"""
        params = {"messages": messages}
        return self._send_request("send_forward_msg", params)

    def send_group_forward_msg(self, group_id: int, messages: List[Dict]) -> Optional[Dict]:
        """发送合并转发 (群聊)"""
        params = {
            "group_id": group_id,
            "messages": messages
        }
        return self._send_request("send_group_forward_msg", params)

    def send_private_forward_msg(self, user_id: int, messages: List[Dict]) -> Optional[Dict]:
        """发送合并转发 (好友)"""
        params = {
            "user_id": user_id,
            "messages": messages
        }
        return self._send_request("send_private_forward_msg", params)

    def upload_group_file(self, group_id: int, file: str, name: str, folder: Optional[str] = None) -> bool:
        """上传群文件"""
        params = {
            "group_id": group_id,
            "file": file,
            "name": name
        }
        if folder is not None:
            params["folder"] = folder
        return self._send_request("upload_group_file", params, expect_data=False) is not None

    def upload_private_file(self, user_id: int, file: str, name: str) -> bool:
        """私聊发送文件"""
        params = {
            "user_id": user_id,
            "file": file,
            "name": name
        }
        return self._send_request("upload_private_file", params, expect_data=False) is not None

    def get_group_root_files(self, group_id: int) -> Optional[Dict]:
        """获取群根目录文件列表"""
        params = {"group_id": group_id}
        return self._send_request("get_group_root_files", params)

    def get_group_files_by_folder(self, group_id: int, folder_id: str) -> Optional[Dict]:
        """获取群子目录文件列表"""
        params = {
            "group_id": group_id,
            "folder_id": folder_id
        }
        return self._send_request("get_group_files_by_folder", params)

    def get_group_file_url(self, group_id: int, file_id: str, busid: int) -> Optional[str]:
        """获取群文件资源链接"""
        params = {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        }
        data = self._send_request("get_group_file_url", params)
        return data.get("url") if data else None

    def friend_poke(self, user_id: int) -> bool:
        """好友戳一戳"""
        params = {"user_id": user_id}
        return self._send_request("friend_poke", params, expect_data=False) is not None

    def group_poke(self, group_id: int, user_id: int) -> bool:
        """群组戳一戳"""
        params = {
            "group_id": group_id,
            "user_id": user_id
        }
        return self._send_request("group_poke", params, expect_data=False) is not None

    def set_group_special_title(self, group_id: int, user_id: int, special_title: str) -> bool:
        """设置群组专属头衔"""
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title
        }
        return self._send_request("set_group_special_title", params, expect_data=False) is not None

    def set_group_reaction(self, group_id: int, message_id: int, code: str, is_add: bool) -> bool:
        """设置群消息表情回应"""
        params = {
            "group_id": group_id,
            "message_id": message_id,
            "code": code,
            "is_add": is_add
        }
        return self._send_request("set_group_reaction", params, expect_data=False) is not None

    def set_essence_msg(self, message_id: int) -> bool:
        """设置群精华消息"""
        params = {"message_id": message_id}
        return self._send_request("set_essence_msg", params, expect_data=False) is not None

    def delete_essence_msg(self, message_id: int) -> bool:
        """删除群精华消息"""
        params = {"message_id": message_id}
        return self._send_request("delete_essence_msg", params, expect_data=False) is not None

    def get_essence_msg_list(self, group_id: int) -> Optional[List[Dict]]:
        """获取群精华消息列表"""
        params = {"group_id": group_id}
        data = self._send_request("get_essence_msg_list", params)
        return data.get("messages") if data else None


    # end region

    # region LLonebot API
class LLonebotAPI:
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

    def set_qq_avatar(self, file: str) -> bool:
        """设置QQ头像"""
        params = {"file": file}
        return self._send_request("set_qq_avatar", params, expect_data=False)

    def get_group_ignore_add_request(self) -> List[Dict]:
        """获取已过滤的加群请求列表"""
        return self._send_request("get_group_ignore_add_request")

    def get_file(self, file_id: str) -> Dict:
        """下载文件"""
        params = {"file_id": file_id}
        return self._send_request("get_file", params)

    def forward_friend_single_msg(self, user_id: int, message_id: int) -> bool:
        """转发单条消息到好友"""
        params = {
            "user_id": user_id,
            "message_id": message_id
        }
        return self._send_request("forward_friend_single_msg", params, expect_data=False)

    def forward_group_single_msg(self, group_id: int, message_id: int) -> bool:
        """转发单条消息到群"""
        params = {
            "group_id": group_id,
            "message_id": message_id
        }
        return self._send_request("forward_group_single_msg", params, expect_data=False)

    def set_msg_emoji_like(self, message_id: str, emoji_id: str) -> bool:
        """发送表情回应"""
        params = {
            "message_id": message_id,
            "emoji_id": emoji_id
        }
        return self._send_request("set_msg_emoji_like", params, expect_data=False)

    def get_friends_with_category(self) -> List[Dict]:
        """获取带分组的好友列表"""
        return self._send_request("get_friends_with_category")

    def set_online_status(self, status: int, ext_status: int = 0, battery_status: int = 0) -> bool:
        """设置在线状态"""
        params = {
            "status": status,
            "ext_status": ext_status,
            "battery_status": battery_status
        }
        return self._send_request("set_online_status", params, expect_data=False)

    def get_profile_like(self) -> Dict:
        """获取自身点赞列表"""
        return self._send_request("get_profile_like")

    def friend_poke(self, user_id: int) -> bool:
        """好友戳一戳"""
        params = {"user_id": user_id}
        return self._send_request("friend_poke", params, expect_data=False)

    def group_poke(self, group_id: int, user_id: int) -> bool:
        """群组戳一戳"""
        params = {
            "group_id": group_id,
            "user_id": user_id
        }
        return self._send_request("group_poke", params, expect_data=False)

    def download_file(self, file: str, base64: bool = False) -> Dict:
        """下载文件，支持base64参数"""
        params = {
            "file": file,
            "base64": base64
        }
        return self._send_request("download_file", params)

    # end region