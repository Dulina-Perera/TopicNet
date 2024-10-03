# backend/mindmap-generation/examples/layout-modeling/convert_pdfs_to_imgs.py

# %%
import os

from pdf2image import convert_from_path
from PIL import Image
from typing import List

# %%
# Identify the pdfs to convert.
pdfs: List[str] = os.listdir("./data/pdfs")

# Create a directory to store the images if it doesn't exist.
if not os.path.exists("./data/imgs"):
	os.makedirs("./data/imgs")

# For each pdf, create a subdirectory to store the images if it doesn't exist.
for pdf in pdfs:
  pdf_name: str = pdf.split(".")[0]

  if not os.path.exists(f"./data/imgs/{pdf_name}"):
    os.makedirs(f"./data/imgs/{pdf_name}")

# For each pdf, convert it to images and save them in the corresponding subdirectory.
for pdf in pdfs:
  pdf_name: str = pdf.split(".")[0]

  pages: List[Image.Image] = convert_from_path(f"./data/pdfs/{pdf}")
  for (i, page) in enumerate(pages):
    page.save(f"./data/imgs/{pdf_name}/page_{i}.png", "PNG")

  print(f"Converted {pdf} to images.")
