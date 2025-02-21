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

class SubjectData(BaseModel) :
    area : str
    subject : str
    examples : str

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

# @app.post("/DescriptionFeedback")
# async def process_data(data : dict):
#     columns = data['target'][0]
#     target = data['target'][1:]
#     eval_df = pd.DataFrame(target, columns=columns)
#     names = eval_df.iloc[:,-2]

#     feedback_targets = eval_df.iloc[:,-1]
#     numbers = eval_df.iloc[:,-3]

#     print(data['criteria']['integration'])
    
#     prompt = ChatPromptTemplate.from_messages([
#         ('system',"""
#         너는 지금부터 학생의 서술형 평가 답변에 대한 피드백을 작성할거야.
    
#         피드백 평가 요소는 다음과 같아 :  {elements}
#         각 평가 요소에 대한 수준별 기준은 다음과 같아. {integration}

#         이 외에도 평가에 반영해야 하는 요소는 다음과 같아 : {extra} 

#         위 기준을 참고하여 각 평가 요소 별로 수준을 체크해주고, 더 나은 답변을 작성할 수 있도록 피드백을 제공해줘.

#         피드백 양식은 다음과 같아. 만약 평가 요소가 여러개라면 반드시 평가요소별로 피드백을 제공해줘.
#         - 수준 : (평가 요소 - 평가 수준 순서대로 써줘.)
#         - 피드백 : (여기에 학생의 결과물에 대한 피드백을 써줘. 평가 요소가 여러개일 경우, 각각에 대한 피드백을 작성해줘.)
        
#         """),
#         ('human','피드백을 제공해주어야 하는 학생의 답변은 다음과 같아. : {input}')
#         ])
    
#     llm = ChatOpenAI(
#     temperature=0.5,
#     model='gpt-4o-mini',
#     verbose=False
#     ) 

#     chain = (
#         prompt
#         | llm
#         | StrOutputParser()
#     )

#     feedback_results = {}
#     for i, t in enumerate(feedback_targets) :
#         # WebSocket 상태 전송
#         for websocket in connected_clients:
#             await send_websocket_update(f"현재 {names[i]} 학생에 대한 피드백을 작성하는 중입니다...")

#         result = await chain.ainvoke({
#         "extra" : data['extra'],
#         "elements" : data['criteria']['elements'],
#         "integration" : data['criteria']['integration'],
#         "input" : t
#         })
#         feedback_results[names[i]] = (str(numbers[i]), t, result)
        
#         print(names[i],type(names[i]),numbers[i],type(numbers[i]), t, type(t), result, type(result))
        
#     for websocket in connected_clients:
#         await send_websocket_update(f"피드백 작성을 완료하였습니다.")

#     # print(feedback_results)    
#     response = {"status": "success", "result": feedback_results}
#     return response

# async def send_websocket_update(message: str):
#     """
#     연결된 모든 WebSocket 클라이언트에 메시지 전송
#     """
#     for websocket in connected_clients:
#         try:
#             await websocket.send_text(message)
#         except Exception as e:
#             print(f"Error sending WebSocket message: {e}")
#             connected_clients.remove(websocket)  # 문제 발생 시 클라이언트 제거



@app.post("/DescriptionFeedbackTEST")
async def process_data(data : dict):

    print(data['criteria']['integration'])
    prompt = ChatPromptTemplate.from_messages([
        ('system',"""
        너는 지금부터 학생의 서술형 평가 답변에 대한 피드백을 작성할거야.
    
        피드백 평가 요소는 다음과 같아 :  {elements}
        각 평가 요소에 대한 수준별 기준은 다음과 같아. {integration}

        이 외에도 평가에 반영해야 하는 요소는 다음과 같아 : {extra} 

        평가 요소에 대한 수준별 기준을 참고하여 각 평가 요소 별로 수준을 체크해주고, 더 나은 답변을 작성할 수 있도록 피드백을 제공해줘.
        수준을 체크할때는 엄격하게 평가해주어야 해.

        피드백 양식은 다음과 같아. 만약 평가 요소가 여러개라면 반드시 평가요소별로 피드백을 제공해줘.
        - 수준 : (평가 요소 - 평가 수준 순서대로 써줘.)
        - 피드백 : (여기에 학생의 결과물에 대한 피드백을 써줘. 평가 요소가 여러개일 경우, 각각에 대한 피드백을 작성해줘.)
        
        """),
        ('human','피드백을 제공해주어야 하는 학생의 답변은 다음과 같아. : {input}')
    ])

    print(prompt)


    llm = ChatOpenAI(
    temperature=0.5,
    model='gpt-4o-mini',
    verbose=False
    ) 

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )
    results = []
    for t in data['target'] :
        result = await chain.ainvoke({
        "extra" : data['extra'],
        "elements" : data['criteria']['elements'],
        "integration" : data['criteria']['integration'],
        "input" : t
        })
        results.append(result)
    response = {"status": "success", "result": results}
    return response

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
