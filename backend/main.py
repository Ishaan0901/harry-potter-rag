from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()


#   Model:
model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


#   Load the document:
book=PyPDFLoader('resources/harrypotter.pdf')
doc=book.load()



#   Chunking:
splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
chunks=splitter.split_documents(doc)



#   vectorStore:
store = Chroma.from_documents(
    documents=chunks,
    embedding=model,
    persist_directory="database/vectorStore"
)