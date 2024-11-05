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
        ChatCallbackHandler(mh,"education_law"),
    ],
)

page_template = BasicChatbotPageTemplate(mh, llm, "education_law")
page_template.set_title("교육법","💼")
page_template.set_chat_ui(el_prompt, 
                          "본 페이지에서는 초중등 교육법을 확인할 수 있습니다!")