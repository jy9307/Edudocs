# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

#-----------------------------------------------------규정

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap = 200,
#     keep_separator = True,
#     separators=[r"\n제"],  # 정규표현식 포함
#     is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
# )


# loaders = [
#     # 파일을 로드합니다.
#     TextLoader("교육공무원법.txt"),
#     TextLoader("복무규정.txt")
# ]

# docs = []  # 빈 리스트를 생성합니다.


# for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
#     docs.extend(
#         loader.load_and_split(text_splitter=splitter)
#     )  

# # 저장할 경로 지정
# DB_PATH = "./chroma_db"

# # 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
# persist_db = Chroma.from_documents(
#     docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="work_law"
# )


#-------------------------------------------------------초중등교육법

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 200,
    keep_separator = True,
    separators=[r"\n제"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


loaders = [
    # 파일을 로드합니다.
    TextLoader("초중등교육법.txt"),
]

docs = []  # 빈 리스트를 생성합니다.


for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )  

# 저장할 경로 지정
DB_PATH = "./chroma_db"

# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="edu_law"
)


#-------------------------------------------------------성취기준

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 1500,
#     chunk_overlap = 200,
#     # keep_separator = True,
#     # separators=[r"\n초등학교"],  # 정규표현식 포함
#     # is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
# )


# loaders = [
#     # 파일을 로드합니다.
#     TextLoader("./초등 성취기준.txt"),
# ]

# docs = []  # 빈 리스트를 생성합니다.
# for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
#     docs.extend(
#         loader.load_and_split(text_splitter=splitter)
#     ) 
#      # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.
# # 저장할 경로 지정
# DB_PATH = "./chroma_db"

# # 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
# persist_db = Chroma.from_documents(
#     docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="achievement_standard"
# )

#-------------------------------------------------------초중등 교육법
