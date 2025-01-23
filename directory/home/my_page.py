import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# Firebase Admin SDK 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  # 서비스 계정 키 파일 경로
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 페이지 기본 설정
st.set_page_config(
    page_title="마이 페이지",
    page_icon="👤",
    layout="centered",
)

# 로그인 상태 확인
def main_page() :
    user_ref = db.collection("users").document(st.session_state["uid"])
    user_doc = user_ref.get()

    point_transactions = user_ref.collection('point').stream()

    total_points = 0
    for transaction in point_transactions:
        transaction_data = transaction.to_dict()
        points = transaction_data.get('points', 0)
        total_points += points

    if user_doc:
        user_data = user_doc.to_dict()
        st.title("내 정보")
        with st.container(border=True):
            st.write(f"**아이디:** {user_data.get('username')}")
            st.write(f"**이름:** {user_data.get('name')}")
            st.write(f"**이메일:** {user_data.get('email')}")
            st.write(f"**잔여 포인트:** {total_points}")
            signup_date = user_data.get('signup_date')
            if isinstance(signup_date, datetime):
                signup_date = signup_date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                st.write(f"**가입일:** {signup_date}")
            else:
                st.write(f"**가입일:** {signup_date}")

            # Navigation Buttons
            if st.button("🔍 내가 생성한 답변들"):
                st.session_state.my_page = "search_history"
                st.rerun()
            if st.button("💰 포인트 사용 이력"):
                st.session_state.my_page = "point_history"
                st.rerun()
    else:
        st.error("사용자 정보를 불러올 수 없습니다.")

def point_history_page():

    # Get the user document reference
    user_ref = db.collection("users").document(st.session_state["uid"])
    
    # Retrieve all documents in the 'point' subcollection, ordered by date descending
    point_transactions = user_ref.collection('point').order_by('date', direction=firestore.Query.DESCENDING).stream()

    # Prepare data for DataFrame
    point_history = []
    for transaction in point_transactions:
        transaction_data = transaction.to_dict()
        date = transaction_data.get('date')
        # Convert Firestore Timestamp to datetime if necessary
        if isinstance(date, firestore.firestore.SERVER_TIMESTAMP.__class__):
            date = date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date = str(date)  # Convert to string if it's neither Timestamp nor datetime
        points = transaction_data.get('points')
        description = transaction_data.get('description')
        point_history.append({
            '날짜': date,
            '포인트': points,
            '세부내용': description
        })
    
    if point_history:
        # Create DataFrame
    
        point_df = pd.DataFrame(point_history)
        st.title("💰 포인트 사용 이력 확인하기")
        st.table(point_df)
    else:
        st.title("💰 포인트 사용 이력 확인하기")
        st.write("포인트 사용 내역이 없습니다.")

    # Back Button
    if st.button("메인 페이지로 돌아가기"):
        st.session_state.my_page = "main"
        st.rerun()

def search_history_page():
    st.title("🔍 검색 이력 확인하기")

    # Get the user document reference
    user_ref = db.collection("users").document(st.session_state["uid"])

    # Retrieve all documents in the 'results' subcollection, ordered by date descending
    results = user_ref.collection('result').order_by('date', direction=firestore.Query.DESCENDING).stream()

    search_history = []
    for result_doc in results:
        result_data = result_doc.to_dict()
        date = result_data.get('date')
        # Convert Firestore Timestamp to datetime if necessary
        if isinstance(date, firestore.firestore.SERVER_TIMESTAMP.__class__):
            date = date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date = str(date)
        service_name = result_data.get('service_name', 'N/A')
        point_used = result_data.get('point_used')
        result_text = result_data.get('result', 'N/A')

        search_history.append({
            'date': date,
            'service_name': service_name,
            'point_used': point_used,
            'result': result_text
        })

    if search_history:
        st.write("최근 검색 내역입니다:")
        for history in search_history:
            with st.container(border=True):
                st.markdown(f"""
                **날짜:** {history.get('date')}  
                **서비스 이름:** {history.get('service_name')}  
                **사용 포인트:** {history.get('point_used')}  
                **생성 결과:** 
                """)
                st.write(f"""
                {history.get('result')}
""")
    else:
        st.write("검색 내역이 없습니다.")

    # Back Button
    if st.button("메인 페이지로 돌아가기"):
        st.session_state.my_page = "main"
        st.rerun()


# Initialize session state
if "my_page" not in st.session_state :
    st.session_state.my_page = "main"

# Page routing
if st.session_state.my_page == "main":
    main_page()
elif st.session_state.my_page == "search_history":
    search_history_page()
elif st.session_state.my_page == "point_history":
    point_history_page()