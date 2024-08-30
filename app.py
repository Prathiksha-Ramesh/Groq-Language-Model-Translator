from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes  #helps to create api

import os
from dotenv import load_dotenv
load_dotenv()

#loading the groq_api key:

groq_api_key=os.getenv('GROQ_API_KEY')

#initializing the groq-llm-model
model=ChatGroq(model='Gemma2-9b-It',groq_api_key=groq_api_key)



#prompt templates:

system_template='Translate the following into {language}:'
prompt=ChatPromptTemplate.from_messages(
    [('system',system_template),
     ('user',"{text}")]
)

#parser:
parser=StrOutputParser()

#creating the chain:
chain=prompt|model|parser

#app definition:

app=FastAPI(title='Langchain server',
            version='1.0',
            description='A simple API server using langchain runnable interfaces')

#adding the chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)