#!/bin/bash
set -euo pipefail

# Simple installer for PyCarDisplay on Raspberry Pi
USER_HOME="${HOME:-/home/$USER}"
DESKTOP="$USER_HOME/Desktop"
REPO_URL="https://github.com/Mr0o/PyCarDisplay.git"
TARGET_DIR="$DESKTOP/PyCarDisplay"

mkdir -p "$DESKTOP"

if command -v git >/dev/null 2>&1; then
    if [ -d "$TARGET_DIR/.git" ]; then
        echo "Updating existing repository at $TARGET_DIR"
        git -C "$TARGET_DIR" pull --rebase
    else
        echo "Cloning repository to $TARGET_DIR"
        git clone "$REPO_URL" "$TARGET_DIR"
    fi
else
    echo "git is not installed. Please install git and re-run this script."
    exit 1
fi

cd "$TARGET_DIR"

# Create Python venv if missing
if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is not installed. Please install python3 and re-run."
    exit 1
fi

if [ ! -d "env" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv env
fi

# Use venv pip to install requirements
PIP_BIN="$TARGET_DIR/env/bin/pip"
"$PIP_BIN" install --upgrade pip setuptools wheel
if [ -f "requirements.txt" ]; then
    "$PIP_BIN" install -r requirements.txt
fi

# Make run.sh executable
if [ -f "run.sh" ]; then
    chmod +x run.sh
fi

# Add startup entry to .bashrc if not already present
STARTUP_LINE="bash \"$TARGET_DIR/run.sh\" &"
BASHRC="$USER_HOME/.bashrc"
grep -Fxq "$STARTUP_LINE" "$BASHRC" 2>/dev/null || echo "$STARTUP_LINE" >> "$BASHRC"

echo -e "\n\nInstallation complete. Please reboot your Raspberry Pi to start PyCarDisplay automatically."