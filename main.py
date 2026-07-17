from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("astrbot_plugin_add_one", "Xc_Star", "自动+1", "1.0.5")
class MyPlugin(Star):
    def __init__(self, context: Context):
        self.last_msg = {}
        self.is_added = False
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def add_one(self, event: AstrMessageEvent):
        this_msg = str(event.get_message_str())
        this_group_id = int(event.get_group_id())
        if this_msg == self.last_msg.get(this_group_id) and not self.is_added:
            self.is_added = True
            yield event.plain_result(this_msg) # 发送一条纯文本消息

        if self.is_added and self.last_msg.get(this_group_id) != this_msg:
            self.is_added = False

        self.last_msg[this_group_id] = this_msg

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
