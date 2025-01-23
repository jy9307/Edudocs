from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
# from langchain_community.vectorstores.milvus import Milvus
from langchain_chroma import Chroma

load_dotenv()

class load_Document() :

    def __init__(self) -> None:
        return

    # def select_document(self, page_name) :
        
    #     self.embedder = OpenAIEmbeddings()
        
    #     self.vectorstore = Milvus(
    #         embedding_function=self.embedder,
    #         collection_name=page_name,
    #         connection_args={"uri": "http://localhost:19530"},
    #         )
        
    #     return self.vectorstore
    
    def Chroma_select_document(self, page_name) :

        DB_PATH = "./db/chroma_db"

        self.vectorstore = Chroma(
            persist_directory=DB_PATH,
            embedding_function=OpenAIEmbeddings(),
            collection_name=page_name,
            )
        
        return self.vectorstore
    
    def Chroma_get_document(self, page_name) :

        DB_PATH = "./db/chroma_db"

        self.vectorstore = Chroma.get(
            persist_directory=DB_PATH,
            embedding_function=OpenAIEmbeddings(),
            collection_name=page_name,
            )
        
        return self.vectorstore


