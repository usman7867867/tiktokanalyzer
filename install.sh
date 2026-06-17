#!/bin/bash
# USMAN TikTok Analyzer - Installation Script for Termux
echo "=========================================="
echo " USMAN TikTok Analyzer - Installer"
echo "=========================================="

# Update packages
pkg update -y && pkg upgrade -y

# Install python and git if not present
pkg install python git -y

# Create project directories if not already
mkdir -p data reports

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Make main.py executable
chmod +x main.py

echo ""
echo "Installation complete!"
echo "Run the tool with: python main.py"
