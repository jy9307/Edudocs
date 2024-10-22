from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from dotenv import load_dotenv
from langchain_community.vectorstores.milvus import Milvus
import os

class load_Document() :

    def __init__(self) -> None:
        return

    def select_document(self, page_name) :
        
        self.embedder = OpenAIEmbeddings(api_key='sk-proj-p6i01xc1aEXcJuDQK4NrT3BlbkFJUECFk0uxAI7YoBtTAHvh')
        
        self.vectorstore = Milvus(
            embedding_function=self.embedder,
            collection_name=page_name,
            connection_args={"uri": "http://localhost:19530"},
            )
        
        return self.vectorstore
    


