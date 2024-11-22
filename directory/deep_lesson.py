from app.set_page import BasicInputBoxPageTemplate, MessageHandler, ChatCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from app.set_prompt import deep_lesson_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"deep_lesson") ],
)

as_examples = [
    {'input' : "소수의 나눗셈",
     'output' : """ 
     초등학교 5학년,6학년 수학 수와 연산 성취기준\n
[6수01-14] ‘(자연수 )(자연수 )’에서 나눗셈의 몫을 소수로 나타낼 수 있다.\n
[6수01-15] 소수의 나눗셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.
"""},
    {'input' : "사회 지리 ",
     'output' : """
초등학교 3학년,4학년 사회 지도로 _만나는 _우리_지역 성취기준\n
[4사05-01] 우리 지역을 표현한 다양한 종류의 지도를 찾아보고 , 지도의 요소를 이해한다 .\n
[4사05-02] 지도에서 우리 지역의 위치를 파악하고 , 우리 지역의 지리 정보를 탐색한다 .\n
\n
초등학교 5학년,6학년 사회 우리나라 국토 여행 성취기준\n
[6사01-01] 우리나라 산지, 하천, 해안 지형의 위치를 확인하고 지형의 분포 특징을 탐구한다.\n
[6사01-02] 독도의 지리적 특성과 독도에 대한 역사 기록을 바탕으로 영토로서 독도의 중요성을 이해한다.\n
\n
초등학교 5학년,6학년 사회 지구_대륙_그리고 _국가들 성취기준\n
[6사09-01] 세계를 표현하는 다양한 공간 자료의 특징을 이해하고 , 지구본과 세계지도에서 위치를 표현하는 방법을 익힌다.\n
[6사09-02] 세계 주요 대륙과 대양을 파악하고 , 우리나라 및 세계 여러 국가의 위치와 영토의 특징을 이해한다.
"""},
]


## prompt에 예시 첨부를 위한 변수 설정
as_example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

deep_lesson_prompt =  ChatPromptTemplate.from_messages([
    ("system", """"
     아래 내용을 바탕으로 context의 자료를참고하여 양식에 맞춘 지도안을 작성해주세요.\n"
     
    양식
    "교과: {subject}\n역량: {competency}\n성취기준: {achievement_standard}\n\n"
    "핵심 아이디어:\n지식, 이해:\n과정, 기능:\n가치, 태도:\n핵심어:\n핵심 문장:\n핵심 질문:\n"
     
    context : {context}
     """),
     ("human", "{input}")
])

page_template = BasicInputBoxPageTemplate(mh_instance=mh, llm=llm, page_name="deep_lesson")
page_template.set_title("깊이 있는 수업 지도안 생성 프로그램","🎓")
page_template.input_box(items = ['교과', '역량', '성취기준'])
page_template.generate_button(prompt_name=deep_lesson_prompt, 
                              variables = ["subject", "competency", "achievement_standard"],
                              input = "지도안 생성",
                              button_name= "검색")
