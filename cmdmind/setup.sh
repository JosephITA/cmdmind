#!/bin/bash

# Ensure ~/bin exists
mkdir -p ~/bin

# Create symbolic link
ln -sf "$(pwd)/shell_assistant.py" ~/bin/ask

# Make both scripts executable
chmod +x shell_assistant.py
chmod +x ~/bin/ask

# Add ~/bin to PATH if not already there
if ! grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
fi

echo "Setup complete! Please run this command in your terminal:"
echo "source ~/.zshrc"
