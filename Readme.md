# Edudocs

## 환경변수 설정하는 법

- 프로젝트 루트 디렉토리(기본 폴더)에 .env파일을 생성하고 아래와 같이 입력한다.

```
OPENAI_API_KEY = "자신의 OpenAI API키"

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY= 랭체인(랭스미스)API 키
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="프로젝트명"

```
- 이후 파이썬 파일에서 다음과 같이 설정하면 따로 api키를 넣지 않고도 내 ChatGPT 인스턴스가 자동으로 api를 제공받는다.

```python 

from dotenv import load_dotenv

load_dotenv()

```

## Template 사용하는 법

### BasicInputBoxTemplate

- 템플릿 인스턴스 생성
- 인풋 박스를 가진 페이지를 만들기 위해 BasicInputBoxTemplate 인스턴스를 생성한다.  
- 스트리밍 기능(실시간으로 결과 받아오기)을 활성화하기 위해 MessageHandler와 ChatCallBackHadler 인스턴스도 함께 생성한다.

```python
from app.set_page import BasicInputBoxPageTemplate, MessageHandler, ChatCallbackHandler

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"milvus에 업로드한 콜렉션 이름") ],
)

page_template = BasicInputBoxPageTemplate(mh_instance=mh, llm=llm, page_name="milvus에 업로드한 콜렉션 이름")

```
- 탭 제목과 페이지 제목 설정

```python
page_template.set_title("내가 원하는 페이지 제목","내가 원하는 이모지(이모티콘)")
```

- 인풋박스 만들기
- 다음과 같이 설정하면 박스1,박스2,박스3이라는 인풋박스가 생성된다.

```python
page_template.input_box(items =  ['박스1','박스2','박스3'])
```

- 프롬프트 설정
- 내가 인풋박스에서 내용을 가져와서 프롬프트에 삽입하고 싶다면 아래와 같이 설정한다.
- {}안에 들어있는 요소를 변수(variable)이라고 부른다.
- 프롬프트 틀 안에 원하는 개수만큼 변수를 삽입한다.(여기서는 예시로 box1,box2,box3를 설정하였다)
- context에는 검색된 자료가 들어가므로 건드리지 않는다.

```python

example_prompt =  ChatPromptTemplate.from_messages([
    ("system", """"

    박스 1 : {box1},
    박스 2 : {box2},
    박스 3 : {box3}      

    내가 업로드한 자료 : {context}
     """),
     ("human", "{input}")
])

```

- 박스들을 기반으로 LLM작동시키는 버튼을 만드는 법
- generate_button 함수의 인자는 다음과 같이 제공한다.
- 프롬프트 이름, 버튼 위에 나오는 글자, 프롬프트에 넣은 변수들(input과 context 제외), 추가 지시사항(안써도 됨)

```python

page_template.generate_button(prompt_name=example_prompt, 
                              button_name= "검색",
                              variables = ["subject", "competency", "achievement_standard"],
                              input = "따로 지시하고 싶은 추가 사항이 있을 경우 기재, 없으면 삭제"
                              )

```


### BasicChatbotPageTemplate

- 템플릿 인스턴스 생성
- 채팅창을 가진 페이지를 만들기 위해 BasicChatbotPageTemplate 인스턴스를 생성한다.  
- 스트리밍 기능(실시간으로 결과 받아오기)을 활성화하기 위해 MessageHandler와 ChatCallBackHadler 인스턴스도 함께 생성한다.

```python
from app.set_page import BasicChatbotPageTemplate MessageHandler, ChatCallbackHandler

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"milvus에 업로드한 콜렉션 이름") ],
)

page_template = BasicChatbotPageTemplate(mh_instance=mh, llm=llm, page_name="milvus에 업로드한 콜렉션 이름")

```

- 탭 제목과 페이지 제목 설정

```python

page_template.set_title("내가 원하는 페이지 제목","내가 원하는 이모지(이모티콘)")

```

- 프롬프트 설정

```python
example_prompt =  ChatPromptTemplate.from_messages([
    ("system", """Context에 제공된 내용을 참고하여 내 질문과 지시에 응해줘.
     
     Context: {context}"""),
     ("human", "{input}")
])

```

- 채팅창 설정
- page_info는 최초에 보이는 설명 말풍선
- 나머지는 set_chat_ui에서 다음과 같이 설정한다.
- prompt_name에는 프롬프트 이름, page_info에는 page_info를 설정

```python
page_info = '''본 페이지는 사용자의 질문에 센스있게 대답합니다. '''

page_template.set_chat_ui(prompt_name = wl_prompt,
                          page_info = page_info,
)

```

## Milvus VectorDB에 자료 업로드 하는 법


