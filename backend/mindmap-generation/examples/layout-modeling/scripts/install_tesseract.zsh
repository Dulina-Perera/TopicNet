# backend/mindmap-generation/examples/layout-modeling/scripts/install_tesseract.sh

#!/usr/bin/env zsh

# Install Tesseract.
sudo pacman -S tesseract tesseract-data-eng
echo "\n\n"

# Ensure that Tesseract is installed.
tesseract --version
echo "\n\n"

# Install `pyesseract` for the `TopicNet` conda environment.
uv pip install pytesseract
