import fitz  # PyMuPDF
import html
import os

# Define color code (optional, for visualization)
colors = {
    'title': (255, 0, 0),
    'text': (0, 255, 0),
    'figure': (0, 0, 255),
    'table': (255, 255, 0),
    'list': (0, 255, 255)
}

# Function to detect text and images and create annotations
def create_annotations(page):
    annotations = []

    # Detect text blocks
    for block in page.get_text("dict")["blocks"]:
        if block["type"] == 0:  # Text block
            bbox = block["bbox"]
            annotations.append({
                'bbox': bbox,
                'category': 'text',
                'content': block["lines"]
            })

    # Detect images
    for img in page.get_images(full=True):
        try:
            xref = img[0]
            bbox = page.get_image_bbox(xref)
            annotations.append({
                'bbox': [bbox.x0, bbox.y0, bbox.width, bbox.height],
                'category': 'figure',
                'xref': xref
            })
        except ValueError as e:
            print(f"Skipping invalid image reference: {e}")

    return annotations

# Function to create XHTML content from annotations
def create_xhtml_content(page, annotations):
    xhtml_content = ""
    
    for annotation in annotations:
        bbox = annotation['bbox']
        x0, y0, x1, y1 = bbox

        if annotation['category'] == 'text':
            # Combine text lines into paragraphs
            paragraphs = []
            for line in annotation['content']:
                text = " ".join([html.escape(span['text']) for span in line['spans']])
                paragraphs.append(f"<p>{text}</p>")
            xhtml_content += "\n".join(paragraphs)
        
        elif annotation['category'] == 'figure':
            xref = annotation['xref']
            pix = fitz.Pixmap(page.parent, xref)
            img_name = f"image_{xref}.png"
            pix.save(img_name)  # Save image to file
            xhtml_content += f'<img src="{img_name}" alt="Figure" style="position:absolute; left:{x0}px; top:{y0}px; width:{x1 - x0}px; height:{y1 - y0}px;">'

    return xhtml_content

# Open a PDF and annotate it
pdf_path = "pdf/example.pdf"
output_dir = "output_xhtml_pages"
os.makedirs(output_dir, exist_ok=True)
document = fitz.open(pdf_path)

for page_num in range(document.page_count):
    page = document.load_page(page_num)
    annotations = create_annotations(page)
    xhtml_content = create_xhtml_content(page, annotations)
    
    xhtml = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<meta charset="UTF-8" />\n<title>Annotated PDF - Page {page_num+1}</title>\n<style>p { margin: 0; padding: 0; }</style>\n</head>\n<body>\n'
    xhtml += f"<div style='position:relative;'>\n{xhtml_content}\n</div>\n"
    xhtml += '</body>\n</html>'
    
    # Save the XHTML file for the current page
    output_xhtml_path = os.path.join(output_dir, f"output_page_{page_num+1}.xhtml")
    with open(output_xhtml_path, "w", encoding="utf-8") as f:
        f.write(xhtml)
    
    print(f"Annotated XHTML for page {page_num+1} saved to {output_xhtml_path}")

print(f"All pages processed and saved to {output_dir}")
