from fastapi import FastAPI, Form, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List, Dict

from app.set_documents import load_Document
from app.set_prompt import *
import tools

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.query_constructor.base import AttributeInfo

from io import BytesIO
import pandas as pd
import langchain
import json
import asyncio

langchain.debug = False
langchain.llm_cache = False

class InputOnlyData(BaseModel):
    input : str 


class SimpleFeatureData(BaseModel) :
    description : str
    examples : str

class FeatureData(BaseModel) :
    description : List[str]
    examples : str
    extra : str

def get_text(file_obj):
    extractor = tools.HWPExtractor(file_obj)  # file_obj는 BytesIO
    return extractor.get_text()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 Origin (React 개발 서버)
    allow_credentials=True,                  # 쿠키 전달 허용
    allow_methods=["*"],                     # 허용할 HTTP 메서드 (예: GET, POST 등)``
    allow_headers=["*"],                     # 허용할 HTTP 헤더
)

@app.post("/WorkLaw")
async def process_data(data : dict):

    query = data['query']

    docs = load_Document().Chroma_select_document("work_law")

    self_retriever = tools.LoadSelfQueryRetriever(docs, 0.5)

    self_retriever.metadata_info([
            AttributeInfo(
        name="cluase_title",
        description="""법률 항목의 이름입니다.
        One of ['휴직', '특별연수', '조교의 임용', '승진', '휴가의 종류', '적용범위', '명예퇴직', '징계위원회의 설치', '근무시간 면제 시간의 사용', '인사위원회의 기능', '인사교류', '당직 및 비상근무', '목적', '연수기관 및 근무장소 외에서의 연수', '초빙교원', '연가계획 및 승인', '임용의 원칙', '교권의 존중과 신분보장', '보직 등 관리의 원칙', '벌칙', '대학의 장 등의 임기', '공립대학의 장 등의 임용', '시간외근무 및 공휴일 등 근무', '근무기강의 확립', '지방교육공무원 인사위원회', '연수와 교재비', '정년', '휴가기간 중의 토요일 또는 공휴일', '겸직 허가', '근무시간 등의 변경', '교장·교감 등의 자격', '영리 업무의 금지', '정의', '정치적 행위', '인사위원회의 설치', '교육감 소속 교육전문직원의 채용 및 전직 등', '특별휴가', '연가 일수', '보수결정의 원칙', '교수 등의 임용', '선서', '경력경쟁채용 등', '출장공무원', '국가공무원법과의 관계', '사실상 노무에 종사하는 공무원', '겸직 금지', '전직 등의 제한', '지방공무원법과의 관계', '병가', '교원의 불체포특권', '연수 실적 및 근무성적의 평정', '대학인사위원회', '휴직기간 등', '공립대학 교육공무원의 고충처리', '휴가기간의 초과', '연가 일수에서의 공제', '징계사유의 시효에 관한 특례', '보수에 관한 규정', '해직된 공무원의 근무', '장학관 등의 임용', '과태료', '교수 등의 자격', '연수의 기회균등', '인사기록', '겸임', '대학의 장의 임용', '공가', '교육전문직원의 자격', '고위공직자의 공무 외 국외여행', '우수 교육공무원 특별 승진', '승진후보자 명부', '친절ㆍ공정한 업무 처리', '지방교육전문직원 인사위원회', '교감ㆍ교사ㆍ장학사 등의 임용', '고충처리', '임용권의 위임 등', '강임자의 우선승진임용 제한', '파견근무', '교육연수기관에의 교원 배치', '근무시간 등', '신체검사', '연수기관의 설치', '교사의 신규채용 등', '징계의결의 요구', '교사의 자격', '교육감 소속 교육전문직원의 임용', '기간제교원', '현업 공무원 등의 근무시간과 근무일', '부총장ㆍ대학원장ㆍ단과대학장의 보직']""",
        type='string'
    ),
    ])

    self_retriever.docs_info("학교에서 근무하는 공무원(교원)이 지켜야 하는 법률을 담고 있습니다.")

    retriever = self_retriever.retriever_load()

    laws = retriever.batch([query])[0]

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    ) 

    chain = (
    work_law_prompt
    |llm
    |StrOutputParser()
    )

    result = await chain.ainvoke({
        "input" : query,
        "context" : laws
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/WorkLaw-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:

        query = data.get("query").strip()

        docs = load_Document().Chroma_select_document("work_law")

        self_retriever = tools.LoadSelfQueryRetriever(docs, 0.5)

        self_retriever.metadata_info([
                AttributeInfo(
            name="clause_title",
            description="""법률 항목의 이름입니다.
            One of ['선거 관련 사무 수행 공무원의 휴무', '겸임', '정치적 행위', '지방교육공무원 인사위원회', '조사ㆍ질문', '선서', '휴가기간의 초과', '다문화학생등에 대한 교육 지원', '교육과정 영향 사전협의', '대학 교원의 신규채용 등', '보수결정의 원칙', '수업료 등', '학교발전기금', '시간외근무 및 공휴일 등 근무', '부총장ㆍ대학원장ㆍ단과대학장의 보직', '출장공무원', '겸직 허가', '학생의 징계', '근로청소년을 위한 특별학급 등', '고위공직자의 공무 외 국외여행', '연수의 기회균등', '겸직 금지', '교육행정기관에의 순회교사 배치', '휴가의 종류', '교과용 도서의 사용', '연수기관 및 근무장소 외에서의 연수', '강임자의 우선승진임용 제한', '학교의 장 및 교원의 학생생활지도', '전문상담교사의 배치 등', '교육비 지원을 위한 자료 등의 수집 등', '부정행위자에 대한 조치', '목적', '친권자 등에 대한 보조', '벌칙', '적용범위', '보수에 관한 규정', '학교회계의 운영', '교직원의 구분', '근무시간 등', '교권의 존중과 신분보장', '징계사유의 시효에 관한 특례', '교원 개인정보의 보호', '취학 의무', '특수학급', '병가', '친절ㆍ공정한 업무 처리', '벌금형의 분리 선고', '대학의 장 등의 임기', '정년', '통합교육', '교수 등의 임용', '사서, 실기, 보건, 영양교사의 자격', '인사교류', '교원의 불체포특권', '인사위원회의 기능', '승진후보자 명부', '당직 및 비상근무', '고등기술학교', '연가 일수', '학교 규칙', '허가권의 위임', '연가 사용의 권장', '교육전문직원의 자격', '학교 등의 폐쇄', '교사의 자격', '선거운동의 제한', '대학의 장의 임용', '교육감 소속 교육전문직원의 임용', '허가권자', '지방교육전문직원 인사위원회', '휴직', '시ㆍ도학생징계조정위원회의 설치', '통학 지원', '시정 또는 변경 명령 등', '정보시스템을 이용한 업무처리', '특수학교', '학교운영위원회의 구성ㆍ운영', '상담교사 자격', '공가', '수업연한', '권한의 위임', '학생 관련 자료 제공의 제한', '근무시간 등의 변경', '연수 실적 및 근무성적의 평정', '인사기록', '학년제', '휴업명령 및 휴교처분', '학교운영위원회 위원의 연수 등', '별표2-교감 및 교장의 자격', '학교의 병설', '휴직기간 등', '공립대학의 장 등의 임용', '보직 등 관리의 원칙', '비용의 징수', '「국가공무원법」과의 관계', '장학금 지급 및 의무복무', '학교생활기록', '공모에 따른 교장 임용 등', '고등공민학교', '교원의 자격', '고교학점제 지원 등', '준교사 자격', '교육비 지원', '보고서 제출 및 등록', '수석교사의 자격', '지도ㆍ감독', '정의', '고등학교 등의 무상교육', '입학자격 등', '대안학교', '학교운영위원회의 설치', '학교 및 교육과정 운영의 특례', '학교시설 등의 이용', '교육비 지원의 신청', '학력인정 시험', '우수 교육공무원 등의 특별 승진', '결격사유', '휴가기간 중의 토요일 또는 공휴일', '의무교육', '교장 등의 임용', '학교회계의 설치', '수업 등', '임용권의 위임 등', '근무혁신기본계획의 수립 등', '채용의 제한', '고용자의 의무', '영리 업무의 금지', '복장 및 복제 등', '당연퇴직', '대학인사위원회', '학과 및 학점제 등', '취학 의무의 면제 등', '학생ㆍ기관ㆍ학교 평가', '방송통신중학교', '직위해제', '징계위원회의 설치', '기능', '계약제 임용 등', '전직 등의 제한', '겸임근무', '영리업무 및 겸직금지에 관한 특례', '시설ㆍ설비ㆍ교구의 점검 등', '학생의 인권보장 등', '인사관리의 전자화', '교직원의 임무', '초빙교원', '인사위원회의 설치', '교장ㆍ교감 등의 자격', '장학관 등의 임용', '정보시스템을 이용한 업무처리 등에 대한 지도ㆍ감독', '금융정보등의 제공', '보고', '근무시간 면제 시간의 사용', '교육감 소속 교육전문직원의 채용 및 전직 등', '10일 이상 연속된 연가 사용의 보장', '복무 실태의 확인ㆍ점검', '신체검사', '자격취소 등', '교육비 지원 업무의 전자화', '「지방공무원법」과의 관계', '고충처리', '과태료', '외국인 교원', '근무기강의 확립', '외국인학교', '재심청구', '교육연수기관 등에의 교원 배치', '조기진급 및 조기졸업 등', '교감ㆍ교사ㆍ장학사 등의 임용', '명예퇴직', '수석교사의 임용 등', '특별연수', '국립ㆍ공립ㆍ사립 학교의 구분', '양성평등을 위한 임용계획의 수립 등', '1급 정교사 자격', '학생의 안전대책 등', '방송통신고등학교', '학교의 설립 등', '징계의결의 요구', '학교민원 처리 계획의 수립ㆍ시행 등', '현업 공무원 등의 근무시간과 근무일', '비밀 엄수', '분교', '학교의 통합ㆍ운영', '사실상 노무에 종사하는 공무원', '학력의 인정', '시간선택제공무원 등의 휴가에 관한 특례', '교원의 휴가에 관한 특례', '파견근무', '연수기관의 설치', '교육통계조사 등', '교사 자격 취득의 결격사유', '심사위원회의 설치', '청문', '교육과정 등', '연가의 저축', '사후관리 등', '특별휴가', '승진', '연가 일수에서의 공제', '연가계획 및 승인', '공립대학 교육공무원의 고충처리', '교수 등의 자격', '각종학교', '임용의 원칙', '교원자격증 대여ㆍ알선 금지', '경력경쟁채용 등', '장학지도', '보호자의 의무 등', '대학의 장 후보자 추천을 위한 선거사무의 위탁', '해직된 공무원의 근무', '산학겸임교사 등', '학교의 종류', '교사의 신규채용 등', '책임 완수', '학생자치활동', '기간제교원', '과정', '2급 정교사 자격', '연수와 교재비', '조교의 임용', '교육정보시스템의 구축ㆍ운영 등', '취학 의무 및 방해 행위의 금지', '학업에 어려움을 겪는 학생에 대한 교육']""",
            type='string'
        ),
        ])

        self_retriever.docs_info("학교에서 근무하는 공무원(교원)이 지켜야 하는 법률을 담고 있습니다.")

        retriever = self_retriever.retriever_load()
        laws = retriever.batch([query])[0]

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        ) 

        chain = (
        work_law_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
                "input" : query,
                "laws" : laws
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()


@app.post("/CommendDocs")
async def process_data(    
    activities: str = Form(...),
    hwpFile: UploadFile = File(...)
):
    print("Received activities:", activities)
    file_bytes = await hwpFile.read()
    buffer = BytesIO(file_bytes)
    criteria = get_text(buffer)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    ) 

    chain = (
    commend_prompt
    |llm
    |StrOutputParser()
    )

    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "input" : activities,
        "criteria" : criteria
        })
    response = {"status": "success", "result": result}
    return response

@app.post("/OfficialDocs")
async def process_data(data : dict):

    docs = load_Document().Chroma_select_document("official_document")

    self_retriever = tools.LoadSelfQueryRetriever(docs, 0.5)

    self_retriever.metadata_info([
            AttributeInfo(
        name="범주",
        description="""공문의 범주입니다. 
        One of ['현장체험학습','학업중단숙려제','학업성적관리위원회','교육과정','평가 도구', '학교생활기록부','방과후학교','학교운영위원회','학교폭력','학교회계','교외체험학습']""",
        type='string'
    ),
    ])

    self_retriever.docs_info("학교에서 공적 업무 처리를 위해 작성하는 공문의 예시")

    retriever = self_retriever.retriever_load()

    examples = retriever.batch([data['topic']])[0]

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    ) 

    chain = (
    official_docs_prompt
    |llm
    |StrOutputParser()
    )

    print("공문 생성기 : ",data['topic'])

    result = await chain.ainvoke({
        "input" : data['topic'],
        "context" : examples
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/OfficialDocs-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        topic = data.get("topic").strip()

        docs = load_Document().Chroma_select_document("official_document")

        self_retriever = tools.LoadSelfQueryRetriever(docs, 0.5)

        self_retriever.metadata_info([
                AttributeInfo(
            name="범주",
            description="""공문의 범주입니다. 
            One of ['현장체험학습','학업중단숙려제','학업성적관리위원회','교육과정','평가 도구', '학교생활기록부','방과후학교','학교운영위원회','학교폭력','학교회계','교외체험학습']""",
            type='string'
        ),
        ])

        self_retriever.docs_info("학교에서 공적 업무 처리를 위해 작성하는 공문의 예시")

        retriever = self_retriever.retriever_load()

        examples = retriever.batch([data['topic']])[0]
        print(examples)

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        ) 

        chain = (
        official_docs_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
                    "input" : topic,
                    "context" : examples
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/ParentNoti")
async def process_data(data : dict):

    docs = load_Document().Chroma_select_document("parent_notification")

    self_retriever = tools.LoadSelfQueryRetriever(docs, 0.5)

    self_retriever.metadata_info([
            AttributeInfo(
        name="범주",
        description="""가정통신문의 범주입니다. 
        One of ['교육과정 운영','방과후학교, 돌봄교실, 늘봄교실 등', '현장체험학습', '통학버스', '보건, 건강 등', '학교폭력, 안전, 정보 등', '기타']""",
        type='string'
    ),
    ])

    self_retriever.docs_info("학교에서 가정으로 보내는 가정통신문 예시 문서")

    retriever = self_retriever.retriever_load()

    examples = retriever.batch([data['topic']])[0]

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    ) 

    chain = (
    parent_noti_prompt
    |llm
    |StrOutputParser()
    )

    print("가통 생성기 주제 : ",data['topic'])

    result = await chain.ainvoke({
        "input" : data['topic'],
        "detail" : data['detail'],
        "examples" : examples
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/ParentNoti-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        print(data)
        if data.get("detail") : 
            detail = data.get("detail").strip()
        else : 
            detail = ""
        topic = data.get("topic").strip()

        docs = load_Document().Chroma_select_document("parent_notification")

        self_retriever = tools.LoadSelfQueryRetriever(docs, 0.5)

        self_retriever.metadata_info([
                AttributeInfo(
            name="범주",
            description="""가정통신문의 범주입니다. 
            One of ['교육과정 운영','방과후학교, 돌봄교실, 늘봄교실 등', '현장체험학습', '통학버스', '보건, 건강 등', '학교폭력, 안전, 정보 등', '기타']""",
            type='string'
        ),
        ])

        self_retriever.docs_info("학교에서 가정으로 보내는 가정통신문 예시 문서")

        retriever = self_retriever.retriever_load()

        examples = retriever.batch([data['topic']])[0]

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        ) 

        chain = (
        parent_noti_prompt
        |llm
        |StrOutputParser()
        )
        # 스트리밍 체인 실행

        async for chunk in chain.astream({
                "input" : data['topic'],
                "detail" : data['detail'],
                "examples" : examples
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/SafetyPhrase")
async def process_data(data : dict):

    docs = load_Document().Chroma_select_document("safety_phrase")

    examples = docs.get(where={"영역" : data['area']})['documents'][0]

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    safety_phrase_prompt
    |llm
    |StrOutputParser()
    )
    
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "detail" : data['detail'],
        "area" : data['area'],
        "examples" : examples
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/SafetyPhrase-ws")
async def generate_websocket(websocket: WebSocket):
    print(123)
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])


    try:
        if data.get("detail") : 
            detail = data.get("detail").strip()
        else : 
            detail = ""
        area = data.get("area").strip()

        docs = load_Document().Chroma_select_document("safety_phrase")

        examples = docs.get(where={"영역" : area})['documents'][0]

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        safety_phrase_prompt
        |llm
        |StrOutputParser()
        )

        # 스트리밍 체인 실행

        async for chunk in chain.astream({
                    "detail" : detail,
                    "area" : area,
                    "examples" : examples
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()


@app.post("/SubjectRecord")
async def process_data(data : dict):

    docs = load_Document().Chroma_select_document("subject_record")

    examples = docs.get(where={"과목" : data['subject']})['documents'][0]

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    subject_record_prompt
    |llm
    |StrOutputParser()
    )
    
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "subject" : data['subject'],
        "area" : data['area'],
        "examples" : examples
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/SubjectRecord-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    print(1)
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:

        subject = data.get("subject").strip()
        area = data.get("area").strip()
        print(data)

        docs = load_Document().Chroma_select_document("subject_record")
        examples = docs.get(where={"과목" : subject })['documents'][0]
        print(examples)

        llm = ChatOpenAI(
            temperature=0.5,
            model='gpt-4o-mini',
            verbose=False,
            streaming=True,
        )

        chain = (
            subject_record_prompt
            |llm
            |StrOutputParser()
        )

        # 스트리밍 체인 실행

        async for chunk in chain.astream({"subject": subject, "area": area, "examples" : examples}):
            # 웹소켓을 통해 각 청크 전송
            print(chunk)
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/ExtraSelf")
async def process_data(data : dict):
    print(data)

    docs = load_Document().Chroma_select_document("extra_record")
    selections = data['area']

    examples = []
    for s in selections :
        s = s.strip()
        print(s)
        examples.append(docs.get(where={"영역" : s})['documents'][0])

    area = ', '.join(selections)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    extra_record_prompt
    |llm
    |StrOutputParser()
    )
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "area" : area,
        "u_area" : data['unregistered_area'],
        "examples" : examples
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/ExtraSelf-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    print(1)
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        print(data)
        if data.get("custom") : 
            custom = data.get("custom").strip()
        else : 
            custom = ""

        docs = load_Document().Chroma_select_document("extra_record")
        selections = data['area']

        examples = []
        for s in selections :
            s = s.strip()
            print(s)
            examples.append(docs.get(where={"영역" : s})['documents'][0])

        area = ', '.join(selections)

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        extra_record_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
                    "area" : area,
                    "u_area" : custom,
                    "examples" : examples
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/ExtraClub")
async def process_data(data : dict):
    print(data)

    docs = load_Document().Chroma_select_document("extra_record")
    selections = data['area']

    examples = []
    for s in selections :
        s = s.strip()
        print(s)
        examples.append(docs.get(where={"영역" : s})['documents'][0])

    area = ', '.join(selections)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    extra_record_prompt
    |llm
    |StrOutputParser()
    )
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "area" : area,
        "u_area" : data['unregistered_area'],
        "examples" : examples
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/ExtraClub-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        print(data)
        if data.get("custom") : 
            custom = data.get("custom").strip()
        else : 
            custom = ""
            
        docs = load_Document().Chroma_select_document("extra_record")
        selections = data['area']

        examples = []
        for s in selections :
            s = s.strip()
            print(s)
            examples.append(docs.get(where={"영역" : s})['documents'][0])

        area = ', '.join(selections)

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        extra_record_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
                    "area" : area,
                    "u_area" : custom,
                    "examples" : examples
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/ExtraCareer")
async def process_data(data : dict):

    docs = load_Document().Chroma_select_document("extra_record")

    examples = []
    examples.append(docs.get(where={"종류" : "진로"})['documents'][0])
    examples = ', '.join(examples)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    career_prompt
    |llm
    |StrOutputParser()
    )
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "activities" : data['activities'],
        "examples" : examples,
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/ExtraCareer-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        activities = data.get("activities").strip()
            
        docs = load_Document().Chroma_select_document("extra_record")

        examples = []
        examples.append(docs.get(where={"종류" : "진로"})['documents'][0])
        examples = ', '.join(examples)

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        career_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
            "activities" : activities,
            "examples" : examples,
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/StudentFeature")
async def process_data(data : dict):
    print(data)

    docs = load_Document().Chroma_select_document("student_feature")

    features = ', '.join(data['features'])

    examples = []
    for f in data['features'] :
        examples.append(docs.get(where={"영역" : f})['documents'][0])
    examples = ', '.join(examples)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    student_feature_prompt
    |llm
    |StrOutputParser()
    )
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "description" : features,
        "examples" : examples,
        "length" : data['length'],
        "extra" : data['unregistered_features']
    })
    response = {"status": "success", "result": result}
    return response


@app.websocket("/StudentTrait-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        traits = data.get("features")
        custom_traits = data.get("custom_traits")
        length = data.get("length")

            
        docs = load_Document().Chroma_select_document("student_feature")

        features = ', '.join(traits)

        examples = []
        for f in data['features'] :
            examples.append(docs.get(where={"영역" : f})['documents'][0])
        examples = ', '.join(examples)

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        student_feature_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
            "description" : traits,
            "examples" : examples,
            "length" : length,
            "extra" : custom_traits
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/StudentFeatureSimple")
async def process_data(data : dict):
    print(data)

    docs = load_Document().Chroma_select_document("student_feature")

    examples = docs.as_retriever().batch([data['unregistered_features']])[0]
    example_data = []
    for i in examples :
        example_data.append(i.page_content)
    example_data = "\n".join(example_data)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    student_feature_simple_prompt
    |llm
    |StrOutputParser()
    )
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "description" : data['unregistered_features'],
        "examples" : examples,
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/StudentTraitSimple-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        custom_traits = data.get("custom_traits")

        docs = load_Document().Chroma_select_document("student_feature")

        examples = docs.as_retriever().batch([custom_traits])[0]

        example_data = []
        for i in examples :
            example_data.append(i.page_content)
        example_data = "\n".join(example_data)

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        student_feature_simple_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
            "description" : custom_traits,
            "examples" : examples,
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()

@app.post("/StudentFeatureRecord")
async def process_data(data : dict):
    print(data)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    student_feature_record_prompt
    |llm
    |StrOutputParser()
    )
    
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "input": data['features']
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/StudentTraitRecord-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        trait = data.get("trait")

        
        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        student_feature_record_prompt
        |llm
        |StrOutputParser()
        )

        async for chunk in chain.astream({
        "input": trait
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()


@app.post("/AssessmentPlanning")
async def process_data(data : dict):
    
    docs = load_Document().Chroma_select_document("assessment_planning")

    examples = docs.as_retriever().batch([data['as']])[0]

    achievement_standard = data['as']
    element = '평가요소도 함께 생성해주세요.' if data['element'] == '' else data['element']
    subject= data['subject']
    descriptive = data['descriptive_assessment']

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    assessment_planning_prompt
    |llm
    |StrOutputParser()
    )

    result = await chain.ainvoke({
        "example" : examples,
        "subject" : subject,
        "element" : element,
        "as" : achievement_standard,
        "descriptive" : descriptive
    })

    print(result)

    response = {"status": "success", "result": result}
    return response


@app.post("/PreschoolTrait")
async def process_data(data : dict):


    docs = load_Document().Chroma_select_document("preschool_trait")

    age = data['age'].strip()
    arealevel_dict = data['arealevel']


    examples = []
    traits = []  
    for area, level in arealevel_dict.items():
        traits.append(f"해당 학생의 {area} 영역은 {level} 수준입니다.")
        filter_criteria = {
                    "$and": [
                        {"나이": {"$eq": age}},
                        {"영역": {"$eq": area}},
                        {"수준": {"$eq": level}}
                    ]
                }
        
        print(filter_criteria)
        examples.append(docs.get(where=filter_criteria)['documents'][0])
    traits = '\n'.join(traits)
    examples = ', '.join(examples)

    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    )

    chain = (
    preschool_trait_prompt
    |llm
    |StrOutputParser()
    )
    
    # 비동기 처리 (예: 데이터 처리 시뮬레이션)
    result = await chain.ainvoke({
        "age" : age,
        "traits": traits,
        "examples" : examples
    })
    response = {"status": "success", "result": result}
    return response

@app.websocket("/PreschoolTrait-ws")
async def generate_websocket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive()
    data= json.loads(data['text'])

    try:
        age = data.get("age")
        arealevel_dict = data.get('arealevel')

        docs = load_Document().Chroma_select_document("preschool_trait")

        examples = []
        traits = []  
        for area, level in arealevel_dict.items():
            traits.append(f"해당 학생의 {area} 영역은 {level} 수준입니다.")
            filter_criteria = {
                        "$and": [
                            {"나이": {"$eq": age}},
                            {"영역": {"$eq": area}},
                            {"수준": {"$eq": level}}
                        ]
                    }
            
            print(filter_criteria)
            examples.append(docs.get(where=filter_criteria)['documents'][0])
        traits = '\n'.join(traits)
        examples = ', '.join(examples)

        llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini',
        verbose=False
        )

        chain = (
        preschool_trait_prompt
        |llm
        |StrOutputParser()
        )
    

        async for chunk in chain.astream({
        "age" : age,
        "traits": traits,
        "examples" : examples
                    }):
            # 웹소켓을 통해 각 청크 전송
            await websocket.send_text(chunk)
        
        # 스트리밍 종료 신호
        await websocket.send_text("[END]")

    except Exception as e:
        print(e)
        # 오류 처리
        await websocket.send_text(f"Error: {str(e)}")
    
    finally:
        await websocket.close()
