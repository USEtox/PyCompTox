"""
Configuration management for PyCompTox.

This module handles API key storage and retrieval.
"""

import os
from pathlib import Path
from typing import Optional


def get_config_dir(create: bool = False) -> Path:
    """
    Get the configuration directory for PyCompTox.

    Args:
        create (bool): Create the directory if it does not exist. Defaults to
            False, so simply asking where config lives does not write to disk.
            Only ``save_api_key()`` needs to create it.

    Returns:
        Path: The configuration directory path.

    The configuration directory is located at:
    - Windows: %APPDATA%\\PyCompTox
    - macOS/Linux: ~/.pycomptox
    """
    if os.name == 'nt':  # Windows
        config_dir = Path(os.getenv('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'PyCompTox'
    else:  # macOS/Linux
        config_dir = Path.home() / '.pycomptox'

    if create:
        config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_api_key_file(create_dir: bool = False) -> Path:
    """
    Get the path to the API key file.

    Args:
        create_dir (bool): Create the containing directory. Only needed by
            callers that are about to write the file.

    Returns:
        Path: The API key file path.
    """
    return get_config_dir(create=create_dir) / 'api_key.txt'


def save_api_key(api_key: str) -> None:
    """
    Save the API key to the configuration file.
    
    Args:
        api_key (str): The CompTox Dashboard API key to save.
        
    Example:
        >>> from pycomptox.config import save_api_key
        >>> save_api_key("your_api_key_here")
        >>> print("API key saved successfully!")
    """
    if not api_key or not api_key.strip():
        raise ValueError("API key cannot be empty")

    api_key_file = get_api_key_file(create_dir=True)
    api_key_file.write_text(api_key.strip(), encoding='utf-8')
    
    # Set file permissions to be readable only by the owner (on Unix-like systems)
    if os.name != 'nt':
        api_key_file.chmod(0o600)


def load_api_key() -> Optional[str]:
    """
    Load the API key from the configuration file.
    
    Returns:
        Optional[str]: The API key if found, None otherwise.
        
    The function looks for the API key in the following order:
    1. COMPTOX_API_KEY environment variable
    2. Saved configuration file
    
    Example:
        >>> from pycomptox.config import load_api_key
        >>> api_key = load_api_key()
        >>> if api_key:
        ...     print("API key loaded successfully!")
        ... else:
        ...     print("No API key found. Please set one using save_api_key()")
    """
    # First, check environment variable
    env_key = os.getenv('COMPTOX_API_KEY')
    if env_key:
        return env_key.strip()
    
    # Then, check saved configuration file
    api_key_file = get_api_key_file()
    if api_key_file.exists():
        try:
            api_key = api_key_file.read_text(encoding='utf-8').strip()
            if api_key:
                return api_key
        except Exception:
            pass
    
    return None


def delete_api_key() -> bool:
    """
    Delete the saved API key from the configuration file.
    
    Returns:
        bool: True if the key was deleted, False if it didn't exist.
        
    Example:
        >>> from pycomptox.config import delete_api_key
        >>> if delete_api_key():
        ...     print("API key deleted successfully!")
        ... else:
        ...     print("No saved API key found.")
    """
    api_key_file = get_api_key_file()
    if api_key_file.exists():
        api_key_file.unlink()
        return True
    return False


def get_config_info() -> dict:
    """
    Get information about the current configuration.
    
    Returns:
        dict: Configuration information including paths and API key status.
        
    Example:
        >>> from pycomptox.config import get_config_info
        >>> info = get_config_info()
        >>> print(f"Config directory: {info['config_dir']}")
        >>> print(f"API key saved: {info['has_saved_key']}")
    """
    api_key_file = get_api_key_file()
    return {
        'config_dir': str(get_config_dir()),
        'api_key_file': str(api_key_file),
        'has_saved_key': api_key_file.exists(),
        'has_env_key': bool(os.getenv('COMPTOX_API_KEY')),
        'api_key_available': load_api_key() is not None
    }
