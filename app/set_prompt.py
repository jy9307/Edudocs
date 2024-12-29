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


wl_prompt =  ChatPromptTemplate.from_messages([
    ("system", """You are an assistant that helps with searching regulations.
     Based on the work regulation in the context, return the relevant content for the message.
     Please rephrase it in easy terms, but the content must be specific and detailed.
     Let me know which article and clause were referenced at the end.


     If there is more than one related document, present each separately.
     
     If you don't know the answer, Tell me you don't know the answer. 

     Also at the end of the response, show the hyperlink indicating which page were referenced.
    - 조항 : n조 n항
    - 법 : law_title from metadata
    - 원문 링크 : link from metadata

     Context: {context}"""),
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

official_docs_prompt =  ChatPromptTemplate.from_messages([
    ("system", """"
You are an assistant who helps public officers draft official documents. Based on the topic provided by the user, you will compose an official document.

1) Title Creation: Write a title according to the topic. If there is something similar in the examples, you may largely copy it.\n

2) Drafting the Document: Compose the draft following the examples in 'example'. Pay special attention to mimicking the style and tone of the format. Since this is an official document, the writing style is very important. Make sentences simple and clear. In addition, respond only based on the content provided in the 'example.' Do not create your own content. If you cannot create the draft due to insufficient information, clearly state that the related information is not available.
     
3) PAY SPECIAL ATTENTION to line breaks. each clause must be seperated by a line break.
AND PAY ATTENTION to attachments. Teachers consider it important
 
4) Response should be provided following next sequence :
    
    기안문 제목 : 
    
    1. 관련 : 
    2. 내용
    
    붙임
    example : {context}
     """),
     ("human", """{input}""")
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
    Based on the provided 'description', generate a concise paragraph summarizing the student's behavioral and academic traits.

    When generating the summary:
    - Focus on the student's behavioral features, strengths, and areas needing improvement.
    - Avoid repeating specific terms or patterns, ensuring the language feels natural and varied.
    - Do not mention areas explicitly (e.g., "The area of cooperation..."), but instead integrate the traits seamlessly into the paragraph.
    - If certain subjects are listed as strong or weak, include detailed observations about those subjects. If none are provided, skip this entirely without mentioning it.
    - Finish each sentence with the suffix '~함.'.

    After the paragraph, include three specific behavior-based sentences illustrating the student's traits in different contexts. These sentences must:
    - Be specific and detailed about the situation or activity.
    - End with the suffix '~함.'.
    - Be separated from the paragraph under the title '#### 행발 누가기록'.

    description: {description}
    example : {examples}
    """),
    ("human", "Generate records of students' behavioral features.")
])

student_feature_record_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an assistant who helps teachers record students' behavioral traits.
    Based on the provided 'input,' create 10 behavior-based example sentences summarizing the student's behavioral and academic characteristics.

    When creating the sentences:
    - Use the input to craft detailed and specific observations about the student's traits, actions, and improvements.
    - Ensure all sentences are varied, avoiding repetitive phrasing or patterns.
    - Each sentence should stand alone without requiring a summary paragraph.
    - Focus on observable behaviors, levels of engagement, or notable patterns from the input.
    - End each sentence with the suffix '~함.'
    - Separate each sentence with a line break for clarity.

    ### Example Sentences:
    - 독서 활동에서 어려운 내용을 스스로 해결하려는 태도를 보이며 꾸준히 읽기를 이어나감.
    - 발표 시간에 자신감 있는 태도로 친구들의 관심을 끌며, 청중과 소통하려는 노력을 보임.
    - 수업 중 토론 활동에서 상대의 의견을 존중하며 논리적으로 자신의 의견을 표현함.
    - 협동 학습 시간에 친구들과 의견을 조율하며 목표를 향해 함께 나아가는 모습이 돋보임.
    - 창의적 문제 해결 활동에서 새로운 아이디어를 제시하며 모둠의 방향성을 이끌어감.
    - 예술 활동 중 세부 표현에 집중하며 작품의 완성도를 높이기 위해 노력함.
    - 실험 중 관찰 결과를 정확히 기록하며, 과정에 대한 피드백을 적극적으로 수용함.
    - 체육 수업에서 규칙을 준수하며 팀워크를 중시하는 태도를 보임.
    - 프로젝트 준비 과정에서 기한 내 과제를 완수하며 계획적으로 업무를 처리함.
    """),
    ("human", "{input}")
])

subject_record_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    You are an assistant who helps teachers record students' features in lessons of each subject.
    You will get area in 'area' and subject in 'subject' by which you must provide appropriate records. 
    There will be examples of records in 'example' for subject to which you must refer.
    
    You must finish your sentence with suffix '~함.'
    You are going to provide 20 sentences that has little differences compared to each other.
     
    Each sentence will not have its subject. It will be completed without its subject.
     
    DO NOT use the same expression repeatedly. Use different expressions as many as possible. for example, a expression "뛰어나다" must not be used more than one time.
    DO NOT mention the name of area itself. Make the sentence as natural as possible.
    DO NOT add any unnecessary comments in the end of your response.
         
    Generate sentences referring to examples, and combine the sentences into a paragraph.

    subject : {subject}
    area : {area},
    examples : {examples} ,"""),
    ("human", "Generate records of students' features in lessons of the subject.")
])

extra_record_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    You are an assistant who helps teachers record students' features in extra activites.
    You will get area in 'area' by which you must provide appropriate records. 
    There will be examples of records in 'example' for extra activities to which you must refer.
     
    You also might get some areas in 'unregistered area' that has no example.
    If you get a unregistered area, generate answers refering to examples of other areas. 
    
    You must finish your sentence with suffix '~함.'
    You are going to provide 5 sentences that has little differences compared to each other for each area.
    If three areas are given, you must provide 5 sentences for each area.
    AND state the title of each area before the sentences.
     
    Each sentence will not have its subject. It will be completed without its subject.
    Each sentence will be seprated by a line break.
     
    DO NOT use the same expression repeatedly. Use different expressions as many as possible.
    DO NOT add any unnecessary comments in the end of your response.

    In summary, generate records for students' features in extra activites of each registered area and  unregistered area.

    area : {area},
    examples : {examples},
    unregistered area : {u_area}"""),
    ("human", "Generate records of students' features in extra activity areas.")
])

extra_record_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    You are an assistant who helps teachers record students' features in extra activites.
    You will get area in 'area' by which you must provide appropriate records. 
    There will be examples of records in 'example' for extra activities to which you must refer.
     
    You also might get some areas in 'unregistered area' that has no example.
    If you get a unregistered area, generate answers refering to examples of other areas. 
    
    You must finish your sentence with suffix '~함.'
    You are going to provide 5 sentences that has little differences compared to each other for each area.
    If three areas are given, you must provide 10 sentences for each area.
    AND state the title of each area before the sentences.
     
    Each sentence will not have its subject. It will be completed without its subject.
    Each sentence will be seprated by a line break.
     
    DO NOT use the same expression repeatedly. Use different expressions as many as possible.
    DO NOT add any unnecessary comments in the end of your response.

    In summary, generate records for students' features in extra activites of each registered area and  unregistered area.

    area : {area},
    examples : {examples},
    unregistered area : {u_area}"""),
    ("human", "Generate records of students' features in extra activity areas.")
])

career_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    You are an assistant who helps teachers record students' features in activites related to career.
    You will get the names of the activities from 'activities' by which you must provide appropriate records. 
    There will be examples of records in 'example' for extra activities to which you must refer.

    Use the example as a reference, but try to use more elaborate expressions.
    Do not use the exact same expression repetedly.
    You must finish your sentence with suffix '~함.
    You are going to provide 5 sentences that has little differences compared to each other for each activity.
    If three activities are given, you must provide 5 sentences for each activity.
    Each sentence will be seprated by a line break(\n).
    
    activities : {activities}
    examples : {examples}"""),
    ("human", "Generate records of students' features in extra activity areas.")
])

commend_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an assistant who helps teachers write down their own commendation documents.
    The user will provide their outcomes seperated by comma.
    You need to generate a complete document divided by two parts refering to the outcomes the user provide. 

    Title of Part one would be "### 공적 요지".
    It is one sentence with able to explain the user's activities.
    A sentence should be based on the six Ws and one H principle.
    Most of all, it must include the time period which is usually from March to November.
    Sentences of part one should be finished with "~에 기여함."
    
    Title of Part one would be "### 공적 내용".
    It will include a concrete version of the outcomes.
    Sentences of this part must align with the assessment criteria.
    The assessment criteria are as follows : {criteria}
    Use the provided activity names as the titles for each section with numbers. 
    For each section, expand and elaborate on the details as much as possible, including the target audience, time period, what was done, and how it was accomplished. Each sentence should be separated by a line break.
    Be especially detailed and specific about the operational methods using all the knowledge you have.
    Referencing the criteria will make it even better. Ensure that each sentence ends with the '~함' ending.
     
    You need to pay special attention to line breaks.     
    Each part must begin with the title of it.

    Example is as follows :
     
### 공적 요지
2024년 3월부터 12월까지 수준 및 단계별로 체계화한 문서 및 동영상강의 온라인 원격 콘텐츠 개발 및 공유 활동으로 코로나 상황에서 교육활동에 기여함

### 공적 내용     
1. 코로나 19 상황 원격 콘텐츠 개발 및 개별 지도 개요

◦ 온라인 휴업기간(3.2.-4.5.) 중 학습 과정 구성 및 운영

◦ 온라인 개학 과정 중 원격 콘텐츠 개발
- 공식 온라인 개학으로 원격수업 진행 시 1학년 영어 교육과정 재구성한 동영상강의를 녹화 제작하여 학습 과정에 활용함
- 수준 및 단계별로 체계화한 원격 콘텐츠를 학생들에게 제시하여 학습하도록 하고 오프라인 등교 수업 시 피드백을 통해 완전 학습이 되도록 도움
- 동영상학습 과정은 문서자료와 함께 개인 블로그로 체계적으로 제시하여 학교 학생은 물론 누구라도 볼 수 있도록 공개해 둠
- 동영상강의 코스 개인블로그 페이지

2. 교육과정 재구성 콘텐츠 개발(자체 커리큘럼 구성) 및 무료 공개

◦ 단계별 체계적 어휘 자료 개발
- 1단계 : (최우선순위) 수능 필수 영단어 1300개
- 2단계 : (collocation) 필수 영어어휘구 800개
- 3단계 : (어근접사 활용) Rootfix Basic 660개(Basic) - 1036(Advanced) 
- 4단계 : (우리말 해석보다 명쾌한) 영영풀이 기본어휘 180
- 기타 : 210개 명문장으로 통째로 암기하는 어휘 590개, 알파벳순 주요 수능영어 어휘집 등

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

◦ 동영상강의 콘텐츠 제작 및 공유

- 축적된 문서 영어콘텐츠의 내용을 동영상강의로 제작하여 코로나 상황의 학교 온라인 수업으로 활용하면서 모두가 볼 수 있도록 무료로 공개함
- 단계별, 수준별로 구성된 문서자료의 흐름을 따라 개별적 자기주도학습이 가능하도록 구성함
- 단계별 동영상 강의 내용 
◦ Flipped Learning 활용
- 자체 제작한 동영상강의를 활용하여 온라인 기간 학습한 내용을 등교 개학 수업 시 피드백을 하면서 적극적인 학습을 유도함


◦ 코로나 상황을 넘어서는 공교육 패러다임의 모델 제시
- 기본부터 스스로 학습할 수 있도록 제작한 동영상강의 및 영어 멘토링 학습코칭 프로그램의 활용으로 자기주도학습과 그 과정에 필요한 유기적이고 체계적인 학습콘텐츠 제공이 동시에 이루어지는 큰 효과를 거둘 수 있었으며 코로나 상황 종료 후에도 공교육 살리기 프로젝트로 지속적 활용이 가능한 패러다임의 모델이 될 것으로 기대함



4. 시공간 초월 교실 밖 학습코칭

◦ 사교육대항 공교육살리기 프로젝트 영어멘토링 학습코칭으로 개별화 교육
- 실시기간 : 현재까지 15년간 매년
- 대상자 : 희망 학생 모두 지도함(매년 60-120명 정도)
- 목표 : 자신의 수준에 맞게 꾸준히 학습 습관을 형성하기
- 코칭방식 : 출발점 진단 후 방향 설정, 수시로 학습상담, 주 1회 점검
- 점검내용 : 매일 학습하는 단어 및 구문독해

- 온라인 장점 활용 : 시공간 초월 학습 점검 및 코칭 가능. 격려 편지나 학습자료 등 온라인상에 탑재 활용. 공통 학습교재 강의 수강희망자를 대상으로 자체 제작 동영상강의 무료 수강 기회 부여
- 대면수업 기간에는 수준과 수요에 따른 현장 방과후수업으로 다양한 지도
- 시간과 공간과 학생 수준을 가리지 않고 개별화 교육 가능함. 온라인, 전화, 대면 상담 등의 다양한 방법도 활용 가능

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