from bs4 import BeautifulSoup

xhtml_file_path = 'page090-original.xhtml'

def read_xhtml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # Ensure correct encoding
        xhtml_content = file.read()
    return xhtml_content

# read the span tags from the xhtml file
def get_span_tags(xhtml_content):
    soup = BeautifulSoup(xhtml_content, 'html.parser')
    body = soup.find('body')
    if body:
        span_tags = body.find_all('span')
        return span_tags
    return []

def write_chars_to_file(lines):
    chars = []
    xhtml_content = read_xhtml_file(xhtml_file_path)
    span_tags = get_span_tags(xhtml_content)
    current_bottom = ''
    for tag in span_tags:
        text = tag.get_text()
        style = tag.get('style')
        if style:
            style_properties = style.split(';')
            
            for prop in style_properties:
                if 'bottom' in prop:
                    chars.append(f'{text}')
                    bottom = prop.split(';')[0].strip()
                    if current_bottom is not None:
                        if bottom != current_bottom:
                            chars.append(f'\n')
                    current_bottom = bottom
                
    lines = [f"{text}" for text in chars]
    with open('output.txt', 'w', encoding='utf-8') as file:  # Ensure correct encoding
        file.write(f''.join(lines))

def main():
    chars = []
    write_chars_to_file(chars)
    return

main()