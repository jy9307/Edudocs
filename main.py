import streamlit as st
import requests
import streamlit as st
from streamlit_oauth import OAuth2Component
import json
import base64
import os


st.logo("resources/logo.png", size = 'large')

def logout() :
    del st.session_state["auth"]
    del st.session_state["token"]
    st.rerun()

# 페이지 정의

### 기본 페이지
home_page = st.Page("home.py", title = "홈", icon=":material/home:", default=True)

if "auth" not in st.session_state :
    account_page = st.Page("login.py", title="Log in", icon=":material/login:")
else:
    account_page = st.Page(logout, title="Log out", icon=":material/logout:")

help_page = st.Page("directory/settings/help.py", title = "도움말", icon=":material/help:")


### 게시판
review = st.Page("directory/board/review.py", title="사용후기", icon=":material/edit:")
request = st.Page("directory/board/request.py", title="기능요청", icon=":material/library_add:")

### 법령 및 규정
work_law = st.Page("directory/laws/work_law.py", title="복무규정", icon=":material/work:")
educational_laws = st.Page("directory/laws/education_law.py", title="초중등 교육법", icon=":material/work:")

### 교육과정
achievement_standard = st.Page("directory/curriculum/achievemet_standard.py", title="성취기준", icon=":material/school:")

### 나이스
extra_record = st.Page("directory/neis/extra_record.py", title="창체 누가기록 생성기", icon=":material/book:")
student_record = st.Page("directory/neis/student_record.py", title="학생부 기재요령", icon=":material/book:")
student_feature = st.Page("directory/neis/student_feature.py", title="행발 생성기", icon=":material/book:")
subject_record = st.Page("directory/neis/subject_record.py", title="과목 누가기록 생성기", icon=":material/book:")

### 행정지원
official_docs = st.Page("directory/desk_job/official_docs.py", title="공문 생성기", icon=":material/article:")
commend_docs = st.Page("directory/desk_job/commend_docs.py", title="공적조서 생성기", icon=":material/article:")

### 수업
deep_lesson = st.Page("directory/lesson/deep_lesson.py", title="깊이있는 수업 단원 설계", icon=":material/article:")
edutech_lesson = st.Page("directory/lesson/edutech_lesson.py", title="에듀테크 지도안", icon=":material/school:")


pg = st.navigation(
    
        {   "홈" : [home_page],
            "계정 관리" : [account_page,help_page],
            "게시판" : [review, request],
            "나이스" : [student_feature,subject_record, extra_record],
            "행정지원" : [official_docs, commend_docs],
            "법령 및 규정": [work_law, educational_laws],
            "교육과정" : [achievement_standard],
            "수업"  : [deep_lesson, edutech_lesson]
                    }
    )

pg.run()


with st.sidebar :
    if "auth" not in st.session_state:
        st.markdown("로그인해주세요!")
    else :
        user_id = st.session_state['auth']
        st.markdown(f"{user_id}님 환영합니다")
        # if st.session_state["auth"] != None :
        #     st.markdown(f"{st.session_state['auth']}님 환영합니다!")
        # else :
        #     st.markdown("오프라인 모드")
