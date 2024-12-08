#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
import click
import yaml
import os
import subprocess
import platform
from typing import Optional, List
import openai
import anthropic
from mistralai.client import MistralClient
from collections import deque

# Get the actual path of the script, even when called through a symlink
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.yml")
HISTORY_SIZE = 3
command_history = deque(maxlen=HISTORY_SIZE)

def get_system_info():
    system = platform.system()
    if system == "Darwin":
        mac_version = platform.mac_ver()[0]
        return f"macOS {mac_version}"
    elif system == "Linux":
        distro = " ".join(platform.linux_distribution()) if hasattr(platform, 'linux_distribution') else platform.version()
        return f"Linux ({distro})"
    elif system == "Windows":
        return f"Windows {platform.release()}"
    return system

def load_config():
    if not os.path.exists(CONFIG_FILE):
        click.echo(f"Error: Config file not found at {CONFIG_FILE}")
        click.echo("Please create a config.yml file with your API keys and settings.")
        exit(1)
    
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def jls_extract_def(jls_extract_var):
    return jls_extract_var


def get_command_from_llm(prompt: str, config: dict) -> str:
    provider = config.get('llm_provider', 'openai')
    system_info = get_system_info()
    current_dir = os.getcwd()
    
    # Create context with command history
    history_context = "\n".join([f"Previous command {i+1}: {cmd}" for i, cmd in enumerate(command_history)])
    context = f"""Current directory: {current_dir}
Previous commands: {history_context if command_history else 'None'}"""

    system_prompt = f"""You are a command-line translation tool for {system_info}.

Previous commands typed by the user: {context}

RESPONSE FORMAT:
- Output ONLY the command
- No explanations
- No formatting
- No quotes
- No newlines
- No OS labels
- No multiple options
- If sudo needed, prefix with 'SUDO_REQUIRED:'

Examples of CORRECT responses:
ls -la
SUDO_REQUIRED: systemctl restart nginx
ps aux | grep python

Examples of INCORRECT responses:
```ls -la```
The command is: ls -la
macOS command: ls -la
Try this: ls -la
or use this: ls
Here are some options:
1. ls -la
2. ls

REMEMBER: Return EXACTLY ONE command, nothing else."""
    
    if provider == 'openai':
        client = openai.OpenAI(api_key=config['openai']['api_key'])
        response = client.chat.completions.create(
            model=config['openai']['model'],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=config.get('max_tokens', 100),
            temperature=config.get('temperature', 0.7)
        )
        return response.choices[0].message.content.strip()
    
    elif provider == 'anthropic':
        client = anthropic.Anthropic(api_key=config['anthropic']['api_key'])
        response = client.messages.create(
            model=config['anthropic']['model'],
            max_tokens=config.get('max_tokens', 100),
            messages=[{
                "role": "user",
                "content": f"{system_prompt}\n\nUser request: {prompt}"
            }]
        )
        return response.content[0].text.strip()
    
    # elif provider == 'mistral':
    #     client = MistralClient(api_key=config['mistral']['api_key'])
    #     messages = [
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": prompt}
    #     ]
    #     chat_response = client.chat(
    #         model=config['mistral']['model'],
    #         messages=messages
    #     )
    #     return chat_response.choices[0].message.content.strip()
    
    # else:
    #     raise ValueError(f"Unsupported LLM provider: {provider}")
    elif provider == 'mistral':
        from mistralai import Mistral  # Import the correct Mistral client class
        client = Mistral(api_key=config['mistral']['api_key'])  # Initialize the client with the API key
    
        # Prepare the messages
        jls_extract_var = prompt
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": jls_extract_def(jls_extract_var)}
        ]
    
        # Send the chat request using the new method
        response = client.chat.complete(
            model=config['mistral']['model'],
            messages=messages,
            max_tokens=config.get('max_tokens', 100),
            temperature=config.get('temperature', 0.7)
    )
    
    # Return the response content
    return response.choices[0].message.content.strip()
@click.command()
@click.argument('prompt', type=str)
@click.option('-e', '--execute', is_flag=True, help='Execute the generated command after confirmation')
def cli(prompt: str, execute: bool):
    """Translate natural language into shell commands using AI."""
    config = load_config()
    
    try:
        command = get_command_from_llm(prompt, config)
        
        # Handle sudo prefix
        needs_sudo = False
        if command.startswith('SUDO_REQUIRED:'):
            needs_sudo = True
            command = command.replace('SUDO_REQUIRED:', '').strip()
        
        click.echo(f"\nGenerated command:" + (" (requires sudo)" if needs_sudo else ""))
        click.echo(command)
        
        if execute:
            if click.confirm('\nDo you want to execute this command?', default=False):
                if needs_sudo:
                    command = f"sudo {command}"
                result = subprocess.run(command, shell=True, text=True, capture_output=True)
                command_history.append(command)
                click.echo("\nCommand output:")
                if result.stdout:
                    click.echo(result.stdout)
                if result.stderr:
                    click.echo(result.stderr, err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)

if __name__ == '__main__':
    cli()
