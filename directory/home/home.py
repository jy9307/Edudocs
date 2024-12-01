import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# 페이지 기본 설정
st.set_page_config(
    page_title="Edudocs",
    page_icon=":writing_hand:",
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
    if "auth" in st.session_state:
        # 'auth'가 존재할 때: 로그아웃 버튼 표시
        logout_html = """
        <div 
                style="
                border: 2px solid #ccc; 
                border-radius: 8px; 
                padding: 5px; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
                background: #f7f7f7; 
                text-align: center; 
                font-family: Arial, sans-serif; 
                color: #333;
            ">
            <a href="http://www.edudocs.site/logout" 
                style="text-decoration: none; color: #333;"
                target="_self">
                <strong>로그아웃</strong>
            </a>
        </div>
        """
        st.markdown(logout_html, unsafe_allow_html=True)
    else:
        # 'auth'가 없을 때: 로그인 버튼 표시
        login_html = """
        <div 
                style="
                border: 2px solid #ccc; 
                border-radius: 8px; 
                padding: 5px; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
                background: #f7f7f7; 
                text-align: center; 
                font-family: Arial, sans-serif; 
                color: #333;
            ">
            <a href="http://www.edudocs.site/login" 
                style="text-decoration: none; color: #333;"
                target="_self">
                <strong>로그인</strong>
            </a>
        </div>
        """
        st.markdown(login_html, unsafe_allow_html=True)
with col2:
        login_html = """
        <div 
                style="
                border: 2px solid #ccc; 
                border-radius: 8px; 
                padding: 5px; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
                background: #f7f7f7; 
                text-align: center; 
                font-family: Arial, sans-serif; 
                color: #333;
            ">
            <a href="http://www.edudocs.site/help" 
                style="text-decoration: none; color: #333;"
                target="_self">
                <strong>도움말</strong>
            </a>
        </div>
        """


with st.container(border=True) : 
    st.write("""
###### v0.1 업데이트 소식(2024. 11. 30)
- 공적 조서 생성기 추가 : 번거로웠던 공적 조서를 더 쉽게 작성해보세요!
- 공문 생성기 업데이트 : 공문 생성기가 더 다양한 공문을 생성할 수 있습니다.
             """)
