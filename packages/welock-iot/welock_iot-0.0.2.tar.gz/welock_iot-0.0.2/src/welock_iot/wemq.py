"""Mqtt."""

import asyncio
import json
import ssl
from typing import Any
from urllib.parse import urlsplit

import aiomqtt

from .client import WeLockApi
from .models import WeLockException, logger

ssl_context = ssl.create_default_context()


class WeMqttConfig:
    """Mqtt config."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Init mqconfig."""
        self.url = config.get("url", "")
        self.client_id = config.get("clientId", "")
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.keepalive = config.get("keepalive", 60)
        self.topic = config.get("topic")


class WeMqttClient:
    """Mqtt client."""

    def __init__(self, welockapi: WeLockApi) -> None:
        """."""
        super().__init__()
        self.api = welockapi
        self.client = None
        self.mq_config = None
        self._message_listener = None
        self._running = False
        self._listener_task = None

    async def connect(self, listener) -> None:
        """Connect mqtt broker."""
        self._message_listener = listener
        self._listener_task = asyncio.create_task(self._listen())

    async def _get_config(self):
        config = await self.api.mqttConfig()
        mq_config = WeMqttConfig(config)
        self.mq_config = mq_config

    async def _listen(self):
        await self._get_config()
        reconnect_interval = 30
        self._running = True
        while self._running:
            url = urlsplit(self.mq_config.url)
            _tls_context = None
            if url.scheme == "ssl":
                _tls_context = ssl_context
            try:
                async with aiomqtt.Client(
                    hostname=url.hostname,
                    port=url.port,
                    identifier=self.mq_config.client_id,
                    username=self.mq_config.username,
                    password=self.mq_config.password,
                    keepalive=self.mq_config.keepalive,
                    tls_context=_tls_context,
                ) as mqttc:
                    self.client = mqttc
                    await self.client.subscribe(self.mq_config.topic)
                    logger.info("mqtt client connected.")
                    async for message in self.client.messages:
                        self._process_message(message)
            except aiomqtt.MqttError as mqtt_err:
                logger.error(
                    "[%s] mqtt client disconnected!",
                    self.mq_config,
                    exc_info=True,
                )
                await asyncio.sleep(reconnect_interval)
                if isinstance(mqtt_err, aiomqtt.MqttCodeError):
                    if mqtt_err.rc in [3, 4, 5]:
                        logger.error(
                            "[%s] connect failed.",
                            mqtt_err.rc,
                        )
                        await self._get_config()
            except WeLockException:
                await asyncio.sleep(reconnect_interval)
                logger.error("[%s] unexcept exception:", self.mq_config, exc_info=True)

    def _process_message(self, msg: aiomqtt.message.Message) -> None:
        """Mqtt on message."""
        logger.debug(f"{msg.topic} :payload-> {msg.payload.decode('utf8')}")
        try:
            msg_dict = json.loads(msg.payload.decode("utf8"))
            self._message_listener(msg_dict)
        except json.JSONDecodeError as ex:
            logger.error("_on_message error %s", ex)

    async def disconnect(self) -> None:
        """UnRegister listener."""
        if self._listener_task is None:
            return
        self._listener_task.cancel()
        self._listener_task = None
        self._running = False
        self.client = None
