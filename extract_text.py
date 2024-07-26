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
        class_prooperties = tag.get('class')
        print(f'{class_prooperties}')
        if style:
            style_properties = style.split(';')
            
            for prop in style_properties:
                if 'bottom' in prop:
                    chars.append(f'{text}')
                    bottom = prop.split(';')[0].strip()
                    if current_bottom is not None:
                        if bottom != current_bottom:
                            pop_char = chars.pop()
                            chars.append(f'###')
                            for class_property in class_prooperties:
                                chars.append(f' {class_property}')
                            chars.append(f'###{style}')
                            chars.append(f'\n')
                            chars.append(f'{pop_char}')
                    # print(f'{current_bottom}\t{bottom}\t{text}')
                    current_bottom = bottom
                
    lines = [f"{text}" for text in chars]
    with open('output.txt', 'w', encoding='utf-8') as file:  # Ensure correct encoding
        file.write(f''.join(lines))
        
def add_span_tags_to_xhtml(chars):
    input_file_path = 'output.txt'
    output_file_path = 'output2.txt'

    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            class_properties = ''
            if len(line.split('###')) > 1:
                class_properties = line.split('###')[1]
                wrapped_line = f'<span class = \"{class_properties}\" style=\"{line.split('###')[2].replace('\n', '')}\">{(line.split('###'))[0].strip()}</span>\n'
            else:
                class_properties = ''
            
            outfile.write(wrapped_line)
    return

def main():
    chars = []
    write_chars_to_file(chars)
    add_span_tags_to_xhtml(chars)
    return

main()