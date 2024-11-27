import streamlit as st
from google.cloud import firestore
import os

# 서비스 계정 키 파일 경로 설정
key_path = 'firebase_key.json'

# 환경 변수로 GOOGLE_APPLICATION_CREDENTIALS 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

# Firestore 클라이언트 초기화
db = firestore.Client()

st.title("EDUDOCS 사용 후기")
st.write("사용후기를 남겨서 다른 선생님들께 공유해주세요!")

# 입력 폼 생성
with st.form("message_form"):
    if 'auth' in st.session_state :
        st.write(st.session_state['auth'])
        user_name = st.session_state['auth']
    else :
        user_name = st.text_input("아이디")
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
    # 사용자 이름을 작게 표시
    st.markdown(f"**{msg['name']}**", unsafe_allow_html=True)
    # 메시지를 박스 안에 넣어 정리된 형태로 표시
    st.info(msg['message'])
    # 메시지 구분선 추가
    st.markdown("<hr style='border:1px solid #ddd;'/>", unsafe_allow_html=True)
