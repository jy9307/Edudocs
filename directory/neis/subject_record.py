import streamlit as st
from app.set_page import  MessageHandler, ChatCallbackHandler
from app.set_documents import load_Document
from app.set_prompt import subject_record_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"subject_record") ],
)

docs = load_Document().Chroma_select_document("subject_record")

st.title("과목 누가기록 생성기")

# 설명
st.markdown("##### 1. 과목을 고르세요.")

# 옵션 리스트
options = [
    "국어","수학","사회","과학","영어","음악","도덕","체육","미술","실과"
]

# 사용자가 선택한 옵션 저장
selection = st.pills("", options)

# 선택한 특성에 대해 각각 평가 (아쉬움/뛰어남)
if selection:
    st.markdown("##### 2. 과목의 어떤 영역 또는 활동에 대한 누가기록을 원하시나요? ")

    area = st.text_input("")


    if st.button("누가기록 생성!"):
        # 누가기록 예시 사전 로드 및 조합
        examples = docs.get(where={"과목" : selection})['documents'][0]

        st.markdown("### 생성된 누가기록 : ")
        chain = (
            subject_record_prompt
            |llm
            |StrOutputParser()
            )
        
        with st.container(border=True) :
            chain.invoke({
                "area" : area,
                "subject" : selection,
                "examples" : examples,
                })


