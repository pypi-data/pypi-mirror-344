from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteResourceRequest(_message.Message):
    __slots__ = ("local_resource_id", "reporter_type")
    LOCAL_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    REPORTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    local_resource_id: str
    reporter_type: str
    def __init__(self, local_resource_id: _Optional[str] = ..., reporter_type: _Optional[str] = ...) -> None: ...
