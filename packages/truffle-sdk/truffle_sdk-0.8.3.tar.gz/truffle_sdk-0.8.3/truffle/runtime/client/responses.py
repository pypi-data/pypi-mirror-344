"""
Response wrapper classes for better handling of different response types.
"""

from typing import Any, Dict, Optional, List
from dataclasses import dataclass
import json

import truffle.platform.sdk_pb2 as sdk_pb2
from google.protobuf.json_format import MessageToDict
from ..types.enums import FinishReason
from ..types.messages import GenerationUsage, SortedEmbedding

@dataclass
class SearchResponse:
    """
    Wrapper for the sdk_pb2.GenerateResponse protobuf message.
    Provides direct access to the underlying proto fields.
    """
    _proto: sdk_pb2.GenerateResponse

    @property
    def content(self) -> str:
        """The main response content."""
        return self._proto.response

    @property
    def finish_reason(self) -> FinishReason:
        """The reason generation finished."""
        if not self._proto.HasField("finish_reason"):
            return FinishReason.UNSPECIFIED
        return FinishReason.from_proto(self._proto.finish_reason)

    @property
    def usage(self) -> Optional[GenerationUsage]:
        """Token usage information."""
        if not self._proto.HasField("usage"):
            return None
        return GenerationUsage.from_proto(self._proto.usage)

    @property
    def error(self) -> Optional[str]:
        """Error message, if any."""
        if self._proto.HasField("error"):
             return self._proto.error
        return None

    def to_proto(self) -> sdk_pb2.GenerateResponse:
        """Return the internal protobuf message."""
        return self._proto

    @classmethod
    def from_proto(cls, proto: sdk_pb2.GenerateResponse) -> 'SearchResponse':
        """Create a wrapper instance from a protobuf message."""
        if not isinstance(proto, sdk_pb2.GenerateResponse):
            raise TypeError(f"Expected sdk_pb2.GenerateResponse, got {type(proto)}")
        return cls(_proto=proto)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the wrapped proto to a dictionary."""
        d = MessageToDict(self._proto, preserving_proto_field_name=True)
        if "finish_reason" in d:
            d["finish_reason"] = self.finish_reason.value
        if "usage" in d and self.usage:
            d["usage"] = {
                "prompt_tokens": self.usage.prompt_tokens,
                "completion_tokens": self.usage.completion_tokens,
                "approx_time": self.usage.approx_time
            }
        return d

    def __repr__(self) -> str:
        return f"SearchResponse(content='{self.content[:50]}...', finish_reason={self.finish_reason.value})"

@dataclass
class InferenceResponse:
    """
    Wrapper for the sdk_pb2.TokenResponse protobuf message.
    Provides direct access to the underlying proto fields for a single token/chunk.
    """
    _proto: sdk_pb2.TokenResponse

    @property
    def token(self) -> str:
        """The token content for this chunk."""
        return self._proto.token

    @property
    def finish_reason(self) -> FinishReason:
        """The reason generation finished, if applicable to this chunk."""
        if not self._proto.HasField("finish_reason"):
            return FinishReason.UNSPECIFIED
        return FinishReason.from_proto(self._proto.finish_reason)

    @property
    def usage(self) -> Optional[GenerationUsage]:
        """Token usage information, if applicable to this chunk."""
        if not self._proto.HasField("usage"):
            return None
        return GenerationUsage.from_proto(self._proto.usage)

    @property
    def error(self) -> Optional[str]:
        """Error message, if any, for this chunk."""
        if self._proto.HasField("error"):
            return self._proto.error
        return None

    def to_proto(self) -> sdk_pb2.TokenResponse:
        """Return the internal protobuf message."""
        return self._proto

    @classmethod
    def from_proto(cls, proto: sdk_pb2.TokenResponse) -> 'InferenceResponse':
        """Create a wrapper instance from a protobuf message."""
        if not isinstance(proto, sdk_pb2.TokenResponse):
            raise TypeError(f"Expected sdk_pb2.TokenResponse, got {type(proto)}")
        return cls(_proto=proto)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the wrapped proto to a dictionary."""
        d = MessageToDict(self._proto, preserving_proto_field_name=True)
        if "finish_reason" in d:
            d["finish_reason"] = self.finish_reason.value
        if "usage" in d and self.usage:
            d["usage"] = {
                "prompt_tokens": self.usage.prompt_tokens,
                "completion_tokens": self.usage.completion_tokens,
                "approx_time": self.usage.approx_time
            }
        return d

    def __repr__(self) -> str:
        return f"InferenceResponse(token='{self.token}', finish_reason={self.finish_reason.value})"

@dataclass
class EmbeddingResponse:
    """
    Wrapper for the sdk_pb2.EmbedResponse protobuf message.
    Provides access to embedding results and helper methods.
    """
    _proto: sdk_pb2.EmbedResponse
    _query: Optional[str] = None

    @property
    def query(self) -> Optional[str]:
        """Return the query associated with these embeddings (if provided)."""
        return self._query

    @property
    def results(self) -> List[SortedEmbedding]:
        """Return the list of embedding results."""
        return [SortedEmbedding.from_proto(r) for r in self._proto.results]

    def filter(self, threshold: float) -> 'EmbeddingResponse':
        """Filter results by similarity threshold (modifies internal proto)."""
        current_results = list(self._proto.results)
        self._proto.results.clear()
        self._proto.results.extend([r for r in current_results if r.score >= threshold])
        return self

    def top_k(self, k: int) -> 'EmbeddingResponse':
        """Get top k results (modifies internal proto)."""
        sorted_docs = sorted(
            self._proto.results,
            key=lambda x: x.score,
            reverse=True
        )[:k]
        self._proto.results.clear()
        self._proto.results.extend(sorted_docs)
        return self

    def to_proto(self) -> sdk_pb2.EmbedResponse:
        """Return the internal protobuf message."""
        return self._proto

    @classmethod
    def from_proto(cls, proto: sdk_pb2.EmbedResponse, query: Optional[str] = None) -> 'EmbeddingResponse':
        """Create a wrapper instance from a protobuf message."""
        return cls(_proto=proto, _query=query)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary including the query."""
        data = {
            'results': [
                {'text': r.text, 'score': r.score}
                for r in self.results
            ]
        }
        if self._query:
            data['query'] = self._query
        return data

    def __repr__(self) -> str:
        count = len(self.results)
        return f"EmbeddingResponse(query='{self._query}', results_count={count})" 