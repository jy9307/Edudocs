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


st.set_page_config(
    page_title="과목 누가기록 생성기",
    page_icon="📄",
    layout="wide"
)

st.title("과목 누가기록 생성기😆")

st.write("선택한 과목과 영역(활동)에 따라 총 20개의 누가기록 예시가 생성됩니다.")

with st.container(border=True) :

    # 설명
    st.markdown("##### 1. 과목을 고르세요.")

    # 옵션 리스트
    options = [
        "국어","수학","사회","과학","영어","음악","도덕","체육","미술","실과"
    ]

    # 사용자가 선택한 옵션 저장
    selection = st.pills("과목은 하나씩만 고를 수 있습니다.", options)

    # 선택한 특성에 대해 각각 평가 (아쉬움/뛰어남)
    if selection:
        st.markdown("##### 2. 과목의 어떤 영역 또는 활동에 대한 누가기록을 원하시나요? ")

        area = st.text_input("원하는 결과가 나오지 않을 경우, 구체적으로 내용을 적을수록 더 정확한 결과를 얻을 수 있습니다.")


if st.button("누가기록 생성!"):
    if selection :

        # 누가기록 예시 사전 로드 및 조합
        examples = docs.get(where={"과목" : selection})['documents'][0]

        st.markdown("### 생성된 누가기록 : ")
        chain = (
        subject_record_prompt
        | llm
        | StrOutputParser()
        )


        with st.container(border=True) :
            chain.invoke({
            "area" : area,
            "subject" : selection,
            "examples" : examples,
         })
    else :
        st.warning("과목과 세부 영역(활동)을 먼저 선택해주세요.")


