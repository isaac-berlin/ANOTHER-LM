import os
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CHROMADB_PATH = os.getenv("CHROMADB_PATH", "./chroma_db")

# Initialize FastAPI
app = FastAPI(title="RAG API", description="A Retrieval-Augmented Generation API", version="1.0")

# Initialize Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=CHROMADB_PATH, embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Load LLM Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_id = "mistralai/Mistral-7B-Instruct-v0.2"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.float16, device_map="auto"
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=250, return_full_text=False)
llm = HuggingFacePipeline(pipeline=pipe)

# Define RAG Chain
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an AI assistant with access to retrieved knowledge. Below is some context:
    {context}

    Using this information, answer the following question in a clear and concise manner:
    {question}

    If the context does not provide enough information, state that explicitly.
    """
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, chain_type="stuff", chain_type_kwargs={"prompt": prompt_template}
)

# API Request Model
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Welcome to the RAG API. Use /query to ask a question."}

@app.post("/query")
def query_rag(request: QueryRequest):
    response = qa_chain.invoke(request.question)
    return {"question": request.question, "response": response}

# Run the server: `uvicorn rag_api:app --host 0.0.0.0 --port 8000 --reload`
