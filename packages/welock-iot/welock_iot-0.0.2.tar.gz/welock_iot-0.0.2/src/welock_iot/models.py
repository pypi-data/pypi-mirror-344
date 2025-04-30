"""Welock."""

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Any

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG)

default_handler = logging.StreamHandler()
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s] [welock-%(module)s] %(message)s")
)

logger.addHandler(default_handler)


class DeviceType(Enum):
    """Welock device type : lock,sensor,gateway."""

    WELOCK = 1
    WIFIBOX3 = 3
    DOORS = 6
    NOTSUPPORT = 100

    @classmethod
    def value2name(cls, value):
        """."""
        for member in cls:
            if member.value == value:
                return member.name
        return None

    @classmethod
    def value2enum(cls, value):
        """."""
        for member in cls:
            if member.value == value:
                return member
        return cls.NOTSUPPORT


class RequestResultStatus(Enum):
    """."""

    SUCCESS = 0
    FAILED = -1


OPENTYPE: dict[int, str] = {
    1: "Fp",
    2: "Passcode",
    3: "Card",
    4: "BTremote",
    5: "433",
    6: "App",
    10: "Passcode",
    11: "Tem pwd",
    12: "Tem pwd",
    13: "Tem pwd",
    14: "Passcode",
    15: "FB",
    16: "NFC",
    17: "WIFIBOX",
    19: "Vacation",
    211: "Local",
}


class WeLockDevice:
    """."""

    device_id: str
    device_name: str
    ble_name1: str
    ble_name2: str
    model_name: str
    device_type: DeviceType
    status: dict[str, Any] = {}
    battery: int
    model_name2: str

    def __init__(self) -> None:
        """."""

    @property
    def model_show(self) -> str:
        """."""
        if self.model_name:
            return self.model_name
        if self.model_name2:
            return self.model_name2
        return None


class WeLockData:
    """."""

    type: str
    unlock_type: int
    user_id: str
    unlock_result: int
    result_desc: str
    value: Any
    unlock_time: int
    user_remark: str

    def __init__(self) -> None:
        """."""


class WeLockException(Exception):
    """Exception when api returns an error."""


class WeLockRequestException(WeLockException):
    """."""

    def __init__(
        self,
        code: str,
        desc: str,
    ) -> None:
        """Initialize the api error."""

        self.code = code
        self.message = desc


@dataclass
class RequestResult:
    """."""

    code: str
    data: Any
    msg: str


class WeLockMessageListener(metaclass=ABCMeta):
    """message listener."""

    @abstractmethod
    def on_message(self, msg_data: dict[str, Any]) -> None:
        """On device message receive."""
