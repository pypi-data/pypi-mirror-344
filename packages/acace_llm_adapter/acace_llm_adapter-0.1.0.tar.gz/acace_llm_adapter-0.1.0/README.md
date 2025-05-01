# ACACE LLM Adapter

A Language Model adapter module for the Adaptive Context-Aware Content Engine (ACACE).

## Features

- OpenAI API integration
- Anthropic API integration
- Unified interface for multiple LLM providers
- Error handling and retries

## Installation

```bash
pip install acace_llm_adapter
```

## Usage

```python
from acace_llm_adapter import LLMAdapter

# Initialize with your API keys
adapter = LLMAdapter(
    openai_api_key="your-openai-key",
    anthropic_api_key="your-anthropic-key"
)

# Generate content using OpenAI
response = adapter.generate(
    "Write a short story about a robot learning to paint.",
    provider="openai",
    model="gpt-4"
)

# Generate content using Anthropic
response = adapter.generate(
    "Write a short story about a robot learning to paint.",
    provider="anthropic",
    model="claude-3-opus-20240229"
)
```

## License

MIT License 