import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 초기 세션 상태 설정
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

# 텍스트 입력 받기
text = st.text_input("여기에 텍스트를 입력하세요", value=st.session_state.original_text)

# "문장 이어서 쓰기" 버튼 동작
if st.button("문장 이어서 쓰기") :
    generate_prompt =  ChatPromptTemplate.from_messages([
        ("system","""지금까지 작성된 글을 읽고, 글의 내용을 자연스럽게 이어서 한 문장을 작성해봐.
        """),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini'
    )

    chain = (generate_prompt|llm|StrOutputParser())

    result = chain.invoke({
        "input" : text        
    })

    # 결과를 세션 상태에 저장
    st.session_state.generated_text = result
    st.success("문장이 추가되었습니다!")

# "직전 문장으로 돌아가기" 버튼 동작
if st.button("직전 문장으로 돌아가기"):
    st.session_state.generated_text = st.session_state.original_text  # 원래 텍스트로 복원
    st.success("직전 상태로 되돌아갔습니다!")

# 결과 출력
st.text_area("결과", value=st.session_state.generated_text, height=200)

# "복사하기" 버튼 동작
if st.button("복사하기"):
    # Streamlit에서는 브라우저 클립보드 직접 접근이 어려워 사용자가 텍스트를 복사하도록 알림 표시
    st.text_area("복사할 텍스트", value=st.session_state.generated_text, height=200)
    st.success("완성된 텍스트가 복사 영역에 표시되었습니다. 복사하려면 Ctrl+C를 사용하세요.")

# "글쓰기 모음집" 버튼 동작
if st.button("글쓰기 모음집"):
    padlet_url = "https://padlet.com/sres5002/8-23-dp6gx9cp2tuln5tn"
    st.markdown(f"""
    <script>
    window.open("{padlet_url}", "_blank");
    </script>
    """, unsafe_allow_html=True)
    st.success("Padlet 사이트로 이동합니다!")