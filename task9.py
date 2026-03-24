from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import google.generativeai as genai


from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

load_dotenv()
key=os.getenv("key")
genai.configure(api_key=key)

app=FastAPI(title="mental stress healthcare chatbot")
 
class query(BaseModel):
    question:str

@app.get('/')
def name():
    return {"welcome to mental stress chatbot":"hi ask anything"}

@app.post('/ask')
def ask_something(data:query):
    model = genai.GenerativeModel("gemini-3-flash-preview")
    response = model.generate_content(data.question)  
    return {
        "question": data.question,
        "response": response.text
    }

class SummarizeRequest(BaseModel):
    text:str

llm = ChatOllama(model="llama3:latest")  
summarize_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text in short:\n\n{text}"
)



@app.post("/summarize")
def summarize(req: SummarizeRequest):
    prompt = summarize_prompt.format(text=req.text)
    response =llm.invoke(prompt)

    return {
        "summary": response.content
    }




