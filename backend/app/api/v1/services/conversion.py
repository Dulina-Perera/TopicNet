# backend/mindmap-generation/api/v1/services/convert.py

# %%
import mimetypes
import os
import pathlib
import pymupdf
import pymupdf4llm

from pymupdf import Document
from typing import Union

# %%
SAMPLES_DIR: str = "../../../samples"

# %%
def convert_pdf_to_md(
  pdf_path: str,
  output_dir: str
) -> None:
	# Check if the file exists and is a file.
	if os.path.exists(pdf_path) and os.path.isfile(pdf_path):
		# Check if the file extension is '.pdf'.
		if pdf_path.lower().endswith(".pdf"):
			# Confirm the MIME type is 'application/pdf'.
			mime_type: Union[str, None]
			mime_type, _ = mimetypes.guess_type(pdf_path)
			if mime_type == "application/pdf":
				# Extract the content as Markdown.
				md_content: str = pymupdf4llm.to_markdown(pdf_path)

				# If the output directory does not exist, create it.
				if not os.path.exists(output_dir):
					os.makedirs(output_dir)

				# Write the Markdown content to a file.
				md_path: str = os.path.join(output_dir, pathlib.Path(pdf_path).stem + ".md")
				pathlib.Path(md_path).write_bytes(md_content.encode("utf-8"))

				print(f"Markdown content extracted and saved to '{md_path}'.")
			else:
				raise ValueError(f"File '{pdf_path}' is not a PDF file.")
		else:
			raise ValueError(f"File '{pdf_path}' is not a PDF file.")
	else:
		raise FileNotFoundError(f"File '{pdf_path}' does not exist.")


def convert_pdf_to_txt(
	pdf_path: str,
	output_dir: str
) -> None:
	# Check if the file exists and is a file.
	if os.path.exists(pdf_path) and os.path.isfile(pdf_path):
		# Check if the file extension is '.pdf'.
		if pdf_path.lower().endswith(".pdf"):
			# Confirm the MIME type is 'application/pdf'.
			mime_type: Union[str, None]
			mime_type, _ = mimetypes.guess_type(pdf_path)
			if mime_type == "application/pdf":
				# Open the PDF file, read through each page, and extract the text content.
				with pymupdf.open(pdf_path) as pdf:
					txt_content: str = ""
					for page in pdf:
						txt_content += page.get_text() + "\n"

				# If the output directory does not exist, create it.
				if not os.path.exists(output_dir):
					os.makedirs(output_dir)

				# Write the plain text content to a file.
				txt_path: str = os.path.join(output_dir, pathlib.Path(pdf_path).stem + ".txt")
				pathlib.Path(txt_path).write_text(txt_content)

				print(f"Plain text content extracted and saved to '{txt_path}'.")
			else:
				raise ValueError(f"File '{pdf_path}' is not a PDF file.")
		else:
			raise ValueError(f"File '{pdf_path}' is not a PDF file.")
	else:
		raise FileNotFoundError(f"File '{pdf_path}' does not exist.")

# %%
if __name__ == "__main__":
  convert_pdf_to_md(
		os.path.join(SAMPLES_DIR, "pdf", "cognitive_analytics.pdf"),
		os.path.join(SAMPLES_DIR, "md")
	)

  convert_pdf_to_txt(
		os.path.join(SAMPLES_DIR, "pdf", "cognitive_analytics.pdf"),
		os.path.join(SAMPLES_DIR, "txt")
	)
