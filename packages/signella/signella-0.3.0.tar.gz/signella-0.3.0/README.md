# Signella

A simple Redis-based variable sharing singleton for Python.

## Installation

```bash
pip install signella
```

## Usage

```python
from signella import signal

# Set values
signal['name'] = 'Jimmy'

# Get values
print(signal['name'])  # 'Jimmy'

# Use compound keys
signal['user', 123, 'profile'] = {'name': 'Jimmy', 'age': 30}
print(signal['user', 123, 'profile'])  # {'name': 'Jimmy', 'age': 30}
```

## Features

- Automatically starts a Redis server if one isn't available
- Simple dictionary-like interface with JSON serialization
- Support for namespacing via RADIOVAR_NS environment variable
- Override port via RADIOVAR_PORT environment variable
- Command-line interface for help and information

## Command-line Usage

After installation, you can use the `signella` command in your terminal:

```bash
# Display help, Redis connection status, and current environment settings
signella help
```

The command will show colorful output with information about:
- Redis connection status with automatic check
- Current environment variable settings
- Usage examples
- Available environment variables and their descriptions