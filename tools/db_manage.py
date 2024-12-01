import streamlit as st
from firebase_admin import firestore
from datetime import datetime, timezone

# Firestore 클라이언트 가져오기
db = firestore.client()

# Firestore에 데이터 추가 함수
def send_data_to_firestore(collection_name, document_id, data, merge=True):
    try:
        # 컬렉션과 문서 참조
        doc_ref = db.collection(collection_name).document(document_id)
        
        # 데이터 추가
        doc_ref.set(data, merge=merge)
        print(f"Document '{document_id}' added to collection '{collection_name}'")
    except Exception as e:
        print(f"Error adding document: {e}")

def send_point_used_to_firestore(points,description) :
    user_ref = db.collection("users").document(st.session_state.get("uid"))
    point_used_data = {
        "date": datetime.now(timezone.utc),
        "points" : -points,
        "description": f"{description} 사용"
    }
    user_ref.collection('point').add(point_used_data)


def send_generate_result_to_firestore(service_name, points, result):
    user_ref = db.collection("users").document(st.session_state.get("uid"))
    generate_result_data = {
        "date": datetime.now(timezone.utc),
        "service_name": service_name,
        "point_used" : points,
        "result": result
    }
    user_ref.collection('result').add(generate_result_data)
    send_point_used_to_firestore(points, service_name)