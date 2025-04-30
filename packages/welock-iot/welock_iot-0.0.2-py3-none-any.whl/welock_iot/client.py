"""WeLock api for iot ."""

import asyncio
from collections.abc import Mapping
from typing import Any, cast
from urllib.parse import urljoin

from aiohttp import ClientError, ClientResponse, ClientSession

from .auth_token_manager import OauthTokenManager
from .models import (
    DeviceType,
    RequestResult,
    RequestResultStatus,
    WeLockDevice,
    WeLockRequestException,
    logger,
)

RQ_LOCK = asyncio.Lock()


class WeLockApi:
    """Api for welock."""

    BASE = "https://iot.we-lock.com/"

    def __init__(self, oauth_mgr: OauthTokenManager) -> None:
        """Initialize WeLockApi auth."""
        self._oauth_mgr = oauth_mgr

    @property
    async def _async_get_access_token(self) -> str:
        """Return a valid access token."""
        return await self._oauth_mgr.check_and_refresh_token()

    @property
    def _web_session(self) -> ClientSession:
        """Return the client session."""
        return self._oauth_mgr.client_session()

    async def _parse_resp(self, resp: ClientResponse) -> Mapping[str, Any]:
        """Parse the response content."""
        body = ""
        status_code = resp.status
        if status_code == 200:
            body = await resp.json()
        else:
            try:
                resp.raise_for_status()
            except ClientError as client_err:
                body = await resp.text()
                logger.debug("API returned: %s", body)
                raise WeLockRequestException("-1", "request failed!") from client_err
            except WeLockRequestException:
                raise

        return cast(dict, await resp.json())

    def _result_resp(self, resp: Mapping[str, Any]) -> RequestResult:
        """Convert response result ."""
        rq = RequestResult(None, None, None)
        rq.code = -1
        if resp:
            rq.code = resp.get("code", -1)
            rq.data = resp.get("data", None)
            rq.msg = resp.get("msg", None)

        return rq

    async def request(
        self, method: str, path: str, auth_required: bool = True, **kwargs: Any
    ) -> ClientResponse:
        """Add headers."""
        headers = kwargs.pop(
            "headers", {"Content-Type": "application/x-www-form-urlencoded"}
        )
        params = kwargs.pop("params", None)
        data = kwargs.pop("data", None)
        url = urljoin(self.BASE, path)

        extra_headers = kwargs.pop("extra_headers", None)
        extra_params = kwargs.pop("extra_params", None)
        extra_data = kwargs.pop("extra_data", None)
        if auth_required:
            access_token = await self._async_get_access_token
            headers["Authorization"] = f"{access_token}"

        if extra_headers:
            headers.update(extra_headers)
        if extra_params:
            params = params or {}
            params.update(extra_params)
        if extra_data:
            data = data or {}
            data.update(extra_data)
        return await self._web_session.request(
            method, url, **kwargs, headers=headers, params=params, data=data, timeout=8
        )

    async def post(self, path: str, params: Mapping[str, Any]) -> Mapping[str, Any]:
        """Post request."""
        resp = await self.request("post", path, True, params=params)
        return await self._parse_resp(resp)

    def __parse_to_list(self, data: list) -> list[WeLockDevice]:
        """Convert to welock device."""
        device_list = []
        for item in data:
            device = WeLockDevice()
            device.device_id = item.get("number", None)
            device.device_name = item.get("notes", None) or f"{device.device_id}"
            device.model_name = item.get("model", None)
            device.device_type = DeviceType.value2enum(item.get("deviceType", 1))
            gateway = item.get("gatewayModel", None)
            device.model_name2 = gateway
            if (
                gateway
                and gateway != "WIFIBOX3"
                and device.device_type == DeviceType.WIFIBOX3
            ):
                device.device_type = DeviceType.NOTSUPPORT
            bleInfos = item.get("bluetooth", None)
            if isinstance(bleInfos, list):
                if len(bleInfos) == 1:
                    device.ble_name1 = bleInfos[0].get("deviceName", None)
                    device.battery = bleInfos[0].get("power", 1)
                else:
                    for ble in bleInfos:
                        position = ble.get("position", None)
                        deviceName = ble.get("deviceName", None)
                        power = ble.get("power", 1)
                        if position in (1, 0):
                            device.ble_name1 = deviceName
                            device.battery = power

            device_list.append(device)
        return device_list

    async def get_locks(self) -> list[WeLockDevice]:
        """Enumerate all locks in the account."""
        device_list = []
        res = await self.post("Device/List", [])

        rq = self._result_resp(res)
        if rq.code == RequestResultStatus.SUCCESS.value:
            if isinstance(rq.data, list):
                device_list = self.__parse_to_list(rq.data)
        elif rq.code == RequestResultStatus.FAILED.value:
            raise WeLockRequestException(
                RequestResultStatus.FAILED.value, "get list failed"
            )

        return device_list

    async def unlock(self, device: WeLockDevice) -> bool:
        """Unlock."""
        result = False
        params = {}
        params["number"] = device.device_id
        params["deviceName"] = device.ble_name1
        res = await self.post("Device/GatewayUnlocking", params)
        rq = self._result_resp(res)
        if rq.code == RequestResultStatus.SUCCESS.value:
            result = True
        elif rq.code == RequestResultStatus.FAILED.value:
            result = False
        return result

    async def remoteControl(self, device: WeLockDevice) -> bool:
        """Wifibox remote control."""
        result = False
        params = {}
        params["number"] = device.device_id
        res = await self.post("Device/triggerSwitch", params)
        rq = self._result_resp(res)

        if rq.code == RequestResultStatus.SUCCESS.value:
            result = True
        elif rq.code == RequestResultStatus.FAILED.value:
            result = False
        return result

    async def mqttConfig(self) -> Mapping[str, Any]:
        """Get the user mqtt config."""
        config = {}
        res = await self.post("MQTT/info", [])
        rq = self._result_resp(res)
        if rq.code == RequestResultStatus.SUCCESS.value:
            if isinstance(rq.data, Mapping):
                config = rq.data

        return config
