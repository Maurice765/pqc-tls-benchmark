#!/usr/bin/env fish

# Create virtual environment if it doesn't exist
if not test -d .venv
    echo "Creating virtual environment..."
    python3 -m venv .venv
end

# Activate virtual environment (Using the Fish specific script)
source .venv/bin/activate.fish

# Install dependencies
echo "Installing dependencies..."
if test -f requirements.txt
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found."
end

echo "Setup complete! Run 'source .venv/bin/activate.fish' to activate the environment manually."