import subprocess
from urllib.parse import urlparse, quote
import pathlib

def get_lightpanda_path():
    """Return the path to the lightpanda binary."""
    # Get the directory of this file
    package_dir = pathlib.Path(__file__).parent
    # Construct path to the binary
    binary_path = package_dir / "bin" / "lightpanda"
    if not binary_path.exists():
        raise FileNotFoundError("lightpanda binary not found in package")
    return binary_path

def parse_url(url: str):
    # Step 1: Parse the URL
    parsed = urlparse(url)
    scheme = parsed.scheme    # 'https'
    netloc = parsed.netloc    # 'example.co.uk'
    path = parsed.path        # '/路径/测试'
    query = parsed.query      # 'query=测试'

    # Step 2: Quote non-ASCII parts (path and query)
    quoted_path = quote(path, safe='/')  # Safe characters like '/' are not encoded
    quoted_query = quote(query, safe='=&')  # Safe characters for query strings

    # Step 3: Reconstruct the URL (optional)
    quoted_url = f"{scheme}://{netloc}{quoted_path}"
    if quoted_query:
        quoted_url += f"?{quoted_query}"
    return quoted_url

def get(url: str) -> str:
    """
    Fetch HTML content from a URL using the lightpanda binary.

    Args:
        url (str): The URL to fetch HTML from.

    Returns:
        str: The HTML content as a string.

    Raises:
        FileNotFoundError: If the lightpanda binary is not found.
        subprocess.CalledProcessError: If the command execution fails.
    """
    cmd = f'"{get_lightpanda_path()}" fetch --dump "{parse_url(url)}"'
    try:
        resp = subprocess.getoutput(cmd)
        lines = resp.split("\n")
        for idx, line in enumerate(lines):
            if line.startswith("info") or line.startswith("warning") or "(browser)" in line:
                continue
            else:
                _html = lines[idx:]
                break
        html = "\n".join(_html)
        return html
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Failed to execute lightpanda: {e}")