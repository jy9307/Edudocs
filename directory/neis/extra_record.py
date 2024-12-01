import streamlit as st
from app.set_page import  MessageHandler, ChatCallbackHandler
from app.set_documents import load_Document
from app.set_prompt import extra_record_prompt, career_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from tools.db_manage import send_generate_result_to_firestore

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"extra_record") ],
)

docs = load_Document().Chroma_select_document("extra_record")

if "extra_record_messages" not in st.session_state:
    st.session_state["extra_record_messages"] = []

st.set_page_config(
    page_title="창체 누가기록 생성기",
    page_icon="📄",
    layout="wide"
)

st.title("창체 누가기록 생성기")

tab1, tab2, tab3 = st.tabs(["자율", "동아리", "진로"])

with tab1 :
    st.write("선택한 활동별로 각각 5개의 누가기록 예시가 생성됩니다.")

    with st.container(border=True) :
        # 설명
        st.markdown("##### 활동을 고르세요.")

        # 옵션 리스트
        options = [
            '여름 개학식', '학급 규칙 세우기', '여름방학 돌아보기', '사이버폭력 예방교육', '학급임원선거', '성폭력예방교육', '교통안전교육', '약물 및 사이버중독 예방교육', '직업 안전교육', '실종유괴 예방교육', '학급회의', '언어폭력예방주간활동', '찾아가는 에너지교실', '소방훈련', '학교폭력 예방교육', '재난안전교육', '생존수영교육', '장애이해교육'
        ]

        # 사용자가 선택한 옵션 저장
        selections = st.pills("원하는 활동을 모두 골라주세요.", options, selection_mode='multi')

        unregistered_area = st.text_input("""그 외에도 기술하고 싶은 활동이 있다면 적어주세요.""", "없음")

    if st.button("누가기록 생성!", key="자율"):
        if selections :

            examples = []
            for s in selections :
                examples.append(docs.get(where={"영역" : s})['documents'][0])

            area = ', '.join(selections)

            st.markdown("### 생성된 누가기록 : ")
            chain = (
            extra_record_prompt
            | llm
            | StrOutputParser()
            )


            with st.container(border=True) :
                chain.invoke({
                "area" : area,
                "u_area" : unregistered_area,
                "examples" : examples,
            })
            if 'auth' in st.session_state :
                send_generate_result_to_firestore("창체 누가기록",10, st.session_state["extra_record_messages"][-1]['message'])
        
        else :
            st.warning("과목과 세부 영역(활동)을 먼저 선택해주세요.")

with tab2 :
    st.write("선택한 동아리별로 각각 5개의 누가기록 예시가 생성됩니다.")

    with st.container(border=True) :
        # 설명
        st.markdown("##### 동아리를 고르세요.")

        # 옵션 리스트
        options = [
            '연극부', '그림부', '밴드부', '댄스부', '코딩부', '드론부', '방탈출게임제작부', '미니게임제작부', '쿠킹부'
        ]

        # 사용자가 선택한 옵션 저장
        selections = st.pills("원하는 동아리를 모두 골라주세요.", options, selection_mode='multi')

        unregistered_area = st.text_input("""그 외에도 동아리가 있다면 모두 적어주세요.""", "없음")

    if st.button("누가기록 생성!", key="동아리"):
        if selections :

            examples = []
            for s in selections :
                examples.append(docs.get(where={"영역" : s})['documents'][0])

            area = ', '.join(selections)

            st.markdown("### 생성된 누가기록 : ")
            chain = (
            extra_record_prompt
            | llm
            | StrOutputParser()
            )


            with st.container(border=True) :
                chain.invoke({
                "u_area" : unregistered_area,
                "area" : area,
                "examples" : examples,
            })
            if 'auth' in st.session_state :
                send_generate_result_to_firestore("창체 누가기록",10, st.session_state["extra_record_messages"][-1]['message'])
        else :
            st.warning("과목과 세부 영역(활동)을 먼저 선택해주세요.")

with tab3 :
    st.write("누가기록을 만들고 싶은 진로활동의 이름을 모두 적어주세요.")

    with st.container(border=True) :
        activities = st.text_input("""ex) 워크넷검사, mbti검사, 잡월드체험 """, "")

    if st.button("누가기록 생성!", key="진로"):
        if activities != "" :

            examples = []
            examples.append(docs.get(where={"종류" : "진로"})['documents'][0])
            area = ', '.join(selections)

            st.markdown("### 생성된 누가기록 : ")
            chain = (
            career_prompt
            | llm
            | StrOutputParser()
            )


            with st.container(border=True) :
                chain.invoke({
                "activities" : activities,
                "examples" : examples,
            })
            if 'auth' in st.session_state :
                send_generate_result_to_firestore("창체 누가기록",10, st.session_state["extra_record_messages"][-1]['message'])
        else :
            st.warning("활동을 먼저 적어주세요.")