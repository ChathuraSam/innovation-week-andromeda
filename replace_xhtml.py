from bs4 import BeautifulSoup

def get_span_tags_from_text_file(text_file):
    span_tags = {}
    with open(text_file, 'r', encoding='utf-8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')
        tags = soup.find_all('span')
        for tag in tags:
            style = tag.get('style', '')
            style_dict = dict(item.strip().split(':') for item in style.split(';') if item.strip())
            bottom_value = style_dict.get('bottom', '').strip()
            if bottom_value:
                span_tags[bottom_value] = tag
    return span_tags

def replace_span_tags(xhtml_file, text_file):
    span_tags_from_text = get_span_tags_from_text_file(text_file)
    
    with open(xhtml_file, 'r', encoding='utf-8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')
        
        span_tags = soup.find_all('span')
        for tag in span_tags:
            style = tag.get('style', '')
            style_dict = dict(item.strip().split(':') for item in style.split(';') if item.strip())
            bottom_value = style_dict.get('bottom', '').strip()
            
            if bottom_value in span_tags_from_text:
                # Replace span tag with the corresponding span tag from the text file
                new_span = span_tags_from_text[bottom_value]
                tag.replace_with(new_span)

    # Save modified XHTML content back to file
    with open(xhtml_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

# Example usage:
xhtml_file = './page090.xhtml'
text_file = './text.txt'

replace_span_tags(xhtml_file, text_file)
