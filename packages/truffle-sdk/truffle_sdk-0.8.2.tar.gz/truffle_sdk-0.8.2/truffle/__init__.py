"""
Truffle SDK - A simple interface for truffle tools and models.
"""

from typing import List, Dict, Any, Optional, Iterator

__version__ = "0.7.2"

from .runtime import Runtime, tool, args, group, HOST
from .common import get_logger, log
from .api import TruffleClient
from .types import *
from .utils.banner import get_truffle_banner, should_show_banner
from .runtime.types.responses import (
    SystemToolResponse, TokenResponse, GenerateResponse, 
    UserResponse, EmbedResponse
)
from .runtime.types.models import ModelDescription
from .runtime.types.enums import ResponseFormat

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Display banner only if not in container/app context
if should_show_banner():
    print(get_truffle_banner(), end='')

# Singleton management
_default_client: Optional[TruffleClient] = None

def _get_client() -> TruffleClient:
    global _default_client
    if _default_client is None:
        _default_client = TruffleClient()
    return _default_client

def run(class_instance: Any) -> Any:
    """Run a Truffle application.
    
    Args:
        class_instance: An instance of a class with Truffle tools.
        
    Returns:
        The result of building the Truffle application.
    """
    log.info(f"Building and running Truffle app: {class_instance.__class__.__name__}")
    rt = Runtime()()
    return rt.build(class_instance)

# Clean API surface
def perplexity_search(
    query: str,
    model: str = "sonar-pro",
    response_fmt: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> SystemToolResponse:
    """Clean interface for Perplexity search."""
    return _get_client().perplexity_search(query, model, response_fmt, system_prompt)

def infer(
    prompt: str,
    model_id: Optional[int] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    response_format: Optional[ResponseFormat] = None,
    response_schema: Optional[str] = None,
    system_prompt: Optional[str] = None,
    context_idx: Optional[int] = None,
    **kwargs
) -> Iterator[TokenResponse]:
    """Clean interface for streaming inference."""
    return _get_client().infer(
        prompt, model_id, temperature, max_tokens,
        response_format, response_schema, system_prompt,
        context_idx, **kwargs
    )

def infer_sync(
    prompt: str,
    model_id: Optional[int] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    response_format: Optional[ResponseFormat] = None,
    response_schema: Optional[str] = None,
    system_prompt: Optional[str] = None,
    context_idx: Optional[int] = None,
    **kwargs
) -> GenerateResponse:
    """Clean interface for synchronous inference."""
    return _get_client().infer_sync(
        prompt, model_id, temperature, max_tokens,
        response_format, response_schema, system_prompt,
        context_idx, **kwargs
    )

def ask_user(
    message: str, 
    reason: Optional[str] = "Tool needs input to continue."
) -> UserResponse:
    """Clean interface for user interaction."""
    return _get_client().ask_user(message, reason)

def query_embed(
    query: str, 
    documents: List[str]
) -> EmbedResponse:
    """Clean interface for embeddings."""
    return _get_client().query_embed(query, documents)

def get_models() -> List[ModelDescription]:
    """Clean interface for model listing."""
    return _get_client().get_models()

def close():
    """Close the default client if it exists."""
    global _default_client
    if _default_client is not None:
        _default_client.close()
        _default_client = None

# Export everything
__all__ = [
    "Runtime", "tool", "args", "group", "HOST", "get_logger", "log", "run",
    "__version__",
    'TruffleClient',  # Still expose for advanced usage
    'perplexity_search',
    'infer',
    'infer_sync',
    'ask_user',
    'query_embed',
    'get_models',
    'close'
]