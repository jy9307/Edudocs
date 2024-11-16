from app.set_page import BasicInputBoxPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import proro_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"official_document") ],
)

page_template = BasicInputBoxPageTemplate(mh_instance=mh, llm=llm, page_name="official_document")
page_template.set_title("K-에듀파인 내부기안 자동작성 도우미","🎓")
page_template.input_box(['기안문 제목', '관련 근거 (예)한국초등학교-1736(2024.10.11)', '붙임 파일 제목'])
page_template.generate_button(prompt_name=proro_prompt, 
                              variables = ["text", "basis", "file"],
                              button_name= "검색")