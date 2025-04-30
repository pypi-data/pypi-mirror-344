"""Manager res and data."""

import datetime
from typing import Any

from .client import WeLockApi
from .const import BINARYSENSORS_DOOR_KEY, SENSOR_BATTERY_KEY, SENSOR_RECORD_KEY
from .models import (
    OPENTYPE,
    WeLockData,
    WeLockDevice,
    WeLockException,
    WeLockMessageListener,
    logger,
)
from .wemq import WeMqttClient


class Resmanager:
    """Manager res and data."""

    def __init__(self, api: WeLockApi) -> None:
        """Init."""
        self.api = api
        self.mqclient = None
        self.device_map: dict[str, WeLockDevice] = {}
        self.device_listeners = set()

    async def initWeMq(self):
        """Init mq and start mq."""
        if self.mqclient is not None:
            await self.mqclient.disconnect()
            self.mqclient = None
        if self.api is not None:
            mq = WeMqttClient(self.api)
            await mq.connect(self.on_message)
            self.mqclient = mq

    def on_message(self, msg_data: dict):
        """Receive message."""
        logger.debug(f"mq receive-> {msg_data}")
        self._process_user_data(msg_data)

    def __convert_to_welockdata(self, status: list, device_id: str) -> dict:
        values = {}
        dev = self.device_map.get(device_id, None)
        if dev:
            values = dev.status or {}

        for item in status:
            we_data = WeLockData()
            types = item.get("type", "").strip()
            we_data.type = types
            if types in ("Unlock", "RelayAction"):
                we_data.type = SENSOR_RECORD_KEY
            if types == "Battery":
                we_data.type = SENSOR_BATTERY_KEY
            we_data.unlock_type = item.get("unlockType", 0)
            if we_data.unlock_type == 31:
                we_data.type = BINARYSENSORS_DOOR_KEY
            if we_data.type:
                we_data.unlock_result = item.get("unlockResult", 0)
                we_data.result_desc = item.get("resultDescription", None)
                we_data.user_id = f"{item.get('userId', '')}"
                if types == "Unlock":
                    we_data.unlock_time = item.get("catchTime", item.get("time", 0))
                    we_data.unlock_type = item.get("unlockType", 17)
                    we_data.user_remark = item.get("uRemark", None)
                elif types == "RelayAction":
                    we_data.unlock_time = item.get("time", item.get("catchTime", 0))
                    we_data.user_id = item.get("userId", device_id)
                    we_data.user_remark = item.get("uRemark", None)
                we_data.value = self.__getDataValue(we_data)
                values[we_data.type] = we_data.value
        return values

    def __getDataValue(self, we_data: WeLockData) -> Any:
        """Show detail info."""
        value = None
        try:
            if we_data.type == SENSOR_RECORD_KEY:
                value = f"unlocked by {OPENTYPE.get(we_data.unlock_type, '')}({we_data.user_remark if we_data.user_remark is not None else we_data.user_id}) at {self.__dateFormat(we_data.unlock_time)}"
            elif we_data.type == BINARYSENSORS_DOOR_KEY:
                value = we_data.unlock_result == 1
            elif we_data.type == SENSOR_BATTERY_KEY:
                value = int(we_data.result_desc, 16)
        except AttributeError:
            pass
        except WeLockException:
            pass
        return value

    def __dateFormat(self, timestamp_ms) -> str:
        """Datetime format."""
        timestamp = timestamp_ms / 1000.0
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        return dt_object.strftime("%Y-%m-%d %H:%M:%S")

    def _process_user_data(self, data: dict) -> None:
        """Parse the data."""
        try:
            device_id = data.get("number", "")
            status = data.get("status", [])
            device = self.device_map.get(device_id, None)
            if device:
                if isinstance(status, list):
                    values = self.__convert_to_welockdata(status, device_id)
                    device.status = values
            for listener in self.device_listeners:
                listener.update_device(device)
        except KeyError as ke:
            logger.error("_process_user_data1 = %s", ke)
        except TypeError as er:
            logger.error("_process_user_data2 = %s", er)

    def add_device_listener(self, listener: WeLockMessageListener):
        """Add device listener."""
        self.device_listeners.add(listener)

    async def update_device_list(self):
        """Return the locks."""
        self.device_map.clear()
        if device_list := await self.api.get_locks():
            for device in device_list:
                self.device_map[device.device_id] = device

    async def unlock(self, device: WeLockDevice) -> bool:
        """."""
        await self.api.unlock(device)
        return True

    async def remote_control(self, device: WeLockDevice) -> bool:
        """."""
        await self.api.remoteControl(device)
        return True
