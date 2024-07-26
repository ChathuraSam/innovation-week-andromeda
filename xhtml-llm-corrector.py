from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

# run >> pip install -r requirements.txt OR install manually the below libraries
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

    You are an expert in identifying meaningful words series from a series of characters.
    Given the xhtml span tags below, read it line by line and modify the text content of each span tag by breaking it down into a series of individual words without adding extra words to complete it as a sentence.
    
    XHTML spans to fix:
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
input_file = "output2.txt"
output_file = "response_from_llm.xhtml"

# Process the XHTML file
process_xhtml_file(input_file, output_file)

print("XHTML file processed.")