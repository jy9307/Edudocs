from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

####----------Add metadata

def add_metadata(docs, key, value) :
    for i, d in enumerate(docs) :

        d.metadata[key] = value

####----------add metadata for achivement standards
def add_as_metadata(docs) :
    for i, d in enumerate(docs) :
        meta_splitter = d.page_content.split(" ")

        d.metadata['school'] = meta_splitter[0]
        d.metadata['grade'] = meta_splitter[1]
        d.metadata['subject'] = meta_splitter[2]
        d.metadata['area'] = meta_splitter[3]

def add_keyword_metadata(docs) :

    for i, d in enumerate(docs) :
        print(i)
        llm  = ChatOpenAI(
            model="gpt-4o-mini",
            temperature = 0
        )
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """Find keywords from the message. Show keywords seperated by space.
                1. Keywords MUST include the article number and the title of the article as keywords.                
                Article numbers should be formed as '제{{n}}조'
                
                2. Keywords inclue exceptional educational terms in the messages.
                
                """,
            ),
            ("human", "{doc}"),
        ])
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"doc" : d})

        d.metadata['keywords'] = list(result.split(" "))
 
        
####--------------Miluvs  Upload

def milvus_upload(collection_name, docs, drop_old=True) :
    embedder = OpenAIEmbeddings(model='text-embedding-3-small')

    vector_store = Milvus(
    embedding_function=embedder,
    collection_name=collection_name,
    connection_args={"host": "3.38.106.139", "port": "19530"},  # Separate host and port
    drop_old=drop_old,
)

    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs, 
                            ids=uuids,)
    

####--------- Upload achievement_standard

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap = 200,
#     keep_separator = True,
#     separators=[r"\n초등학교"],  # 정규표현식 포함
#     is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
# )


# loaders = [
#     # 파일을 로드합니다.
#     TextLoader("./초등 성취기준.txt"),
# ]

# docs = []  # 빈 리스트를 생성합니다.
# for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
#     docs.extend(
#         loader.load_and_split(text_splitter=splitter)
#     )  # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.

# add_as_metadata(docs)

# milvus_upload("achievement_standard",docs)

####--------- Upload work_law

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap = 200,
#     keep_separator = True,
#     separators=[r"\n제"],  # 정규표현식 포함
#     is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
# )


# loaders = [
#     # 파일을 로드합니다.
#     TextLoader("./복무규정.txt"),
# ]

# docs_1 = []  # 빈 리스트를 생성합니다.
# for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
#     docs_1.extend(
#         loader.load_and_split(text_splitter=splitter)
#     )  # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.


# add_metadata(docs_1, "link", "https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B5%AD%EA%B0%80%EA%B3%B5%EB%AC%B4%EC%9B%90%20%EB%B3%B5%EB%AC%B4%EA%B7%9C%EC%A0%95")
# add_metadata(docs_1, "law_title", "국가공무원 복무규정")

# loaders = [
#     # 파일을 로드합니다.
#     TextLoader("./교육공무원법.txt"),
# ]

# docs_2 = []  # 빈 리스트를 생성합니다.
# for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
#     docs_2.extend(
#         loader.load_and_split(text_splitter=splitter)
#     )  # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.


# add_metadata(docs_2, "link", "https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B5%90%EC%9C%A1%EA%B3%B5%EB%AC%B4%EC%9B%90%EB%B2%95")
# add_metadata(docs_2, "law_title", "교육공무원법")

# docs = docs_1+docs_2
# milvus_upload("work_law",docs)


loaders = [
    # 파일을 로드합니다.
    PyPDFLoader("./깊이있는수업.pdf"),
]

docs = []  # 빈 리스트를 생성합니다.
for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
    docs.extend(
        loader.load_and_split()
    )  # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.

milvus_upload("deep_lesson",docs)








