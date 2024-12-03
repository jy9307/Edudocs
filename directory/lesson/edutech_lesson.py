import streamlit as st
from app.set_page import BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.set_documents import load_Document
from app.set_prompt import edutech_lesson_prompt
from app.set_page import BasicChatbotPageTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tools.db_manage import send_generate_result_to_firestore, send_stats_to_firestore

load_dotenv()

docs = load_Document()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"edutech_lesson_plan"),
    ],
)


page_template = BasicChatbotPageTemplate(mh_instance=mh,llm=llm, page_name="edutech_lesson_plan")
page_template.set_title("에듀테크 지도안 작성기","🎓")

page_info = """본 페이지에서는 2022 개정 교육과정 성취기준을 확인할 수 있습니다. \n
주제를 적으면 관련된 성취기준을 찾아드립니다!."""


message = st.chat_input("찾고싶은 내용을 입력하세요")
if message :
    with st.chat_message("human") :
            st.markdown(message)

    chain = (
        {"input" : RunnablePassthrough(),
        "achievement_standard" : docs.Chroma_select_document("achievement_standard").as_retriever(),
        "examples" : docs.Chroma_select_document("edutech_lesson").as_retriever(),
        "edutech_collection" : docs.Chroma_select_document("edutech_collection").as_retriever(),
        }
        | edutech_lesson_prompt 
        | llm
        | StrOutputParser()
    )


    with st.chat_message("ai"):
        chain.invoke(message)
        send_stats_to_firestore("deep_lesson")
        if 'auth' in st.session_state :
            send_generate_result_to_firestore("깊이있는 수업",0, st.session_state["deep_lesson_messages"][-1]['message'])