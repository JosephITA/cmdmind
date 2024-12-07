# Shell Assistant

A command-line tool that translates natural language into Linux shell commands using AI.

## Installation

1. Clone this repository
2. Install the requirements:
```bash
pip install -r requirements.txt
```
3. Make the script executable:
```bash
chmod +x shell_assistant.py
```
4. Copy the example config file and add your API keys:
```bash
cp config.yml.example config.yml
# Edit config.yml with your preferred text editor
```

## Configuration

The tool uses a `config.yml` file in the same directory as the script. Here's an example configuration:

```yaml
# LLM Provider Configuration
# Choose one of: 'openai', 'anthropic', or 'mistral'
llm_provider: "openai"

# OpenAI Configuration
openai:
  api_key: "your-openai-api-key-here"
  model: "gpt-3.5-turbo"  # or "gpt-4" if you have access

# Anthropic Configuration
anthropic:
  api_key: "your-anthropic-api-key-here"
  model: "claude-2"  # or "claude-instant-1"

# Mistral Configuration
mistral:
  api_key: "your-mistral-api-key-here"
  model: "mistral-tiny"  # or "mistral-small", "mistral-medium"

# General Settings
max_tokens: 100
temperature: 0.7
```

Choose your preferred LLM provider by setting the `llm_provider` field and adding the corresponding API key.

## Usage

```bash
# Basic usage - will show the generated command
./shell_assistant.py "what you want to do"

# Execute the command after confirmation
./shell_assistant.py "what you want to do" -e

# Examples
./shell_assistant.py "find all PDF files modified in the last 24 hours"
./shell_assistant.py "create a backup of my home directory" -e
```

## Features

- Translates natural language into shell commands using AI
- Supports multiple LLM providers (OpenAI, Anthropic, Mistral)
- Optional command execution with confirmation
- Configurable via YAML config file
- Safe execution with user confirmation
