import streamlit as st
from app.set_page import BasicInputBoxPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import proro_prompt
from app.set_documents import load_Document
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
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

page_template = BasicInputBoxPageTemplate(mh_instance=mh, llm=llm, page_name="official_document")
page_template.set_title("K-에듀파인 내부기안 자동작성 도우미","🎓")
page_template.input_box(['작성하려는 공문', '관련 근거 (예)한국초등학교-1736(2024.10.11)', '붙임 파일 제목'])

retriever = load_Document().select_document("official_document").as_retriever()

if st.button("공문 생성"):
        variables = ["basis", "file"]
        variables =  {f"{variables[i]}": page_template.inputs[i+1] for i in range(2)}
        context = retriever.batch([page_template.inputs[0]])
        chain = (
            proro_prompt
            | llm  
            | StrOutputParser()
        )

        chain.invoke({
                "context" : context[0],
                **variables,
                "input" : page_template.inputs[0]
                })

