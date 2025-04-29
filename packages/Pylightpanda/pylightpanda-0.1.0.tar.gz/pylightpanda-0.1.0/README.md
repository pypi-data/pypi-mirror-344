# Pylightpanda

A Python package wrapping the `lightpanda` binary to fetch HTML content from URLs.

## Installation

```bash
pip install pylightpanda
```

## Usage
```python
import pylightpanda as lp

url = "https://google.com"
html = lp.get(url)
print(html)
```

## License
MIT