# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# 저장할 경로 지정
DB_PATH = "./chroma_db"

#-----------------------------------------------------규정

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 200,
    keep_separator = True,
    separators=[r"\n제"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


loaders = [
    # 파일을 로드합니다.
    TextLoader("work_laws.txt"),
    TextLoader("work_laws_for_educator.txt")
]

docs = []  # 빈 리스트를 생성합니다.


for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )  

# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="work_law"
)


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

# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="edu_law"
)


#-------------------------------------------------------성취기준

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 200,
    # keep_separator = True,
    # separators=[r"\n초등학교"],  # 정규표현식 포함
    # is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


loaders = [
    # 파일을 로드합니다.
    TextLoader("./초등 성취기준.txt"),
]

docs = []  # 빈 리스트를 생성합니다.
for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    ) 

# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="achievement_standard"
)

#-------------------------------------------------------공문

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    keep_separator = True,
    separators=["기안문"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


loaders = [
    # 파일을 로드합니다.
    TextLoader("./official_document.txt"),
]

docs = []  # 빈 리스트를 생성합니다.
for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )
     # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.


# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="official_document"
)

####--------- Upload edutech

loaders = [
    TextLoader("./에듀테크 수업 설계안.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 200,
    keep_separator = True,
    separators=[r"\n\(\d+\)"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="edutech_lesson"
)


loaders = [
    TextLoader("./에듀테크 종류.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 200,
    keep_separator = True,
    separators=[r"\n\(\d+\)"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="edutech_collection"
)

####--------- Upload 깊이있는 수업

loaders = [
    TextLoader("./깊이있는 수업 단원 설계 예시 자료.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 200,
    keep_separator = True,
    separators=[r"\n\(\d+\)"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="deep_lesson"
)

####--------- Upload 행발예시

loaders = [
    TextLoader("행발예시.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 0,
    keep_separator = True,
    separators=[r"\d+"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

for d in docs:
    lines = d.page_content.splitlines()
    d.metadata['영역'] = lines[1].split(":")[1].strip()
    d.metadata['수준'] = lines[2].split(":")[1].strip()
    print(d)

persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="student_feature"
)

####--------- Upload 과목 누가기록

loaders = [
    TextLoader("과목별 누가기록.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 0,
    keep_separator = True,
    separators=["-"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

for d in docs:
    lines = d.page_content.splitlines()
    d.metadata['과목'] = lines[0].split(" ")[1]
    print(d)

persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="subject_record"
)

####--------- Upload 창체 누가기록

loaders = [
    TextLoader("창체(자율)누가기록.txt"),
    TextLoader("동아리(자율)누가기록.txt"),
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 0,
    keep_separator = True,
    separators=["-"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

for d in docs:
    lines = d.page_content.splitlines()
    d.metadata['영역'] = lines[0].split("-")[1].strip()
    if d.metadata['source'] == '동아리(자율)누가기록.txt' :
        d.metadata['종류'] = '동아리'

    else : 
        d.metadata['종류'] = '자율'

persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="extra_record"
)