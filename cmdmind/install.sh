#!/bin/bash

# Get the directory of the script
SCRIPT_DIR=$(dirname "$(realpath "$0")")
SCRIPT_PATH="$SCRIPT_DIR/shell_assistant.py"

# Check if the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: $SCRIPT_PATH does not exist. Please check the path."
    exit 1
fi

# Create the global 'ask' command
echo "#!/bin/bash
python3 \"$SCRIPT_PATH\" \"\$@\"" | sudo tee /usr/local/bin/ask > /dev/null

# Make it executable
sudo chmod +x /usr/local/bin/ask

echo "Installation complete! You can now use 'ask' from anywhere."