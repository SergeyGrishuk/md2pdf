#!/bin/bash
# Build md2pdf as a standalone executable using PyInstaller

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building md2pdf executable..."

# Create/use a build virtual environment
if [ ! -d ".build-venv" ]; then
    echo "Creating build environment..."
    uv venv .build-venv
fi

source .build-venv/bin/activate

# Install dependencies and PyInstaller
echo "Installing dependencies..."
uv pip install -e .
uv pip install pyinstaller

# Create entry point script for PyInstaller
cat > _entry.py << 'EOF'
from md2pdf.cli import main

if __name__ == "__main__":
    main()
EOF

# Build the executable
echo "Packaging with PyInstaller..."
pyinstaller \
    --onefile \
    --name md2pdf \
    --clean \
    --noconfirm \
    --add-data "md2pdf/styles:md2pdf/styles" \
    _entry.py

# Cleanup
rm -f _entry.py
deactivate

echo ""
echo "  Build complete!"
echo "  Executable: $SCRIPT_DIR/dist/md2pdf"
echo ""
echo "  To install, run: ./install.sh"
