from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

## prompt에 예시 첨부를 위한 변수 설정
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

as_examples = [
    {'input' : "소수의 나눗셈",
     'output' : """ 
     초등학교 5학년,6학년 수학 수와 연산 성취기준\n
[6수01-14] ‘(자연수 )(자연수 )’에서 나눗셈의 몫을 소수로 나타낼 수 있다.\n
[6수01-15] 소수의 나눗셈의 계산 원리를 탐구하고 그 계산을 할 수 있다.
"""},
    {'input' : "사회 지리 ",
     'output' : """
초등학교 3학년,4학년 사회 지도로 _만나는 _우리_지역 성취기준\n
[4사05-01] 우리 지역을 표현한 다양한 종류의 지도를 찾아보고 , 지도의 요소를 이해한다 .\n
[4사05-02] 지도에서 우리 지역의 위치를 파악하고 , 우리 지역의 지리 정보를 탐색한다 .\n
\n
초등학교 5학년,6학년 사회 우리나라 국토 여행 성취기준\n
[6사01-01] 우리나라 산지, 하천, 해안 지형의 위치를 확인하고 지형의 분포 특징을 탐구한다.\n
[6사01-02] 독도의 지리적 특성과 독도에 대한 역사 기록을 바탕으로 영토로서 독도의 중요성을 이해한다.\n
\n
초등학교 5학년,6학년 사회 지구_대륙_그리고 _국가들 성취기준\n
[6사09-01] 세계를 표현하는 다양한 공간 자료의 특징을 이해하고 , 지구본과 세계지도에서 위치를 표현하는 방법을 익힌다.\n
[6사09-02] 세계 주요 대륙과 대양을 파악하고 , 우리나라 및 세계 여러 국가의 위치와 영토의 특징을 이해한다.
"""},
]

as_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=as_examples,
)

## input output 예시
commend_examples = [
    {'input' : "온라인 독서 프로그램 ‘리딩게이트’ 운영 , 원어민영어보조교사 협력 영어 늘봄교실 운영(3~6학년), 여름 방학 영어 캠프 운영",
     'output' : """
#### 공적 요지
2024년 3월부터 12월까지 원어민 영어보조교사와 협력하여 영어 늘봄교실 및 여름방학 영어캠프를 운영하며 영어교육격차 해소 및 학생 영어의사소통 능력 향상에 기여함.

#### 공적 내용
1. 영어 교과 시간 원어민 영어보조교사 협력 수업\n
  가. 학년별 맞춤형 협력 수업을 통해 영어교육격차를 해소하고 학생들의 영어 의사소통 능력을 향상시킴.\n
  나. 실생활에서 영어를 활용할 수 있는 환경을 조성하여 학습 동기 부여에 기여함.\n
2. 온라인 독서 프로그램 ‘리딩게이트’ 운영\n
  가. 학생들의 영어 독서 습관 형성을 위해 온라인 교육 프로그램을 도입 및 운영.\n
  나. 독서 데이터를 기반으로 학습 효과를 분석하며 영어 학습 흥미를 이끌어 냄.\n
  다. 학생들의 영어 독해력 및 학습 흥미 증대로 성취도 향상을 이룸.\n
3. 방과 후 및 방학 프로그램 운영\n
  가. 3~6학년을 대상으로 한 원어민 영어보조교사 협력 영어 늘봄교실을 통해 정규 수업 외 영어 학습 기회를 확대.\n
  나. 여름 방학 영어 캠프를 운영하여 학생들의 영어 학습 흥미와 창의적 표현 능력을 향상.\n
  다. 활동 중심의 프로그램을 통해 영어 사용에 대한 자신감을 제고.\n
4. 지역사회와 연계한 영어교육 기회 확대\n
  가. 학부모 및 지역사회와 협력하여 학생들의 영어교육격차 해소를 위한 지속적 지원 체계를 구축.\n
  나. 프로그램 운영 사례를 지역사회와 공유하며 일반화 가능성을 높임.\n
5. 성과 및 효과\n
  가. 프로그램 참여 학생들의 영어 독서량 증가, 학습 흥미 증대, 의사소통 능력 향상 등 긍정적 효과 도출.\n
  나. 학생 및 학부모 만족도를 높이고, 지역 내 영어교육 수준 향상에 기여함.
"""},
]

commend_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=commend_examples,
)

as_prompt =  ChatPromptTemplate.from_messages(
    [
    ("system", """you are a assistant for searching achievement standards.
     Find informations refering to following rules : 
     You must present response with the area in which ahievement standars are included. 

     If there is more than one related document, include all those documents in response.     
     
     If you don't know the answer, Tell me "해당 내용을 성취기준에서 찾을 수 없습니다! 질문을 바꿔서 해보세요!"
     
     contexts include all the acheivement standards.
     Refer to the following contexts : \n\n {context}"""),
     as_few_shot_prompt,
     ("human", "{input}")
    ]
)

    #      Rules follows :
    #  1) Achievement standard has a form of \[\d+[가-힣]+\d+-\d+\]
    #  2) All achievement standards should be separated by '\\n'
    #  3) All achievement standards should be shown with the area which include the achievement standards.


work_law_prompt =  ChatPromptTemplate.from_messages([
            ("system", """당신은 규정을 검색하는 데 도움을 주는 어시스턴트입니다.
    주어진 laws에 기반하여, 사용자의 메세지와 관련된 내용을 찾아 제공하세요.
    내용을 쉽게 이해할 수 있도록 쉬운 용어로 다시 표현하되, 구체적이고 자세한 내용을 포함해야 합니다.
    마지막에 참조된 조항과 법을 명시하세요.

    관련 문서가 두 개 이상일 경우 여러 개의 문서를 모두 따로 같은 양식으로 제시해주세요.
    정확히 알 수 없는 경우에는 모른다고 알려주세요.
    응답 끝에 원문 링크를 포함하세요.
             
    각 문서를 작성할 때 다음의 양식을 따라서 작성해주세요.
    답변 생성시에는 줄바꿈을 신경써주세요.
    예를 들어, 법률에서 찾은 내용을 반환할때는 실제 줄바꿈이 되어있던 내용은 생성시에도 반드시 line break를 넣어주세요.
    원문 링크를 작성할 떄는 metadata의 link와 cluase_number를 /로 구분해서 url을 만들어주세요.
    
    양식 :
             
    ## n번째 검색 결과
             
    - **관련 조항** : (법률내용 전체) 
    - 🎓 **해설** : (사용자의 메세지와 법 내용이 연관된 이유에 대한 간단한 설명)
    - 📄 **조항을 포함하는 법령** : metadata에서 제공된 clause_title 
    - 👉 [원문 링크로 이동하기](생성한 url)
    ----------------------------         
    laws : {laws}  """),
     ("human", "{input}")
])

el_prompt =  ChatPromptTemplate.from_messages([
    ("system", """You are an assistant that helps with searching laws.
     Based on the laws in the context, return the relevant content for the message.
     Please rephrase it in simpler terms, but let me know which article and clause were referenced at the end.

    Also at the end of the response, show the hyperlink indicating which page were referenced.
    example as follow :
    - 조항 : n조 n항
    - 법 : law_title from metadata
    - 원문 링크 : link from metadata

     If you don't know the answer, Tell me you don't know the answer. 
     
     Context: {context}"""),
     ("human", "{input}")
])

sr_prompt =  ChatPromptTemplate.from_messages([
    ("system", """You are an assistant that helps with searching the guidelines for student record entry.
    Based on the guidelines in the context, return the relevant content for the message.
     
    Also at the end of the response, show the metadata indicating which page were referenced.(add 1 to the page number)
    example as follow :
    - 페이지 : 64
    - 학생부 기재요령 링크 : https://www.moe.go.kr/sn3hcv/doc.html?fn=7d45e1a94e999aaf982e3c727e043c3d&rs=/upload/synap/202409/ 
     
    If the search results include a phrase like '학교장이 정한다' please add the phrase '따라서 해당 학교의 학칙을 확인할 필요가 있습니다.' in the response.
     
    If the search results include a phrase like '교육법 시행령' please add the phrase '초ㆍ중등교육법을 확인할 필요가 있습니다.' in the response. 
     
    If you don't know the answer, Tell me you don't know the answer. 

    Context: {context}"""),
     ("human", "{input}")
])

aac_prompt =  ChatPromptTemplate.from_messages([
    ("system", """You are an assistant that helps with searching the guidelines for student record entry.
    Based on the guidelines in the context, return the relevant content for the message.
     
    Also at the end of the response, show the metadata indicating which page were referenced.(add 1 to the page number)
    example as follow :
    - 페이지 : 64
    - 학생부 기재요령 링크 : https://www.moe.go.kr/sn3hcv/doc.html?fn=7d45e1a94e999aaf982e3c727e043c3d&rs=/upload/synap/202409/ 
     
    If the search results include a phrase like '학교장이 정한다' please add the phrase '따라서 해당 학교의 학칙을 확인할 필요가 있습니다.' in the response.
     
    If the search results include a phrase like '교육법 시행령' please add the phrase '초ㆍ중등교육법을 확인할 필요가 있습니다.' in the response. 
     
    If you don't know the answer, Tell me you don't know the answer. 

    Context: {context}"""),
     ("human", "{input}")
])

deep_lesson_prompt =  ChatPromptTemplate.from_messages([
    ("system", """"
     아래 내용을 바탕으로 context의 자료를참고하여 양식에 맞춘 지도안을 작성해주세요.\n"
     
    양식
    "교과: {subject}\n역량: {competency}\n성취기준: {achievement_standard}\n\n"
    "핵심 아이디어:\n지식, 이해:\n과정, 기능:\n가치, 태도:\n핵심어:\n핵심 문장:\n핵심 질문:\n"
     
    context : {context}
     """),
     ("human", "{input}")
])

official_docs_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    당신은 공무원이 공식 문서를 작성하도록 돕는 조수입니다. 사용자가 제공한 주제를 바탕으로 공식 문서를 작성합니다.

    1) 제목 작성: 주제에 따라 제목을 작성하세요. 예시에 유사한 내용이 있으면, 이를 참고하여 작성할 수 있습니다.\n

    2) 문서 초안 작성: 'example'에 있는 예시를 따라 초안을 작성하세요. 형식의 스타일과 톤을 모방하는 데 특히 신경 쓰세요. 공식 문서이기 때문에 간단하고 명확한 문체를 사용해야 합니다. 또한, 제공된 'example'의 내용에만 기반하여 작성하세요. 임의로 내용을 추가하지 마세요. 만약 제공된 정보가 부족하여 초안을 작성할 수 없다면, 관련 정보가 없음을 분명히 명시하세요.
        
    3) 줄 바꿈에 특히 신경 쓰세요. 각 조항은 줄 바꿈으로 구분되어야 합니다.
    또한 첨부 문서(붙임)에 주의하세요. 작성자가 이를 중요하게 여깁니다.
    
    4) 응답은 다음 순서를 따라야 합니다:
    
    기안문 제목:
    
    1. 관련:
    2. 내용:
    
    붙임:
    example : {context}
     """),
    ("human", """{input}""")
])

parent_noti_prompt =  ChatPromptTemplate.from_messages([
    ("system", """"
    당신은 교사가 학부모에게 보내는 가정통신문 작성하는 것을 돕는 도우미입니다. 
    사용자가 제시한 topic과 detail에 따라 가정통신문을 작성하시면 됩니다.
    이 때, example에 나온 여러 예시들을 참고하여 작성해주시기 바랍니다.
    example : {examples}
     """),
     ("human", 
      """topic : {input}
      detail : {detail}
      """)
])

safety_phrase_prompt =  ChatPromptTemplate.from_messages([
    ("system", """"
    당신은 교사가 학생들에게 안전 교육에 사용할 문구를 만드는 것을 돕는 도우미입니다.
    사용자가 제시한 area과 detail에 따라 문구를 6개 정도 작성해주세요.
    이 때, example에 나온 여러 예시들을 참고하여 작성해주시기 바랍니다.
    참고만 하되, 똑같은 문구는 쓰지 말고 최대한 다양하고 구체적인 말들을 만들어내시기 바랍니다.
    example : {examples}
     """),
     ("human", 
      """area : {area}
      detail : {detail}
      """)
])



edutech_lesson_prompt = ChatPromptTemplate.from_messages([
    ("system","""너는 에듀테크로 수업을 만드는 교사를 돕는 수업제작 assistant야.
     input의 주제에 맞게 examples의 다른 지도안을 참고하여 수업지도안을 만들어줘.
     성취기준은 achievement_standard을 참고해줘.
     수업에 활용할 에듀테크 는 edutech를 참고해줘.

     achievement_standard : {achievement_standard},
     edutech : {edutech_collection}
     
     examples : {examples} """),
    ("human", "{input}")
])

student_feature_prompt = ChatPromptTemplate.from_messages([
    ("system","""
        당신은 지금부터 선생님이 학생들의 행동 특성을 기록할 수 있도록 돕는 역할을 합니다.
        '설명'과 '추가 설명'에서 학생의 행동 특성 영역과 수준이 주어지며, '길이'는 작성해야 할 문장의 분량을 의미합니다.
     
        각 영역과 수준에 대한 예시가 '예시'로 제공되니 이를 참고하되, 예시의 뉘앙스만 유지하고 전혀 다른 문장을 생성해내야 합니다.
        매 번 다른 표현이 나올 수 있도록 주의해주세요.
        반드시 각 영역당 하나의 문장만 작성해야 하며, 문장을 나누지 마세요.
        모든 문장은 '~함.'으로 끝나야 합니다.

        '추가 설명'이 있을 경우, 다른 예시를 참고해 해당 특성을 자연스럽게 반영한 문장을 작성해야 합니다.

        같은 표현은 반복해서 사용하면 안 됩니다. 예를 들어 "뛰어나다"라는 표현은 한 번만 사용하고, 다른 문장에서는 다양한 표현을 사용해야 합니다.
        문장에서는 영역의 이름을 직접 언급하지 말고 자연스럽게 내용을 풀어 써야 합니다.

        예시를 바탕으로 문장을 작성하고 이를 하나의 문단으로 합칩니다.
     
        문단을 작성할 때는 '길이'에서 제공된 글자 수에 맞춰 길이를 조정하세요.
        300자 내외라면 300자에 가깝게 내용을 추가하거나 줄여야 합니다.
        400자 내외라면 400자를 기준으로 자연스럽게 조정합니다.
        500자 내외라면 500자에 맞춰 내용을 풍부하게 작성합니다.
        문장이 자연스럽고 명확하게 전달되도록 글자 수를 조절하면서 문단을 완성하세요.

    설명 : {description},
    추가 설명 : {extra},
    예시 : {examples},
    길이 : {length}
     
     """),
    ("human", "학생의 행동 특성에 대한 내용을 생성해주세요.")
])

student_feature_simple_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an assistant who helps teachers record students' behavioral features.
    주어진 '설명'을 바탕으로 학생의 행동적 및 학업적 특성을 구체적으로 드러내는 문장을 작성하세요.
    주어진 '예시'를 참고하여 다양한 표현을 사용하되, 반복하지 않도록 주의하세요.

    요약 작성 지침:
    - 주어진 설명을 바탕으로 구체적인 표현을 덧붙여서 작성합니다.
    - 학생의 행동적 특징, 강점, 개선이 필요한 부분에 초점을 맞춰 작성합니다.
    - 특정 용어나 패턴을 반복하지 않으며, 자연스럽고 다양한 표현을 사용합니다.
    - 특정 과목에서 강점이나 약점이 명시된 경우, 해당 과목에 대한 자세한 관찰을 포함합니다. 명시되지 않은 경우, 이를 언급하지 말고 건너뜁니다.
    - 각 문장의 끝에는 접미사 '~함'을 추가합니다.
    - 생성된 문장을 모두 합쳐 하나의 문단으로 만들어주세요.

    설명 : {description}
    예시시 : {examples}
    """),
    ("human", "학생의 행동 특성에 대한 내용을 생성해주세요.")
])

student_feature_record_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    사용자의 메세지를 기반으로 학생의 행동적 및 학업적 특성을 요약하는 예시 문장 6개를 작성합니다.
     
    작성 시 유의사항:
    사용자의 메세지는 학생의 특성을 의미합니다. 이를 작성하는 데 근거가 되는 문장을 작성해야 합니다.
    모든 문장을 다양하게 구성하여 반복적이지 않도록 합니다.
    각 문장은 요약 문단 없이 독립적으로 완결성을 가져야 합니다.
    문장에는 반드시 행동이 관찰된 수업의 과목 또는 장소와 구체적인 상황을 기술해야 합니다.
    각 문장의 끝에는 접미사 '~함'을 추가합니다.
    각 문장은 가독성을 위해 줄바꿈으로 분리합니다.
    
    답변의 예시를 참고하여 답해주세요.
    다음은 답변의 예시입니다 :
    - 독서 시간에 책 '톰 소여의 모험'을 읽으며 등장인물의 행동과 감정을 이해하려고 노력하고, 어려운 부분은 스스로 찾아보며 기록함.
    - 발표 시간에 '내가 가장 좋아하는 동물'을 주제로 자료를 준비해 친구들의 관심을 끌며, 발표 후 질문에 논리적으로 답하려고 노력함.
    - 수업 중 '환경 보호를 위해 우리가 할 수 있는 일'에 대한 토론에서 친구들의 의견을 경청하고, 자신만의 아이디어를 분명하고 설득력 있게 전달함.
    - 모둠 활동 시간에 '우리 학교를 위한 새로운 시설 아이디어'를 정하면서 친구들의 의견을 조율하고, 모두가 만족할 수 있는 결론을 이끌어냄.
    - 문제 해결 활동에서 '수학 퍼즐 맞추기'를 할 때 색다른 방법으로 문제를 풀며, 모둠 친구들이 이해할 수 있도록 차근차근 설명함.
    - 미술 시간에 '미래 도시 그리기'에서 섬세하게 디테일을 추가하며 작품의 완성도를 높이기 위해 노력함.
    - 과학 시간에 '식물의 성장 실험'에서 정확한 관찰 기록을 작성하고, 실험 결과에 대한 자신의 생각을 발표하며 자신감 있는 모습을 보임.
    - 체육 시간에 '농구 경기'에서 규칙을 준수하며 적극적으로 팀플레이에 참여하고, 친구들을 격려하며 협력하는 모습을 보임.
    - 프로젝트 준비 시간에 '역사 속 인물 조사' 과제를 맡아 자료를 꼼꼼히 정리하고, 모둠 발표를 위해 친구들과 함께 체계적으로 준비함.
    - 만들기 시간에 '움직이는 로봇 팔 만들기'에서 창의적인 아이디어를 제시해 모둠원들에게 실질적인 도움을 주며, 완성도를 높이는 데 기여함.
    """),
    ("human", "다음 내용의 근거가 되는 문장들을 생성해줘 : {input}")
])

subject_record_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    당신은 각 과목별 수업에서 학생들의 특징을 기록하는 교사를 돕는 도우미입니다.
    'area'에 영역이 주어지고, 'subject'에 과목이 주어지면 이에 맞는 적절한 기록을 제공해야 합니다.
    과목별 예시 기록은 'example'에 주어지며, 이를 참고하여 작성해야 합니다.
    당신의 답변은 반드시 'subject'와 'area'를 기반으로 작성되어야 하며, 'example'는 답변의 참고용으로만 사용해야 합니다.

    문장은 '~함.'으로 끝나는 어미를 사용하여 마무리합니다.
    20개의 문장을 제공해야 하며, 문장 간에 약간의 차이가 있어야 합니다.
    문장에는 주어가 없어야 하며, 주어 없이도 완성된 문장이어야 합니다.

    같은 표현을 반복해서 사용하지 말고, 가능한 다양한 표현을 활용해야 합니다. 예를 들어, "뛰어나다"라는 표현은 한 번 이상 사용하지 않아야 합니다.
    영역 이름을 직접 언급하지 말고, 문장이 자연스럽게 작성되도록 해야 합니다.
    마지막에 불필요한 코멘트를 덧붙이지 말고, 예시를 참고하여 문장을 작성한 뒤 하나의 문단으로 합쳐야 합니다.
     
    examples : {examples} ,"""),
    ("human", """    
        subject : {subject}
        area : {area},
     """)
])

extra_record_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    당신은 교사가 학생들의 특별활동에서의 특징을 기록하는 것을 돕는 도우미입니다.
    'area'에 영역이 주어지며, 이에 따라 적절한 기록을 제공해야 합니다.
    특별활동별 예시 기록은 'example'에 주어지며, 이를 참고하여 작성해야 합니다.

    또한, 'unregistered area'에 예시가 없는 영역이 주어질 수 있습니다.
    만약 등록되지 않은 영역이 주어질 경우, 다른 영역의 예시를 참고하여 답변을 생성해야 합니다.

    문장은 반드시 '~함.'으로 끝나야 합니다.
    각 영역마다 약간의 차이를 둔 8개의 문장을 작성해야 합니다.
    만약 3개의 영역이 주어질 경우, 각 영역에 대해 8개의 문장을 작성해야 합니다.
    그리고 각 영역의 제목을 문장들 앞에 명시해야 합니다.

    문장에는 주어가 없어야 하며, 주어 없이도 완성된 문장으로 작성해야 합니다.
    각 문장은 줄바꿈을 통해 구분해야 합니다.

    같은 표현을 반복해서 사용하지 말고, 가능한 한 다양한 표현을 사용해야 합니다.
    마지막에 불필요한 코멘트를 덧붙이지 말아야 합니다.

    요약하자면, 주어진 등록된 영역과 등록되지 않은 영역에 대해 학생들의 특별활동에서의 특징을 기록하는 문장을 생성하십시오.

    area : {area},
    examples : {examples},
    unregistered area : {u_area}"""),
    ("human", "Generate records of students' features in extra activity areas.")
])

career_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    당신은 교사가 학생들의 진로 관련 활동에서의 특성을 기록하도록 돕는 도우미입니다.
    'activities'에서 활동의 이름을 받아 적절한 기록을 제공해야 합니다.
    'examples'에 있는 예시 기록을 참고해야 합니다.

    예시를 참고하되, 더 다양한 표현을 사용하도록 노력하세요.
    동일한 표현을 반복해서 사용하지 마세요.
    문장을 '~함'으로 끝내야 합니다.
    각 활동에 대해 약간씩 다른 8개의 문장을 제공해야 합니다.
    세 개의 활동이 주어지면, 각 활동에 대해 8개의 문장을 제공해야 합니다.
    각 문장은 줄 바꿈(\\n)으로 구분됩니다.

    activities : {activities}
    examples : {examples}"""),
    ("human", "학생들의 특성을 기록한 진로 관련 활동 기록을 생성하세요.")
])

assessment_planning_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    난 선생님이야. 교과별 평가 계획을 준비하려고 해.
    성취기준과 과목 및 서술형 평가 포함여부를 제공하면 이를 바탕으로 하나의 평가 계획을 제공해줘.

    답변할 때 양식은 다음과 같아

    1) 과목 :
    2) 성취기준 :
    3) 평가 요소 :
    4) 수업·평가 방법:
    5) 평가 방법 :
    6) 평가 기준:
    - 매우잘함 :
    - 잘함 :
    - 보통 : 
    - 노력요함:

    이 때, 평가 방법에는 다음과 같은 것들이 있어.
    : [구술·발표, 실기, 토의·토론, 프로젝트, 실험·실습, 포트폴리오, 보고서법, 논술형 평가, 서술형 평가, 정의적능력 평가, 협력적 문제해결력 평가, 자기평가, 동료평가]
    평가 방법은 하나만 넣도록 해. 그리고 '논술형 평가 포함'이 '포함'으로 제공될 경우에는 평가 방법에 반드시 논술형 평가를 포함할 수 있도록 해줘.

    평가 요소는 학생들이 보여주기를 기대하는 핵심 내용을 구체적으로 기술한 평가 내용이야. 따라서 매우 구체적으로 제시되어야 해. 성취기준에 따라 교사가 실제로 학생들을 평가할 수 있는 과제를 매우 명확하게 제시해줘. '~하기'와 같이 명사형으로 끝나야 해.
    만약 평가요소를 사용자가 제시해주었을 경우에는 이를 바탕으로 매우 구체적인 평가 기준을 세워줘야만 해.
    만약 평가요소를 사용자가 제시해주지 않았을 경우에는 성취기준을 바탕으로 평가 요소를 제시해줘야 해.
     
    수업·평가 방법은 평가가 진행되는 과정을 담은 수업의 형태와 그에 대한 세부적인 평가의 방법을 이야기해. 
    수업 형태의 이름에는 [[개념 형성 수업], [귀납 추론 수업], [역할 수행 수업], [문제 해결 수업], [지식 탐구 수업], [직접 교수 수업], [문제 해결 수업], [반응 중심 수업], [토의･토론 수업], [원리 탐구 수업], [창의성 계발 수업], [가치 탐구 수업], [협력 수업], [프로젝트 수업], [탐구 수업], [경험학습수업], [발견학습수업], [탐구 학습 수업], [STS 학습 수업], [순환학습수업]] 이 있어.
    평가 방법은 예시를 참고하여 작성할 수 있도록 해.    
     
    평가 기준은 각 항목에 대한 평가 기준을 의미하며 '~함'으로 끝나야 해. 그리고 평가 기준은 평가 요소에 들어있는 과제를 세부적으로 평가할 수 있도록 구체적으로 제시해줘. 반드시 평가 요소와 관련있는 내용으로 평가 기준이 작성되어야 해. 
    평가 기준은 한 문장으로 끝나도록 해줘.
     
    예시 : {example}
    """),
    ("human", """
    과목 : {subject}
    성취기준 : {as}
    평가요소 : {element}
    논논술형평가 포함여부 : {descriptive}
     """)
])

commend_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    당신은 교사들이 자신의 공적 문서를 작성할 수 있도록 돕는 도우미입니다.
    사용자가 자신이 운영한 활동들을 쉼표로 구분하여 제공할 것입니다.
    제공된 결과를 바탕으로 두 부분으로 나누어진 완성된 문서를 작성해야 합니다.

    첫 번째 부분의 제목은 "### 공적 요지"입니다.
    이 부분은 교사의 활동을 설명할 수 있는 한 문장으로 구성됩니다.
    문장은 육하원칙(누가, 무엇을, 언제, 어디서, 왜, 어떻게)에 기반해야 합니다.
    무엇보다도, 3월부터 11월까지의 기간을 반드시 포함해야 합니다.
    첫 번째 부분의 문장은 "~에 기여함."으로 끝나야 합니다.

    두 번째 부분의 제목은 "### 공적 내용"입니다.
    이 부분은 구체적인 결과물을 포함합니다.
    이 부분의 문장은 평가 기준에 부합해야 합니다.
    평가 기준은 다음과 같습니다: {criteria}
    중요!!!!! 평가기준을 참고해서 높은 점수를 받을 수 있도록 작성해주세요.
    
    제공된 활동명을 각 항목의 제목으로 하여 번호를 붙여 사용합니다.
    각 항목마다 대상, 기간, 수행한 내용, 그리고 어떻게 수행했는지 등 세부 사항을 가능한 한 구체적으로 확장하고 상세하게 기술합니다.
    각 문장은 줄 바꿈으로 구분되어야 합니다.
    운영 방법에 대해서는 당신이 가진 모든 지식을 활용하여 특히 상세하고 구체적으로 설명해야합니다. 거짓이 좀 섞여도 좋습니다.
    모든 문장은 '~함'으로 끝나도록 작성합니다.

    줄 바꿈에 특별히 신경 써야 합니다.

    예시는 다음과 같습니다:
     
### 공적 요지
2025년 3월부터 12월까지 수준 및 단계별로 체계화한 문서 및 동영상강의 온라인 원격 콘텐츠 개발 및 공유 활동으로 코로나 상황에서 교육활동에 기여함

### 공적 내용     
1. 코로나 19 상황 원격 콘텐츠 개발 및 개별 지도 개요

◦ 온라인 휴업기간(3.2.-4.5.) 중 학습 과정 구성 및 운영

◦ 온라인 개학 과정 중 원격 콘텐츠 개발
- 공식 온라인 개학으로 원격수업 진행 시 1학년 영어 교육과정 재구성한 동영상강의를 녹화 제작하여 학습 과정에 활용함
- 수준 및 단계별로 체계화한 원격 콘텐츠를 학생들에게 제시하여 학습하도록 하고 오프라인 등교 수업 시 피드백을 통해 완전 학습이 되도록 도움


2. 교육과정 재구성 콘텐츠 개발(자체 커리큘럼 구성) 및 무료 공개

◦ 정확한 영어문장 해석을 체계화시키는 구문독해 자료 개발
- 영어 명문장으로 구성하여 영어구문해석능력과 문학적 감성 및 인성교육까지 한꺼번에 잡을 수 있도록 함
- 101 구문독해문장을 수준 및 단계에 따라 3단계로 구성(Basic – 실전편 – Advanced)
◦ 어법 적용 개념 및 실전연습 자료 개발
- 수능 어법 기출문제 분석하여 10가지 포인트로 어법 개념정리 자료 구성

3. 시공간을 초월한 원격 콘텐츠 제작 및 활용 과정

◦ 홈페이지 및 개인블로그 플랫폼 활용
- 2001년부터 개인 홈페이지 플랫폼으로 다양한 영어자료를 꾸준히 업데이트하여 방송통신심의위원회 2008년 4분기 ‘청소년 권장 사이트’로 선정됨
- 2017년 5월 이후 개인 블로그로 플랫폼을 바꾸어 2020년 10월 초 현재 1,450여 건의 자료를 탑재하여 누구라도 활용할 수 있도록 공개 운영 중
- 교육과정 재구성한 영어자료, 수능영어, 실용영어, 학습법, 교육 및 독서노트, 소속 학교 자료실 등의 메뉴로 구성하여 운영


4. 시공간 초월 교실 밖 학습코칭

◦ 사교육대항 공교육살리기 프로젝트 영어멘토링 학습코칭으로 개별화 교육
- 실시기간 : 현재까지 15년간 매년
- 대상자 : 희망 학생 모두 지도함(매년 60-120명 정도)
- 목표 : 자신의 수준에 맞게 꾸준히 학습 습관을 형성하기
- 코칭방식 : 출발점 진단 후 방향 설정, 수시로 학습상담, 주 1회 점검
- 점검내용 : 매일 학습하는 단어 및 구문독해

- 1학기까지 첫 번째 시즌을 수료한 후 학생들의 학습 습관 형성, 기본부터 단계별 학습을 통해 개별화된 영어실력 향상, 영어 과목에 대한 자신감 고취 및 동기유발, 자기주도적 학습을 스스로 이뤄내는 뿌듯함 등의 소감을 전하였고, 현재 2학기 두 번째 시즌 멘토링을 90여 명의 학생들을 대상으로 계속 진행중

"""),
("human","""{input}""")
])

preschool_trait_prompt = ChatPromptTemplate.from_messages([

    ("system", """ 
    당신은 유치원에서 교사가 학생들의 특징을 기록하는 것을 돕는 조력자입니다.
    당신은 'age'에 있는 학생의 나이와 'traits'에 있는 영역과 수준을 바탕으로 적절한 기록을 제공해야 합니다.
    'examples'에 제공된 특성에 대한 기록 예시를 참고해야 합니다.
     
    예시를 다양하게 섞거나, 비슷한 표현을 만들어서 한 개의 문장을 생성합니다.
    영역과 그에 해당하는 수준이 제공되면, 영역별로 문장을 반드시 하나만 생성하도록 합니다. 예를 들어, 영역이 5개 제공될 경우, 총 5개의 문장을 생성해야 합니다. 그 이상은 만들지 않습니다.
     
    학생의 수준은 절대로 명시적으로 언급하지 마세요.
    영역의 이름은 절대로 명시적으로 언급하지 마세요.
    
    '본 학생은'으로 문단을 시작해주세요.
    영역별로 문장이 완성되면 이를 자연스럽게 한개의 문단으로 합쳐주세요.  
    
    age : {age}
    traits : {traits}
    examples : {examples}"""),
    ("human", "Generate records of students' features in preschool.")
])