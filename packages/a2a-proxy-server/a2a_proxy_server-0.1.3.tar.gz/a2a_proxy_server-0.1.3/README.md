# A2A Proxy Server

A proxy server for Google's A2A (Agent-to-Agent) protocol.

## Installation

This package requires a two-step installation:

1. First, install the Google A2A package from GitHub:

   ```
   uv pip install git+https://github.com/djsamseng/A2A.git@prefixPythonPackage#subdirectory=samples/python
   ```

   or using pip:

   ```
   pip install git+https://github.com/djsamseng/A2A.git@prefixPythonPackage#subdirectory=samples/python
   ```

2. Then, install the a2a-proxy-server package:
   ```
   uv pip install a2a-proxy-server
   ```
   or using pip:
   ```
   pip install a2a-proxy-server
   ```

## Usage

```bash
a2a-proxy-server --help
```

## Development

For local development, the package includes UV configuration in `pyproject.toml` to
automatically install dependencies from GitHub:

```bash
cd a2a-proxy-server
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```
