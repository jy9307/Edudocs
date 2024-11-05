<<<<<<< HEAD:directory/work_law.py
# -*- coding: utf-8 -*-

=======
>>>>>>> 56aa33443c53072e9b45b5d5dfb30a73da3029c3:directory/laws/work_law.py
from app.set_page import BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import wl_prompt
from app.set_documents import load_Document
from langchain_openai import ChatOpenAI
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import (
    StructuredQueryOutputParser,
    get_query_constructor_prompt,
)
from langchain.retrievers.self_query.milvus import MilvusTranslator
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()
vectorstore = load_Document().select_document("work_law")

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"work_law"),
    ],
)

<<<<<<< HEAD:directory/work_law.py
llm_selfquery = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
)


metadata_field_info = [
    AttributeInfo(
        name="article_name",
        description="""The name of article. 
        One of ['당직 및 비상근무', '인사위원회의 기능', '승진', '조교의 임용', '장학금 지급 및 의무복무', '근무시간 면제 시간의 사용', '근무시간 등', '선거 관련 사무 수행 공무원의 휴무', '복무 실태의 확인ㆍ점검', '교사의 자격', '당연퇴직', '연수기관 및 근무장소 외에서의 연수', '시간선택제공무원 등의 휴가에 관한 특례', '지방교육전문직원 인사위원회', '교육행정기관에 순회교사 배치', '겸직 허가', '지방공무원법과의 관계', '수석교사의 임용 등', '공가', '정치적 행위', '신체검사', '휴가기간 중의 토요일 또는 공휴일', '지방공무원법과의 관계', '보수결정의 원칙', '겸임근무', '대학 교원의 신규채용 등', '보고', '고위공직자의 공무 외 국외여행', '연가 사용의 권장', '기간제교원', '허가권자', '인사위원회의 설치', '근무혁신기본계획의 수립 등', '파견근무', '적용범위', '연가 일수', '대학의 장의 임용', '영리 업무의 금지', '부정행위자에 대한 조치', '겸직 금지', '연가의 저축', '근무시간 등의 변경', '특별휴가', '강임자의 우선승진임용 제한', '보고서 제출 및 등록', '연가계획 및 승인', '징계사유의 시효에 관한 특례', '사실상 노무에 종사하는 공무원', '허가권의 위임', '심사위원회의 설치', '지방교육공무원 인사위원회', '10일 이상 연속된 연가 사용의 보장', '결격 사유', '병가', '연수의 기회균등', '공립대학 교육공무원의 고충처리', '임용의 원칙', '징계위원회의 설치', '연수기관의 설치', '직위해제', '교원의 불체포특권', '현업 공무원 등의 근무시간과 근무일', '출장공무원', '양성평등을 위한 임용계획 수립', '연가 일수에서의 공제', '목적', '정의', '해직된 공무원의 근무', '대학의 장 후보자 추천을 위한 선거사무의 위탁', '목적', '교권의 존중과 신분보장', '비밀 엄수', '임용권의 위임 등', '시간외근무 및 공휴일 등 근무', '책임 완수', '장학관 등의 임용']""".encode('utf-8').decode('unicode_escape'),
        type='string'
    ),
    AttributeInfo(
        name = "law_title",
        description= "The title of the law in which this article is included.",
        type='string'
    ),
    AttributeInfo(
        name="link",
        description="The url link which is connected to the original law.",
        type='string'
    )]

prompt = get_query_constructor_prompt(
    "law about the work of public officer",  # 문서 내용 설명
    metadata_field_info,  # 메타데이터 필드 정보
)

# StructuredQueryOutputParser 를 생성
output_parser = StructuredQueryOutputParser.from_components()

# query_constructor chain 을 생성
query_constructor = prompt | llm_selfquery | output_parser

document_content_description = "law about the work of public officer"

# retriever = SelfQueryRetriever.from_llm(
#     llm_selfquery,
#     vectorstore,
#     document_content_description,
#     metadata_field_info,
#     verbose= True
# )

retriever = SelfQueryRetriever(
    query_constructor=query_constructor,  # 이전에 생성한 query_constructor chain 을 지정
    vectorstore=vectorstore,  # 벡터 저장소를 지정
    structured_query_translator=MilvusTranslator()  # 쿼리 변환기
)

=======
>>>>>>> 56aa33443c53072e9b45b5d5dfb30a73da3029c3:directory/laws/work_law.py
page_template = BasicChatbotPageTemplate(mh_instance=mh, 
                                         llm=llm, 
                                         page_name= "work_law")
page_template.set_title("복무규정","💼")

page_info = """본 페이지에서는 교육 공무원으로서 참고할 수 있는 다양한 법률 정보를 확인할 수 있습니다!

문장으로 검색할 수도 있습니다만, 명확한 검색 결과를 위해서는 키워드로 검색하는 것을 추천드립니다.

ex) "휴직 종류 종류와 기간", "특별휴가 종류와 기간", "징계와 처벌"

**본 검색 결과는 참고용일 뿐이므로, 확실한 정보를 원하신다면 함께 제공되는 법률 조항과 원문 링크를 함께 확인하시기 바랍니다!**
"""

page_template.set_chat_ui_with_retriever(wl_prompt,
                          page_info,
                          retriever=retriever,
                          )