# %%
# %pip install -qqq --upgrade pdfminer.six

# %%
from io import StringIO
from pdfminer.high_level import extract_text, extract_text_to_fp

# %%
def extract_text_as_string(pdf_path: str) -> str:
    """
    Extract text from a PDF file and return it as a string.
    
    :param pdf_path: Path to the input PDF file.
    :return: Extracted text as a string.
    """
    strout: StringIO = StringIO()
    with open(pdf_path, "rb") as fin:
        extract_text_to_fp(fin, strout)
    return strout.getvalue().strip()


def extract_text_to_file(pdf_path: str, text_file_path: str) -> None:
    """
    Extract text from a PDF file and save it to a text file.
    
    :param pdf_path: Path to the input PDF file.
    :param text_file_path: Path to the output text file.
    """
    with open(pdf_path, "rb") as fin:
        text: str = extract_text(fin)
    
    with open(text_file_path, "w") as fout:
        fout.write(text)

# %%
if __name__ == "__main__":
    pdf_path: str = "Documents/Slides.pdf"

    # Extract text from the PDF file and print it.
    # text: str = extract_text_as_string(pdf_path)
    # print(text)

    # Save the extracted text to a text file.
    text_file_path: str = "Documents/Slides.txt"
    extract_text_to_file(pdf_path, text_file_path)
