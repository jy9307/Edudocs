import streamlit as st
from app.set_page import  MessageHandler, ChatCallbackHandler
from app.set_documents import load_Document
from app.set_prompt import commend_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from tools.db_manage import send_generate_result_to_firestore

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"commend_docs") ],
)

docs = load_Document().Chroma_select_document("commend_docs")

if "commend_docs_messages" not in st.session_state:
    st.session_state["commend_docs_messages"] = []

st.set_page_config(
    page_title="공적 조서 생성기",
    page_icon="📄",
    layout="wide"
)

st.title("공적 조서 생성기")

st.write("공적 조서에 적고 싶은 내용들을 쉼표로 구분하여 적어주세요.")

with st.container(border=True) :
    outcomes = st.text_input("""ex)  온라인 독서 프로그램 ‘리딩게이트’ 운영 , 원어민영어보조교사 협력 영어 늘봄교실 운영(3~6학년), 여름 방학 영어 캠프 운영""", "")

if st.button("공적조서 생성"):
    if outcomes != "" :

        st.markdown("### 생성된 공적 조서 : ")
        chain = (
        commend_prompt
        | llm
        | StrOutputParser()
        )


        with st.container(border=True) :
            chain.invoke({
            "input" : outcomes
        })
        if 'auth' in st.session_state :
            send_generate_result_to_firestore("공문 생성기", 10, result=st.session_state["commend_docs_messages"][-1]['message'])
    else :
        st.warning("활동을 먼저 적어주세요.")
