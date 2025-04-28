"""
Builder classes for constructing conversations and other structured objects.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import truffle.platform.sdk_pb2 as sdk_pb2
from ..types.messages import Context, Content
from ..types.enums import Role

class ConversationBuilder:
    """
    Fluent builder for constructing conversation contexts.
    Provides a clean API for building chat histories.
    """
    def __init__(self):
        self._messages: List[Content] = []
        self._system_prompt: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
        self._temperature: float = 0.7
        self._max_tokens: Optional[int] = None
        self.history: List[tuple[str, str]] = []

    def system(self, message: str) -> 'ConversationBuilder':
        """Set system prompt"""
        self._system_prompt = message
        self.history.append(("system", message))
        self._messages.append(Content(role=Role.SYSTEM, content=message))
        return self

    def user(self, message: str, **kwargs) -> 'ConversationBuilder':
        """Add user message"""
        self.history.append(("user", message))
        self._messages.append(Content(role=Role.USER, content=message))
        return self

    def assistant(self, message: str, **kwargs) -> 'ConversationBuilder':
        """Add assistant message"""
        self.history.append(("assistant", message))
        self._messages.append(Content(role=Role.AI, content=message))
        return self

    def temperature(self, temp: float) -> 'ConversationBuilder':
        """Set temperature for generation"""
        self._temperature = temp
        return self

    def max_tokens(self, tokens: int) -> 'ConversationBuilder':
        """Set max tokens for generation"""
        self._max_tokens = tokens
        return self

    def with_metadata(self, **kwargs) -> 'ConversationBuilder':
        """Add conversation-level metadata"""
        self._metadata.update(kwargs)
        return self

    def build(self) -> Dict[str, Any]:
        """Build final conversation context dictionary (for external use if needed)."""
        return {
            "messages": [{"role": msg.role.value, "content": msg.content} for msg in self._messages],
            "system_prompt": self._system_prompt,
            "metadata": self._metadata,
            "temperature": self._temperature,
            "max_tokens": self._max_tokens
        }

    def build_context(self) -> Context:
        """Build our Context wrapper object."""
        context = Context()
        role_mapping = {
            "system": Role.SYSTEM,
            "user": Role.USER,
            "assistant": Role.AI,
        }
        for role_str, message in self.history:
            role = role_mapping.get(role_str)
            if role:
                context.add_message(role, message)
        return context

    def build_context_proto(self) -> sdk_pb2.Context:
        """Convert conversation history to raw proto format (for gRPC)."""
        return self.build_context().to_proto()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class ResponseBuilder:
    """
    Builder for constructing formatted responses.
    Handles different response formats and metadata.
    """
    def __init__(self, content: Any):
        self._content = content
        self._metadata = {}
        self._format = "text"

    def as_json(self) -> 'ResponseBuilder':
        """Format response as JSON"""
        self._format = "json"
        return self

    def as_markdown(self) -> 'ResponseBuilder':
        """Format response as markdown"""
        self._format = "markdown"
        return self

    def with_metadata(self, **kwargs) -> 'ResponseBuilder':
        """Add response metadata"""
        self._metadata.update(kwargs)
        return self

    def build(self) -> Dict[str, Any]:
        """Build final response"""
        return {
            "content": self._format_content(),
            "metadata": self._metadata,
            "format": self._format
        }

    def _format_content(self) -> Any:
        """Format content based on specified format"""
        if self._format == "json":
            import json
            return json.loads(str(self._content))
        elif self._format == "markdown":
            return f"```\n{self._content}\n```"
        return str(self._content)

class SearchBuilder:
    """
    Builder for constructing search requests.
    Provides clean API for configuring search parameters.
    """
    def __init__(self, query: str):
        self._query = query
        self._model = "sonar-pro"
        self._response_format = None
        self._system_prompt = None
        self._metadata = {}

    def model(self, model: str) -> 'SearchBuilder':
        """Set model to use"""
        self._model = model
        return self

    def format(self, fmt: str) -> 'SearchBuilder':
        """Set response format"""
        self._response_format = fmt
        return self

    def system_prompt(self, prompt: str) -> 'SearchBuilder':
        """Set system prompt"""
        self._system_prompt = prompt
        return self

    def with_metadata(self, **kwargs) -> 'SearchBuilder':
        """Add search metadata"""
        self._metadata.update(kwargs)
        return self

    def build(self) -> Dict[str, Any]:
        """Build final search request"""
        return {
            "query": self._query,
            "model": self._model,
            "response_format": self._response_format,
            "system_prompt": self._system_prompt,
            "metadata": self._metadata
        } 