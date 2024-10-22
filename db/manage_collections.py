from pymilvus import connections, Collection

# Milvus 서버에 연결
connections.connect("default", host="localhost", port="19530")  # Milvus 서버의 host와 port에 맞게 수정

# 컬렉션 이름 지정
collection_name = "student_records"

# 컬렉션 불러오기
collection = Collection(collection_name)

# 컬렉션 로드 (메모리에 올리기)
collection.load()

# 컬렉션 데이터 조회 (전체 엔티티 불러오기)
# 'id', 'field1', 'field2' 등의 필드는 컬렉션에 저장된 필드 이름에 맞게 수정해야 함
results = collection.query(expr='', output_fields=["page", "text"], limit=100)

# 결과 출력
for result in results:
    print(result)