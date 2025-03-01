# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
import re

# API 키 정보 로드
load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# 저장할 경로 지정
DB_PATH = "./chroma_db"

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
    TextLoader("txt/work_laws_for_educator.txt"),
    TextLoader("txt/laws_for education.txt")
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
        d.metadata['clause_title'] = title
        d.metadata['clause_number'] = number
        d.metadata['link'] = 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B5%AD%EA%B0%80%EA%B3%B5%EB%AC%B4%EC%9B%90%EB%B3%B5%EB%AC%B4%EA%B7%9C%EC%A0%95/'

    elif d.metadata["source"] == "txt/work_laws_for_educator.txt" :
        d.metadata['law_title'] = '교육공무원법'
        d.metadata['clause_title'] = title
        d.metadata['clause_number'] = number
        d.metadata['link'] = 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B5%90%EC%9C%A1%EA%B3%B5%EB%AC%B4%EC%9B%90%EB%B2%95/'

    else :
        d.metadata['law_title'] = '초중등교육법'
        d.metadata['clause_title'] = title
        d.metadata['clause_number'] = number
        d.metadata['link'] = 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%B4%88%EC%A4%91%EB%93%B1%EA%B5%90%EC%9C%A1%EB%B2%95/'
    titles.append(title)

titles = list(set(titles))
print(titles)
print(len(titles))