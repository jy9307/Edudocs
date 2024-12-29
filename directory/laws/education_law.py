from app.set_page import BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import el_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"edu_law"),
    ],
)

page_template = BasicChatbotPageTemplate(mh, llm, "edu_law")
page_template.set_title("교육법","💼")
page_info = """
✔️**본 페이지는 현재 테스트 중인 페이지입니다.**

본 페이지에서는 초중등 교육법과 관련된 내용을 확인할 수 있습니다!

문장으로 검색할 수도 있습니다만, 명확한 검색 결과를 위해서는 키워드로 검색하는 것을 추천드립니다.


**본 검색 결과는 참고용일 뿐이므로, 확실한 정보를 원하신다면 함께 제공되는 법률 조항과 원문 링크를 함께 확인하시기 바랍니다!**
"""
page_template.set_chat_ui(el_prompt, 
                          page_info)