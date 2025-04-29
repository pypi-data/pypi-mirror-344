import requests
import xarray as xr
import time
from io import BytesIO
from pathlib import Path
from typing import Dict, Any, Optional, Union, BinaryIO

from .config import read_config_file, DEFAULT_CONFIG_FILE
from .exceptions import APIError, ConfigurationError, DownloadError
from .api import make_request
from .utils.validation import validate_feature

class Client:
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None, 
                 quiet: bool = False, config_file: Optional[str] = None,
                 verify: bool = True, timeout: int = 60):
        """
        Initialize the Terrakio API client.
        
        Args:
            url: API base URL (optional, will use config file if not provided)
            key: API key or token (optional, will use config file if not provided)
            quiet: If True, suppress progress messages
            config_file: Path to configuration file (default is ~/.terrakioapirc)
            verify: Verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.quiet = quiet
        self.verify = verify
        self.timeout = timeout
        
        # Try to get config from parameters first, then config file
        if url is not None and key is not None:
            self.url = url
            self.key = key
        else:
            if config_file is None:
                config_file = DEFAULT_CONFIG_FILE
            
            try:
                config = read_config_file(config_file)
                self.url = config.get('url')
                self.key = config.get('key')
            except Exception as e:
                raise ConfigurationError(
                    f"Failed to read configuration: {e}\n\n"
                    "To fix this issue:\n"
                    "1. Create a file at ~/.terrakioapirc with:\n"
                    "url: https://terrakio-server-candidate-d4w6vamyxq-ts.a.run.app/wcs_secure\n"
                    "key: your-api-key\n\n"
                    "OR\n\n"
                    "2. Initialize the client with explicit parameters:\n"
                    "client = terrakio_api.Client(\n"
                    "    url='https://terrakio-server-candidate-d4w6vamyxq-ts.a.run.app/wcs_secure',\n"
                    "    key='your-api-key'\n"
                    ")"
                )
        
        # Validate configuration
        if not self.url:
            raise ConfigurationError("Missing API URL in configuration")
        if not self.key:
            raise ConfigurationError("Missing API key in configuration")
            
        # Ensure URL doesn't end with slash
        self.url = self.url.rstrip('/')
        
        if not self.quiet:
            print(f"Using Terrakio API at: {self.url}")
        
        # Initialize session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.key
        })
    
    def wcs(self, expr: str, feature: Dict[str, Any], in_crs: str = "epsg:4326",
            out_crs: str = "epsg:4326", output: str = "csv", resolution: int = -1,
            **kwargs):
        """
        Make a WCS request to the Terrakio API.
        
        Args:
            expr: Expression string for data selection
            feature: GeoJSON Feature dictionary containing geometry information
            in_crs: Input coordinate reference system (default: "epsg:4326")
            out_crs: Output coordinate reference system (default: "epsg:4326")
            output: Output format (default: "csv")
            resolution: Resolution value (default: -1)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Data in the requested format (xr.Dataset for netcdf, pd.DataFrame for csv)
        """
        # Validate the feature object
        validate_feature(feature)
        
        # Prepare the payload
        payload = {
            "feature": feature,
            "in_crs": in_crs,
            "out_crs": out_crs,
            "output": output,
            "resolution": resolution,
            "expr": expr,
            **kwargs
        }
        
        if not self.quiet:
            print(f"Requesting data with expression: {expr}")
        
        try:
            # Make the API request
            response = self.session.post(self.url, json=payload, timeout=self.timeout, verify=self.verify)
            
            # Handle HTTP errors
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                
                raise APIError(error_msg)
            
            # Handle different output formats
            if output.lower() == "csv":
                import pandas as pd
                return pd.read_csv(BytesIO(response.content))
            elif output.lower() == "netcdf":
                return xr.open_dataset(BytesIO(response.content))
            else:
                # Try to determine the format and use appropriate reader
                try:
                    return xr.open_dataset(BytesIO(response.content))
                except ValueError:
                    import pandas as pd
                    try:
                        return pd.read_csv(BytesIO(response.content))
                    except:
                        # If all else fails, return the raw content
                        return response.content
            
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
    
    def close(self):
        """Close the client session."""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()