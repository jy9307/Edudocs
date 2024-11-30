import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# 페이지 기본 설정
st.set_page_config(
    page_title="My App",
    page_icon=":star:",
    layout="centered",  # 'centered' 또는 'wide'
)

# 로고 표시
st.image("resources/logo.png", use_container_width=True)

st.markdown("""
<style>
.stPageLink {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# 버튼 생성
col1, col2 = st.columns([1, 1])  # 두 개의 버튼을 나란히 배치

with col1:
    with stylable_container(
    key="login_columns",
    css_styles="""
            {
                border: 2px solid #ccc; /* 부드러운 회색 테두리 */
                border-radius: 8px; /* 둥근 모서리 */
                padding: 5px; /* 내부 여백 */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
                background: #f7f7f7;
                font-family: Arial, sans-serif; /* 깔끔한 폰트 */
            }
            
"""                    ) :
        
        st.page_link("login.py", label="#### **로그인**")

with col2:
    with stylable_container(
    key="help_columns",
    css_styles="""
            {
                border: 2px solid #ccc; /* 부드러운 회색 테두리 */
                border-radius: 8px; /* 둥근 모서리 */
                padding: 5px; /* 내부 여백 */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
                background: #f7f7f7;
                font-family: Arial, sans-serif; /* 깔끔한 폰트 */
            }
"""                    ) :
        st.page_link("directory/settings/help.py", label="#### **도움말**")


with st.container(border=True) : 
    st.write("""
###### v0.1 업데이트 소식(2024. 11. 30)
- 공적 조서 생성기 추가 : 번거로웠던 공적 조서를 더 쉽게 작성해보세요!
- 공문 생성기 업데이트 : 공문 생성기가 더 다양한 공문을 생성할 수 있습니다.
             """)
