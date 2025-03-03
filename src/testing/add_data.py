import os
import sys
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

from langchain.prompts import PromptTemplate
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load environment variables
load_dotenv()
chromadb_path = os.getenv("CHROMADB_PATH")


if chromadb_path is None:
    print("CHROMADB_PATH is not set")
    sys.exit(1)

# Step 1: Initialize the Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 2: Initialize ChromaDB and Add Documents
vectorstore = Chroma(persist_directory=chromadb_path, embedding_function=embedding_model)

# Ensure we add documents if none exist
documents = [
    "Machine learning is a field of artificial intelligence.",
    "Deep learning uses neural networks for training large models.",
    "Vector databases are useful for similarity search.",
    "ChromaDB is a lightweight vector database for AI applications.",
    "Sentence transformers generate semantic embeddings."
]

# Check if the collection already contains embeddings
if len(vectorstore.get()["documents"]) == 0:
    vectorstore.add_texts(documents)
    print("✅ Added documents to ChromaDB.")

# Step 3: Define a Retrieval-Augmented Generation (RAG) Chain
model_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load model correctly
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"  # Automatically assigns to GPU (if available)
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100, device=device)
llm = HuggingFacePipeline(pipeline=pipe)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Fetch top 3 relevant documents

# Step 4: Define a Custom Prompt Template for RAG
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="You are a helpful AI assistant. Given the following information:\n\n{context}\n\nAnswer the question: {question}"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template}
)

# Step 5: Query the RAG System
query = "What is deep learning?"
response = qa_chain.invoke(query)

# Step 6: Output Response
print("🤖 LLM Response:")
print(response)
