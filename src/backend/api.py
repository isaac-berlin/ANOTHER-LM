import os
import torch
import logging
import hashlib
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pathlib import Path
import shutil
import pymupdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
CHROMADB_PATH = os.getenv("CHROMADB_PATH", "./chroma_db")

# Initialize FastAPI
app = FastAPI(title="RAG API", description="A Retrieval-Augmented Generation API", version="1.0")

# Initialize Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=CHROMADB_PATH, embedding_function=embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Load LLM Model with Quantization
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_id = "mistralai/Mistral-7B-Instruct-v0.2"

quantization_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, return_full_text=False, pad_token_id=tokenizer.eos_token_id, max_new_tokens=512)
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
    llm=llm, retriever=retriever, chain_type="stuff", chain_type_kwargs={"prompt": prompt_template}, return_source_documents=True, 
)

# API Request Model
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Welcome to the RAG API. Use /query to ask a question or /upload to process a document."}

@app.post("/query")
def query_rag(request: QueryRequest):
    logger.info(f"Received query: {request.question}")
    response = qa_chain.invoke(request.question)
    
    answer = response["result"]
    sources = list(set(doc.metadata.get("source", "Unknown") for doc in response.get("source_documents", [])))
    
    logger.info(f"Generated response: {answer}")
    return {"question": request.question, "response": answer, "sources": sources}

# Function to extract text from a PDF file using pymupdf
def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = pymupdf.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# Function to chunk text before storing in vector database
def split_text(text: str, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def get_text_hash(text: str) -> str:
    """Generate a SHA256 hash of the document text to detect duplicates."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def store_document_text(text: str, file_name: str):
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in the document.")

    text_hash = get_text_hash(text)

    # Check if the document hash already exists in ChromaDB
    existing_docs = vectorstore.similarity_search(text, k=1)  # Check similar texts
    for doc in existing_docs:
        if doc.metadata.get("hash") == text_hash:
            raise HTTPException(status_code=400, detail="Duplicate document detected. Upload rejected.")

    # Chunk text and store it in vectorstore
    chunks = split_text(text)
    vectorstore.add_texts(chunks, metadatas=[{"source": file_name, "hash": text_hash}] * len(chunks))

    logger.info(f"Stored document: {file_name} with {len(chunks)} chunks and hash {text_hash}")
    return {"message": "Document processed successfully", "file": file_name}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a PDF or TXT file, extracts its content, chunks it, and stores it in the vector database.
    """
    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in ["pdf", "txt"]:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    
    save_path = Path(f"uploads/{file.filename}")
    os.makedirs("uploads", exist_ok=True)
    
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    logger.info(f"Uploaded file: {file.filename}")
    
    if file_extension == "pdf":
        extracted_text = extract_text_from_pdf(str(save_path))
    elif file_extension == "txt":
        with open(save_path, "r", encoding="utf-8", errors="replace") as f:
            extracted_text = f.read()
    
    return store_document_text(extracted_text, file.filename)
