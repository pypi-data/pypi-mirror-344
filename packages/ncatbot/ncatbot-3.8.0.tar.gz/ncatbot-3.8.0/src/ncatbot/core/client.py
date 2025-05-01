import asyncio
import time
import traceback
from threading import Lock, Thread

from ncatbot.adapter import Websocket, check_websocket, launch_napcat_service
from ncatbot.core.api import BotAPI
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.core.request import Request
from ncatbot.utils import (
    OFFICIAL_GROUP_MESSAGE_EVENT,
    OFFICIAL_NOTICE_EVENT,
    OFFICIAL_PRIVATE_MESSAGE_EVENT,
    OFFICIAL_REQUEST_EVENT,
    OFFICIAL_STARTUP_EVENT,
    config,
    get_log,
    run_func_async,
)

_log = get_log()


class BotClient:
    registered = False

    def __init__(self, plugins_path="plugins", *args, **kwargs):

        def check_duplicate_register():
            if BotClient.registered:
                _log.error(
                    "一个主程序只允许注册一个 BotClient 实例, 请检查你的引导程序"
                )
                exit(1)
            BotClient.registered = True

        check_duplicate_register()
        self.api = BotAPI()
        self._subscribe_group_message_types = []
        self._subscribe_private_message_types = []
        self._group_event_handlers = []
        self._private_event_handlers = []
        self._notice_event_handlers = []
        self._request_event_handlers = []
        self._startup_event_handlers = []
        self.plugins_path = plugins_path
        from ncatbot.plugin import EventBus, PluginLoader

        self.plugin_sys = PluginLoader(None)
        self.plugin_sys.event_bus = EventBus(plugin_loader=self.plugin_sys)

    async def _handle_group_event(self, msg: dict):
        msg: GroupMessage = GroupMessage(msg)
        _log.debug(msg)
        for handler, types in self._group_event_handlers:
            if types is None or any(i["type"] in types for i in msg.message):
                await run_func_async(handler, msg)
        from ncatbot.plugin.event.event import Event, EventSource

        await self.plugin_sys.event_bus.publish_async(
            Event(
                OFFICIAL_GROUP_MESSAGE_EVENT,
                msg,
                EventSource(msg.user_id, msg.group_id),
            )
        )

    async def _handle_private_event(self, msg: dict):
        msg: PrivateMessage = PrivateMessage(msg)
        _log.debug(msg)
        for handler, types in self._private_event_handlers:
            if types is None or any(i["type"] in types for i in msg.message):
                await run_func_async(handler, msg)
        from ncatbot.plugin.event.event import Event, EventSource

        await self.plugin_sys.event_bus.publish_async(
            Event(OFFICIAL_PRIVATE_MESSAGE_EVENT, msg, EventSource(msg.user_id, "root"))
        )

    async def _handle_notice_event(self, msg: dict):
        # msg: NoticeMessage = NoticeMessage(msg)
        _log.debug(msg)
        for handler in self._notice_event_handlers:
            await run_func_async(handler, msg)
        from ncatbot.plugin import Event

        await self.plugin_sys.event_bus.publish_async(Event(OFFICIAL_NOTICE_EVENT, msg))

    async def _handle_request_event(self, msg: dict):
        msg = Request(msg)
        _log.debug(msg)
        for handler in self._request_event_handlers:
            await run_func_async(handler, msg)
        from ncatbot.plugin import Event

        await self.plugin_sys.event_bus.publish_async(
            Event(OFFICIAL_REQUEST_EVENT, msg)
        )

    async def _handle_startup_event(self):
        for handler in self._startup_event_handlers:
            await run_func_async(handler)
        from ncatbot.plugin import Event

        await self.plugin_sys.event_bus.publish_async(
            Event(OFFICIAL_STARTUP_EVENT, None)
        )

    def group_event(self, types=None):
        self._subscribe_group_message_types = types

        def decorator(func):
            self._group_event_handlers.append((func, types))
            return func

        return decorator

    def private_event(self, types=None):
        self._subscribe_private_message_types = types

        def decorator(func):
            self._private_event_handlers.append((func, types))
            return func

        return decorator

    def notice_event(self):
        def decorator(func):
            self._notice_event_handlers.append(func)
            return func

        return decorator

    def request_event(self):
        def decorator(func):
            self._request_event_handlers.append(func)
            return func

        return decorator

    def add_startup_handler(self, func):
        self._startup_event_handlers.append(func)

    def add_group_event_handler(self, func):
        self._group_event_handlers.append((func, None))

    def add_private_event_handler(self, func):
        self._private_event_handlers.append((func, None))

    def add_notice_event_handler(self, func):
        self._notice_event_handlers.append(func)

    def add_request_event_handler(self, func):
        self._request_event_handlers.append(func)

    async def _run_async(self):
        def info_subscribe_message_types():
            subsribe_group_message_types = (
                "全部消息类型"
                if self._subscribe_group_message_types is None
                else self._subscribe_group_message_types
            )
            subsribe_private_message_types = (
                "全部消息类型"
                if self._subscribe_private_message_types is None
                else self._subscribe_private_message_types
            )
            _log.debug(f"已订阅消息类型:[群聊]{subsribe_group_message_types}")
            _log.debug(f"已订阅消息类型:[私聊]{subsribe_private_message_types}")

        async def time_schedule_heartbeat():
            while True:
                await asyncio.sleep(1)
                self.plugin_sys.time_task_scheduler.step()

        info_subscribe_message_types()
        websocket_server = Websocket(self)
        if not config.skip_plugin_load:
            await self.plugin_sys.load_plugins(api=self.api)
        else:
            _log.warning("插件加载被跳过")
        while True:
            try:
                asyncio.create_task(time_schedule_heartbeat())
                await websocket_server.on_connect()
            except Exception:
                _log.info("正在尝试重连服务器...")
                EXPIER = time.time() + 300
                interval = 1
                while not (await check_websocket(config.ws_uri)):
                    _log.info(f"正在尝试重连服务器...第 {interval} s")
                    time.sleep(interval)
                    interval *= 2
                    if time.time() > EXPIER:
                        _log.error("重连服务器超时, 退出程序")
                        exit(1)

            _log.info("重连服务器成功")

    def _start(self, *args, **kwargs):
        try:
            asyncio.run(self._run_async())
        except asyncio.CancelledError:
            pass
        except Exception:
            _log.error(traceback.format_exc())
        finally:
            # TODO 非正常退出时不会正常保存
            self.exit(exit_process=True)

    def run(self, *args, **kwargs):
        """启动"""
        for key in config.__dict__:
            if key in kwargs:
                config.__dict__[key] = kwargs[key]
        config.validate_config()
        launch_napcat_service(*args, **kwargs)  # 保证 NapCat 正常启动
        _log.info("NapCat 服务启动登录完成")
        self._start(*args, **kwargs)

    def run_none_blocking(self, *args, **kwargs):
        """非阻塞启动"""
        Thread(target=self.run, args=args, kwargs=kwargs, daemon=True).start()
        return self.api

    def run_blocking(self, *args, **kwargs):
        """阻塞启动"""
        lock = Lock()
        lock.acquire()  # 全局加锁
        self.add_startup_handler(
            lambda: lock.release()
        )  # 在 NcatBot 接口可用时, 释放全局锁
        self.run_none_blocking(*args, **kwargs)
        lock.acquire()  # 等待 NcatBot 启动完成
        return self.api

    def exit(self, exit_process=False):
        """嵌入模式中主动触发退出"""
        try:
            _log.info("插件卸载中...")
            self.plugin_sys.unload_all()
            _log.info("清理回调函数...")
            self._group_event_handlers.clear()
            self._private_event_handlers.clear()
            self._notice_event_handlers.clear()
            self._request_event_handlers.clear()
            _log.info("清理工作结束, NcatBot 已经正常退出")
        except Exception:
            _log.error("清理工作失败, 报错如下:")
            _log.error(traceback.format_exc())
            return False
        if exit_process:
            exit(0)
        return True
