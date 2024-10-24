from app.set_page import BasicInputBoxPageTemplate, MessageHandler, ChatCallbackHandler
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"test"),
    ],
)

page_template = BasicInputBoxPageTemplate(mh_instance=mh, llm=llm, page_name="test")
page_template.set_title("성취기준 검색기","🎓")
page_template.input_box(['학년', '과목', '영역'])
page_template.run_button('검색')