"""
Core model types and descriptions for the Truffle runtime.
Provides a clean wrapper around the protobuf model description.
"""

from typing import Optional, List, Dict
from datetime import datetime, timedelta
import truffle.platform.sdk_pb2 as sdk_pb2
from .enums import ModelType

class ModelDescription:
    """
    Wrapper for the sdk_pb2.ModelDescription protobuf message.
    Provides a Pythonic interface to the model's properties.
    The protobuf definition is the single source of truth.
    """
    def __init__(self, proto: Optional[sdk_pb2.ModelDescription] = None, **kwargs):
        """Initialize from a proto instance or keyword arguments."""
        if proto:
            self._proto = proto
        else:
            # Basic keyword arg handling - more robust parsing could be added
            self._proto = sdk_pb2.ModelDescription(**kwargs)

    @property
    def model_id(self) -> int:
        return self._proto.model_id

    @model_id.setter
    def model_id(self, value: int):
        self._proto.model_id = value

    @property
    def name(self) -> str:
        return self._proto.name

    @name.setter
    def name(self, value: str):
        self._proto.name = value

    @property
    def description(self) -> str:
        return self._proto.description

    @description.setter
    def description(self, value: str):
        self._proto.description = value

    @property
    def capabilities(self) -> sdk_pb2.ModelDescription.Capabilities:
        # Return the underlying capabilities proto message directly
        # Consumers can access its fields (structured_output, etc.)
        return self._proto.capabilities

    @property
    def type(self) -> ModelType:
        """Get the model type as our clean enum."""
        return ModelType.from_proto(self._proto.type)

    @type.setter
    def type(self, value: ModelType):
        """Set the model type from our clean enum."""
        self._proto.type = value.to_proto()

    @property
    def is_local(self) -> bool:
        return self._proto.is_local

    @is_local.setter
    def is_local(self, value: bool):
        self._proto.is_local = value

    def to_proto(self) -> sdk_pb2.ModelDescription:
        """Return the internal protobuf message."""
        return self._proto

    @classmethod
    def from_proto(cls, proto: sdk_pb2.ModelDescription) -> 'ModelDescription':
        """Create a wrapper instance from a protobuf message."""
        if not isinstance(proto, sdk_pb2.ModelDescription):
            raise TypeError(f"Expected sdk_pb2.ModelDescription, got {type(proto)}")
        return cls(proto=proto)

    def __repr__(self) -> str:
        return f"ModelDescription(model_id={self.model_id}, name='{self.name}', type={self.type.value})"

class ModelRegistry:
    """
    Thread-safe cache for model descriptions.
    """
    def __init__(self, cache_ttl: int = 300):  # 5 minute default TTL
        self._models: Dict[int, ModelDescription] = {}
        self._last_update: Optional[datetime] = None
        self._cache_ttl = timedelta(seconds=cache_ttl)

    def update_models(self, models: List[ModelDescription]) -> None:
        """Update the cached models."""
        self._models = {model.model_id: model for model in models}
        self._last_update = datetime.now()

    def get_models(self) -> List[ModelDescription]:
        """Get all cached models."""
        return list(self._models.values())

    def get_model(self, model_id: int) -> Optional[ModelDescription]:
        """Get a specific model by ID."""
        return self._models.get(model_id)

    def is_stale(self) -> bool:
        """Check if the cache is stale."""
        if self._last_update is None:
            return True
        return (datetime.now() - self._last_update) > self._cache_ttl

    def clear(self) -> None:
        """Clear the cache."""
        self._models.clear()
        self._last_update = None 