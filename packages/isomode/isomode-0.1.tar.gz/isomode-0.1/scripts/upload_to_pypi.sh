#!/bin/bash
set -e  # Exit on error

# Function to validate and read PyPI tokens
get_pypi_creds() {
    python3 - << 'EOF'
from configparser import ConfigParser
from pathlib import Path
import sys

def validate_token(token, section):
    if not token.startswith("pypi-"):
        print(f"Error: {section} token must start with 'pypi-'", file=sys.stderr)
        print(f"Get your token from https://pypi.org/manage/account/token/", file=sys.stderr)
        sys.exit(1)

def read_pypirc():
    pypirc = Path.home() / '.pypirc'
    if not pypirc.exists():
        print("Error: ~/.pypirc not found", file=sys.stderr)
        sys.exit(1)
        
    config = ConfigParser()
    config.read(pypirc)
    
    for section in ['pypi', 'testpypi']:
        if section not in config:
            print(f"Error: {section} section missing in ~/.pypirc", file=sys.stderr)
            sys.exit(1)
        
        if 'password' not in config[section]:
            print(f"Error: API token missing in {section} section", file=sys.stderr)
            sys.exit(1)
            
        validate_token(config[section]['password'], section)
            
    print(f"PYPI_TOKEN={config['pypi']['password']}")
    print(f"TEST_TOKEN={config['testpypi']['password']}")

read_pypirc()
EOF
}

# Get credentials from .pypirc
eval $(get_pypi_creds)

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf dist/ build/ *.egg-info

# Install or update uv if not already installed
echo "Ensuring uv is installed..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install build
echo "Installing build package..."
uv pip install --upgrade build

# Build the package
echo "Building package..."
python -m build

# Ask for confirmation before uploading
read -p "Do you want to upload to PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # First attempt to upload to test.pypi.org
    echo "First, uploading to Test PyPI..."
    UV_PUBLISH_USERNAME="__token__" UV_PUBLISH_PASSWORD="$TEST_TOKEN" \
    UV_REPOSITORY_URL=https://test.pypi.org/legacy/ \
    uv publish dist/*
    
    # Ask for confirmation before uploading to real PyPI
    read -p "Test upload successful. Upload to real PyPI? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Uploading to PyPI..."
        UV_PUBLISH_USERNAME="__token__" UV_PUBLISH_PASSWORD="$PYPI_TOKEN" \
        uv publish dist/*
        echo "Upload complete!"
    else
        echo "Skipping upload to PyPI"
    fi
else
    echo "Upload cancelled"
fi

echo "
Note: Configure your ~/.pypirc with API tokens:

[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxx

[testpypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxx
repository = https://test.pypi.org/legacy/

Get your tokens from:
- PyPI: https://pypi.org/manage/account/token/
- TestPyPI: https://test.pypi.org/manage/account/token/

And set proper permissions: chmod 600 ~/.pypirc"
