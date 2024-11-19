from pymilvus import connections, Collection, utility
from langchain_community.vectorstores.milvus import Milvus 
from langchain_milvus.retrievers import MilvusCollectionHybridSearchRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_milvus.utils.sparse import BM25SparseEmbedding
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from dotenv import load_dotenv

# Milvus 서버에 연결
connections.connect("default", host="3.38.106.139", port="19530")  # Milvus 서버의 host와 port에 맞게 수정

collection_name = "work_law"

# 컬렉션 불러오기
collection = Collection(collection_name)

vectorstore = Milvus(
    embedding_function=OpenAIEmbeddings(),
    collection_name=collection_name,
    connection_args={"host": "3.38.106.139", "port": "19530"},
    )

bm25_embedding = BM25SparseEmbedding(['Context : The segment primarily discusses the legal framework surrounding political activities as defined in Article 27 of a specific law. It outlines the types of actions considered political acts, including organizing or supporting political parties, campaigning for or against candidates in elections, and participating in protests. Additionally, it specifies the limitations on these political activities, detailing various forms of participation, such as publishing political materials, expressing support or opposition in public gatherings, and using symbols associated with political parties. The article emphasizes the legal boundaries and responsibilities related to engaging in political actions. \n \n제27조(정치적 행위) ① 법 제65조의 정치적 행위는 다음 각 호의 어느 하나에 해당하는 정치적 목적을 가진 것\n을 말한다.\n 1. 정당의 조직, 조직의 확장, 그 밖에 그 목적 달성을 위한 것\n2. 특정 정당 또는 정치단체를 지지하거나 반대하는 것\n3. 법률에 따른 공직선거에서 특정 후보자를 당선하게 하거나 낙선하게 하기 위한 것\n② 제1항에 규정된 정치적 행위의 한계는 제1항에 따른 정치적 목적을 가지고 다음 각 호의 어느 하나에 해당\n하는 행위를 하는 것을 말한다.\n 1. 시위운동을 기획ㆍ조직ㆍ지휘하거나 이에 참가하거나 원조하는 행위\n2. 정당이나 그 밖의 정치단체의 기관지인 신문과 간행물을 발행ㆍ편집ㆍ배부하거나 이와 같은 행위를 원조하\n거나 방해하는 행위\n3. 특정 정당 또는 정치단체를 지지 또는 반대하거나 공직선거에서 특정 후보자를 지지 또는 반대하는 의견을\n집회나 그 밖에 여럿이 모인 장소에서 발표하거나 문서ㆍ도서ㆍ신문 또는 그 밖의 간행물에 싣는 행위\n4. 정당이나 그 밖의 정치단체의 표지로 사용되는 기(旗)ㆍ완장ㆍ복식 등을 제작ㆍ배부ㆍ착용하거나 착용을 권\n유 또는 방해하는 행위\n5. 그 밖에 어떠한 명목으로든 금전이나 물질로 특정 정당 또는 정치단체를 지지하거나 반대하는 행위\n[전문개정 2011. 7. 4.]'])

retriever = MilvusCollectionHybridSearchRetriever(vectorstore, bm25_embedding)

results = retriever.invoke("휴직")
print(results)

# # 컬렉션 데이터 조회 (전체 엔티티 불러오기)
# # 'id', 'field1', 'field2' 등의 필드는 컬렉션에 저장된 필드 이름에 맞게 수정해야 함
# results = collection.query(expr='', output_fields=["page_content"], limit=100)

# # 결과 출력
# for result in results:
#     print(result)