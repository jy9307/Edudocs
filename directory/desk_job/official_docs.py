import streamlit as st
from app.set_page import  BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import proro_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"official_document") ],
)

page_template = BasicChatbotPageTemplate(mh_instance=mh, llm=llm, page_name="official_document")
page_template.set_title("K-에듀파인 기안문 작성 도우미","🎓")
page_template.set_chat_ui(proro_prompt, 
                          "본 페이지에서는 주제에 따라 기안문의 예시를 받아볼 수 있습니다!")

# page_template.input_box(['작성하려는 공문', '관련 근거 (예)한국초등학교-1736(2024.10.11)', '붙임 파일 제목'])

# retriever = load_Document().Chroma_select_document("official_document").as_retriever()

# if st.button("공문 생성"):
#         variables = ["basis", "file"]
#         variables =  {f"{variables[i]}": page_template.inputs[i+1] for i in range(2)}
#         context = retriever.batch([page_template.inputs[0]])
#         chain = (
#             proro_prompt
#             | llm  
#             | StrOutputParser()
#         )

#         chain.invoke({
#                 "context" : context[0],
#                 **variables,
#                 "input" : page_template.inputs[0]
#                 })

