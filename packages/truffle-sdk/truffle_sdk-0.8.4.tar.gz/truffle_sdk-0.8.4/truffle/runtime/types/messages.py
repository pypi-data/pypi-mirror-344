"""
Message type wrappers for protobuf messages.
Provides clean Python classes that wrap the underlying protobuf messages,
following the same pattern as our ModelDescription wrapper.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import truffle.platform.sdk_pb2 as sdk_pb2
from .enums import Role, ResponseFormat

@dataclass
class GenerationUsage:
    """Clean wrapper for protobuf GenerationUsage message."""
    prompt_tokens: int
    completion_tokens: int
    approx_time: float

    @classmethod
    def from_proto(cls, proto: Optional[sdk_pb2.GenerationUsage]) -> Optional['GenerationUsage']:
        """Create from protobuf message."""
        if proto is None:
            return None
        return cls(
            prompt_tokens=proto.prompt_tokens,
            completion_tokens=proto.completion_tokens,
            approx_time=proto.approx_time
        )

    def to_proto(self) -> sdk_pb2.GenerationUsage:
        """Convert to protobuf message."""
        return sdk_pb2.GenerationUsage(
            prompt_tokens=self.prompt_tokens,
            completion_tokens=self.completion_tokens,
            approx_time=self.approx_time
        )

@dataclass
class Content:
    """Clean wrapper for protobuf Content message."""
    role: Role
    content: str

    @classmethod
    def from_proto(cls, proto: sdk_pb2.Content) -> 'Content':
        """Create from protobuf message."""
        return cls(
            role=Role.from_proto(proto.role),
            content=proto.content
        )

    def to_proto(self) -> sdk_pb2.Content:
        """Convert to protobuf message."""
        return sdk_pb2.Content(
            role=self.role.to_proto(),
            content=self.content
        )

class Context:
    """Clean wrapper for protobuf Context message."""
    def __init__(self):
        self._history: List[Content] = []

    @property
    def history(self) -> List[Content]:
        """Get message history."""
        return self._history

    def add_message(self, role: Role, content: str) -> None:
        """Add a message to the context."""
        self._history.append(Content(role=role, content=content))

    @classmethod
    def from_proto(cls, proto: sdk_pb2.Context) -> 'Context':
        """Create from protobuf message."""
        context = cls()
        for msg in proto.history:
            context._history.append(Content.from_proto(msg))
        return context

    def to_proto(self) -> sdk_pb2.Context:
        """Convert to protobuf message."""
        proto = sdk_pb2.Context()
        for msg in self._history:
            proto.history.append(msg.to_proto())
        return proto

@dataclass
class SortedEmbedding:
    """Clean wrapper for protobuf SortedEmbedding message."""
    text: str
    score: float

    @classmethod
    def from_proto(cls, proto: sdk_pb2.SortedEmbedding) -> 'SortedEmbedding':
        """Create from protobuf message."""
        return cls(
            text=proto.text,
            score=proto.score
        )

    def to_proto(self) -> sdk_pb2.SortedEmbedding:
        """Convert to protobuf message."""
        return sdk_pb2.SortedEmbedding(
            text=self.text,
            score=self.score
        )

@dataclass
class GenerateResponseFormat:
    """Clean wrapper for protobuf GenerateResponseFormat message."""
    format: ResponseFormat
    schema: Optional[str] = None

    @classmethod
    def from_proto(cls, proto: Optional[sdk_pb2.GenerateResponseFormat]) -> Optional['GenerateResponseFormat']:
        """Create from protobuf message."""
        if proto is None:
            return None
        return cls(
            format=ResponseFormat.from_proto(proto.format),
            schema=proto.schema if proto.HasField("schema") else None
        )

    def to_proto(self) -> sdk_pb2.GenerateResponseFormat:
        """Convert to protobuf message."""
        proto = sdk_pb2.GenerateResponseFormat(
            format=self.format.to_proto()
        )
        if self.schema is not None:
            proto.schema = self.schema
        return proto 