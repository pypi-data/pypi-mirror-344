"""Upload utilities

This module provides utilities for uploading files to the Truffle server.
"""

import getpass
import requests
import base64
import os
import time
import json
import webbrowser
from pathlib import Path
from typing import Optional, Callable, Tuple, List
import filecmp
import logging as log

from ..platform.sdk_pb2 import AppUploadProgress
from .logger import log, upload_log
from .errors import ErrorHandler, ErrorContext
from ..types import UploadProgress, UploadError, UploadState
from ..runtime.upload.tracker import UploadTracker
from .image import validate_png, is_whitelisted_icon
from .userdata import get_client_userdata_dir

# Helper function to determine environment name
def _get_environment_name(url: str) -> str:
    """Determines the environment name based on the URL."""
    if "overcast" in url:
        return "Truffle Cloud(prod)"  # Use lowercase prod
    elif "forecast" in url:
        return "Truffle Cloud(staging)" # Use lowercase staging
    else:
        return url # Fallback to URL if neither keyword is found

# Define function to get the base URL dynamically
def get_base_url() -> str:
    default_url = "https://overcast.itsalltruffles.com:2087"
    url = default_url
    url_source = "default"
    try:
       # Use the updated get_client_userdata_dir which handles dev paths
       client_dir = get_client_userdata_dir() 
       url_file = client_dir / "current-url"
       if url_file.exists() and url_file.is_file():
            with open(url_file, "r") as f:
                url_file_contents = f.read().strip()
                if url_file_contents: # Ensure file is not empty
                    # Basic validation: check if it looks like an HTTP/S URL
                    if url_file_contents.startswith("http://") or url_file_contents.startswith("https"):
                        url = url_file_contents
                        url_source = "file"
                    else:
                        upload_log.warning(f"Content of {url_file} does not look like a valid URL: '{url_file_contents}'. Using default.")
                else:
                    upload_log.warning(f"{url_file} is empty. Using default API base URL.")
       else:
           # Only log debug if the file doesn't exist, not an error
           upload_log.debug(f"'current-url' file not found in {client_dir}. Using default API base URL.")
           
    except ValueError as ve:
        # Catch error from get_client_userdata_dir if no dir is found
        upload_log.warning(f"Could not determine client directory to check for 'current-url': {ve}. Using default API base URL.")
    except Exception as e:
        # Catch other potential errors (e.g., permission issues)
        upload_log.error(f"Error reading 'current-url' file: {str(e)}. Using default API base URL.")
        
    # Ensure the final URL doesn't have a trailing slash, as it's used for f-string concatenation
    url = url.rstrip('/')

    # Determine environment name using the helper function
    env_name = _get_environment_name(url)
        
    # Log the determined environment
    upload_log.info(f"Using API base URL: {env_name}")
        
    return url

# Define API base URL by calling the function
API_BASE_URL = get_base_url()

# Define Download URL
TRUFFLE_DOWNLOAD_URL = "https://itsalltruffles.com/"

# Define constants
TRUFFLE_VERSION = "1.0.0"
MAX_BUNDLE_SIZE = 100 * 1024 * 1024  # 100MB in bytes
UPLOAD_TIMEOUT = 300  # 5 minutes

# Define AppUploadError class
class AppUploadError(Exception):
    """Error raised when an app upload fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class Uploader:
    """Handles file uploads to the Truffle server"""
    
    def __init__(self, upload_timeout: int = 300, retry_count: int = 3, retry_delay: int = 2, log_level: int = 2):
        """Initialize the uploader
        
        Args:
            upload_timeout: Upload timeout in seconds
            retry_count: Number of retries
            retry_delay: Delay between retries in seconds
            log_level: Logging level for SSE messages
        """
        self.upload_url = f"{API_BASE_URL}/install"  # Construct URL from base
        self.upload_timeout = upload_timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.log_level = log_level
    
    def verify_service(self) -> Tuple[bool, Optional[str]]:
        """Verify that the upload service is available
        
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        try:
            # Create a session with a short timeout
            session = requests.Session()
            session.timeout = 5
            
            # Try to connect to the service using self.upload_url
            response = session.get(
                self.upload_url,
                verify=False,
                timeout=5
            )
            
            # Check if the service is available
            if response.status_code >= 500 or response.status_code == 404 or response.status_code == 451:
                return False, f"Upload service is not available (status code: {response.status_code})"
            return True, None
            
        except Exception as e:
            return ErrorHandler.handle_exception(e, ErrorContext("Uploader", "verify_service"))
    
    def _decode_base64(self, data: bytes) -> bytes:
        """Decode base64 data and remove null bytes
        
        Args:
            data: Base64 encoded data
            
        Returns:
            bytes: Decoded data
        """
        try:
            decoded = base64.b64decode(data)
            while decoded.endswith(b'\0'):  # Remove null bytes
                decoded = decoded[:-1]
            return decoded
        except Exception as e:
            upload_log.error(f"Error decoding base64: {str(e)}")
            upload_log.detail(f"Data: {data}")
            raise
    
    def _validate_file(self, file_path: Path) -> Tuple[bool, Optional[str], Optional[int]]:
        """Validate a file for upload
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            Tuple[bool, Optional[str], Optional[int]]: Success status, error message, and file size
        """
        try:
            if not file_path.exists():
                return False, f"File not found: {file_path}", None
            
            if not file_path.is_file():
                return False, f"Path is not a file: {file_path}", None
            
            if file_path.suffix != '.truffle':
                return False, f"File is not a .truffle file: {file_path}", None
            
            # Check file size (max 100MB)
            file_size = os.path.getsize(file_path)
            if file_size > 100 * 1024 * 1024:  # 100MB in bytes
                return False, f"File too large: {self.format_size(file_size)} (max 100MB)", None
            
            # Verify it's a valid zip file
            try:
                import zipfile
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Check for required files - using flat structure
                    required_files = {'main.py', 'manifest.json', 'requirements.txt'}
                    files_in_zip = set(zip_ref.namelist())
                    missing_files = required_files - files_in_zip
                    if missing_files:
                        return False, f"Missing required files in bundle: {', '.join(missing_files)}", None
                    
                    # Validate manifest.json
                    try:
                        manifest_data = zip_ref.read('manifest.json')
                        manifest_json = json.loads(manifest_data)
                        if not isinstance(manifest_json.get('manifest_version'), int):
                            return False, "manifest_version must be an integer", None
                            
                        # Add developer_id if missing
                        if 'developer_id' not in manifest_json:
                            try:
                                manifest_json['developer_id'] = self.get_user_id()
                                # Convert manifest to bytes
                                manifest_bytes = json.dumps(manifest_json, indent=2).encode('utf-8')
                                
                                # Create new zip with flattened structure
                                import shutil
                                temp_zip = Path(file_path).with_suffix('.temp.truffle')
                                
                                with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                                    # Write the updated manifest
                                    new_zip.writestr('manifest.json', manifest_bytes)
                                    # Copy other files as-is
                                    for name in ['main.py', 'requirements.txt']:
                                        new_zip.writestr(name, zip_ref.read(name))
                                    # Copy icon if it exists
                                    if 'icon.png' in files_in_zip:
                                        new_zip.writestr('icon.png', zip_ref.read('icon.png'))
                                
                                # Replace original with updated zip
                                shutil.move(temp_zip, file_path)
                                
                                upload_log.detail("Added developer_id to manifest.json")
                            except Exception as e:
                                return False, f"Failed to add developer_id: {str(e)}", None
                            
                        # Check if icon.png exists and validate it
                        if 'icon.png' in files_in_zip:
                            # Extract icon.png to a temporary file for validation
                            import tempfile
                            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_icon:
                                temp_icon.write(zip_ref.read('icon.png'))
                                temp_icon_path = Path(temp_icon.name)
                            
                            try:
                                # First check if this is our standard icon
                                if is_whitelisted_icon(temp_icon_path):
                                    os.unlink(temp_icon_path)
                                    return True, None, file_size
                                    
                                # Only validate dimensions if not the standard icon
                                is_valid, error_msg, _ = validate_png(
                                    temp_icon_path,
                                    min_width=128,
                                    min_height=128,
                                    max_width=5000,
                                    max_height=5000,
                                    require_transparency=False
                                )
                                if not is_valid:
                                    os.unlink(temp_icon_path)
                                    return False, error_msg, None
                                    
                                # Clean up and return success
                                os.unlink(temp_icon_path)
                                return True, None, file_size
                            except Exception as e:
                                return False, f"Invalid icon.png: {str(e)}", None
                    except Exception as e:
                        return False, f"Invalid manifest.json: {str(e)}", None
            except zipfile.BadZipFile:
                return False, "Invalid zip file format", None
            
            return True, None, file_size
            
        except Exception as e:
            return False, f"File validation failed: {str(e)}", None
    
    def _parse_error_response(self, response: requests.Response) -> str:
        """Parse an error response from the server
        
        Args:
            response: The response containing the error
            
        Returns:
            str: The error message
        """
        # Special case for 418 status code (no session)
        if response.status_code == 418:
            return "You don't have a valid session. Please log in to the Truffle app first."
            
        # Read the entire error response
        error_content = b""
        for chunk in response.iter_content(chunk_size=1024):
            error_content += chunk
            
        # Log the raw error content for debugging
        upload_log.error(f"Upload failed with status code {response.status_code}")
        upload_log.detail(f"Raw error content: {error_content}")
        
        # Try to decode the error content if it's base64 encoded
        try:
            # Check if the content looks like base64
            if error_content and all(c in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in error_content):
                error_content = self._decode_base64(error_content)
        except Exception as e:
            upload_log.detail(f"Error decoding base64 error content: {str(e)}")
            # Continue with original error content if decoding fails
            
        # Try to parse as JSON
        try:
            error_json = json.loads(error_content.decode('utf-8', errors='replace'))
            error_message = error_json.get('message', 'Unknown error')
            error_details = error_json.get('details', '')
            return f"{error_message}: {error_details}"
        except Exception:
            # If not JSON, just return the raw error
            return f"Upload failed with status code {response.status_code}: {error_content.decode('utf-8', errors='replace')}"
    
    def _process_protobuf_message(self, data: bytes, last_progress: int) -> Tuple[bool, Optional[str], int]:
        """Process a protobuf message or status message"""
        try:
            # Try to parse as protobuf first
            try:
                prog = AppUploadProgress()
                prog.ParseFromString(data)
                
                # Check for errors
                if prog.HasField("error"):
                    return False, f"Upload error: {prog.error.raw_error}", last_progress
                
                # Level 2: Log SSE message details
                upload_log.detail("SSE Message Received:", level=2)
                upload_log.detail(f"  Step: {prog.step}", level=2)
                upload_log.detail(f"  Type: {prog.type}", level=2)
                
                # Handle log messages with proper leveling
                if prog.latest_logs and prog.latest_logs.strip():
                    log_message = prog.latest_logs.strip()
                    # Check if it's a pip-related message
                    if any(pip_msg in log_message for pip_msg in [
                        "Requirement already satisfied",
                        "Collecting ",
                        "Installing collected packages",
                        "Successfully installed"
                    ]):
                        # Send pip messages to trace level
                        upload_log.trace(log_message)
                    else:
                        # Non-pip messages go to info level
                        upload_log.info(log_message)
                    
                    # Always include in detail level
                    upload_log.detail(f"  Logs: {prog.latest_logs}", level=2)
                
                return True, None, prog.progress
                
            except Exception as e:
                # If not a protobuf, try to decode as a status message
                try:
                    message = data.decode('utf-8', errors='replace')
                    if "icon.png valid" in message:
                        upload_log.detail("SSE Status Text Received:", level=2)
                        upload_log.detail(f"  {message}", level=2)
                        return True, None, last_progress
                    upload_log.info(message)
                    return True, None, last_progress
                except Exception as decode_err:
                    upload_log.error(f"Error parsing message: {str(e)}")
                    upload_log.debug(f"Raw data: {data}", level=3)
                    return False, str(e), last_progress
            
        except Exception as e:
            upload_log.error(f"Error processing message: {str(e)}")
            upload_log.debug(f"Raw data: {data}", level=3)
            return False, str(e), last_progress
    
    def upload_file(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """Upload a file to the server
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        # Get the user ID
        try:
            user_id = self.get_user_id()
        except Exception as e:
            return ErrorHandler.handle_exception(e, ErrorContext("Uploader", "get_user_id"))
        
        # Validate the file
        is_valid, error_msg, file_size = self._validate_file(file_path)
        if not is_valid:
            return False, error_msg
        
        # Determine environment name for logging using the helper function
        env_name = _get_environment_name(self.upload_url)
            
        # Retry logic for transient failures
        for attempt in range(self.retry_count + 1):
            try:
                if attempt > 0:
                    upload_log.warning(f"Retrying upload (attempt {attempt + 1}/{self.retry_count + 1}) to {env_name}")
                    time.sleep(self.retry_delay)
                
                # Log file name only, without the "to env_name" suffix
                upload_log.info(f"Uploading file: {file_path.name} ({self.format_size(file_size)})" )
                
                # Open the bundle file
                with open(file_path, 'rb') as f:
                    # Set up the file upload with multipart/form-data format
                    files = {
                        'file': (file_path.stem, f, 'application/zip'),
                    }
                    
                    # Set up headers with only user_id
                    headers = {
                        'user_id': user_id,
                    }
                    
                    # Make the request with streaming enabled and a shorter timeout
                    upload_log.info(f"Connecting to {env_name}...") # Use updated env_name format
                    response = requests.post(
                        self.upload_url,
                        files=files,
                        headers=headers,
                        stream=True,
                        timeout=60,
                        verify=False
                    )
                    
                    # Process response
                    return self._process_upload_response(response)
                    
            except requests.exceptions.Timeout:
                upload_log.error("Upload timed out after 60 seconds")
                if attempt == self.retry_count:
                    return False, "Upload timed out after 60 seconds"
            except Exception as e:
                upload_log.error(f"Upload attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.retry_count:
                    return False, str(e)
        
        return False, "Upload failed after all retry attempts"
    
    def _process_upload_response(self, response: requests.Response) -> Tuple[bool, Optional[str]]:
        """Process the upload response stream"""
        if response.status_code != 200:
            error_content = self._parse_error_response(response)
            return False, error_content

        upload_log.info("Upload started, processing server response...", level=1)
        buffer = b""
        last_progress = 0
        last_log_time = time.time()

        try:
            for line_bytes in response.iter_lines(decode_unicode=False, chunk_size=512):
                # Level 3: Log raw network data before any processing
                upload_log.debug(f"Raw network data received: {line_bytes}", level=3)

                # Show a progress indicator every 5 seconds
                current_time = time.time()
                if current_time - last_log_time > 5:
                    upload_log.info("Still uploading...", level=1)
                    last_log_time = current_time

                line = line_bytes.decode('utf-8', errors='replace')

                if not line:
                    if buffer:
                        # Level 2: Log buffer processing
                        upload_log.detail(f"Processing message buffer: {buffer}", level=2)
                        decoded = self._decode_base64(buffer)
                        success, message, last_progress = self._process_protobuf_message(decoded, last_progress)
                        if not success:
                            return False, message
                        buffer = b""
                    continue

                if line.startswith('data:'):
                    buffer += line_bytes[5:].lstrip()

            # Process any remaining data
            if buffer:
                # Level 2: Log final buffer processing
                upload_log.detail(f"Processing final buffer: {buffer}", level=2)
                decoded = self._decode_base64(buffer)
                success, message, _ = self._process_protobuf_message(decoded, last_progress)
                if not success:
                    return False, message

            upload_log.success("Upload completed successfully")
            return True, None

        except Exception as e:
            upload_log.error(f"Error processing upload response: {str(e)}")
            return False, str(e)
    
    def _read_error_response(self, response: requests.Response) -> str:
        """Read and parse an error response
        
        Args:
            response: The response containing the error
            
        Returns:
            str: The error message
        """
        return self._parse_error_response(response)
    
    def get_user_id(self) -> str:
        """Get the user's ID from the Truffle client
        
        Returns:
            str: The user's ID
            
        Raises:
            AppUploadError: If no user ID is found or if client directory is not found
        """
        try:
            client_dir = get_client_userdata_dir()
            magic_number_path = client_dir / "magic-number.txt"

            if not magic_number_path.exists():
                upload_log.info("Redirecting to download page...")
                try:
                    webbrowser.open_new_tab(TRUFFLE_DOWNLOAD_URL)
                    upload_log.info(f"Opening download link: {TRUFFLE_DOWNLOAD_URL} in your web browser...")
                except webbrowser.Error as e:
                    upload_log.error(f"Error opening web browser: {e}")
                    upload_log.info("Please open the following link manually in your browser:")
                    upload_log.info(TRUFFLE_DOWNLOAD_URL)
                # Raise specific error instructing user
                raise AppUploadError("No user ID found - please download and login to the Truffle client first")

            with open(magic_number_path, "r") as f:
                user_id = f.read().strip()
            return user_id

        except ValueError as e:
            # Convert ValueError from get_client_userdata_dir to AppUploadError
            raise AppUploadError(f"Could not find Truffle client directory: {str(e)}")
    
    def format_size(self, size_bytes: int) -> str:
        """Format a size in bytes to a human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def create_zip_bundle(self, src_dir: Path, dst_file: Path, exclude_patterns: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
        """Create a zip bundle from a source directory
        
        Args:
            src_dir: Source directory to zip
            dst_file: Destination file path
            exclude_patterns: Optional list of glob patterns to exclude
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message
        """
        try:
            # Default exclude patterns
            if exclude_patterns is None:
                exclude_patterns = ["*.DS_Store", "*.truffle"]
            
            # Check if source directory exists
            if not src_dir.exists():
                return False, f"Source directory not found: {src_dir}"
            
            if not src_dir.is_dir():
                return False, f"Source path is not a directory: {src_dir}"
            
            # Create parent directory if it doesn't exist
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Define required files and their source paths
            required_files = {
                'main.py': src_dir / 'src' / 'app' / 'main.py',
                'manifest.json': src_dir / 'src' / 'config' / 'manifest.json',
                'requirements.txt': src_dir / 'src' / 'config' / 'requirements.txt'
            }
            
            # Verify all required files exist
            missing_files = []
            for name, path in required_files.items():
                if not path.exists():
                    missing_files.append(str(path))
            
            if missing_files:
                return False, f"Missing required files: {', '.join(missing_files)}"
            
            # Create zip with flattened structure
            import zipfile
            with zipfile.ZipFile(dst_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add required files with flattened names
                for dest_name, src_path in required_files.items():
                    zipf.write(src_path, dest_name)
                
                # Add icon.png if it exists (from src/config)
                icon_path = src_dir / 'src' / 'config' / 'icon.png'
                if icon_path.exists():
                    zipf.write(icon_path, 'icon.png')
            
            # Log using parent directory and filename
            upload_log.success(f"Created bundle: {dst_file.parent.name}/{dst_file.name}")
            return True, None
            
        except Exception as e:
            error_msg = f"Failed to create bundle: {str(e)}"
            upload_log.error(error_msg)
            return False, error_msg

def upload_file(file_path: str, user_id: str, progress_callback=None) -> UploadState:
    """
    Upload a file to the server with progress tracking.
    
    Args:
        file_path: Path to the file to upload
        user_id: User ID for authentication
        progress_callback: Optional callback for progress updates
        
    Returns:
        UploadState object with the result of the upload
        
    Raises:
        AppUploadError: If the upload fails
    """
    try:
        # Validate inputs
        if not os.path.exists(file_path):
            raise AppUploadError(f"File not found: {file_path}")
            
        if not user_id:
            raise AppUploadError("User ID is required")
            
        # Initialize upload state with proto enum int
        state = UploadState(
            file_path=file_path,
            user_id=user_id,
            progress=0.0,
            step=AppUploadProgress.UploadStep.STEP_UNKNOWN, # Use proto enum
            message="Initializing upload",
            error=None
        )
        
        # Create upload tracker - Assuming UploadTracker constructor doesn't need changes related to Step/Type enums
        tracker = UploadTracker() # Pass callback if it was used: UploadTracker(progress_callback)
        
        # Prepare the request
        url = f"{API_BASE_URL}/install"
        headers = {
            'Content-Type': 'application/octet-stream',
            'Accept': 'application/json, application/x-protobuf, text/plain',
            'X-Truffle-Version': TRUFFLE_VERSION
        }
        
        # Open the file and prepare for upload
        with open(file_path, "rb") as f:
            file_size = os.path.getsize(file_path)
            
            # Create a generator for the file data
            def file_generator():
                chunk_size = 8192  # 8KB chunks
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
                    
            # Make the request
            response = requests.post(
                url,
                headers=headers,
                data=file_generator(),
                stream=True,
                timeout=30
            )
            
            # Check for error status codes
            if response.status_code != 200:
                # Special case for 418 status code (no session)
                if response.status_code == 418:
                    error = AppUploadError("You don't have a valid session. Please log in to the Truffle app first.")
                    state.error = error
                    state.step = AppUploadProgress.UploadStep.STEP_VERIFY_BUNDLE # Use proto enum
                    state.message = "Session error"
                    return state
                
                # Read the entire error response
                error_content = b""
                for chunk in response.iter_content(chunk_size=1024):
                    error_content += chunk
                upload_log.error(f"Upload failed with status code {response.status_code}")
                upload_log.detail(f"Raw error content: {error_content}")
                # Try decoding error content
                try:
                    if error_content and all(c in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in error_content):
                        decoded_content = base64.b64decode(error_content)
                        while decoded_content.endswith(b'\0'):
                            decoded_content = decoded_content[:-1]
                        error_content = decoded_content
                except Exception as e:
                    upload_log.detail(f"Error decoding base64 error content: {str(e)}")
                error = AppUploadError(f"Upload failed with status code {response.status_code}: {error_content.decode('utf-8', errors='replace')}")
                state.error = error
                state.step = AppUploadProgress.UploadStep.STEP_VERIFY_BUNDLE # Use proto enum
                return state
                
            # Process the response stream
            buffer = b""
            for chunk in response.iter_content(chunk_size=1024):
                buffer += chunk
                
                # Process complete messages in the buffer
                while b'\n\n' in buffer:
                    message_end = buffer.index(b'\n\n') + 2
                    message = buffer[:message_end]
                    buffer = buffer[message_end:]
                    if not message.strip():
                        continue
                    try:
                        data_start = message.find(b'data: ') + 6
                        if data_start < 6: continue
                        data = message[data_start:].strip()
                        # Try decoding data
                        try:
                            if data and all(c in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in data):
                                decoded_data = base64.b64decode(data)
                                while decoded_data.endswith(b'\0'):
                                    decoded_data = decoded_data[:-1]
                                data = decoded_data
                        except Exception as e:
                            upload_log.detail(f"Error decoding base64 data: {str(e)}")
                        
                        # Parse the progress update using tracker
                        # Assume tracker.parse_progress now returns UploadProgress with proto enum ints
                        progress_update = tracker.parse_progress(data)
                        
                        # Update the state
                        state.progress = progress_update.progress
                        state.step = progress_update.step # This is now a proto enum int
                        state.message = progress_update.message
                        state.error = progress_update.error # This is now a string or None
                        
                        # Convert string error back to UploadError if necessary for state
                        if isinstance(state.error, str):
                           state.error = UploadError(code="UPLOAD_FAILED", message=state.error) 
                        elif state.error is not None: # Handle case if progress.error wasn't a string
                           # Log a warning or handle appropriately if the error type is unexpected
                           upload_log.warning(f"Unexpected error type from tracker: {type(state.error)}")
                           state.error = UploadError(code="UNKNOWN_ERROR", message=str(state.error))

                        # Call the progress callback if provided
                        if progress_callback:
                            progress_callback(state)
                            
                    except Exception as e:
                        upload_log.error(f"Error parsing SSE message: {str(e)}")
                        upload_log.detail(f"Message content: {message}")
                        continue
                        
            # Process any remaining data in the buffer
            if buffer:
                try:
                    progress_update = tracker.parse_progress(buffer)
                    state.progress = progress_update.progress
                    state.step = progress_update.step
                    state.message = progress_update.message
                    state.error = progress_update.error
                    
                    # Convert string error back to UploadError if necessary for state
                    if isinstance(state.error, str):
                       state.error = UploadError(code="UPLOAD_FAILED", message=state.error) 
                    elif state.error is not None:
                       upload_log.warning(f"Unexpected error type from tracker: {type(state.error)}")
                       state.error = UploadError(code="UNKNOWN_ERROR", message=str(state.error))

                    if progress_callback:
                        progress_callback(state)
                except Exception as e:
                    upload_log.error(f"Error parsing final buffer: {str(e)}")
                    
            # Check if the upload was successful
            if state.error:
                return state
                
            # Update the state to indicate success
            state.progress = 1.0
            state.step = AppUploadProgress.UploadStep.STEP_INTALLED # Use proto enum
            state.message = "Upload completed successfully"
            
            if progress_callback:
                progress_callback(state)
                
            return state
            
    except Exception as e:
        upload_log.error(f"Upload failed: {str(e)}")
        # Ensure state.error is an UploadError instance
        if not isinstance(state.error, UploadError):
             state.error = AppUploadError(str(e)) # Assuming AppUploadError is suitable
        state.step = AppUploadProgress.UploadStep.STEP_VERIFY_BUNDLE # Use proto enum
        # Check if state exists before returning, handle potential NameError if exception occurred before state init
        if 'state' in locals():
           return state
        else: # Create a minimal error state if initialization failed
           return UploadState(
               file_path=file_path, 
               user_id=user_id, 
               progress=0.0, 
               step=AppUploadProgress.UploadStep.STEP_VERIFY_BUNDLE, 
               message=f"Upload initialization failed: {str(e)}",
               error=AppUploadError(str(e))
           ) 