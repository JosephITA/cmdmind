#!/bin/bash

# Create the script in /usr/local/bin
echo '#!/bin/bash
python3 /Users/joseph/Dev/Windsfurf/cmdmind/shell_assistant.py "$@"' | sudo tee /usr/local/bin/ask > /dev/null

# Make it executable
sudo chmod +x /usr/local/bin/ask

echo "Installation complete! You can now use 'ask' from anywhere."
