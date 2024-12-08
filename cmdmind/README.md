# CmdMind 🧠

An AI-powered command-line assistant that translates natural language into shell commands.

## Features

- 🤖 Natural language to shell command translation
- 🔄 Context-aware command suggestions
- 🌟 Support for multiple AI providers (OpenAI, Anthropic, Mistral)
- 💡 Command history awareness
- 🔒 Safe execution with preview and confirmation
- 📁 Path-aware command generation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JosephITA/cmdmind.git
cd cmdmind
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up configuration:
```bash
cp config.yml.example config.yml
# Edit config.yml with your API keys
```

4. Install the command:
```bash
sudo ./install.sh
```

## Usage

Simply use the `ask` command followed by your request:

```bash
ask "show me disk usage"
ask "find large files in downloads folder" -e
ask "list all python processes" -e
```

Use the `-e` flag to execute the command after preview.

## Configuration

Edit `config.yml` to:
- Choose your preferred AI provider
- Set API keys
- Configure model parameters

## License

MIT License
