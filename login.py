import streamlit as st
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv
import os, base64, json
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime, timezone

load_dotenv()

# Firebase Admin SDK 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  # 서비스 계정 키 파일 경로
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 페이지 기본 설정
st.set_page_config(
    page_title="로그인 페이지",
    page_icon="🔒",
    layout="centered",
)

# 로그인 UI
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown('<h2 class="login-title">로그인</h2>', unsafe_allow_html=True)


# OAuth2 설정
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
            print("상태:user_doc.exists")
            user_data = user_doc.to_dict()
            points = user_data.get("points", 0)
        else:
            print("상태 : user_doc.없음")
            # 사용자 초기 데이터 생성
            user_data = {
                "email": email,
                "name": name,
                "points": 0,
                "last_login": datetime.now(timezone.utc())
            }
            user_ref.set(user_data)
            points = 0

        st.session_state["auth"] = email.split("@")[0]
        st.session_state["token"] = result["token"]
        st.session_state["point"] = user_data['points']
        st.session_state["last_login"] = user_data['last_login']
        print("rerun전")
        st.rerun()
else:
    st.success("이미 로그인 상태입니다.")
    if st.button("Logout"):
        del st.session_state["auth"]
        del st.session_state["token"]
        st.rerun()
