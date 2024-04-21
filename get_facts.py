import os
import requests
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


custom_prompt_template = """
Your task is to extract facts from the call transcripts that are relevant to the below question.
The question is - {query}.

The order of conversation in transcript is important as it may introduce new facts, modify existing facts, or remove facts altogether. 
You must only present the final facts, eliminate any intermediate decisions.
Avoid including names of people or organizations.
Do not include any unneccesary content which is not asked in the question.
Do not respond with anything outside of the call transcript. If you don't know, say, "I don't know"

Example:
Chat 1: "We should use red on our landing page."
Chat 2: "We shouldn’t have a landing page."
Final list of facts:
Team decided not to have a landing page.

"""

template="""
Your task is to extract facts from the call transcripts that are relevant to the below question.
The question is - {query}.

The order of conversation in transcript is important as it may introduce new facts, modify existing facts, or remove facts altogether. 
You must only present the final facts, eliminate any intermediate decisions.
Avoid including names of people or organizations.
Do not include any unneccesary content which is not asked in the question.
Do not respond with anything outside of the call transcript. If you don't know, say, "I don't know"

Example:
Chat 1: "We should use red on our landing page."
Chat 2: "We shouldn’t have a landing page."
Final list of facts:
Team decided not to have a landing page.

Respond with the following format
{output_format}
"""

output_format = """
- Bullet point format
- Separate each bullet point with a new line
- Each bullet point should be concise
"""



# def process_txt_files(urls):
#     concatenated_content = ""
#     for url in urls:
#         response = requests.get(url.strip())
#         # print(response)
#         if response.status_code == 200:
#             content = response.text
#             concatenated_content += content
#             concatenated_content += "\n\n"
#     return concatenated_content

def process_txt_files(urls):
    concatenated_content = ""
    try:
        for url in urls:
            response = requests.get(url.strip())
            response.raise_for_status() 
            if response.status_code == 200:
                content = response.text
                concatenated_content += content
                concatenated_content += "\n\n"
    except requests.RequestException as e:
        print(f"Error accessing URL: {e}")
        return "Incorrect URL"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "Incorrect URL"
    return concatenated_content



def get_facts(question, documents):

    concatenated_content = process_txt_files(documents)

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=2000, chunk_overlap=500) #change chunk size
    texts = text_splitter.create_documents([concatenated_content])

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    system_message_prompt = SystemMessagePromptTemplate.from_template(custom_prompt_template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt_map = ChatPromptTemplate.from_messages(messages=[system_message_prompt, human_message_prompt])

    system_message_prompt_combine = SystemMessagePromptTemplate.from_template(template)
    human_template_combine="{text}"
    human_message_prompt_combine = HumanMessagePromptTemplate.from_template(human_template_combine)
    chat_prompt_combine = ChatPromptTemplate.from_messages(messages=[system_message_prompt_combine, human_message_prompt_combine])

    chain = load_summarize_chain(llm,
                             chain_type="map_reduce",
                             map_prompt=chat_prompt_map,
                             combine_prompt=chat_prompt_combine,
                             verbose=True)

    output = chain.run({
                        "input_documents": texts,
                        "query" : question,
                        "output_format" : output_format,
                    })

    facts_bulleted = output.split('\n')
    # facts_bulleted.pop(0)

    return facts_bulleted