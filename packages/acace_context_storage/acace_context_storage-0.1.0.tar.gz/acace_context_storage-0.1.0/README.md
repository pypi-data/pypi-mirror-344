# ACACE Context Storage

A context storage module for the Adaptive Context-Aware Content Engine (ACACE).

## Features

- Session-based context storage
- Context retrieval and updates
- Memory-efficient storage
- Simple API

## Installation

```bash
pip install acace_context_storage
```

## Usage

```python
from acace_context_storage import ContextStorage

# Initialize context storage
storage = ContextStorage()

# Store context for a session
storage.store_context("session1", "This is the context for session 1")

# Retrieve context
context = storage.get_context("session1")
print(context)  # Output: "This is the context for session 1"

# Update context
storage.store_context("session1", "Updated context for session 1")
```

## License

MIT License 