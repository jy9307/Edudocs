import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin SDK 초기화
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

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

# 예제 데이터
collection_name = "users"
document_id = "user123"
data = {
    "name": "Jay Lee",
    "email": "jaylee@example.com",
    "age": 30
}

# 데이터 전송
send_data_to_firestore(collection_name, document_id, data)
