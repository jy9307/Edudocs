import streamlit as st
from app.set_page import  BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
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

page_template = BasicChatbotPageTemplate(mh_instance=mh, llm=llm, page_name="official_document")
page_template.set_title("K-에듀파인 기안문 작성 도우미","🎓")
page_template.set_chat_ui(proro_prompt, 
                          "본 페이지에서는 주제에 따라 기안문의 예시를 받아볼 수 있습니다!")

