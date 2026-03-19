#!/bin/bash
# md2pdf installation script
# Installs md2pdf executable to ~/.local/bin

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
EXECUTABLE="$SCRIPT_DIR/dist/md2pdf"

# Check if executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "Error: Executable not found at $EXECUTABLE"
    echo "Run './build.sh' first to build the executable."
    exit 1
fi

echo "Installing md2pdf..."

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Copy executable
cp "$EXECUTABLE" "$BIN_DIR/md2pdf"
chmod +x "$BIN_DIR/md2pdf"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "NOTE: $BIN_DIR is not in your PATH."
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo "  md2pdf installed successfully!"
echo "  Run 'md2pdf --help' to get started."
