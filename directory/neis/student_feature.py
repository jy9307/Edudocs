import streamlit as st
from app.set_page import  MessageHandler, ChatCallbackHandler
from app.set_documents import load_Document
from app.set_prompt import student_feature_prompt, student_feature_simple_prompt, student_feature_record_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# from tools.db_manage import send_generate_result_to_firestore, send_stats_to_firestore
import requests
import asyncio

async def generate_chain(input_data, chain):
    """비동기 체인 호출"""
    
    return await chain.ainvoke(input_data)

mh = MessageHandler()
llm = ChatOpenAI(
    temperature=0.9,
    model='gpt-4o-mini',
    streaming= True,
    stream_usage=True,
    # callbacks=[
    #     ChatCallbackHandler(mh,"student_feature") ],
)

if "student_feature_messages" not in st.session_state:
    st.session_state["student_feature_messages"] = []

docs = load_Document().Chroma_select_document("student_feature")

st.set_page_config(
    page_title="행발 생성기",
    page_icon="📄",
    layout="wide"
)

st.markdown(docs.get()['documents'][:])

st.title("행발 생성기")
st.write("""
         - 특성 기반 생성기는 다양한 옵션을 사전 제공하고 이를 바탕으로 행발을 생성합니다. 
         - 간편 생성기는 선생님이 기술한 내용만을 바탕으로 행발을 생성합니다.
         - 행발 누가기록 생성기는 행발의 근거가 되는 누가기록을 생성합니다. """)
tab1, tab2, tab3 = st.tabs(["특성 기반 생성", "간편 생성", "행발 누가기록"])

with tab1 :
    with st.container(border= True) :
        # 설명
        st.markdown("##### 1. 행발에 포함시키고 싶은 특성들을 고르세요!")

        # 옵션 리스트
        options = [
            "학습태도", "사회성 및 교우 관계", "책임감 및 성실성", "리더십 및 협동심",
            "창의성", "운동 능력", "긍정적 태도", "의사소통 능력 및 표현력", "예술적 능력",
            "도덕성", "자신감", "계획성", "독서 습관 및 지적 호기심", "생활 습관"
        ]

        # 사용자가 선택한 옵션 저장
        selection = st.pills("x", options, selection_mode="multi",default='학습태도', label_visibility='collapsed')

        # 선택한 특성에 대해 각각 평가 (아쉬움/뛰어남)
        evaluation = {}

        st.write("---")
        st.markdown("##### 2. 각 특성에 대해 평가를 선택하세요:")
        for feature in selection:
            eval_result = st.radio(feature, ["아쉬움", "뛰어남"], horizontal=True)
            evaluation[feature] = eval_result

        st.write("---")
        st.markdown("##### 3. 그 외에 적고 싶은 특성이 있다면 적어주세요.")
        st.write("(없을 경우 내버려두셔도 됩니다)")
        extra_feature = st.text_input("""ex)고집이 셈, 에너지가 넘침, """, "없음")


    if st.button("행발 생성!", key="구체"):
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
                with st.spinner("대답을 생성중입니다! 잠시만 기다려주세요...."):
                    response_data = requests.post("http://127.0.0.1:8000/FeatureProcess", json={
                        "description" : features,
                        "examples" : examples,
                        "extra" : extra_feature
                        })
                    result = response_data.json()
                    # result = asyncio.create_task(generate_chain({
                    #     "description" : features,
                    #     "examples" : examples,
                    #     "extra" : extra_feature
                    #     }, chain))
                    st.markdown("### 생성된 행발")
                    st.write(result['result'])
            #     result = chain.invoke()
            #     token_usage = round(result.usage_metadata['total_tokens']*0.02)
            #     print(token_usage)
            # send_stats_to_firestore("student_feature")
            # if 'auth' in st.session_state :
            #     send_generate_result_to_firestore("행발",0, st.session_state["student_feature_messages"][-1]['message'])
                

        else:
            st.warning("먼저 특성을 선택하고 평가를 입력하세요.")

with tab2 :
    st.markdown("##### 학생의 특징을 적어주세요.")
    description = st.text_input("""ex) 교우관계가 좋음, 수업에 열정적으로 참여함, 고집이 셈, 에너지가 넘침 등""", "")

    if st.button("행발 생성!", key="간편"):
        examples = docs.as_retriever().batch(["description"])[0]
        example_data = []
        for i in examples :
            example_data.append(i.page_content)
        example_data = "\n".join(example_data)

        # chain = (
        #     student_feature_simple_prompt
        #     |llm
        #     |StrOutputParser()
        #     )
        with st.container(border=True) :
            with st.spinner("대답을 생성중입니다! 잠시만 기다려주세요...."):
                response_data = requests.post("http://127.0.0.1:8000/SimpleFeatureProcess", json={
                    "description" : description,
                    "examples" : example_data
                    })
                result = response_data.json()
                # result = asyncio.run(generate_chain({
                #     "description" : description,
                #     "examples" : examples[0]
                #     }, chain))
                st.markdown("### 생성된 행발")
                st.write(result['result'])
        # send_stats_to_firestore("student_feature_simple")
        # if 'auth' in st.session_state :
        #     send_generate_result_to_firestore("행발",0, st.session_state["student_feature_messages"][-1]['message'])

with tab3 :
    st.markdown("##### 누가기록을 생성할 행발을 적어주세요.")
    features = st.text_area("라벨", label_visibility="collapsed")
            
    if st.button("누가기록 생성!", key="누"):
        st.markdown("### 생성된 행발 누가기록")
        # chain = (
        #     student_feature_record_prompt
        #     |llm
        #     |StrOutputParser()
        #     )
        with st.container(border=True) :
            with st.spinner("대답을 생성중입니다! 잠시만 기다려주세요...."):
                response_data = requests.post("http://127.0.0.1:8000/FeatureRecordsDataProcess", json={"input": features})
                result = response_data.json()
                # result = asyncio.run(generate_chain({"input": features}, chain))
                st.markdown("### 생성된 행발 누가기록")
                st.write(result['result'])
        # send_stats_to_firestore("student_feature_record")
        # if 'auth' in st.session_state :
        #     send_generate_result_to_firestore("행발",0, st.session_state["student_feature_messages"][-1]['message'])



