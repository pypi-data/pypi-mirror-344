import os
import platform
from pathlib import Path
from .logger import log

def get_client_userdata_dir() -> Path:
    """Get the Truffle client's user data directory.
    
    Checks for standard ('Truffle') and development ('Truffle-Development') 
    directories, prioritizing the standard one. Logs a warning if the 
    development directory is used.
    
    Returns:
        Path: Path to the user data directory
        
    Raises:
        ValueError: If neither directory can be determined or found.
    """
    system = platform.system().lower()
    standard_name = "TruffleOS"
    dev_name = "TruffleOS-Development"
    
    standard_dir: Optional[Path] = None
    dev_dir: Optional[Path] = None

    if system == "darwin":  # macOS
        app_support = Path.home() / "Library" / "Application Support"
        standard_dir = app_support / standard_name
        dev_dir = app_support / dev_name
    elif system == "windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            base_appdata = Path(appdata)
            standard_dir = base_appdata / standard_name
            dev_dir = base_appdata / dev_name
        else:
            # If APPDATA isn't set, we cannot determine the path
            pass 
    elif system == "linux":
        config_home = Path.home() / ".config"
        standard_dir = config_home / standard_name
        dev_dir = config_home / dev_name
    else:
        raise ValueError(f"Unsupported operating system: {system}")

    # Check standard directory first
    if standard_dir and standard_dir.exists() and standard_dir.is_dir():
        log.debug(f"Using standard user data directory: {standard_dir}") # Added debug log
        return standard_dir
    
    # Check development directory next
    if dev_dir and dev_dir.exists() and dev_dir.is_dir():
        log.warning(f"Using development user data directory: {dev_dir}") # Log warning
        return dev_dir
        
    # If neither directory exists or couldn't be determined (e.g., no APPDATA)
    err_msg = "Could not find Truffle client directory. Looked for:"
    if standard_dir: err_msg += f"\n - {standard_dir}"
    if dev_dir: err_msg += f"\n - {dev_dir}"
    if system == "windows" and not os.getenv("APPDATA"): err_msg += "\n - APPDATA environment variable not set."
    raise ValueError(err_msg) 