"""
TruffleClient implementation for interacting with the TruffleSDK service.
"""

import os
import grpc
from typing import List, Optional, Iterator, Union, Generator, Any
from contextlib import contextmanager

from truffle.platform import APP_SOCK
import truffle.platform.sdk_pb2 as sdk_pb2
import truffle.platform.sdk_pb2_grpc as sdk_pb2_grpc
from truffle.common import get_logger
from ..types.models import ModelDescription
from ..types.enums import Role, ResponseFormat, FinishReason
from ..types.messages import Content, Context, GenerateResponseFormat
from .responses import (
    SearchResponse,
    InferenceResponse,
    EmbeddingResponse,
)
from .builders import ConversationBuilder

logger = get_logger()

class TruffleClient:
    """
    Client for interacting with the TruffleSDK service.
    Implements a singleton pattern for global access with enhanced robustness.
    """
    _instance = None
    _channel = None
    _stub = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating new TruffleClient instance")
            cls._instance = super(TruffleClient, cls).__new__(cls)
            cls._instance._channel = None
            cls._instance._stub = None
            
            # Set the endpoint from APP_SOCK, ensuring proper unix:// prefix
            endpoint = APP_SOCK
            if not endpoint.startswith('unix://'):
                endpoint = f'unix://{endpoint}'
            cls._instance._endpoint = endpoint
            logger.debug(f"Initialized endpoint: {cls._instance._endpoint}")
            
            # Ensure connection is set up
            cls._instance._setup_grpc()
        return cls._instance

    def _setup_grpc(self):
        """Setup gRPC channel and stub."""
        try:
            if self._channel:
                self._channel.close()
            
            logger.debug(f"Setting up gRPC channel with endpoint: {self._endpoint}")
            self._channel = grpc.insecure_channel(self._endpoint)
            self._stub = sdk_pb2_grpc.TruffleSDKStub(self._channel)
            logger.debug("gRPC setup completed successfully")
        except Exception as e:
            logger.error(f"Failed to setup gRPC connection: {e}")
            self._stub = None
            self._channel = None
            raise

    def _ensure_connection(self):
        """Ensure connection to the gRPC server."""
        if self._stub is None:
            logger.debug("No stub found, setting up gRPC...")
            self._setup_grpc()

    def get_models(self) -> List[ModelDescription]:
        """Get available models from the service."""
        try:
            if self._stub is None:
                logger.warning("No connection available, returning empty model list")
                return []
                
            request = sdk_pb2.GetModelsRequest()
            response = self._stub.GetModels(request)
            return [ModelDescription.from_proto(model) for model in response.models]
        except grpc.RpcError as e:
            logger.error(f"gRPC error getting models: {e.details()}")
            return []
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            return []

    def search(
        self,
        query: str,
        model_id: Optional[int] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        response_format: Optional[ResponseFormat] = None,
        system_prompt: Optional[str] = None
    ) -> SearchResponse:
        """
        Perform a search using InferSync.
        
        Args:
            query: The search query (maps to message field in GenerateRequest)
            model_id: Optional model ID to use
            max_tokens: Optional maximum tokens to generate
            temperature: Optional temperature for generation
            response_format: Optional response format specification
            system_prompt: Optional system prompt to prepend
            
        Returns:
            SearchResponse wrapping the GenerateResponse proto
        """
        try:
            if self._stub is None:
                logger.warning("No connection available, returning empty search response")
                return SearchResponse.from_proto(sdk_pb2.GenerateResponse())

            request = sdk_pb2.GenerateRequest(
                message=query,
                model_id=model_id if model_id is not None else 0,
                max_tokens=max_tokens if max_tokens is not None else 0,
                temperature=temperature if temperature is not None else 0.0
            )
            
            if response_format is not None:
                fmt = GenerateResponseFormat(format=response_format)
                request.fmt.CopyFrom(fmt.to_proto())
                
            if system_prompt is not None:
                context = sdk_pb2.Context()
                system = context.history.add()
                system.role = Role.SYSTEM.to_proto()
                system.content = system_prompt
                request.context.CopyFrom(context)
            
            self._ensure_connection()
            response = self._stub.InferSync(request)
            return SearchResponse.from_proto(response)
            
        except grpc.RpcError as e:
            logger.error(f"gRPC error in search: {e.details()}")
            return SearchResponse.from_proto(sdk_pb2.GenerateResponse(
                error=e.details()
            ))
        except Exception as e:
            logger.error(f"Error in search: {e}")
            return SearchResponse.from_proto(sdk_pb2.GenerateResponse(
                error=str(e)
            ))

    def infer(
        self,
        message: Union[str, sdk_pb2.Context],
        model_id: Optional[int] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        response_format: Optional[ResponseFormat] = None
    ) -> Iterator[InferenceResponse]:
        """
        Perform streaming inference using Infer.
        
        Args:
            message: The input message or context (maps to message or context field in GenerateRequest)
            model_id: Optional model ID to use
            max_tokens: Optional maximum tokens to generate
            temperature: Optional temperature for generation
            response_format: Optional response format specification
            
        Yields:
            InferenceResponse objects wrapping TokenResponse protos
        """
        try:
            request = sdk_pb2.GenerateRequest(
                model_id=model_id if model_id is not None else 0,
                max_tokens=max_tokens if max_tokens is not None else 0,
                temperature=temperature if temperature is not None else 0.0
            )
            
            if isinstance(message, sdk_pb2.Context):
                request.context.CopyFrom(message)
            else:
                request.message = message
                
            if response_format is not None:
                fmt = GenerateResponseFormat(format=response_format)
                request.fmt.CopyFrom(fmt.to_proto())
            
            self._ensure_connection()
            response_stream = self._stub.Infer(request)
            
            for response in response_stream:
                yield InferenceResponse.from_proto(response)
                    
        except grpc.RpcError as e:
            logger.error(f"gRPC error in infer: {e.details()}")
            yield InferenceResponse.from_proto(sdk_pb2.TokenResponse(
                token="",
                finish_reason=FinishReason.ERROR.to_proto(),
                error=e.details()
            ))
        except Exception as e:
            logger.error(f"Error in infer: {e}")
            yield InferenceResponse.from_proto(sdk_pb2.TokenResponse(
                token="",
                finish_reason=FinishReason.ERROR.to_proto(),
                error=str(e)
            ))

    def query_embed(
        self,
        query: str,
        documents: List[str],
        model_id: Optional[int] = None
    ) -> EmbeddingResponse:
        """
        Perform semantic search (embedding).
        
        Args:
            query: The query to embed
            documents: List of documents to search through
            model_id: Optional model ID to use
            
        Returns:
            EmbeddingResponse containing search results
        """
        try:
            request = sdk_pb2.EmbedRequest(
                query=query,
                documents=documents,
                model_id=model_id if model_id is not None else 0
            )
            
            self._ensure_connection()
            response = self._stub.Embed(request)
            return EmbeddingResponse.from_proto(response, query=query)
            
        except grpc.RpcError as e:
            logger.error(f"gRPC error in query_embed: {e.details()}")
            return EmbeddingResponse.from_proto(sdk_pb2.EmbedResponse())
        except Exception as e:
            logger.error(f"Error in query_embed: {e}")
            return EmbeddingResponse.from_proto(sdk_pb2.EmbedResponse())

    def tool_update(self, message: str) -> bool:
        """
        Update tool description.
        
        Args:
            message: The tool description update
            
        Returns:
            bool indicating success
        """
        try:
            request = sdk_pb2.ToolUpdateRequest(
                friendly_description=message
            )
            self._ensure_connection()
            response = self._stub.ToolUpdate(request)
            return response.ok
        except grpc.RpcError as e:
            logger.error(f"gRPC error in tool_update: {e.details()}")
            return False
        except Exception as e:
            logger.error(f"Error in tool_update: {e}")
            return False

    def ask_user(
        self,
        message: str,
        reason: Optional[str] = None
    ) -> tuple[str, list[str]]:
        """
        Ask the user a question and get their response.
        
        Args:
            message: The question to ask
            reason: Optional reason for asking
            
        Returns:
            Tuple of (response text, list of attached files)
        """
        try:
            request = sdk_pb2.UserRequest(
                message=message,
                reason=reason or ""
            )
            self._ensure_connection()
            response = self._stub.AskUser(request)
            if response.error:
                logger.error(f"User request failed: {response.error}")
                return "", []
            return response.response or "", list(response.attached_files)
        except grpc.RpcError as e:
            logger.error(f"gRPC error in ask_user: {e.details()}")
            return "", []
        except Exception as e:
            logger.error(f"Error in ask_user: {e}")
            return "", []

    def create_conversation(self) -> ConversationBuilder:
        """Create a new conversation builder."""
        return ConversationBuilder()

    def stream(
        self,
        prompt: str,
        **kwargs  # Pass through other infer args (model_id, temperature, etc.)
    ) -> Generator[str, None, None]:
        """
        Stream tokens from the model.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional arguments passed to infer()
            
        Yields:
            Individual tokens as they are generated
        """
        try:
            for response in self.infer(prompt, **kwargs):
                if response.error:
                    logger.error(f"Stream error: {response.error}")
                    break
                yield response.token
        except Exception as e:
            logger.error(f"Error in stream: {e}")

    def complete(
        self,
        prompt: Union[str, ConversationBuilder],
        **kwargs  # Pass through other infer args
    ) -> str:
        """
        Get a complete response from the model.
        
        Args:
            prompt: The input prompt or conversation
            **kwargs: Additional arguments passed to infer()
            
        Returns:
            The complete generated response
        """
        try:
            if isinstance(prompt, ConversationBuilder):
                context = prompt.build()
                responses = self.infer(context, **kwargs)
            else:
                responses = self.infer(prompt, **kwargs)

            result = []
            for response in responses:
                if response.error:
                    logger.error(f"Complete error: {response.error}")
                    break
                result.append(response.token)
            return "".join(result)
        except Exception as e:
            logger.error(f"Error in complete: {e}")
            return "" 