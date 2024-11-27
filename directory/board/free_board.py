import streamlit as st
from google.cloud import firestore
import os

# 서비스 계정 키 파일 경로 설정
key_path = 'firebase_key.json'

# 환경 변수로 GOOGLE_APPLICATION_CREDENTIALS 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

# Firestore 클라이언트 초기화
db = firestore.Client()

st.title("Firestore를 사용하는 게시판")

# 입력 폼 생성
with st.form("message_form"):
    if 'auth' in st.session_state :
        st.write(st.session_state['auth'])
        user_name = st.session_state['auth']
    else :
        user_name = st.text_input("이름")
    message = st.text_area("메시지")
    submit = st.form_submit_button("등록")

    if submit:
        if user_name and message:
            # Firestore에 데이터 추가
            doc_ref = db.collection('messages').document()
            doc_ref.set({
                'name': user_name,
                'message': message
            })
            st.success("메시지가 등록되었습니다.")
            # 폼 초기화
            st.rerun()
        else:
            st.error("이름과 메시지를 모두 입력해주세요.")

st.divider()

# Firestore에서 데이터 가져오기
docs = db.collection('messages').stream()

for doc in docs:
    msg = doc.to_dict()
    st.subheader(f"{msg['name']}")
    st.write(f"{msg['message']}")
    st.write("---")
