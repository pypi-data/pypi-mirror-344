from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class I2cId(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    I2C0: _ClassVar[I2cId]
    I2C1: _ClassVar[I2cId]

class AddressWidth(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Bits7: _ClassVar[AddressWidth]
    Bits8: _ClassVar[AddressWidth]
    Bits10: _ClassVar[AddressWidth]
    Bits16: _ClassVar[AddressWidth]

class I2cConfigStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CFG_NOT_INIT: _ClassVar[I2cConfigStatusCode]
    CFG_SUCCESS: _ClassVar[I2cConfigStatusCode]
    CFG_BAD_REQUEST: _ClassVar[I2cConfigStatusCode]
    CFG_INVALID_CLOCK_FREQ: _ClassVar[I2cConfigStatusCode]
    CFG_INVALID_SLAVE_ADDR: _ClassVar[I2cConfigStatusCode]
    CFG_INVALID_SLAVE_ADDR_WIDTH: _ClassVar[I2cConfigStatusCode]
    CFG_INVALID_MEM_ADDR_WIDTH: _ClassVar[I2cConfigStatusCode]
    CFG_INTERFACE_ERROR: _ClassVar[I2cConfigStatusCode]

class I2cStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STS_NOT_INIT: _ClassVar[I2cStatusCode]
    STS_SUCCESS: _ClassVar[I2cStatusCode]
    STS_BAD_REQUEST: _ClassVar[I2cStatusCode]
    STS_NO_SPACE: _ClassVar[I2cStatusCode]
    STS_SLAVE_BUSY: _ClassVar[I2cStatusCode]
    STS_SLAVE_NACK: _ClassVar[I2cStatusCode]
    STS_INTERFACE_ERROR: _ClassVar[I2cStatusCode]
I2C0: I2cId
I2C1: I2cId
Bits7: AddressWidth
Bits8: AddressWidth
Bits10: AddressWidth
Bits16: AddressWidth
CFG_NOT_INIT: I2cConfigStatusCode
CFG_SUCCESS: I2cConfigStatusCode
CFG_BAD_REQUEST: I2cConfigStatusCode
CFG_INVALID_CLOCK_FREQ: I2cConfigStatusCode
CFG_INVALID_SLAVE_ADDR: I2cConfigStatusCode
CFG_INVALID_SLAVE_ADDR_WIDTH: I2cConfigStatusCode
CFG_INVALID_MEM_ADDR_WIDTH: I2cConfigStatusCode
CFG_INTERFACE_ERROR: I2cConfigStatusCode
STS_NOT_INIT: I2cStatusCode
STS_SUCCESS: I2cStatusCode
STS_BAD_REQUEST: I2cStatusCode
STS_NO_SPACE: I2cStatusCode
STS_SLAVE_BUSY: I2cStatusCode
STS_SLAVE_NACK: I2cStatusCode
STS_INTERFACE_ERROR: I2cStatusCode

class I2cConfigRequest(_message.Message):
    __slots__ = ("request_id", "clock_freq", "slave_addr", "slave_addr_width", "mem_addr_width", "pullups_enabled")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FREQ_FIELD_NUMBER: _ClassVar[int]
    SLAVE_ADDR_FIELD_NUMBER: _ClassVar[int]
    SLAVE_ADDR_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MEM_ADDR_WIDTH_FIELD_NUMBER: _ClassVar[int]
    PULLUPS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    clock_freq: int
    slave_addr: int
    slave_addr_width: AddressWidth
    mem_addr_width: AddressWidth
    pullups_enabled: bool
    def __init__(self, request_id: _Optional[int] = ..., clock_freq: _Optional[int] = ..., slave_addr: _Optional[int] = ..., slave_addr_width: _Optional[_Union[AddressWidth, str]] = ..., mem_addr_width: _Optional[_Union[AddressWidth, str]] = ..., pullups_enabled: bool = ...) -> None: ...

class I2cConfigStatus(_message.Message):
    __slots__ = ("request_id", "status_code")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    status_code: I2cConfigStatusCode
    def __init__(self, request_id: _Optional[int] = ..., status_code: _Optional[_Union[I2cConfigStatusCode, str]] = ...) -> None: ...

class I2cMasterRequest(_message.Message):
    __slots__ = ("request_id", "slave_addr", "write_data", "read_size", "sequence_id", "sequence_idx")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SLAVE_ADDR_FIELD_NUMBER: _ClassVar[int]
    WRITE_DATA_FIELD_NUMBER: _ClassVar[int]
    READ_SIZE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_IDX_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    slave_addr: int
    write_data: bytes
    read_size: int
    sequence_id: int
    sequence_idx: int
    def __init__(self, request_id: _Optional[int] = ..., slave_addr: _Optional[int] = ..., write_data: _Optional[bytes] = ..., read_size: _Optional[int] = ..., sequence_id: _Optional[int] = ..., sequence_idx: _Optional[int] = ...) -> None: ...

class I2cMasterStatus(_message.Message):
    __slots__ = ("request_id", "status_code", "read_data", "nack_idx", "queue_space", "buffer_space1", "buffer_space2")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    READ_DATA_FIELD_NUMBER: _ClassVar[int]
    NACK_IDX_FIELD_NUMBER: _ClassVar[int]
    QUEUE_SPACE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SPACE1_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SPACE2_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    status_code: I2cStatusCode
    read_data: bytes
    nack_idx: int
    queue_space: int
    buffer_space1: int
    buffer_space2: int
    def __init__(self, request_id: _Optional[int] = ..., status_code: _Optional[_Union[I2cStatusCode, str]] = ..., read_data: _Optional[bytes] = ..., nack_idx: _Optional[int] = ..., queue_space: _Optional[int] = ..., buffer_space1: _Optional[int] = ..., buffer_space2: _Optional[int] = ...) -> None: ...

class I2cSlaveRequest(_message.Message):
    __slots__ = ("request_id", "write_data", "read_size", "write_addr", "read_addr")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    WRITE_DATA_FIELD_NUMBER: _ClassVar[int]
    READ_SIZE_FIELD_NUMBER: _ClassVar[int]
    WRITE_ADDR_FIELD_NUMBER: _ClassVar[int]
    READ_ADDR_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    write_data: bytes
    read_size: int
    write_addr: int
    read_addr: int
    def __init__(self, request_id: _Optional[int] = ..., write_data: _Optional[bytes] = ..., read_size: _Optional[int] = ..., write_addr: _Optional[int] = ..., read_addr: _Optional[int] = ...) -> None: ...

class I2cSlaveStatus(_message.Message):
    __slots__ = ("request_id", "status_code", "read_data", "queue_space")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    READ_DATA_FIELD_NUMBER: _ClassVar[int]
    QUEUE_SPACE_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    status_code: I2cStatusCode
    read_data: bytes
    queue_space: int
    def __init__(self, request_id: _Optional[int] = ..., status_code: _Optional[_Union[I2cStatusCode, str]] = ..., read_data: _Optional[bytes] = ..., queue_space: _Optional[int] = ...) -> None: ...

class I2cSlaveNotification(_message.Message):
    __slots__ = ("access_id", "status_code", "write_data", "read_data", "queue_space")
    ACCESS_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    WRITE_DATA_FIELD_NUMBER: _ClassVar[int]
    READ_DATA_FIELD_NUMBER: _ClassVar[int]
    QUEUE_SPACE_FIELD_NUMBER: _ClassVar[int]
    access_id: int
    status_code: I2cStatusCode
    write_data: bytes
    read_data: bytes
    queue_space: int
    def __init__(self, access_id: _Optional[int] = ..., status_code: _Optional[_Union[I2cStatusCode, str]] = ..., write_data: _Optional[bytes] = ..., read_data: _Optional[bytes] = ..., queue_space: _Optional[int] = ...) -> None: ...

class I2cMsg(_message.Message):
    __slots__ = ("i2c_id", "sequence_number", "config_request", "config_status", "master_request", "master_status", "slave_request", "slave_status", "slave_notification")
    I2C_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CONFIG_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CONFIG_STATUS_FIELD_NUMBER: _ClassVar[int]
    MASTER_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MASTER_STATUS_FIELD_NUMBER: _ClassVar[int]
    SLAVE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SLAVE_STATUS_FIELD_NUMBER: _ClassVar[int]
    SLAVE_NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    i2c_id: I2cId
    sequence_number: int
    config_request: I2cConfigRequest
    config_status: I2cConfigStatus
    master_request: I2cMasterRequest
    master_status: I2cMasterStatus
    slave_request: I2cSlaveRequest
    slave_status: I2cSlaveStatus
    slave_notification: I2cSlaveNotification
    def __init__(self, i2c_id: _Optional[_Union[I2cId, str]] = ..., sequence_number: _Optional[int] = ..., config_request: _Optional[_Union[I2cConfigRequest, _Mapping]] = ..., config_status: _Optional[_Union[I2cConfigStatus, _Mapping]] = ..., master_request: _Optional[_Union[I2cMasterRequest, _Mapping]] = ..., master_status: _Optional[_Union[I2cMasterStatus, _Mapping]] = ..., slave_request: _Optional[_Union[I2cSlaveRequest, _Mapping]] = ..., slave_status: _Optional[_Union[I2cSlaveStatus, _Mapping]] = ..., slave_notification: _Optional[_Union[I2cSlaveNotification, _Mapping]] = ...) -> None: ...
