from app.set_page import BasicEdudocsPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import sr_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"student_record"),
    ],
)

page_template = BasicEdudocsPageTemplate(mh, llm, "student_record")
page_template.set_title("학생부 기재요령","📄")
page_template.set_chat_ui(sr_prompt, 
                          "학생부 기재요령을 확인할 수 있습니다!")