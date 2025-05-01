from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CtrlRequest(_message.Message):
    __slots__ = ("request_id", "get_device_info", "reset_system", "start_bootloader")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    GET_DEVICE_INFO_FIELD_NUMBER: _ClassVar[int]
    RESET_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    START_BOOTLOADER_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    get_device_info: bool
    reset_system: bool
    start_bootloader: bool
    def __init__(self, request_id: _Optional[int] = ..., get_device_info: bool = ..., reset_system: bool = ..., start_bootloader: bool = ...) -> None: ...

class DeviceInfo(_message.Message):
    __slots__ = ("request_id", "device_type", "hardware_version", "firmware_version_major", "firmware_version_minor", "firmware_version_patch", "git_hash")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_MAJOR_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_MINOR_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_PATCH_FIELD_NUMBER: _ClassVar[int]
    GIT_HASH_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    device_type: int
    hardware_version: int
    firmware_version_major: int
    firmware_version_minor: int
    firmware_version_patch: int
    git_hash: str
    def __init__(self, request_id: _Optional[int] = ..., device_type: _Optional[int] = ..., hardware_version: _Optional[int] = ..., firmware_version_major: _Optional[int] = ..., firmware_version_minor: _Optional[int] = ..., firmware_version_patch: _Optional[int] = ..., git_hash: _Optional[str] = ...) -> None: ...

class CtrlMsg(_message.Message):
    __slots__ = ("sequence_number", "ctrl_request", "device_info")
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CTRL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INFO_FIELD_NUMBER: _ClassVar[int]
    sequence_number: int
    ctrl_request: CtrlRequest
    device_info: DeviceInfo
    def __init__(self, sequence_number: _Optional[int] = ..., ctrl_request: _Optional[_Union[CtrlRequest, _Mapping]] = ..., device_info: _Optional[_Union[DeviceInfo, _Mapping]] = ...) -> None: ...
