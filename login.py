import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import base64
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime, timezone

load_dotenv()

# Firestore 초기화
db = firestore.client()


# Firebase Admin SDK 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  # 서비스 계정 키 파일 경로
    firebase_admin.initialize_app(cred)

# 페이지 기본 설정
st.set_page_config(
    page_title="로그인 페이지",
    page_icon="🔒",
    layout="centered",
)

# 스타일 커스텀 CSS
st.markdown(
    """
    <style>
    .login-title {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: #333333;
    }
    .login-input {
        width: 100%;
        margin-bottom: 1rem;
    }
    .login-button {
        display: block;
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .login-button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 로그인 UI
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown('<h2 class="login-title">로그인</h2>', unsafe_allow_html=True)

with st.form("login_form"):
    username = st.text_input("사용자 이름", placeholder="사용자 이름을 입력하세요", key="username", help="로그인 ID를 입력하세요.")
    password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요", key="password")
    login_button = st.form_submit_button("로그인")

    if login_button:
        if username == "admin" and password == "1234":
            st.success(f"환영합니다, {username}!")
        else:
            st.error("사용자 이름 또는 비밀번호가 잘못되었습니다.")

st.markdown('</div>', unsafe_allow_html=True)

# create an OAuth2Component instance
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"


if "auth" not in st.session_state:
    # create a button to start the OAuth2 flow
    oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT)
    result = oauth2.authorize_button(
        name="Continue with Google",
        icon="https://www.google.com.tw/favicon.ico",
        redirect_uri="https://www.edudocs.site",
        scope="openid email profile",
        key="google",
        extras_params={"prompt": "consent", "access_type": "offline"},
        use_container_width=True,
        pkce='S256',
    )
    
    if result:
        # decode the id_token jwt and get the user's email address
        id_token = result["token"]["id_token"]
        # verify the signature is an optional step for security
        payload = id_token.split(".")[1]
        # add padding to the payload if needed
        payload += "=" * (-len(payload) % 4)
        user_info = json.loads(base64.b64decode(payload))
        email = user_info["email"]
        name = user_info.get("name", "Unknown User")
        picture = user_info.get("picture")

        #Firebase 사용자 생성 또는 조회
        try:
            firebase_user = auth.get_user_by_email(email)
        except auth.UserNotFoundError:
            firebase_user = auth.create_user(
                email=email,
                display_name=name,
                photo_url=picture,
            )

                # Firestore에서 사용자 정보 가져오기 또는 초기화
        user_ref = db.collection("users").document(firebase_user.uid)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            points = user_data.get("points", 0)
        else:
            # 사용자 초기 데이터 생성
            user_data = {
                "email": email,
                "name": name,
                "points": 0,
                "last_login": datetime.now(timezone.utc()),
            }
            user_ref.set(user_data)
            points = 0
        st.rerun()
else:
    if st.button("Logout"):
        del st.session_state["auth"]
        del st.session_state["token"]
