from fastapi import FastAPI, Form, File, UploadFile, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from app.set_documents import load_Document
from app.set_prompt import *
from tools.hwp_parser import HWPExtractor
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from io import BytesIO
import pandas as pd
import langchain
import json

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
    extractor = HWPExtractor(file_obj)  # file_obj는 BytesIO
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

connected_clients = set()

@app.websocket("/ws/DescriptionFeedbackProgress")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 연결을 수락하고 연결된 클라이언트를 관리합니다.
    """
    await websocket.accept()
    connected_clients.add(websocket)
    # 연결된 클라이언트 추가
    try:
        while True:
            # WebSocket 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            print(f"Received from client: {data}")
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        connected_clients.remove(websocket)  # 연결 끊긴 클라이언트 제거
        print("WebSocket disconnected")

@app.post("/DescriptionFeedback")
async def process_data(data : dict):
    columns = data['target'][0]
    target = data['target'][1:]
    eval_df = pd.DataFrame(target, columns=columns)
    names = eval_df.iloc[:,-2]

    feedback_targets = eval_df.iloc[:,-1]
    numbers = eval_df.iloc[:,-3]

    print(data['criteria']['integration'])
    
    prompt = ChatPromptTemplate.from_messages([
        ('system',"""
        너는 지금부터 학생의 서술형 평가 답변에 대한 피드백을 작성할거야.
    
        피드백 평가 요소는 다음과 같아 :  {elements}
        각 평가 요소에 대한 수준별 기준은 다음과 같아. {integration}

        이 외에도 평가에 반영해야 하는 요소는 다음과 같아 : {extra} 

        위 기준을 참고하여 각 평가 요소 별로 수준을 체크해주고, 더 나은 답변을 작성할 수 있도록 피드백을 제공해줘.

        피드백 양식은 다음과 같아. 만약 평가 요소가 여러개라면 반드시 평가요소별로 피드백을 제공해줘.
        - 수준 : (평가 요소 - 평가 수준 순서대로 써줘.)
        - 피드백 : (여기에 학생의 결과물에 대한 피드백을 써줘. 평가 요소가 여러개일 경우, 각각에 대한 피드백을 작성해줘.)
        
        """),
        ('human','피드백을 제공해주어야 하는 학생의 답변은 다음과 같아. : {input}')
        ])
    
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

    feedback_results = {}
    for i, t in enumerate(feedback_targets) :
        # WebSocket 상태 전송
        for websocket in connected_clients:
            await send_websocket_update(f"현재 {names[i]} 학생에 대한 피드백을 작성하는 중입니다...")

        result = await chain.ainvoke({
        "extra" : data['extra'],
        "elements" : data['criteria']['elements'],
        "integration" : data['criteria']['integration'],
        "input" : t
        })
        feedback_results[names[i]] = (str(numbers[i]), t, result)
        
        print(names[i],type(names[i]),numbers[i],type(numbers[i]), t, type(t), result, type(result))
        
    for websocket in connected_clients:
        await send_websocket_update(f"피드백 작성을 완료하였습니다.")

    # print(feedback_results)    
    response = {"status": "success", "result": feedback_results}
    return response

async def send_websocket_update(message: str):
    """
    연결된 모든 WebSocket 클라이언트에 메시지 전송
    """
    for websocket in connected_clients:
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending WebSocket message: {e}")
            connected_clients.remove(websocket)  # 문제 발생 시 클라이언트 제거



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
    print(data['activities'])

    docs = load_Document().Chroma_select_document("official_document")

    examples = docs.get(where={"category" : data['category']})['documents'][0]
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

    print("공문 생성기 : ",data['topic'])

    result = await chain.ainvoke({
        "input" : data['topic'],
        "context" : examples
    })
    response = {"status": "success", "result": result}
    return response



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

@app.post("/ExtraCareer")
async def process_data(data : dict):
    print(data)

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


@app.post("/PreschoolTrait")
async def process_data(data : dict):
    print(data)

    docs = load_Document().Chroma_select_document("preschool_trait")

    age = data['age'].strip()
    arealevel_dict = json.loads(data['arealevel'])

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

