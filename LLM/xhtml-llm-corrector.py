from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

# install libraries
# pip install langchain
# pip install langchain-openai
# pip install python-dotenv
    

def process_xhtml_file(input_file, output_file):
    # Read the input XHTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        xhtml_content = file.read()

    load_dotenv()
  
    # Define the prompt template 
    prompt_template = """
    
    You are an expert in EPUB formatting and XHTML,
    
    
    Give below is the xhtml code of the epub which is converted from pdf using PDFnet lib. 
    Having an issue in the content of html content.
    Here the text content of the pdf is generated as a bunch of span tags. 
    But here span tags contain word or subword or character. 
    Can you provide me the modified xhtml code after the text contents of spans which are 
    in the same bottom position in to a one span tag without adding extra text. 
    
    
    Bring all words to one sentence. and form the words in the same line to one span tag.
    
    XHTML content to fix:
     {xhtml_content}

     Please provide the corrected XHTML:
     """

    # Initialize the LLM:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    prompt = PromptTemplate(template=prompt_template, input_variables=["xhtml_content"])
    chain = LLMChain(llm=llm, prompt=prompt)

    # Process the XHTML content using the LLM
    result = chain.run(xhtml_content=xhtml_content)

    print(result)

    # Write the processed content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(result)

    print(f"Processed {input_file} and saved results to {output_file}")

# Example usage
input_file = "test.xhtml"
output_file = "output.xhtml"

# Process the XHTML file
process_xhtml_file(input_file, output_file)

print("XHTML file processed.")