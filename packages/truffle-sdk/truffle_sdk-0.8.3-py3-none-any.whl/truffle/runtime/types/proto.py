from enum import Enum
from typing import Optional, Dict, Any
from ...platform.sdk_pb2 import AppUploadProgress
from ...types import UploadProgress

def create_upload_progress_from_proto(proto_msg: AppUploadProgress) -> UploadProgress:
    """Create an UploadProgress instance from a protobuf message."""
    return UploadProgress(
        step=proto_msg.step,
        progress=proto_msg.progress,
        message=proto_msg.latest_logs,
        error=proto_msg.error.raw_error if proto_msg.HasField('error') else None,
        substep=proto_msg.substep if proto_msg.HasField('substep') else None,
        type=proto_msg.type if proto_msg.HasField('type') else None
    )


def create_proto_from_upload_progress(progress: UploadProgress) -> AppUploadProgress:
    """Create a protobuf message from an UploadProgress instance."""
    proto_msg = AppUploadProgress()
    proto_msg.step = progress.step
    proto_msg.progress = progress.progress
    proto_msg.latest_logs = progress.message

    if progress.error:
        proto_msg.error.raw_error = progress.error

    if progress.substep:
        proto_msg.substep = progress.substep

    if progress.type:
        proto_msg.type = progress.type

    return proto_msg 