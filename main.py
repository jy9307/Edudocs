import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


###계정 관련 endpoint
if st.session_state.logged_in == False :
    account_page = st.Page(login, title="Log in", icon=":material/login:")
else :
    account_page = st.Page(logout, title="Log out", icon=":material/logout:")

help_page = st.Page("directory/settings/help.py", title = "도움말", icon=":material/help:", default=True)


### 법령 관련 endpoint
work_law = st.Page("directory/laws/work_law.py", title="복무규정", icon=":material/work:")
educational_laws = st.Page("directory/laws/education_law.py", title="초중등 교육법", icon=":material/work:")

### 교육과정 관련 endpoint
achievement_standard = st.Page("directory/curriculum/achievemet_standard.py", title="성취기준", icon=":material/school:")

### 학생부 작성 관련 endpoint
student_record = st.Page("directory/records/student_record.py", title="학생부 기재요령", icon=":material/article:")

### test
test = st.Page("directory/test.py", title="연습")

### 깊이있는수업 지도안 endpoint
deep_lesson = st.Page("directory/deep_lesson.py", title="깊이있는수업 지도안 생성기", icon=":material/article:")

pg = st.navigation(
        {   "계정 관리" : [account_page,help_page, test],
            "법령 및 규정": [work_law, educational_laws],
            "교육과정" : [achievement_standard],
            "학생부" : [student_record],
            "깊이있는수업"  : [deep_lesson]
                    }
    )

pg.run()