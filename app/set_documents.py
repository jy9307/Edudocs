from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores.milvus import Milvus

load_dotenv()

class load_Document() :

    def __init__(self) -> None:
        return

    def select_document(self, page_name) :
        
        self.embedder = OpenAIEmbeddings()
        
        self.vectorstore = Milvus(
            embedding_function=self.embedder,
            collection_name=page_name,
            connection_args={"uri": "http://localhost:19530"},
            )
        
        return self.vectorstore
    


