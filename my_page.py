import streamlit as st
import pandas as pd

def main_page(user_info):
    st.title("내 정보")

    st.write(f"**ID**: {user_info.get('name', 'N/A')}")
    st.write(f"**이메일**: {user_info.get('email', 'N/A')}")
    st.write(f"**가입일자**: {user_info.get('member_since', 'N/A')}")
    st.write(f"**잔여 포인트**: {user_info.get('remaining_points', '0')}")

    # Navigation Buttons
    st.subheader("📂 Navigation")
    if st.button("🔍 검색 이력 확인하기"):
        st.session_state.page = "search_history"
        st.rerun()
    if st.button("💰 포인트 사용 이력 확인하기"):
        st.session_state.page = "point_history"
        st.rerun()

    # Logout option
    st.markdown("---")
    st.button("Log Out", key="logout_button")


def search_history_page(user_info):
    st.title("🔍 검색 이력 확인하기")
    search_history = user_info.get("search_history", [])

    if search_history:
        st.write("Here are your recent searches:")

        for history in search_history:
            with st.container():
                st.markdown(f"""
                **날짜:** {history[0]}  
                **서비스 이름:** {history[1]}  
                **사용 포인트:** {history[3]}  
                **생성 결과:** {history[2]}
                """)
                st.markdown("---")
    else:
        st.write("No search history found.")

    # Back Button
    if st.button("Back to Main Page"):
        st.session_state.page = "main"
        st.rerun()


def point_history_page(user_info):
    st.title("💰 포인트 사용 이력 확인하기")
    point_history = user_info.get("point_history", [])

    if point_history:
        st.write("Here is your recent point usage:")
        # Display point history as a table
        point_df = pd.DataFrame(point_history, columns=["날짜", "포인트", "세부내용"])
        st.table(point_df)
    else:
        st.write("No point usage history found.")

    # Back Button
    if st.button("Back to Main Page"):
        st.session_state.page = "main"
        st.rerun()


# Example user_info for testing
user_info = {
    "name": "Jay Lee",
    "email": "jay.lee@example.com",
    "member_since": "2024-01-01",
    "remaining_points": 150,
    "search_history": [
        ["2024-12-01", "Streamlit tutorial", 10, "Success"],
        ["2024-11-30", "Python data visualization", 5, "Success"],
        ["2024-11-29", "How to use Milvus", 0, "Failed"],
    ],
    "point_history": [
        ["2024-12-01", 50, "Redeemed for a gift card"],
        ["2024-11-30", 30, "Used for a discount"],
        ["2024-11-29", 10, "Purchased additional features"],
    ],
}

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "main"

# Page routing
if st.session_state.page == "main":
    main_page(user_info)
elif st.session_state.page == "search_history":
    search_history_page(user_info)
elif st.session_state.page == "point_history":
    point_history_page(user_info)
