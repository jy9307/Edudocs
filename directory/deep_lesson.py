from app.set_page import BasicInputBoxPageTemplate, MessageHandler, ChatCallbackHandler
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

page_template = BasicInputBoxPageTemplate(mh_instance=mh, llm=llm, page_name="deep_lesson")
page_template.set_title("깊이 있는 수업 지도안 생성 프로그램","🎓")
page_template.input_box(['교과', '역량', '성취기준'])
page_template.generate_button(prompt_name=deep_lesson_prompt, 
                              variables = ["subject", "competency", "achievement_standard"],
                              button_name= "검색")