import streamlit as st

# Title of the App
st.title("IB 자동 채점")
# Example data structure (using the leftmost column names as labels)
input_labels = [
    "gemini 명령어",
    "Ai 0",
    "Ai 1-2",
    "Ai 3-4",
    "Ai 5-6",
    "Ai 7-8"
]

feedback_inputs = {}

# Create a table-like layout
st.markdown("### 평가 입력")
for label in input_labels:
    with st.container():
        col1, col2 = st.columns([1, 3])  # Create two columns: one for the label, one for the input
        col1.markdown(f"**{label}**")  # Display label in the first column
        feedback_inputs[label] = col2.text_area(
            label="",
            placeholder=f"{label}에 대한 채점 요소를 작성해주세요.",
            key=label
        )

# Submit button for evaluation
if st.button("평가 제출"):
    st.success("평가가 성공적으로 제출되었습니다!")
    st.markdown("### 제출된 피드백")
    for label, feedback in feedback_inputs.items():
        st.write(f"- **{label} Feedback:** {feedback if feedback else '입력하지 않음'}")

# File upload section
st.markdown("### 학생 평가 파일 업로드")
uploaded_file = st.file_uploader("파일을 업로드하세요 (예: .csv, .xlsx, .txt)", type=["csv", "xlsx", "txt"])

if uploaded_file:
    st.success(f"파일 업로드 성공: {uploaded_file.name}")
    # Placeholder for further processing of the uploaded file
    st.markdown("업로드된 파일이 성공적으로 처리되었습니다.")
