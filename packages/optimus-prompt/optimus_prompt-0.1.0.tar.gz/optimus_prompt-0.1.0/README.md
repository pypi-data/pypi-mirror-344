# Optimus Prompt 🤖

Compare responses from different Language Learning Models (LLMs) to the same prompt.

## Features

- Support for multiple LLM providers:
  - OpenAI (GPT-3.5, GPT-4)
  - Anthropic (Claude)
- Simple prompt input via text file
- Human-readable output format
- Easy to extend with new providers

## Installation

```bash
pip install optimus-prompt
```

## Quick Start

1. Create a `prompt.txt` file with your prompt:
```text
Explain quantum computing in simple terms
```

2. Set up your API keys in a `.env` file:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

3. Run Prompt Prism:
```python
from optimus_prompt.core import Prompt
from optimus_prompt.providers import OpenAIProvider, AnthropicProvider
from optimus_prompt.core import ResponseWriter

# Initialize providers
providers = [
    OpenAIProvider(model="gpt-4"),
    AnthropicProvider(model="claude-3")
]

# Read prompt from file
with open("prompt.txt", "r") as f:
    prompt_text = f.read().strip()
prompt = Prompt(prompt_text)

# Collect responses
responses = []
for provider in providers:
    response = provider.generate(prompt)
    responses.append(response)

# Write responses to file
writer = ResponseWriter("output.txt")
writer.write(prompt, responses)
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/optimus-prompt.git
cd optimus-prompt
```

2. Install Poetry (if not already installed):
```bash
pip install poetry
```

3. Install dependencies:
```bash
poetry install
```

### Running Tests

```bash
poetry run pytest
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.