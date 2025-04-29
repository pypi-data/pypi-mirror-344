"""
Enum wrappers for protobuf enums.
Provides clean Python enums that wrap the underlying protobuf enums,
following the same pattern as our ModelDescription wrapper.
"""

from enum import Enum
import truffle.platform.sdk_pb2 as sdk_pb2

class FinishReason(Enum):
    """Clean wrapper for protobuf GenerateFinishReason enum."""
    UNSPECIFIED = "unspecified"
    LENGTH = "length"
    STOP = "stop"
    ERROR = "error"
    USER = "user"

    @classmethod
    def from_proto(cls, proto_reason: sdk_pb2.GenerateFinishReason) -> 'FinishReason':
        """Convert from protobuf enum to our enum."""
        mapping = {
            sdk_pb2.FINISH_REASON_UNSPECIFIED: cls.UNSPECIFIED,
            sdk_pb2.FINISH_REASON_LENGTH: cls.LENGTH,
            sdk_pb2.FINISH_REASON_STOP: cls.STOP,
            sdk_pb2.FINISH_REASON_ERROR: cls.ERROR,
            sdk_pb2.FINISH_REASON_USER: cls.USER
        }
        return mapping.get(proto_reason, cls.UNSPECIFIED)

    def to_proto(self) -> sdk_pb2.GenerateFinishReason:
        """Convert to protobuf enum."""
        mapping = {
            self.UNSPECIFIED: sdk_pb2.FINISH_REASON_UNSPECIFIED,
            self.LENGTH: sdk_pb2.FINISH_REASON_LENGTH,
            self.STOP: sdk_pb2.FINISH_REASON_STOP,
            self.ERROR: sdk_pb2.FINISH_REASON_ERROR,
            self.USER: sdk_pb2.FINISH_REASON_USER
        }
        return mapping[self]

class ModelType(Enum):
    """Clean wrapper for protobuf ModelDescription.ModelType enum."""
    UNSPECIFIED = "unspecified"
    SMART = "smart"
    FAST = "fast"
    VISION = "vision"
    AGI = "agi"
    
    @classmethod
    def from_proto(cls, proto_type: sdk_pb2.ModelDescription.ModelType) -> 'ModelType':
        """Convert from protobuf enum to our enum."""
        mapping = {
            sdk_pb2.ModelDescription.MODEL_UNSPECIFIED: cls.UNSPECIFIED,
            sdk_pb2.ModelDescription.MODEL_SMART: cls.SMART,
            sdk_pb2.ModelDescription.MODEL_FAST: cls.FAST,
            sdk_pb2.ModelDescription.MODEL_VISION: cls.VISION,
            sdk_pb2.ModelDescription.MODEL_AGI: cls.AGI
        }
        return mapping.get(proto_type, cls.UNSPECIFIED)

    def to_proto(self) -> sdk_pb2.ModelDescription.ModelType:
        """Convert to protobuf enum."""
        mapping = {
            self.UNSPECIFIED: sdk_pb2.ModelDescription.MODEL_UNSPECIFIED,
            self.SMART: sdk_pb2.ModelDescription.MODEL_SMART,
            self.FAST: sdk_pb2.ModelDescription.MODEL_FAST,
            self.VISION: sdk_pb2.ModelDescription.MODEL_VISION,
            self.AGI: sdk_pb2.ModelDescription.MODEL_AGI
        }
        return mapping[self]

class Role(Enum):
    """Clean wrapper for protobuf Content.Role enum."""
    INVALID = "invalid"
    USER = "user"
    AI = "ai"
    SYSTEM = "system"
    
    @classmethod
    def from_proto(cls, proto_role: sdk_pb2.Content.Role) -> 'Role':
        """Convert from protobuf enum to our enum."""
        mapping = {
            sdk_pb2.Content.ROLE_INVALID: cls.INVALID,
            sdk_pb2.Content.ROLE_USER: cls.USER,
            sdk_pb2.Content.ROLE_AI: cls.AI,
            sdk_pb2.Content.ROLE_SYSTEM: cls.SYSTEM
        }
        return mapping.get(proto_role, cls.INVALID)

    def to_proto(self) -> sdk_pb2.Content.Role:
        """Convert to protobuf enum."""
        mapping = {
            self.INVALID: sdk_pb2.Content.ROLE_INVALID,
            self.USER: sdk_pb2.Content.ROLE_USER,
            self.AI: sdk_pb2.Content.ROLE_AI,
            self.SYSTEM: sdk_pb2.Content.ROLE_SYSTEM
        }
        return mapping[self]

class ResponseFormat(Enum):
    """Clean wrapper for protobuf GenerateResponseFormat.ResponseFormat enum."""
    TEXT = "text"
    JSON = "json"
    
    @classmethod
    def from_proto(cls, proto_format: sdk_pb2.GenerateResponseFormat.ResponseFormat) -> 'ResponseFormat':
        """Convert from protobuf enum to our enum."""
        mapping = {
            sdk_pb2.GenerateResponseFormat.RESPONSE_TEXT: cls.TEXT,
            sdk_pb2.GenerateResponseFormat.RESPONSE_JSON: cls.JSON
        }
        return mapping.get(proto_format, cls.TEXT)  # Default to TEXT for unknown values

    def to_proto(self) -> sdk_pb2.GenerateResponseFormat.ResponseFormat:
        """Convert to protobuf enum."""
        mapping = {
            self.TEXT: sdk_pb2.GenerateResponseFormat.RESPONSE_TEXT,
            self.JSON: sdk_pb2.GenerateResponseFormat.RESPONSE_JSON
        }
        return mapping[self] 