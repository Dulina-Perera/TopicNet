# backend/app/services/extract.py

import os
import pymupdf

from pymupdf import Document
from typing import List


def extract_text_from_pdf(pdf_path: str) -> None:
  if not pdf_path.endswith('.pdf'):
    raise ValueError("The provided file is not a PDF.")
  else:
    txt_file_path: str = os.path.splitext(pdf_path)[0] + '.raw.txt'

    try:
      doc: Document = pymupdf.open(pdf_path)
      text_content: List[str] = []

      for page in doc:
        text_content.append(page.get_text())

      with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write('\n'.join(filter(None, text_content)))

      print(f"Text extracted and saved to: {txt_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
