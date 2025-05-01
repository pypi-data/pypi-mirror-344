"""
Static gRPC Servicer implementation for TruffleSDK.
Provides a clean interface between protobuf messages and runtime logic.
"""

import typing
import os
import inspect
import functools
import json
import base64
import time
from concurrent import futures
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple, Union

# Necessary Protobuf / gRPC imports
import grpc
from grpc_reflection.v1alpha import reflection
import google.protobuf

# --- Import Static Protobuf Definitions ---
import truffle.platform.sdk_pb2 as sdk_pb2
import truffle.platform.sdk_pb2_grpc as sdk_pb2_grpc

# --- Import Type Definitions ---
from truffle.common import get_logger
from truffle.platform import APP_SOCK
from .base import BaseRuntime
from .types.models import ModelRegistry, ModelDescription
from .types.messages import (
    Content, Context, SortedEmbedding, GenerationUsage,
    GenerateResponseFormat
)
from .types.responses import (
    SDKResponse, GenerateResponse, TokenResponse,
    EmbedResponse, UserResponse, SystemToolResponse
)
from .types.enums import Role, ResponseFormat, FinishReason, ModelType

logger = get_logger()

class TruffleRuntimeImplementation(sdk_pb2_grpc.TruffleSDKServicer):
    """
    Static gRPC Servicer implementation for TruffleSDK.
    Acts as a bridge, translating proto requests/responses and
    delegating logic to the runtime_instance.
    """
    
    def __init__(self, runtime_instance: BaseRuntime):
        """Initialize with runtime instance that contains core logic.
        
        Args:
            runtime_instance: Instance of BaseRuntime containing core functionality
        """
        self.runtime = runtime_instance
        super().__init__()

    def Infer(
        self,
        request: sdk_pb2.GenerateRequest,
        context: grpc.ServicerContext
    ) -> typing.Iterator[sdk_pb2.TokenResponse]:
        """Handle streaming generation requests.
        
        Args:
            request: The generation request proto
            context: gRPC service context
            
        Yields:
            TokenResponse protos with generation results
        """
        try:
            # Convert request context if provided
            ctx = Context.from_proto(request.context) if request.HasField("context") else Context()
            
            # Convert response format if provided  
            fmt = GenerateResponseFormat.from_proto(request.fmt) if request.HasField("fmt") else None
            
            # Stream responses from runtime
            for token in self.runtime.generate_stream(
                prompt=request.message,
                context=ctx,
                response_format=fmt,
                temperature=request.temperature if request.HasField("temperature") else None,
                max_tokens=request.max_tokens if request.HasField("max_tokens") else None,
                model_id=request.model_id if request.HasField("model_id") else None
            ):
                yield token.to_proto()
            
        except Exception as e:
            logger.error(f"Error in Infer: {str(e)}", exc_info=True)
            yield TokenResponse(
                token="",
                finish_reason=FinishReason.ERROR,
                error=str(e)
            ).to_proto()

    def InferSync(
        self,
        request: sdk_pb2.GenerateRequest,
        context: grpc.ServicerContext
    ) -> sdk_pb2.GenerateResponse:
        """Handle generation requests.
        
        Args:
            request: The generation request proto
            context: gRPC service context
            
        Returns:
            GenerateResponse proto with generation result
        """
        try:
            # Convert request context if provided
            ctx = Context.from_proto(request.context) if request.HasField("context") else Context()
            
            # Convert response format if provided
            fmt = GenerateResponseFormat.from_proto(request.fmt) if request.HasField("fmt") else None
            
            # Call runtime implementation
            result = self.runtime.generate(
                prompt=request.message,
                context=ctx,
                response_format=fmt,
                temperature=request.temperature if request.HasField("temperature") else None,
                max_tokens=request.max_tokens if request.HasField("max_tokens") else None,
                model_id=request.model_id if request.HasField("model_id") else None
            )
            
            # Convert result back to proto
            return result.to_proto()

        except Exception as e:
            logger.error(f"Error in InferSync: {str(e)}", exc_info=True)
            return GenerateResponse(
                response="",
                finish_reason=FinishReason.ERROR,
                error=str(e)
            ).to_proto()

    def Embed(
        self,
        request: sdk_pb2.EmbedRequest,
        context: grpc.ServicerContext
    ) -> sdk_pb2.EmbedResponse:
        """Handle embedding requests.
        
        Args:
            request: The embedding request proto
            context: gRPC service context
            
        Returns:
            EmbedResponse proto with embedding results
        """
        try:
            result = self.runtime.embed(
                query=request.query,
                documents=list(request.documents)
            )
            return result.to_proto()

        except Exception as e:
            logger.error(f"Error in Embed: {str(e)}", exc_info=True)
            return EmbedResponse(results=[]).to_proto()

    def GetModels(
        self,
        request: sdk_pb2.GetModelsRequest,
        context: grpc.ServicerContext
    ) -> sdk_pb2.GetModelsResponse:
        """Handle model listing requests.
        
        Args:
            request: The get models request proto
            context: gRPC service context
            
        Returns:
            GetModelsResponse proto with available models
        """
        try:
            models = self.runtime.get_models()
            response = sdk_pb2.GetModelsResponse()
            for model in models:
                response.models.append(model.to_proto())
            return response
            
        except Exception as e:
            logger.error(f"Error in GetModels: {str(e)}", exc_info=True)
            return sdk_pb2.GetModelsResponse()

    def AskUser(
        self,
        request: sdk_pb2.UserRequest,
        context: grpc.ServicerContext
    ) -> sdk_pb2.UserResponse:
        """Handle user interaction requests.
        
        Args:
            request: The user request proto
            context: gRPC service context
            
        Returns:
            UserResponse proto with user's response
        """
        try:
            result = self.runtime.ask_user(
                message=request.message,
                reason=request.reason if request.HasField("reason") else None
            )
            return result.to_proto()
            
        except Exception as e:
            logger.error(f"Error in AskUser: {str(e)}", exc_info=True)
            return UserResponse(error=str(e)).to_proto()

    def ToolUpdate(
        self,
        request: sdk_pb2.ToolUpdateRequest,
        context: grpc.ServicerContext
    ) -> sdk_pb2.SDKResponse:
        """Handle tool update requests.
        
        Args:
            request: The tool update request proto
            context: gRPC service context
            
        Returns:
            SDKResponse proto indicating success/failure
        """
        try:
            result = self.runtime.tool_update(
                friendly_description=request.friendly_description
            )
            return result.to_proto()

        except Exception as e:
            logger.error(f"Error in ToolUpdate: {str(e)}", exc_info=True)
            return SDKResponse(ok=False, error=str(e)).to_proto()

    def SystemTool(
        self,
        request: sdk_pb2.SystemToolRequest,
        context: grpc.ServicerContext
    ) -> sdk_pb2.SystemToolResponse:
        """Handle system tool requests.
        
        Args:
            request: The system tool request proto
            context: gRPC service context
            
        Returns:
            SystemToolResponse proto with tool results
        """
        try:
            result = self.runtime.system_tool(
                 tool_name=request.tool_name,
                args=dict(request.args)
            )
            return result.to_proto()
            
        except Exception as e:
            logger.error(f"Error in SystemTool: {str(e)}", exc_info=True)
            return SystemToolResponse(error=str(e)).to_proto()

# --- Modified TruffleRuntime ---
class TruffleRuntime(BaseRuntime): # Keep BaseRuntime if needed
    def __init__(self):
        self.runtime_instance = None # Stores the instance with the old logic
        self.server = None
        logger.info("TruffleRuntime initialized (wrapper for gRPC server setup).")

    def build(self, class_instance):
        """
        Sets up and runs the gRPC server using the static TruffleSDKServicer
        implementation, which delegates calls to the provided class_instance.
        """
        logger.info(f"TruffleRuntime building server for instance of {class_instance.__class__.__name__}")
        self.runtime_instance = class_instance

        # Ensure socket path and address are handled correctly
        socket_addr = APP_SOCK # Use the imported APP_SOCK
        if socket_addr.startswith('unix://'):
             socket_path = socket_addr[len('unix://'):]
        else:
             # Assume APP_SOCK is just the path, add prefix for grpc
             socket_path = socket_addr
             socket_addr = f'unix://{socket_path}'
        logger.debug(f"Using socket address: {socket_addr}")
        logger.debug(f"Using socket path: {socket_path}")


        # Ensure socket is clean before binding
        if os.path.exists(socket_path):
            try:
                os.unlink(socket_path)
                logger.info(f"Removed existing socket at {socket_path}")
            except OSError as e:
                logger.error(f"Failed to remove existing socket {socket_path}: {e}. Attempting to continue.")
                # Decide if this is fatal. For robustness, maybe try to continue?
                # raise OSError(f"Cannot start server: failed to remove existing socket {socket_path}") from e

        # Create the gRPC server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # Keep thread pool

        # Instantiate our static servicer implementation, passing the old runtime instance
        try:
             servicer = TruffleRuntimeImplementation(self.runtime_instance)
        except Exception as init_err:
             logger.error(f"Failed to initialize TruffleRuntimeImplementation: {init_err}", exc_info=True)
             raise # Initialization failure is likely fatal

        # Register the servicer with the server
        sdk_pb2_grpc.add_TruffleSDKServicer_to_server(servicer, self.server)
        logger.info("Registered TruffleSDKServicer with gRPC server.")

        # Enable reflection using the *static* service name from sdk_pb2
        SERVICE_NAMES = (
            sdk_pb2.DESCRIPTOR.services_by_name['TruffleSDK'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)
        logger.info(f"Enabled server reflection for services: {SERVICE_NAMES}")

        # Add the insecure port using the address with the unix:// prefix
        try:
             self.server.add_insecure_port(socket_addr)
        except Exception as bind_err:
              logger.error(f"Failed to bind server to address {socket_addr}: {bind_err}", exc_info=True)
              raise # Cannot continue if bind fails

        logger.info(f"gRPC server configured to listen on {socket_addr}")

        # Start the server
        try:
             self.server.start()
             logger.info("Server started successfully. Waiting for termination...")
        except Exception as start_err:
             logger.error(f"Failed to start gRPC server: {start_err}", exc_info=True)
             raise # Cannot continue if start fails


        # Keep the server running. Handle graceful shutdown.
        try:
            # Keep main thread alive
            while True:
                 time.sleep(3600) # Sleep for an hour, or use wait_for_termination
                 # self.server.wait_for_termination() # wait_for_termination blocks
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received, initiating graceful shutdown.")
            self.stop()
        except Exception as loop_err:
             logger.error(f"Error in server main loop: {loop_err}", exc_info=True)
             self.stop() # Attempt graceful shutdown on unexpected error
             raise # Re-raise after attempting shutdown

    def stop(self):
         """Initiates graceful shutdown of the gRPC server."""
         if self.server:
             logger.info("Stopping gRPC server gracefully...")
             # Grace period allows ongoing requests to complete
             shutdown_event = self.server.stop(grace=5.0)
             logger.info("Waiting for server shutdown to complete...")
             shutdown_event.wait(timeout=10.0) # Wait max 10s for shutdown
             if shutdown_event.is_set():
                  logger.info("Server stopped.")
             else:
                  logger.warning("Server shutdown timed out.")
             self.server = None
         else:
              logger.info("Server already stopped or not started.")

# Cleanup potential unused old helper functions if they are not needed by the runtime_instance logic itself
# Example: Remove get_non_function_members, is_jsonable etc. if they were only for dynamic proto generation
# Requires careful checking of the old runtime_instance code.
