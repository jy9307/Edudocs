import streamlit as st
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv
import os, base64, json
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime, timezone
import bcrypt

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

# OAuth2 설정
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

# Check if we're on the signup page
if "page" in st.session_state and st.session_state.page == "signup":
    st.title("회원가입")

    with st.container(border=True):
        st.markdown('<div class="signup-container">', unsafe_allow_html=True)
        st.write("회원가입을 완료하기 위해 아래 추가 정보를 입력해주세요.")
        st.write(f"###### 이메일: {st.session_state.get('email')}")
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")

        username_available = False
        if username:
            # Check if username already exists
            users_ref = db.collection("users")
            query = users_ref.where("username", "==", username).stream()
            existing_users = list(query)
            if existing_users:
                st.error("이미 사용 중인 아이디입니다. 다른 아이디를 선택해주세요.")
                username_available = False
            else:
                st.success("사용 가능한 아이디입니다.")
                username_available = True

        if st.button("제출"):
            if password != password_confirm:
                st.error("비밀번호가 일치하지 않습니다. 다시 확인해주세요.")
            elif not username:
                st.error("아이디를 입력해주세요.")
            elif not username_available:
                st.error("이미 사용 중인 아이디입니다. 다른 아이디를 선택해주세요.")
            else:
                # Hash the password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Update the user_data with additional information
                user_data = {
                    "email": st.session_state.get("email"),
                    "name": st.session_state.get("name"),
                    "username": username,
                    "password": hashed_password,
                    "signup_date": datetime.now(timezone.utc)
                }
                # Save to Firestore
                user_ref = db.collection("users").document(st.session_state.get("uid"))
                user_ref.set(user_data)

                initial_point_data = {
                    "date": datetime.now(timezone.utc),
                    "points": 500,
                    "description": "회원가입 보너스"
                }
                user_ref.collection('point').add(initial_point_data)

                # Update session state and redirect
                st.session_state["auth"] = username
                st.session_state.page = "home"
                st.success("회원가입이 완료되었습니다!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif "auth" not in st.session_state:
    st.image("resources/logo.png")

    # ID/PW 로그인 컨테이너
    with st.container(border=True):
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        username = st.text_input("아이디", key="login_username")
        password = st.text_input("비밀번호", type="password", key="login_password")

        if st.button("로그인", key="login_button"):
            # Fetch user data by username
            users_ref = db.collection("users")
            query = users_ref.where("username", "==", username).stream()
            existing_users = list(query)
            if existing_users:
                user_doc = existing_users[0]
                user_data = user_doc.to_dict()
                stored_password = user_data.get("password")
                if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    st.session_state["auth"] = username
                    st.session_state["point"] = user_data.get('points', 0)
                    st.session_state.page = "home"
                    st.success("로그인 성공!")
                    st.rerun()
                else:
                    st.error("비밀번호가 일치하지 않습니다.")
            else:
                st.error("존재하지 않는 아이디입니다.")
        st.markdown('</div>', unsafe_allow_html=True)

    # OAuth 로그인 컨테이너
    with st.container():
        # Create a button to start the OAuth2 flow
        oauth2 = OAuth2Component(
            CLIENT_ID, CLIENT_SECRET, AUTHORIZE_ENDPOINT, TOKEN_ENDPOINT, TOKEN_ENDPOINT, REVOKE_ENDPOINT
        )
        result = oauth2.authorize_button(
            name="Google로 계속하기",
            icon="https://www.google.com.tw/favicon.ico",
            redirect_uri="https://www.edudocs.site",  # Updated redirect_uri
            scope="openid email profile",
            key="google",
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=True,
            pkce='S256',
        )

        if result:
            # Decode the id_token JWT and get the user's email address
            id_token = result["token"]["id_token"]
            # Verify the signature is an optional step for security
            payload = id_token.split(".")[1]
            # Add padding to the payload if needed
            payload += "=" * (-len(payload) % 4)
            user_info = json.loads(base64.b64decode(payload))
            email = user_info["email"]
            name = user_info.get("name", "Unknown User")
            picture = user_info.get("picture")

            # Firebase 사용자 생성 또는 조회
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
                st.session_state.page = "home"
                st.session_state["auth"] = user_data.get("username", email.split("@")[0])
                st.session_state["token"] = result["token"]
                st.session_state["uid"] = firebase_user.uid
                st.rerun()
            else:
                # Set session state variables and redirect to signup
                st.session_state.page = "signup"
                st.session_state["email"] = email
                st.session_state["name"] = name
                st.session_state["uid"] = firebase_user.uid
                st.rerun()
else:
    st.switch_page("directory/home/home.py")
