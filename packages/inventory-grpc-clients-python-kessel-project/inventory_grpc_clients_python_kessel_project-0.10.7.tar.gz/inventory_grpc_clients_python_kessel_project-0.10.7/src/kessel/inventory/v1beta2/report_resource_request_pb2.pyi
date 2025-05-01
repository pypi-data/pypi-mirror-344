from kessel.inventory.v1beta2 import resource_pb2 as _resource_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReportResourceRequest(_message.Message):
    __slots__ = ("resource",)
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    resource: _resource_pb2.Resource
    def __init__(self, resource: _Optional[_Union[_resource_pb2.Resource, _Mapping]] = ...) -> None: ...
