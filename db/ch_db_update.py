# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
import re

from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

DB_PATH = "./chroma_db"

#-----------------------------------------------------규정

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 10,
    keep_separator = True,
    separators=[r"\n제\d+조"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


loaders = [
    # 파일을 로드합니다.
    TextLoader("txt/work_laws_for_officers.txt"),
    TextLoader("txt/work_laws_for_educator.txt")
]



docs = []  # 빈 리스트를 생성합니다.


for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )  

titles = []
for d in docs:

    lines = d.page_content.splitlines()

    matches = re.findall(r'\((.*?)\)', lines[1])
    title = matches[0] if matches else None

    number = lines[1].split("(")[0]
    titles.append(title)

    if d.metadata["source"] == "txt/work_laws_for_officers.txt" :
        d.metadata['law_title'] = '국가공무원 복무규정'
        d.metadata['cluase_title'] = title
        d.metadata['clause_number'] = number
        d.metadata['link'] = 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B5%AD%EA%B0%80%EA%B3%B5%EB%AC%B4%EC%9B%90%EB%B3%B5%EB%AC%B4%EA%B7%9C%EC%A0%95/'

    else :
        d.metadata['law_title'] = '교육공무원법'
        d.metadata['cluase_title'] = title
        d.metadata['clause_number'] = number
        d.metadata['link'] = 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B5%90%EC%9C%A1%EA%B3%B5%EB%AC%B4%EC%9B%90%EB%B2%95/'


# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="work_law"
)

#-------------------------------------------------------초중등교육법

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap = 200,
#     keep_separator = True,
#     separators=[r"\n제"],  # 정규표현식 포함
#     is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
# )


# loaders = [
#     # 파일을 로드합니다.
#     TextLoader("초중등교육법.txt"),
# ]

# docs = []  # 빈 리스트를 생성합니다.


# for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
#     docs.extend(
#         loader.load_and_split(text_splitter=splitter)
#     )  

# # 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
# persist_db = Chroma.from_documents(
#     docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="edu_law"
# )


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

# # 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
# persist_db = Chroma.from_documents(
#     docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="achievement_standard"
# )

#-------------------------------------------------------공문

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 0,
    keep_separator = True,
    separators=["범주"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


loaders = [
    # 파일을 로드합니다.
    
    TextLoader("txt/official_document.txt"),
]

docs = []  # 빈 리스트를 생성합니다.
for loader in loaders:  # loaders 리스트의 각 로더에 대해 반복합니다.
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )
     # 로더를 사용하여 문서를 로드하고 docs 리스트에 추가합니다.

cats = []
for d in docs :
    lines = d.page_content.splitlines()
    d.metadata['category'] = lines[0].split(":")[1].strip()
    cats.append(d.metadata['category'])

cats = list(set(cats))
print(cats)

# 문서를 디스크에 저장합니다. 저장시 persist_directory에 저장할 경로를 지정합니다.
persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="official_document"
)

####--------- Upload edutech

loaders = [
    TextLoader("txt/에듀테크 수업 설계안.txt")
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
    TextLoader("txt/에듀테크 종류.txt")
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
    TextLoader("txt/깊이있는 수업 단원 설계 예시 자료.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 200,
    keep_separator = True,
    separators=["단원명"],  # 정규표현식 포함
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
    TextLoader("txt/행발예시.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 0,
    keep_separator = True,
    separators=[r"영역"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

area = []
for d in docs:
    lines = d.page_content.splitlines()
    print("------------------")
    print(d)
    
    d.metadata['영역'] = lines[0].split(":")[1].strip()
    d.metadata['수준'] = lines[1].split(":")[1].strip()
    area.append(d.metadata['영역'])
area = set(area)

persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="student_feature"
)

####--------- Upload 과목 누가기록

loaders = [
    TextLoader("txt/과목별 누가기록.txt")
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



persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="subject_record"
)

####--------- Upload 창체 누가기록

loaders = [
    TextLoader("txt/창체(자율)누가기록.txt"),
    TextLoader("txt/동아리(자율)누가기록.txt"),
    TextLoader("txt/진로(자율)누가기록.txt")
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

clubs = []
selfs = []
for d in docs:
    lines = d.page_content.splitlines()
    if "-" in lines[0] : 
        d.metadata['영역'] = lines[0].split("-")[1].strip()
    if d.metadata['source'] == '동아리(자율)누가기록.txt' :
        d.metadata['종류'] = '동아리'
        clubs.append(d.metadata['영역'])

    elif d.metadata['source'] == '창체(자율)누가기록.txt' : 
        d.metadata['종류'] = '자율'
        selfs.append(d.metadata['영역'])

    else :
        d.metadata['종류'] = '진로'

persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="extra_record"
)

####--------- Upload 유치원 특성

loaders = [
    TextLoader("txt/preschool_trait_examples.txt")
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
    d.metadata['나이'] = lines[0].split(" ")[1]
    d.metadata['영역'] = lines[0].split(" ")[2]
    d.metadata['수준'] = lines[0].split(" ")[3]

persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="preschool_trait"
)

####--------- Upload 평가 계획

loaders = [
    TextLoader("txt/assessment_planning_examples.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 0,
    keep_separator = True,
    separators=["▶"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

for d in docs:
    lines = d.page_content.splitlines()
    d.metadata['과목'] = lines[1].split(":")[1].strip()
    d.metadata['성취기준'] = lines[5].split(":")[1].strip()
    # d.metadata['수업 방법'] = lines[8].split(":")[1].strip()
    # d.metadata['평가 방법'] = lines[11].split(":")[1].strip()



persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="assessment_planning"
)

####--------- Upload 가정통신문

loaders = [
    TextLoader("txt/parent_noti_examples.txt")
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,
    chunk_overlap = 0,
    keep_separator = True,
    separators=["- 예시"],  # 정규표현식 포함
    is_separator_regex=True,  # 정규표현식 사용 가능하도록 설정
)


docs =[]
for loader in loaders :
    docs.extend(
        loader.load_and_split(text_splitter=splitter)
    )

for d in docs:
    lines = d.page_content.splitlines()
    d.metadata['범주'] = lines[0].split("(")[1].replace(")","").strip()


persist_db = Chroma.from_documents(
    docs, OpenAIEmbeddings(), persist_directory=DB_PATH, collection_name="parent_notification"
)