from . import platform
from .platform import SDK_SOCK
from .common import get_logger
from .runtime.types.enums import Role, ResponseFormat, FinishReason
from .runtime.types.messages import (
    GenerationUsage, Content, Context, GenerateResponseFormat
)
from .runtime.types.responses import (
    SDKResponse, UserResponse, EmbedResponse, TokenResponse, SystemToolResponse,
    GenerateResponse
)
from .runtime.types.models import ModelDescription

import grpc
import json
import os
import typing
from typing import Any, Dict, Optional, Union, List, Iterator


logger = get_logger()


class TruffleClient:
    def __init__(self, host=SDK_SOCK):
        self.channel = grpc.insecure_channel(host)
        self.stub = platform.sdk_pb2_grpc.TruffleSDKStub(self.channel)
        self.model_contexts: list[Context] = []

    def perplexity_search(
        self,
        query: str,
        model: str = "sonar-pro",
        response_fmt: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> SystemToolResponse:
        """Accesses Perplexity AI's search capabilities via the Truffle backend.

        Args:
            query: The search query.
            model: The Perplexity model to use (e.g., "sonar-pro").
            response_fmt: Optional desired response format (e.g., "markdown", "json").
            system_prompt: Optional custom system prompt for the Perplexity model.

        Returns:
            A SystemToolResponse object containing the Perplexity response content or an error.
        """
        logger.trace(f"Perplexity search called with query: '{query[:50]}...'")
        try:
            # Prepare the request for the generic SystemTool endpoint
            request = platform.sdk_pb2.SystemToolRequest(tool_name="perplexity_search")
            
            # Populate args map with provided parameters
            request.args["query"] = query
            if model:
                 request.args["model"] = model
            if response_fmt:
                 request.args["response_fmt"] = response_fmt
            if system_prompt:
                 request.args["system_prompt"] = system_prompt

            logger.debug(f"Calling SystemTool with args: {request.args}")
            r_proto: platform.sdk_pb2.SystemToolResponse = self.stub.SystemTool(request)

            # Convert the proto response to our wrapper
            response_wrapper = SystemToolResponse.from_proto(r_proto)
            if response_wrapper.error:
                 logger.error(f"Perplexity search via SystemTool failed: {response_wrapper.error}")
            
            return response_wrapper

        except grpc.RpcError as e:
            logger.error(f"gRPC error during Perplexity search: {e.details()}", exc_info=True)
            # Return an error response using our wrapper
            return SystemToolResponse(error=f"gRPC Error: {e.details()}")
        except Exception as e:
            logger.error(f"Unexpected error preparing Perplexity search request: {e}", exc_info=True)
            return SystemToolResponse(error=f"Unexpected Client Error: {e}")

    def get_models(self) -> List[ModelDescription]:
        """Get available models from the service."""
        logger.trace("Get models called")
        try:
            response_proto: platform.sdk_pb2.GetModelsResponse = self.stub.GetModels(
                platform.sdk_pb2.GetModelsRequest()
            )
            return [ModelDescription.from_proto(model_proto) for model_proto in response_proto.models]
        except grpc.RpcError as e:
            logger.error(f"gRPC error getting models: {e.details()}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting models: {e}", exc_info=True)
            return []

    def tool_update(self, message: str) -> SDKResponse:
        """Send a tool update message to the service."""
        logger.trace("Tool update called")
        try:
            r_proto: platform.sdk_pb2.SDKResponse = self.stub.ToolUpdate(
                platform.sdk_pb2.ToolUpdateRequest(friendly_description=message)
            )
            return SDKResponse.from_proto(r_proto)
        except grpc.RpcError as e:
            logger.error(f"gRPC error sending tool update: {e.details()}", exc_info=True)
            return SDKResponse(ok=False, error=f"gRPC Error: {e.details()}")
        except Exception as e:
            logger.error(f"Unexpected error sending tool update: {e}", exc_info=True)
            return SDKResponse(ok=False, error=f"Unexpected Client Error: {e}")

    def ask_user(
        self, message: str, reason: Optional[str] = "Tool needs input to continue."
    ) -> UserResponse:
        """Ask the user a question via the service."""
        logger.trace("Ask user called")
        try:
            response_proto: platform.sdk_pb2.UserResponse = self.stub.AskUser(
                platform.sdk_pb2.UserRequest(message=message, reason=reason)
            )
            return UserResponse.from_proto(response_proto)
        except grpc.RpcError as e:
            logger.error(f"gRPC error asking user: {e.details()}", exc_info=True)
            return UserResponse(error=f"gRPC Error: {e.details()}")
        except Exception as e:
            logger.error(f"Unexpected error asking user: {e}", exc_info=True)
            return UserResponse(error=f"Unexpected Client Error: {e}")

    def query_embed(
        self, query: str, documents: typing.List[str]
    ) -> EmbedResponse:
        """Get embeddings for documents based on a query."""
        logger.trace("Embed called")
        try:
            request = platform.sdk_pb2.EmbedRequest(query=query, documents=documents)
            response_proto: platform.sdk_pb2.EmbedResponse = self.stub.Embed(request)
            logger.debug("Embedding response received from gRPC")
            return EmbedResponse.from_proto(response_proto)
        except grpc.RpcError as e:
            logger.error(f"gRPC error getting embeddings: {e.details()}", exc_info=True)
            return EmbedResponse(results=[])
        except Exception as e:
            logger.error(f"Unexpected error getting embeddings: {e}", exc_info=True)
            return EmbedResponse(results=[])

    def infer(
        self,
        prompt: str,
        model_id: Optional[int] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[ResponseFormat] = None,
        response_schema: Optional[str] = None,
        system_prompt: Optional[str] = None,
        context_idx: Optional[int] = None,
        **kwargs: Any,
    ) -> Iterator[TokenResponse]:
        """Perform streaming inference."""
        logger.trace("Streaming infer called")
        try:
            format_spec: Optional[GenerateResponseFormat] = None
            if response_format:
                format_spec = GenerateResponseFormat(
                    format=response_format,
                    schema=response_schema
                )

            # Fetch or build the context using our wrappers
            if context_idx is not None:
                if system_prompt is not None:
                    logger.warning("Ignoring system_prompt because context_idx was provided.")
                if context_idx < 0 or context_idx >= len(self.model_contexts):
                    raise IndexError(f"context_idx {context_idx} is out of range.")
                current_context: platform.sdk_pb2.Context = self.model_contexts[context_idx]
            else:
                # Create a new context
                self.model_contexts.append(platform.sdk_pb2.Context())
                current_context: platform.sdk_pb2.Context = self.model_contexts[-1]
                if system_prompt:
                    current_context.history.append(
                        platform.sdk_pb2.Content(
                            role=Role.SYSTEM.to_proto(),
                            content=system_prompt
                        )
                    )

            # Add user prompt to context
            current_context.history.append(
                platform.sdk_pb2.Content(
                    role=Role.USER.to_proto(),
                    content=prompt
                )
            )

            # Prepare request
            request = platform.sdk_pb2.GenerateRequest(
                message=prompt,
                model_id=model_id if model_id is not None else 0,
                context=current_context,
                temperature=temperature,
                max_tokens=max_tokens,
                fmt=format_spec,
            )

            response_stream = self.stub.Infer(request)

            full_response_content = ""
            final_response_wrapper: Optional[TokenResponse] = None

            for response_proto in response_stream:
                # Convert each chunk to our wrapper before yielding
                token_response = TokenResponse.from_proto(response_proto)
                yield token_response

                # Accumulate content and track final state
                if token_response.token:
                    full_response_content += token_response.token
                if token_response.finish_reason:
                    final_response_wrapper = token_response # Keep track of the last chunk
                    # Check for immediate errors
                    if token_response.finish_reason == FinishReason.ERROR:
                        logger.error(f"Streaming inference failed with error: {token_response.error}")
                        # No need to add AI response to context on error
                        return # Stop processing the stream
                    # Stop processing if finished (STOP, LENGTH, USER)
                    elif token_response.finish_reason != FinishReason.UNSPECIFIED:
                         break # Exit loop once finished

            current_context.history.append(
                platform.sdk_pb2.Content(
                    role=Role.AI.to_proto(),
                    content="".join(full_response_content),
                )
            )

        except grpc.RpcError as e:
            logger.error(f"gRPC error during streaming inference: {e.details()}", exc_info=True)
            yield TokenResponse(token="", error=f"gRPC Error: {e.details()}", finish_reason=FinishReason.ERROR)
        except IndexError as e:
            logger.error(f"Context index error: {e}", exc_info=True)
            yield TokenResponse(token="", error=str(e), finish_reason=FinishReason.ERROR)
        except Exception as e:
            logger.error(f"Unexpected error during streaming inference: {e}", exc_info=True)
            yield TokenResponse(token="", error=f"Unexpected Error: {e}", finish_reason=FinishReason.ERROR)

    def infer_sync(
        self,
        prompt: str,
        model_id: Optional[int] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[ResponseFormat] = None,
        response_schema: Optional[str] = None,
        system_prompt: Optional[str] = None,
        context_idx: Optional[int] = None,
        **kwargs: Any,
    ) -> GenerateResponse:
        """Perform synchronous inference."""
        logger.trace("Sync infer called")
        try:
            format_spec: Optional[GenerateResponseFormat] = None
            if response_format:
                format_spec = GenerateResponseFormat(
                    format=response_format,
                    schema=response_schema
                )

            # Fetch or build the context using our wrappers
            if context_idx is not None:
                if system_prompt is not None:
                    logger.warning("Ignoring system_prompt because context_idx was provided.")
                if context_idx < 0 or context_idx >= len(self.model_contexts):
                    raise IndexError(f"context_idx {context_idx} is out of range.")
                current_context: platform.sdk_pb2.Context = self.model_contexts[context_idx]
            else:
                # Create a new context
                self.model_contexts.append(platform.sdk_pb2.Context())
                current_context: platform.sdk_pb2.Context = self.model_contexts[-1]
                if system_prompt:
                    current_context.history.append(
                        platform.sdk_pb2.Content(
                            role=Role.SYSTEM.to_proto(),
                            content=system_prompt
                        )
                    )

            current_context.history.append(
                platform.sdk_pb2.Content(
                    role=Role.USER.to_proto(),
                    content=prompt
                )
            )

            request = platform.sdk_pb2.GenerateRequest(
                message=prompt,
                model_id=model_id if model_id is not None else 0,
                context=current_context,
                temperature=temperature,
                max_tokens=max_tokens,
                fmt=format_spec,
            )

            response_proto = self.stub.InferSync(request)
            response_wrapper = GenerateResponse.from_proto(response_proto)

            # Add AI response to context if successful
            if response_wrapper.response and response_wrapper.finish_reason != FinishReason.ERROR:
                current_context.history.append(
                    platform.sdk_pb2.Content(
                        role=Role.AI.to_proto(),
                        content=response_wrapper.response,
                    )
                )

            return response_wrapper

        except grpc.RpcError as e:
            logger.error(f"gRPC error during sync inference: {e.details()}", exc_info=True)
            return GenerateResponse(response="", finish_reason=FinishReason.ERROR, error=f"gRPC Error: {e.details()}")
        except IndexError as e:
            logger.error(f"Context index error: {e}", exc_info=True)
            return GenerateResponse(response="", finish_reason=FinishReason.ERROR, error=str(e))
        except Exception as e:
            logger.error(f"Unexpected error during sync inference: {e}", exc_info=True)
            return GenerateResponse(response="", finish_reason=FinishReason.ERROR, error=f"Unexpected Error: {e}")

    def close(self):
        """Close the gRPC channel"""
        self.channel.close()