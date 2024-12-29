import streamlit as st
import base64

# 페이지 기본 설정
st.set_page_config(
    page_title="Edudocs",
    page_icon=":writing_hand:",
    layout="wide",  # 'centered' 또는 'wide'
)

# 로고 표시
image_path = "resources/logo.png"

# 이미지를 base64로 변환
with open(image_path, "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode()

# HTML로 이미지 가운데 정렬
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded_image}" alt="Image" width="500">
    </div>
    """,
    unsafe_allow_html=True
)

# with col1:
#     if "auth" in st.session_state:
#         # 'auth'가 존재할 때: 로그아웃 버튼 표시
#         logout_html = """
#         <div 
#                 style="
#                 border: 2px solid #ccc; 
#                 border-radius: 8px; 
#                 padding: 5px; 
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
#                 background: #f7f7f7; 
#                 text-align: center; 
#                 font-family: Arial, sans-serif; 
#                 color: #333;
#             ">
#             <a href="http://www.edudocs.site/logout" 
#                 style="text-decoration: none; color: #333;"
#                 target="_self">
#                 <strong>로그아웃</strong>
#             </a>
#         </div>
#         """
#         st.markdown(logout_html, unsafe_allow_html=True)
#     else:
#         # 'auth'가 없을 때: 로그인 버튼 표시
#         # st.page_link("directory/home/login.py", label="로그인")
#         login_html = """
#         <div 
#                 style="
#                 border: 2px solid #ccc; 
#                 border-radius: 8px; 
#                 padding: 5px; 
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
#                 background: #f7f7f7; 
#                 text-align: center; 
#                 font-family: Arial, sans-serif; 
#                 color: #333;
#             ">
#             <a href="http://www.edudocs.site/login" 
#                 style="text-decoration: none; color: #333;"
#                 target="_self">
#                 <strong>로그인</strong>
#             </a>
#         </div>
#         """
#         st.markdown(login_html, unsafe_allow_html=True)
# with col2:
#         help_html = """
#         <div 
#                 style="
#                 border: 2px solid #ccc; 
#                 border-radius: 8px; 
#                 padding: 5px; 
#                 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
#                 background: #f7f7f7; 
#                 text-align: center; 
#                 font-family: Arial, sans-serif; 
#                 color: #333;
#             ">
#             <a href="http://www.edudocs.site/help" 
#                 style="text-decoration: none; color: #333;"
#                 target="_self">
#                 <strong>도움말</strong>
#             </a>
#         </div>
#         """
#         st.markdown(help_html, unsafe_allow_html=True)

help_html = """
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
st.markdown(help_html, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1 :
    st.write("")
    with st.container(border=True) :
        st.write("""
    ##### 후원계좌
    서비스를 이용해주셔 진심으로 너무나 감사드립니다!\n
    작은 금액이라도 후원해주시면 추후 서비스 고도화와 서버 운영에 이용하겠습니다.
    감사합니다.

    농협 356-0592-0682-53
    이주영
    """)
    with st.container(border=True):
            st.write("""
        ##### 🙇‍♂️후원해주신  선생님🙇‍♂️
        ###### 진심으로 감사드립니다. 선생님들 덕분에 사이트 운영이 가능합니다!
       <INFJ>선생님👑  /<구이구이>선생님👑👑 <steady>선생님👑👑 / <깊은산속맑은물>선생님👑👑/ <최명주>선생님👑👑 / <인디-9>선생님👑👑  \n
        <빠다선생>선생님👑 / <선생님감사합니다>선생님👑 / <비주류쌤>선생님👑 / <또먹겠지떡볶이>선생님👑 / <인디이지>선생님👑 / <김영철>선생님👑
        / <GTY>선생님👑 / <주간조퇴안내>선생님👑/ <후원자>선생님👑  / <후원해요>생님👑
                             """)

with col2 :
    st.write("")
    with st.container(border=True) :
        st.write("""
   ##### 공지사항
:red[선생님들의 원활한 사용을 위해 한동안 출근시간 전후로 서버를 변경하여 운영할 예정입니다.]
:red[따라서 08:00-09:00, 16:00-17:00에 일시적으로 사이트 작동이 멈출 수 있습니다.]\n
현재 다양한 피드백을 받아 데이터 조정과 입력 내용 변경을 실시하고 있습니다.\n
더 좋은 서비스가 될 수 있도록 노력하겠습니다!   
 """)
    with st.container(border=True) : 
        st.write("""
    ###### Beta v0.11 업데이트 소식(2024. 12. 06)
    - 과목 생성기 : 통합교과(바,슬,즐)을 추가하였습니다!
                """)

    with st.container(border=True) : 
        st.write("""
    ###### Beta v0.1 업데이트 소식(2024. 11. 30)
    - 공적 조서 생성기 추가 : 번거로웠던 공적 조서를 더 쉽게 작성해보세요!
    - 공문 생성기 업데이트 : 공문 생성기가 더 다양한 공문을 생성할 수 있습니다.
                """)
