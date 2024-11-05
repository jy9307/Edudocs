from pymilvus import connections, Collection, utility 

# Milvus 서버에 연결
connections.connect("default", host="3.38.106.139", port="19530")  # Milvus 서버의 host와 port에 맞게 수정

collections = utility.list_collections() 
# 결과 출력 

print("컬렉션 목록:", collections)