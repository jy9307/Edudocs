import streamlit as st
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv
import os, base64, json, re
from firebase_admin import auth, firestore
from datetime import datetime, timezone
import bcrypt

load_dotenv()

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

WEB_API_KEY = 'AIzaSyBG6tTmcHtpiUF4qF62nEkmfBnAuu8DtxA'  # Firebase 프로젝트의 웹 API 키로 변경

# Check if we're on the signup_add page
if "page" in st.session_state and st.session_state.page == "signup_add":
    st.title("회원가입")

    with st.container(border=True):
        st.write("회원가입을 완료하기 위해 아래 추가 정보를 입력해주세요.")
        st.write(f"###### 이메일: {st.session_state.get('email')}")
        password = st.text_input("비밀번호", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")

        if st.button("제출"):
            if password != password_confirm:
                st.error("비밀번호가 일치하지 않습니다. 다시 확인해주세요.")
            else:
                # Hash the password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Update the user_data with additional information
                user_data = {
                    "email": st.session_state.get("email"),
                    "name": st.session_state.get("name"),
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
                st.session_state["auth"] =  st.session_state["email"].split("@")[0]
                st.session_state.page = "home"
                st.success("회원가입이 완료되었습니다!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if "page" in st.session_state and st.session_state.page == "signup":
    st.title("회원가입")

    with st.container(border=True):
        # 이메일 입력과 중복 확인 버튼을 나란히 배치
        col1, col2, col3 = st.columns(3, vertical_alignment="bottom")
        with col1:
            email = st.text_input("이메일", key="email")
        with col2:
            if st.button("중복 확인"):
                if email:
                    # 이메일 형식 검증
                    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                    if not re.match(email_pattern, email):
                        with col3:
                            st.error("이메일 형식이 올바르지 않습니다.")
                        st.session_state['email_duplicate'] = True  # 이메일 형식이 올바르지 않으면 중복으로 처리
                    else:
                        try:
                            # 이미 등록된 이메일인지 확인
                            auth.get_user_by_email(email)
                            st.session_state['email_duplicate'] = True
                            with col3:
                                st.error("이미 등록된 이메일입니다.")
                        except auth.UserNotFoundError:
                            st.session_state['email_duplicate'] = False
                            with col3:
                                st.success("사용 가능한 이메일입니다.")
                        except Exception as e:
                            st.error(f"오류가 발생했습니다: {e}")
                else:
                    st.warning("이메일을 입력해주세요.")

        # 이메일 중복 확인 여부를 세션 상태로 저장
        if 'email_duplicate' not in st.session_state:
            st.session_state['email_duplicate'] = None

        # 비밀번호 주의사항 표시
        st.write("비밀번호는 8자리 이상이어야 하며, 숫자, 영어, 특수문자를 포함해야 합니다.")

        password = st.text_input("비밀번호", type="password")
        password_confirm = st.text_input("비밀번호 확인", type="password")

        if st.button("가입하기"):
            if st.session_state['email_duplicate'] is None:
                st.warning("이메일 중복 확인을 해주세요.")
            elif st.session_state['email_duplicate']:
                st.error("이미 등록된 이메일이거나, 이메일 형식이 올바르지 않습니다.")
            elif password != password_confirm:
                st.error("비밀번호가 일치하지 않습니다.")
            else:
                # 비밀번호 강도 검증
                password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^\w\s]).{8,}$'
                if not re.match(password_pattern, password):
                    st.error("비밀번호는 8자리 이상이어야 하며, 숫자, 영어, 특수문자를 포함해야 합니다.")
                else:
                    try:
                        # 사용자 생성
                        firebase_user = auth.create_user(
                            email=email,
                            password=password
                        )
                        st.success("회원가입이 완료되었습니다.")
                        st.session_state.page = "login"
                        
                        # 가입 후 세션 상태 초기화
                        st.session_state['email_duplicate'] = None

                        # Hash the password
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                        # Update the user_data with additional information
                        user_data = {
                            "email": st.session_state.get("email"),
                            "name": st.session_state.get("name"),
                            "password": hashed_password,
                            "signup_date": datetime.now(timezone.utc)
                        }
                        # Save to Firestore
                        user_ref = db.collection("users").document(firebase_user.uid)
                        user_ref.set(user_data)

                        initial_point_data = {
                            "date": datetime.now(timezone.utc),
                            "points": 500,
                            "description": "회원가입 보너스"
                        }
                        user_ref.collection('point').add(initial_point_data)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")


elif "auth" not in st.session_state:
    st.image("resources/logo.png")

    # ID/PW 로그인 컨테이너
    with st.container(border=True):
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        email = st.text_input("이메일", key="login_username")
        password = st.text_input("비밀번호", type="password", key="login_password")
        col1, col2 = st.columns([0.1,0.7] ,gap='small')
        with col1 :
            if st.button("로그인", key="login_button"):
                # Fetch user data by username
                users_ref = db.collection("users")
                query = users_ref.where("email", "==", email).stream()
                existing_users = list(query)
                if existing_users:
                    user_doc = existing_users[0]
                    user_data = user_doc.to_dict()
                    stored_password = user_data.get("password")
                    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        st.session_state["auth"] = email
                        st.session_state["point"] = user_data.get('points', 0)
                        st.session_state["uid"] = user_doc.id 
                        st.session_state.page = "home"
                        st.success("로그인 성공!")
                        st.rerun()
                    else:
                        st.error("비밀번호가 일치하지 않습니다.")
                else:
                    st.error("존재하지 않는 아이디입니다.")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2 :
    
            if st.button("회원가입", key= "signup_button") :
                st.session_state.page = "signup"
                st.rerun()

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
                # Set session state variables and redirect to signup_add
                st.session_state.page = "signup_add"
                st.session_state["email"] = email
                st.session_state["name"] = name
                st.session_state["uid"] = firebase_user.uid
                st.rerun()
