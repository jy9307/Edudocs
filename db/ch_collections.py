from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# 저장할 경로 지정
DB_PATH = "./chroma_db"

# 디스크에서 문서를 로드합니다.
persist_db = Chroma(
    persist_directory=DB_PATH,
    embedding_function=OpenAIEmbeddings(),
    collection_name="preschool_trait",
)

persist_db.delete_collection()