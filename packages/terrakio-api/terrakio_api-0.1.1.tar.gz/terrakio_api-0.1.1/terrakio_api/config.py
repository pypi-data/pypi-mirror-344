import os
import yaml
from pathlib import Path
from typing import Dict, Any

from .exceptions import ConfigurationError

# Default configuration file location
DEFAULT_CONFIG_FILE = os.path.expanduser("~/.tkioapirc")

def read_config_file(config_file: str = DEFAULT_CONFIG_FILE) -> Dict[str, Any]:
    """
    Read and parse the configuration file.
    
    Args:
        config_file: Path to the configuration file
        
    Returns:
        Dict[str, Any]: Configuration parameters
        
    Raises:
        ConfigurationError: If the configuration file can't be read or parsed
    """
    config_path = Path(os.path.expanduser(config_file))
    
    if not config_path.exists():
        raise ConfigurationError(
            f"Configuration file not found: {config_file}\n"
            f"Please create a file at {config_file} with the following format:\n"
            "url: https://terrakio-server-candidate-d4w6vamyxq-ts.a.run.app/wcs_secure\n"
            "key: your-api-key-here"
        )
    
    try:
        with open(config_path, 'r') as f:
            content = f.read().strip()
            
            # Support both YAML and simple key: value format
            if ':' in content and '{' not in content:
                # Simple key: value format (like CDSAPI uses)
                config = {}
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = [x.strip() for x in line.split(':', 1)]
                            config[key] = value
                        except ValueError:
                            # Skip lines that don't have a colon
                            pass
                return config
            else:
                # YAML format for more complex configuration
                return yaml.safe_load(content) or {}
    except Exception as e:
        raise ConfigurationError(f"Failed to parse configuration file: {e}")

def create_default_config(url: str, key: str, config_file: str = DEFAULT_CONFIG_FILE) -> None:
    """
    Create a default configuration file.
    
    Args:
        url: API base URL
        key: API key
        config_file: Path to configuration file
        
    Raises:
        ConfigurationError: If the configuration file can't be created
    """
    config_path = Path(os.path.expanduser(config_file))
    
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(config_path, 'w') as f:
            f.write(f"url: {url}\n")
            f.write(f"key: {key}\n")
            f.write("# Configuration file for Terrakio API\n")
    except Exception as e:
        raise ConfigurationError(f"Failed to create configuration file: {e}")