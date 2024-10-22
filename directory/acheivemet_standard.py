from app.set_page import BasicEdudocsPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import as_prompt
from app.set_documents import load_Document
from langchain_openai import ChatOpenAI
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from dotenv import load_dotenv

load_dotenv()

metadata_field_info = [
    AttributeInfo(
        name="subject",
        description="""The subject of achievement standards. 
        One of [국어, 수학, 사회, 과학, 영어, 음악, 도덕, 실과, 체육, 미술]""",
        type='string'
    ),
    AttributeInfo(
        name="grade",
        description="""The grade to which achievement standards would be applied. 
        One of ['1학년,2학년', '3학년,4학년','5학년,6학년']""",
        type='string'
    ),
    AttributeInfo(
    name="area",
    description="""Area distinguish different parts of the subjects.""",
    type='string'
    ),
]

document_content_description = "Achievement standards of 2022 revised national curriculum"


mh = MessageHandler()
vectorstore = load_Document()


llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"achievement_standard"),
    ],
)

llm_selfquery = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
)


retriever = SelfQueryRetriever.from_llm(
    llm_selfquery,
    vectorstore.select_document("achievement_standard"),
    document_content_description,
    metadata_field_info,
    verbose= True
)


page_template = BasicEdudocsPageTemplate(mh, llm, "achievement_standard")
page_template.set_title("성취기준","🎓")

page_info = """본 페이지에서는 2022 개정 교육과정 성취기준을 확인할 수 있습니다. \n
성취기준 검색시에는 '과목'-'학년'-'원하는 키워드' 순으로 검색하면 좋습니다.\n
ex) 수학 3학년 분수"""

page_template.set_chat_ui_with_retriever(as_prompt,
                          page_info,
                          retriever=retriever,
                          search_type='hybrid'
                          )