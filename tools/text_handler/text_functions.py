from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, StuffDocumentsChain, create_extraction_chain
from doc_split import split_paragraph


def summarize(text):
    # Define prompt
    prompt_template = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
    docs = split_paragraph(text)
    print('stuff_chain:', stuff_chain.run(docs))


def extract_key_info(text, **kwargs):
    # Schema
    # schema = {
    #     "properties": {
    #         "title": {"type": "string"},
    #         "content_summary": {"type": "string"},
    #         # "example_code": {"type": "string", "default": ""},
    #     },
    #     "required": ["title", "content_summary"],
    # }
    schema = {'properties': kwargs, 'required': [k for k in kwargs]}

    # Run chain
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
    chain = create_extraction_chain(schema, llm)
    res = chain.run(text)
    return res
