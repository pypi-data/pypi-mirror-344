import requests
from typing import Union, BinaryIO
from pathlib import Path

from ..exceptions import DownloadError

def download_file(url: str, target: Union[str, Path, BinaryIO], 
                session: requests.Session = None, chunk_size: int = 8192,
                timeout: int = 60, verify: bool = True) -> None:
    """
    Download a file from a URL.
    
    Args:
        url: URL to download from
        target: Path or file-like object to write to
        session: Optional requests session to use
        chunk_size: Size of chunks to download
        timeout: Request timeout
        verify: Verify SSL certificates
        
    Raises:
        DownloadError: If download fails
    """
    try:
        # Use provided session or create a new one
        if session is None:
            _session = requests.Session()
        else:
            _session = session
        
        # Stream the download
        with _session.get(url, stream=True, timeout=timeout, verify=verify) as response:
            if not response.ok:
                raise DownloadError(f"Download failed: {response.status_code} {response.reason}")
            
            # Handle different target types
            if isinstance(target, (str, Path)):
                with open(target, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
            else:
                # Assume file-like object
                for chunk in response.iter_content(chunk_size=chunk_size):
                    target.write(chunk)
                    
    except requests.RequestException as e:
        raise DownloadError(f"Download failed: {str(e)}")
    finally:
        # Close the session if we created it
        if session is None and '_session' in locals():
            _session.close()