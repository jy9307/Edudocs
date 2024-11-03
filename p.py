from app.set_page import  MessageHandler
from app.set_documents import load_Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.set_prompt import wl_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

vectorstore = load_Document().select_document('work_law')

prompt =  ChatPromptTemplate.from_messages([
    ("system", """다음 옵션들 중에 사용자의 메세지와 가장 연관되어있다고 생각하는 키워드를 찾아서 반환해줘.
     
     '당직 및 비상근무', '인사위원회의 기능', '승진', '조교의 임용', '장학금 지급 및 의무복무', '근무시간 면제 시간의 사용', '근무시간 등', '선거 관련 사무 수행 공무원의 휴무', '복무 실태의 확인ㆍ점검', '교사의 자격', '당연퇴직', '연수기관 및 근무장소 외에서의 연수', '시간선택제공무원 등의 휴가에 관한 특례', '지방교육전문직원 인사위원회', '교육행정기관에 순회교사 배치', '겸직 허가', '지방공무원법과의 관계', '수석교사의 임용 등', '공가', '정치적 행위', '신체검사', '휴가기간 중의 토요일 또는 공휴일', '지방공무원법과의 관계', '보수결정의 원칙', '겸임근무', '대학 교원의 신규채용 등', '보고', '고위공직자의 공무 외 국외여행', '연가 사용의 권장', '기간제교원', '허가권자', '인사위원회의 설치', '근무혁신기본계획의 수립 등', '파견근무', '적용범위', '연가 일수', '대학의 장의 임용', '영리 업무의 금지', '부정행위자에 대한 조치', '겸직 금지', '연가의 저축', '근무시간 등의 변경', '특별휴가', '강임자의 우선승진임용 제한', '보고서 제출 및 등록', '연가계획 및 승인', '징계사유의 시효에 관한 특례', '사실상 노무에 종사하는 공무원', '허가권의 위임', '심사위원회의 설치', '지방교육공무원 인사위원회', '10일 이상 연속된 연가 사용의 보장', '결격 사유', '병가', '연수의 기회균등', '공립대학 교육공무원의 고충처리', '임용의 원칙', '징계위원회의 설치', '연수기관의 설치', '직위해제', '교원의 불체포특권', '현업 공무원 등의 근무시간과 근무일', '출장공무원', '양성평등을 위한 임용계획 수립', '연가 일수에서의 공제', '목적', '정의', '해직된 공무원의 근무', '대학의 장 후보자 추천을 위한 선거사무의 위탁', '목적', '교권의 존중과 신분보장', '비밀 엄수', '임용권의 위임 등', '시간외근무 및 공휴일 등 근무', '책임 완수', '장학관 등의 임용'
     """),
     ("human", "{input}")
])

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True
)

filter_chain = prompt | llm | StrOutputParser()

chain = (
    {"context" : vectorstore.as_retriever(search_kwargs = {'filter' : {'article_name' : '현업 공무원 등의 근무시간과 근무일'}}), 
     "input" : RunnablePassthrough()
     }
    | wl_prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("현업 공무원 등의 근무시간과 근무일")
print(result)


