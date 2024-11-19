import streamlit as st
from app.set_page import BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from app.set_documents import load_Document
from app.set_prompt import el_prompt
from app.set_page import BasicChatbotPageTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

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

edutech_lesson_prompt = ChatPromptTemplate.from_messages([
    ("system","""너는 에듀테크로 수업을 만드는 교사를 돕는 수업제작 assistant야.
     input의 주제에 맞게 examples의 다른 지도안을 참고하여 수업지도안을 만들어줘.
     성취기준은 achievement_standard을 참고해줘.
     수업에 활용할 에듀테크 는 edutech를 참고해줘.

     achievement_standard : {achievement_standard},
     edutech : {edutech_collection}
     
     examples : {examples} """),
    ("human", "{input}")
])


page_template = BasicChatbotPageTemplate()



st.title("에듀테크 지도안 작성기")
message = st.chat_input("찾고싶은 내용을 입력하세요")
if message :
    with st.chat_message("human") :
            st.markdown(message)

    chain = (
        {"input" : RunnablePassthrough(),
        "achievement_standard" : docs.select_document("achievement_standard").as_retriever(),
        "examples" : docs.select_document("edutech_lesson").as_retriever(),
        "edutech_collection" : docs.select_document("edutech_collection").as_retriever(),
        }
        | edutech_lesson_prompt 
        | llm
        | StrOutputParser()
    )

    with st.chat_message("ai"):
        chain.invoke(message)