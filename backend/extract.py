# %%
import pymupdf

from pymupdf import Document
from typing import List

# %%
print(pymupdf.__doc__)

# %%
doc: Document = pymupdf.open('./cognitive_analytics.pdf')

print(f'Page Count: {doc.page_count}', end='\n\n')
print(f'Metadata: {doc.metadata}', end='\n\n') # Might be possible to extract the title from here!
print(f'Table of Content: {doc.get_toc()}', end='\n\n')

# %%
# for page in doc:
# 	links: List = page.get_links()
# 	print(f'Page: {page.number}\nLinks: {links}', end='\n\n')

# for page in doc:
#   annots: List = page.annots()

#   print(f'Page: {page.number}')
#   if annots:
#     for annot in annots:
#       # Extract details about each annotation
#       annot_text = annot.get_text()
#       if annot_text:
#         print(f'Annotation: {annot_text}')
#   else:
#   	print("No annotations found.\n")

for page in doc:
	print(f'Page: {page.number}')
	print(f'Text: {page.get_text()}', end='\n\n')
