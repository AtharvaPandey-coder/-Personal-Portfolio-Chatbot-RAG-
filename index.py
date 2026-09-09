import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

loader=TextLoader('context.txt',encoding='utf-8')
docs=loader.load()

splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,chunk_overlap=50
)

chunks=splitter.split_documents(docs)
embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vector_store=FAISS.from_documents(chunks,embeddings)

vector_store.save_local('faiss_index')
print(f"Index built successfully")






