"""
Response type wrappers for protobuf response messages.
Provides clean Python classes that wrap the underlying protobuf responses.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import truffle.platform.sdk_pb2 as sdk_pb2
from .enums import FinishReason
from .messages import GenerationUsage, SortedEmbedding

@dataclass
class SDKResponse:
    """Clean wrapper for protobuf SDKResponse message."""
    ok: bool
    error: Optional[str] = None

    @classmethod
    def from_proto(cls, proto: sdk_pb2.SDKResponse) -> 'SDKResponse':
        return cls(
            ok=proto.ok,
            error=proto.error if proto.HasField("error") else None
        )

    def to_proto(self) -> sdk_pb2.SDKResponse:
        proto = sdk_pb2.SDKResponse(ok=self.ok)
        if self.error:
            proto.error = self.error
        return proto

@dataclass
class GenerateResponse:
    """Clean wrapper for protobuf GenerateResponse message."""
    response: str
    finish_reason: FinishReason
    usage: Optional[GenerationUsage] = None
    error: Optional[str] = None

    @classmethod
    def from_proto(cls, proto: sdk_pb2.GenerateResponse) -> 'GenerateResponse':
        return cls(
            response=proto.response,
            finish_reason=FinishReason.from_proto(proto.finish_reason),
            usage=GenerationUsage.from_proto(proto.usage) if proto.HasField("usage") else None,
            error=proto.error if proto.HasField("error") else None
        )

    def to_proto(self) -> sdk_pb2.GenerateResponse:
        proto = sdk_pb2.GenerateResponse(
            response=self.response,
            finish_reason=self.finish_reason.to_proto()
        )
        if self.usage:
            proto.usage.CopyFrom(self.usage.to_proto())
        if self.error:
            proto.error = self.error
        return proto

@dataclass
class TokenResponse:
    """Clean wrapper for protobuf TokenResponse message (used in streaming)."""
    token: str
    finish_reason: Optional[FinishReason] = None
    usage: Optional[GenerationUsage] = None
    error: Optional[str] = None

    @classmethod
    def from_proto(cls, proto: sdk_pb2.TokenResponse) -> 'TokenResponse':
        return cls(
            token=proto.token,
            finish_reason=FinishReason.from_proto(proto.finish_reason) if proto.HasField("finish_reason") else None,
            usage=GenerationUsage.from_proto(proto.usage) if proto.HasField("usage") else None,
            error=proto.error if proto.HasField("error") else None
        )

    def to_proto(self) -> sdk_pb2.TokenResponse:
        proto = sdk_pb2.TokenResponse(token=self.token)
        if self.finish_reason:
            proto.finish_reason = self.finish_reason.to_proto()
        if self.usage:
            proto.usage.CopyFrom(self.usage.to_proto())
        if self.error:
            proto.error = self.error
        return proto

@dataclass
class EmbedResponse:
    """Clean wrapper for protobuf EmbedResponse message."""
    results: List[SortedEmbedding]

    @classmethod
    def from_proto(cls, proto: sdk_pb2.EmbedResponse) -> 'EmbedResponse':
        return cls(
            results=[SortedEmbedding.from_proto(r) for r in proto.results]
        )

    def to_proto(self) -> sdk_pb2.EmbedResponse:
        proto = sdk_pb2.EmbedResponse()
        for r in self.results:
            proto.results.append(r.to_proto())
        return proto

@dataclass
class UserResponse:
    """Clean wrapper for protobuf UserResponse message."""
    response: Optional[str] = None
    attached_files: Optional[List[str]] = None
    error: Optional[str] = None

    @classmethod
    def from_proto(cls, proto: sdk_pb2.UserResponse) -> 'UserResponse':
        return cls(
            response=proto.response if proto.HasField("response") else None,
            attached_files=list(proto.attached_files) if proto.attached_files else None,
            error=proto.error if proto.HasField("error") else None
        )

    def to_proto(self) -> sdk_pb2.UserResponse:
        proto = sdk_pb2.UserResponse()
        if self.response is not None:
            proto.response = self.response
        if self.attached_files:
            proto.attached_files.extend(self.attached_files)
        if self.error:
            proto.error = self.error
        return proto

@dataclass
class SystemToolResponse:
    """Clean wrapper for protobuf SystemToolResponse message."""
    response: Optional[str] = None
    results: Optional[Dict[str, str]] = None
    error: Optional[str] = None

    @classmethod
    def from_proto(cls, proto: sdk_pb2.SystemToolResponse) -> 'SystemToolResponse':
        return cls(
            response=proto.response if proto.HasField("response") else None,
            results=dict(proto.results) if proto.results else None,
            error=proto.error if proto.HasField("error") else None
        )

    def to_proto(self) -> sdk_pb2.SystemToolResponse:
        proto = sdk_pb2.SystemToolResponse()
        if self.response is not None:
            proto.response = self.response
        if self.results:
            proto.results.update(self.results)
        if self.error:
            proto.error = self.error
        return proto 