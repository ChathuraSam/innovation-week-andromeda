import fitz  # PyMuPDF

# Define color code
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
                'category': 'text'
            })

    # Detect images
    for img in page.get_images(full=True):
        try:
            xref = img[0]
            bbox = page.get_image_bbox(xref)
            annotations.append({
                'bbox': [bbox.x0, bbox.y0, bbox.width, bbox.height],
                'category': 'figure'
            })
        except ValueError as e:
            print(f"Skipping invalid image reference: {e}")

    return annotations

# Function to draw annotations on PDF pages
def markup_pdf(page, annotations):
    for annotation in annotations:
        # Get bounding box coordinates
        bbox = annotation['bbox']
        x0, y0, x1, y1 = bbox
        print(f"Drawing rectangle at ({x0}, {y0}), ({x1}, {y1})")

        # Draw rectangle
        rect = fitz.Rect(x0, y0, x1, y1)
        color = colors[annotation['category']]
        color = [c / 255 for c in color]  # Normalize color values to 0-1
        page.draw_rect(rect, color=color, width=2)

        # Draw label
        label = annotation['category']
        text_x, text_y = x0, y0 - 10
        page.insert_text((text_x, text_y), label, fontname="helv", fontsize=10, color=color)

# Open a PDF and annotate it
pdf_path = "pdf/example.pdf"
output_pdf_path = "pdf/output.pdf"
document = fitz.open(pdf_path)

for page_num in range(document.page_count):
    page = document.load_page(page_num)
    annotations = create_annotations(page)
    markup_pdf(page, annotations)

# Save the annotated PDF
document.save(output_pdf_path)
print(f"Annotated PDF saved to {output_pdf_path}")
