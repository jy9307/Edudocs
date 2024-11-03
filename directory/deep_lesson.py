import streamlit as st
from fpdf import FPDF
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import LocalFileStore
from io import BytesIO
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# PDF 로더 설정 및 리트리버 초기화
def initialize_pdf_retriever():
    loader = PyPDFLoader("db/깊이있는수업.pdf")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = loader.load_and_split(text_splitter=text_splitter)

    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    cache_dir = LocalFileStore(f"./.cache/embeddings/회계지침")
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings_model, cache_dir)

    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    return vectorstore.as_retriever()

# AI 모델을 통해 지도안 생성 함수 (PDF와 AI 지식 병합)
def generate_lesson_plan_with_pdf_and_ai(subject, competency, achievement_standard):
    retriever = initialize_pdf_retriever()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

    pdf_based_docs = retriever.get_relevant_documents(f"{subject} {competency} {achievement_standard}")
    pdf_summary = "\n".join([doc.page_content for doc in pdf_based_docs[:3]])

    ai_only_prompt = PromptTemplate(
        input_variables=["subject", "competency", "achievement_standard"],
        template=(
            "교과: {subject}\n"
            "역량: {competency}\n"
            "성취기준: {achievement_standard}\n\n"
            "위 내용을 바탕으로 아래 양식에 맞춘 지도안을 작성해주세요.\n"
            "교과: {subject}\n역량: {competency}\n성취기준: {achievement_standard}\n\n"
            "핵심 아이디어:\n지식, 이해:\n과정, 기능:\n가치, 태도:\n핵심어:\n핵심 문장:\n핵심 질문:\n"
        )
    )
    ai_based_result = llm.invoke(ai_only_prompt.format(
        subject=subject, competency=competency, achievement_standard=achievement_standard
    )).content

    combined_prompt = PromptTemplate(
        input_variables=["pdf_info", "ai_info", "subject", "competency", "achievement_standard"],
        template=(
            "교과: {subject}\n"
            "역량: {competency}\n"
            "성취기준: {achievement_standard}\n\n"
            "예시자료 기반 정보:\n{pdf_info}\n\n"
            "인공지능 기반 정보:\n{ai_info}\n\n"
            "위의 예시자료와 인공지능 분석을 종합하여, 아래 양식에 맞춘 최종 지도안을 작성해주세요.\n"
            "교과: {subject}\n역량: {competency}\n성취기준: {achievement_standard}\n\n"
            "핵심 아이디어:\n지식, 이해:\n과정, 기능:\n가치, 태도:\n핵심어:\n핵심 문장:\n핵심 질문:\n"
        )
    )
    combined_result = llm.invoke(combined_prompt.format(
        pdf_info=pdf_summary,
        ai_info=ai_based_result,
        subject=subject,
        competency=competency,
        achievement_standard=achievement_standard
    )).content

    result = (
        f"**1. 예시자료 기반:**\n{pdf_summary}\n\n"
        f"**2. 인공지능 기반:**\n{ai_based_result}\n\n"
        f"**3. 종합분석:**\n{combined_result}"
    )
    return result

# PDF 생성 함수 (BytesIO로 반환)
def create_pdf(lesson_plan):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    try:
        pdf.add_font("NanumGothic", "", "NanumGothic.ttf", uni=True)
        pdf.set_font("NanumGothic", "", 12)
    except:
        pdf.set_font("Arial", size=12)

    for line in lesson_plan.split('\n'):
        pdf.cell(200, 10, txt=line.encode("latin1", "replace").decode("latin1"), ln=True)

    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_buffer = BytesIO(pdf_output)
    pdf_buffer.seek(0)
    return pdf_buffer

# TXT 파일 생성 함수 (BytesIO로 반환)
def create_txt(lesson_plan):
    txt_buffer = BytesIO()
    txt_buffer.write(lesson_plan.encode("utf-8"))
    txt_buffer.seek(0)
    return txt_buffer

# UI 구성 함수
def lesson_plan_app():
    st.title("깊이 있는 수업 지도안 생성 프로그램")

    subject = st.text_input("교과:")
    competency = st.text_input("역량:")
    achievement_standard = st.text_area("성취기준:")

    if st.button("수업 지도안 생성"):
        lesson_plan = generate_lesson_plan_with_pdf_and_ai(subject, competency, achievement_standard)
        st.text_area("생성된 수업 지도안", lesson_plan, height=300)

        if lesson_plan:
            pdf_buffer = create_pdf(lesson_plan)
            st.download_button(
                label="📄 PDF로 저장",
                data=pdf_buffer,
                file_name="lesson_plan.pdf",
                mime="application/pdf"
            )

            txt_buffer = create_txt(lesson_plan)
            st.download_button(
                label="📄 TXT로 저장",
                data=txt_buffer,
                file_name="lesson_plan.txt",
                mime="text/plain"
            )

# 실행
lesson_plan_app()
