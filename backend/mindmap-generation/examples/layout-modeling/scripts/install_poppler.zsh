# backend/mindmap-generation/examples/layout-modeling/scripts/install_poppler.zsh

#!/usr/bin/env zsh

# Install Poppler.
sudo pacman -S poppler
echo "\n\n"

# Install `pdf2image` for the `TopicNet` conda environment.
uv pip install pdf2image
