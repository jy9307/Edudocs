import streamlit as st
import requests
import streamlit as st
from streamlit_oauth import OAuth2Component
import json
import base64
import os


def logout() :
    del st.session_state["auth"]
    del st.session_state["token"]
    st.rerun()


# 페이지 정의
if "auth" not in st.session_state :
    account_page = st.Page("login.py", title="Log in", icon=":material/login:")
else:
    account_page = st.Page(logout, title="Log out", icon=":material/logout:")

help_page = st.Page("directory/settings/help.py", title = "도움말", icon=":material/help:", default=True)


### 법령 관련 endpoint
work_law = st.Page("directory/laws/work_law.py", title="복무규정", icon=":material/work:")
educational_laws = st.Page("directory/laws/education_law.py", title="초중등 교육법", icon=":material/work:")

### 교육과정 관련 endpoint
achievement_standard = st.Page("directory/curriculum/achievemet_standard.py", title="성취기준", icon=":material/school:")

### 에듀테크 관련 endpoint
edutech_lesson_plan = st.Page("directory/edutech_lesson_plan.py", title="에듀테크 지도안", icon=":material/school:")

### 학생부 작성 관련 endpoint
student_record = st.Page("directory/records/student_record.py", title="학생부 기재요령", icon=":material/article:")

### 깊이있는수업 지도안 endpoint
deep_lesson = st.Page("directory/deep_lesson.py", title="깊이있는수업 지도안 생성기", icon=":material/article:")

### 
official_document = st.Page("directory/proro.py", title="공문작성", icon=":material/article:")

pg = st.navigation(
    
        {   "계정 관리" : [account_page,help_page],
            "법령 및 규정": [work_law, educational_laws, official_document],
            "교육과정" : [achievement_standard],
            "학생부" : [student_record],
            "깊이있는수업"  : [deep_lesson],
            "에듀테크" : [edutech_lesson_plan]
                    }
    )

pg.run()


with st.sidebar :
    if "auth" not in st.session_state:
        st.markdown("오프라인 모드")
    else :
        email = st.session_state['auth']
        email = email.split("@")
        st.markdown(f"{email[0]}님 환영합니다")
        # if st.session_state["auth"] != None :
        #     st.markdown(f"{st.session_state['auth']}님 환영합니다!")
        # else :
        #     st.markdown("오프라인 모드")
