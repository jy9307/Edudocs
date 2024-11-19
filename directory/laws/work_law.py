from app.set_page import BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import wl_prompt
from langchain_openai import ChatOpenAI
from app.set_documents import load_Document
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"work_law"),
    ],
)

page_template = BasicChatbotPageTemplate(mh_instance=mh, 
                                         llm=llm, 
                                         page_name= "work_law")
page_template.set_title("복무규정","💼")

page_info = """본 페이지에서는 교육 공무원으로서 참고할 수 있는 다양한 법률 정보를 확인할 수 있습니다!

문장으로 검색할 수도 있습니다만, 명확한 검색 결과를 위해서는 키워드로 검색하는 것을 추천드립니다.

ex) "휴직 종류 종류와 기간", "특별휴가 종류와 기간", "징계와 처벌"

**본 검색 결과는 참고용일 뿐이므로, 확실한 정보를 원하신다면 함께 제공되는 법률 조항과 원문 링크를 함께 확인하시기 바랍니다!**
"""

retriever = load_Document().select_document("work_law").as_retriever(search_type="mmr",search_kwargs={"k": 10})

page_template.set_chat_ui_with_retriever(wl_prompt,
                          page_info,
                          retriever

)