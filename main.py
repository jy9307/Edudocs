import streamlit as st
import requests
import firebase_admin
from firebase_admin import auth, credentials

# Firebase Admin SDK 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/your-service-account.json")
    firebase_admin.initialize_app(cred)

# Firebase Web App Configuration (반영된 설정 사용)
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyBG6tTmcHtpiUF4qF62nEkmfBnAuu8DtxA",
    "authDomain": "edudocs-d6ba7.firebaseapp.com",
    "clientId": "734856772791.apps.googleusercontent.com",  # 반드시 Firebase 콘솔에서 확인하세요.
    "redirectUri": "http://localhost:8501",  # Streamlit 앱이 실행되는 URL
}

# Streamlit Session State 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = None


# 로그인 함수
def login():
    # Google OAuth Login URL 생성
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code"
        f"&client_id={FIREBASE_CONFIG['clientId']}"
        f"&redirect_uri={FIREBASE_CONFIG['redirectUri']}"
        f"&scope=email profile"
    )
    st.markdown(f"[Log in with Google]({auth_url})")

    # OAuth Callback 처리
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        auth_code = query_params["code"][0]

        # Google Authorization Code를 Firebase ID Token으로 교환
        token_endpoint = "https://oauth2.googleapis.com/token"
        token_payload = {
            "code": auth_code,
            "client_id": FIREBASE_CONFIG["clientId"],
            "client_secret": "YOUR_CLIENT_SECRET",  # Firebase 콘솔에서 클라이언트 비밀 키 확인
            "redirect_uri": FIREBASE_CONFIG["redirectUri"],
            "grant_type": "authorization_code",
        }
        token_response = requests.post(token_endpoint, data=token_payload)
        token_data = token_response.json()

        try:
            id_token = token_data["id_token"]
            decoded_token = auth.verify_id_token(id_token)
            st.session_state.logged_in = True
            st.session_state.user_info = decoded_token
            st.experimental_set_query_params()  # Query Params 초기화
            st.rerun()
        except Exception as e:
            st.error("Authentication failed. Please try again.")
            st.error(str(e))


# 로그아웃 함수
def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.experimental_set_query_params()
        st.rerun()


# 페이지 정의
if not st.session_state.logged_in:
    account_page = st.Page(login, title="Log in", icon=":material/login:")
else:
    account_page = st.Page(logout, title="Log out", icon=":material/logout:")

help_page = st.Page("directory/settings/help.py", title = "도움말", icon=":material/help:", default=True)


### 법령 관련 endpoint
work_law = st.Page("directory/laws/work_law.py", title="복무규정", icon=":material/work:")
educational_laws = st.Page("directory/laws/education_law.py", title="초중등 교육법", icon=":material/work:")

### 교육과정 관련 endpoint
achievement_standard = st.Page("directory/curriculum/achievemet_standard.py", title="성취기준", icon=":material/school:")

### 에듀테크 관련 endpoint
edutech_lesson_plan = st.Page("directory/edutech_lesson_plan.py", title="에듀테크 지도안", icon=":material/school:")

### 학생부 작성 관련 endpoint
student_record = st.Page("directory/records/student_record.py", title="학생부 기재요령", icon=":material/article:")

### test
test = st.Page("directory/test.py", title="연습")

### 깊이있는수업 지도안 endpoint
deep_lesson = st.Page("directory/deep_lesson.py", title="깊이있는수업 지도안 생성기", icon=":material/article:")

### 
official_document = st.Page("directory/proro.py", title="공문작성", icon=":material/article:")

pg = st.navigation(
        {   "계정 관리" : [account_page,help_page, test],
            "법령 및 규정": [work_law, educational_laws, official_document],
            "교육과정" : [achievement_standard],
            "학생부" : [student_record],
            "깊이있는수업"  : [deep_lesson],
            "에듀테크" : [edutech_lesson_plan]
                    }
    )

pg.run()
