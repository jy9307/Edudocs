import streamlit as st
from app.set_page import  MessageHandler, ChatCallbackHandler
from app.set_documents import load_Document
from app.set_prompt import student_feature_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"student_feature") ],
)

docs = load_Document().Chroma_select_document("student_feature")

st.title("행발 생성기")

# 설명
st.markdown("##### 1. 행발에 포함시키고 싶은 특성들을 고르세요!")

# 옵션 리스트
options = [
    "학습태도", "사회성 및 교우 관계", "책임감 및 성실성", "리더십 및 협동심",
    "창의성", "운동 능력", "긍정적 태도", "의사소통 능력 및 표현력", "예술적 능력",
    "도덕성", "자신감", "계획성", "독서 습관 및 지적 호기심", "생활 습관"
]

# 사용자가 선택한 옵션 저장
selection = st.pills("", options, selection_mode="multi")

# 선택한 특성에 대해 각각 평가 (아쉬움/뛰어남)
evaluation = {}
if selection:
    st.markdown("##### 2. 각 특성에 대해 평가를 선택하세요:")
    for feature in selection:
        eval_result = st.radio(feature, ["아쉬움", "뛰어남"], horizontal=True)
        evaluation[feature] = eval_result

    st.markdown("##### 3. 과목별 역량에 대한 설명을 적어주세요")
    st.write("(없을 경우 적지 않으셔도 됩니다)")
    strong_subject = st.text_input("""뛰어난 과목""", "없음")
    weak_subject = st.text_input("""아쉬운 과목""", "없음")    


if st.button("행발 생성!"):
    if evaluation:

        # 버튼 클릭 시 결과 출력
        features = [f"{k} : {evaluation[k]}" for k in evaluation.keys()]

        examples = []
        for feature, result in evaluation.items():
            filter_criteria = {
                        "$and": [
                            {"영역": {"$eq": feature}},
                            {"수준": {"$eq": result}}
                        ]
                    }
            examples.append(docs.get(where=filter_criteria)['documents'][0])
        examples = "\n".join(examples)

        st.markdown("### 생성된 행발")
        chain = (
            student_feature_prompt
            |llm
            |StrOutputParser()
            )
        with st.container(border=True) :
            chain.invoke({
                "description" : features,
                "examples" : examples,
                "strong" : strong_subject,
                "weak" : weak_subject
                })

    else:
        st.warning("먼저 특성을 선택하고 평가를 입력하세요.")



