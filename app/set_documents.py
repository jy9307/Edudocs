from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from dotenv import load_dotenv
from langchain_community.vectorstores.milvus import Milvus
import os

load_dotenv()

class load_Document() :

    def __init__(self) -> None:
        return

    def select_document(self, page_name) :
        
        self.embedder = OpenAIEmbeddings()
        
        self.vectorstore = Milvus(
            embedding_function=self.embedder,
            collection_name=page_name,
            connection_args={"host": "3.39.234.177", "port": "19530"},
            )
        
        return self.vectorstore
    


