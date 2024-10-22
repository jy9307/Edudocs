from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma



# 파일 경로 설정
loader = PyPDFLoader('복무규정.pdf')

text_splitter = RecursiveCharacterTextSplitter(
    # 청크 크기를 매우 작게 설정합니다. 예시를 위한 설정입니다.
    chunk_size=500,
    # 청크 간의 중복되는 문자 수를 설정합니다.
    chunk_overlap=50,
    # 문자열 길이를 계산하는 함수를 지정합니다.
    length_function=len,
    # 구분자로 정규식을 사용할지 여부를 설정합니다.
    is_separator_regex=False,
)

# OpenAI의 "text-embedding-3-large" 모델을 사용하여 임베딩을 생성합니다.
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", 
                              api_key="sk-proj-p6i01xc1aEXcJuDQK4NrT3BlbkFJUECFk0uxAI7YoBtTAHvh")

# PDF 로더 초기화
docs = loader.load_and_split(text_splitter=text_splitter)

db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings_model,
    collection_name="nlp",
)

retriever = db.as_retriever()
retriever.invoke("병에 걸렸을 떄")
