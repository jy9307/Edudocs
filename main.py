import streamlit as st
from firebase_admin import firestore
import streamlit as st
from streamlit_oauth import OAuth2Component


st.logo("resources/logo.png", size = 'large')

def logout() :
    del st.session_state["auth"]
    del st.session_state["token"]
    st.rerun()

# 페이지 정의
signup = st.Page("signup.py", title = "회원가입", icon=":material/home:", default=True)

### 기본 페이지
home_page = st.Page("directory/home/home.py", title = "홈", icon=":material/home:", default=True)
help_page = st.Page("directory/home/help.py", title = "도움말", icon=":material/help:")
my_page = st.Page("directory/home/my_page.py", title = "마이페이지", icon=":material/home:")

if "auth" not in st.session_state :
    account_page = st.Page("directory/home/login.py", title="Log in", icon=":material/login:")
    home = [home_page,account_page,help_page]
else:
    account_page = st.Page(logout, title="Log out", icon=":material/logout:")
    home = [home_page,account_page,my_page,help_page]

### 게시판
review = st.Page("directory/board/review.py", title="사용후기", icon=":material/edit:")
request = st.Page("directory/board/request.py", title="기능요청", icon=":material/library_add:")

boards = [review, request]

### 나이스
extra_record = st.Page("directory/neis/extra_record.py", title="창체 누가기록 생성기", icon=":material/book:")
student_record = st.Page("directory/neis/student_record.py", title="학생부 기재요령", icon=":material/book:")
student_feature = st.Page("directory/neis/student_feature.py", title="행발 생성기", icon=":material/book:")
subject_record = st.Page("directory/neis/subject_record.py", title="과목 누가기록 생성기", icon=":material/book:")

neis = [student_feature,subject_record, extra_record]

### 법령 및 규정
work_law = st.Page("directory/laws/work_law.py", title="복무규정", icon=":material/work:")
educational_laws = st.Page("directory/laws/education_law.py", title="초중등 교육법", icon=":material/work:")

laws = [work_law, educational_laws]

### 교육과정
achievement_standard = st.Page("directory/curriculum/achievemet_standard.py", title="성취기준", icon=":material/school:")

curriculum = [achievement_standard]

### 행정지원
official_docs = st.Page("directory/desk_job/official_docs.py", title="공문 생성기", icon=":material/article:")
commend_docs = st.Page("directory/desk_job/commend_docs.py", title="공적조서 생성기", icon=":material/article:")

desk_job = [official_docs, commend_docs]

### 수업
deep_lesson = st.Page("directory/lesson/deep_lesson.py", title="깊이있는 수업 단원 설계", icon=":material/article:")
edutech_lesson = st.Page("directory/lesson/edutech_lesson.py", title="에듀테크 지도안", icon=":material/school:")

lessons = [deep_lesson, edutech_lesson]


pg = st.navigation(
            {   
            "홈" : home,
            "게시판" : boards,
            "나이스" : neis,
            "행정지원" : desk_job,
            "법령 및 규정": laws,
            "교육과정" : curriculum,
            "수업"  : lessons 
            }
        )

pg.run()


with st.sidebar :
    if "auth" not in st.session_state:
        st.markdown("로그인해주세요!")
    else :
        db = firestore.client()

        user_ref = db.collection("users").document(st.session_state["uid"])
        user_doc = user_ref.get()

        point_transactions = user_ref.collection('point').stream()
        total_points = 0
        for transaction in point_transactions:
            transaction_data = transaction.to_dict()
            points = transaction_data.get('points', 0)
            total_points += points

        user_id = st.session_state['auth']
        st.markdown(f"{user_id} 선생님")
        st.markdown(f"잔여 포인트 : {total_points}")
