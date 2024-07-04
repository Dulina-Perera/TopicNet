# %%
import io
import os
import pymupdf

from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from PIL.PngImagePlugin import PngImageFile
from tqdm import tqdm
from typing import Dict, List, Tuple

# %%
def extract_images_from_pdf(pdf_path: str, output_dir: str = "Images") -> None:
    """
    Extract images from a PDF file and save them to the specified directory.

    :param pdf_path: Path to the input PDF file.
    :param output_dir: Directory to save the extracted images. Default is 'Images'.
    """
    pdf: pymupdf.Document = pymupdf.open(pdf_path)

    for i in tqdm(range(pdf.page_count), desc="Processing Pages for Images"):
        page: pymupdf.Page = pdf[i]
        
        img_lst: List[Tuple] = page.get_images(full=True)
        if img_lst:
            os.makedirs(f"{output_dir}/Page_{i}", exist_ok=True)
        
        for img in img_lst:
            base_img: Dict = pdf.extract_image(img[0])

            img_name: str = img[7].lower().replace(" ", "_"); ext: str = base_img["ext"]
            with Image.open(io.BytesIO(base_img["image"])) as to_save:
                to_save.save(f"{output_dir}/Page_{i}/{img_name}.{ext}", ext.upper())

# %%
if __name__ == "__main__":
    pdf_path: str = "Documents/Slides.pdf"
    extract_images_from_pdf(pdf_path)
