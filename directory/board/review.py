import streamlit as st
from google.cloud import firestore
import os
from datetime import datetime

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
    if 'auth' in st.session_state:
        st.write(st.session_state['auth'])
        user_name = st.session_state['auth']
    else:
        user_name = st.text_input("아이디")
    message = st.text_area("메시지")
    submit = st.form_submit_button("등록")

    if submit:
        if user_name and message:
            # Firestore에 데이터 추가
            doc_ref = db.collection('messages').document()
            doc_ref.set({
                'name': user_name,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'user_id': user_name  # 사용자 ID 저장
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
    doc_id = doc.id  # Firestore 문서 ID 가져오기

    # 두 개의 열 생성: 이름과 메시지, 시간
    col1, col2, col3, col4 = st.columns([1, 4, 2, 1])  # 비율: 이름(좁게), 메시지(넓게), 시간(좁게), 삭제 버튼
    with col1:
        st.markdown(f"**{msg['name']}**")  # 사용자 이름
    with col2:
        st.markdown(f"{msg['message']}")  # 메시지 내용
    with col3:
        # 시간 형식 변환 및 표시
        timestamp = msg.get('timestamp', None)
        if timestamp:
            time_display = datetime.datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M')
        else:
            time_display = "N/A"
        st.markdown(f"{time_display}")
    with col4:
        # 삭제 버튼: 사용자 ID와 세션 ID가 일치할 때만 표시
        if 'auth' in st.session_state and st.session_state['auth'] == msg['user_id']:
            if st.button("삭제", key=f"delete_{doc_id}"):
                # Firestore에서 해당 문서 삭제
                db.collection('messages').document(doc_id).delete()
                st.success("메시지가 삭제되었습니다.")
                st.rerun()  # UI 갱신