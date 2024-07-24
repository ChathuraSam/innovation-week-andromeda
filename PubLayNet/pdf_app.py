import fitz  # PyMuPDF
import ebooklib
from ebooklib import epub
import os

def pdf_to_epub(pdf_path, epub_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Create a new EPUB book
    book = epub.EpubBook()
    
    # Set metadata (adjust as needed)
    book.set_identifier('id123456')
    book.set_title('Sample Book')
    book.set_language('en')
    
    book.add_author('Author Name')
    
    # Loop through each page of the PDF
    for num, page in enumerate(doc):
        text = page.get_text()
        
        # Create an EPUB chapter
        c1 = epub.EpubHtml(title=f'Chapter {num+1}', file_name=f'chap_{num+1}.xhtml', lang='en')
        c1.content = f'<h1>Chapter {num+1}</h1><p>{text}</p>'
        
        # Add chapter to the book
        book.add_item(c1)
    
    # Define EPUB Table of Contents and Book order
    book.toc = [epub.Link(f'chap_{num+1}.xhtml', f'Chapter {num+1}', f'chap_{num+1}') for num in range(len(doc))]
    
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define CSS style
    style = 'BODY {color: black;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Write the EPUB file
    epub.write_epub(epub_path, book, {})
    
    print(f"EPUB file created at {epub_path}")

# Specify the paths to your PDF and desired output EPUB
pdf_path = "pdf/example.pdf"
epub_path = "pdf/output.epub"

pdf_to_epub(pdf_path, epub_path)