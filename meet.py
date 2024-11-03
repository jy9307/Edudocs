from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

# 파일 경로 설정
loader = PyPDFLoader("db/깊이있는수업.pdf")

text_splitter = RecursiveCharacterTextSplitter(
    # 청크 크기를 매우 작게 설정합니다. 예시를 위한 설정입니다.
    chunk_size=500,
    # 청크 간의 중복되는 문자 수를 설정합니다.
    chunk_overlap=50,
    # 문자열 길이를 계산하는 함수를 지정합니다.
    length_function=len,
    # 구분자로 정규식을 사용할지 여부를 설정합니다.
    is_separator_regex=False,
)

# PDF 로더 초기화
docs = loader.load_and_split(text_splitter=text_splitter)

# OpenAI의 "text-embedding-3-large" 모델을 사용하여 임베딩을 생성합니다.
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", 
                              api_key="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")

# 임베딩한 내용을 '복무규정'이라는 이름의 폴더에 넣습니다. <- 자신이 설정한 파일 이름으로 바꾸기
cache_dir = LocalFileStore(f"./.cache/embeddings/회계지침")
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings_model, cache_dir)

# FAISS 벡터스토어를 활용하여 문서들을 임베딩하고 저장합니다.
vectorstore = FAISS.from_documents(docs, cached_embeddings)

# 벡터스토어를 리트리버(검색기)로 활용합니다.
retriever = vectorstore.as_retriever()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key="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", 
)

#프롬프트를 설정합니다.
#context란이 추가된 것을 볼 수가 있습니다. retriever가 사용자의 질문에 따라 조사해온 docs의 조각들이 context안에 들어가게 됨.
prompt = ChatPromptTemplate.from_messages([("system", """context를 참고하여 답변을 줘.
                                            답변할 때는 다음 양식에 따라 보여줘
                                            
    - 답변 :
    - 참고 조항 :
                                            
    context : {context}
                                            
    """), ("human", "{input}")])

#여기가 헷갈릴텐데, 단순하게 생각해보면 좋음
#기존에는 chain.invoke에서 딕셔너리를 활용하여 {"input" : "~~~"}를 넣었음
#여기서는 chain자체에 딕셔너리가 들어있음. 이것은 context, 즉 우리가 검색하려는 자료로부터의 맥락이 LLM에 함께 전달되기 때문
#RunnablePassthrough는 아래 chain.invoke에 들어있는 string을 그냥 있는 그대로 가져와주는 역할을 해서
#input에는 chain.invoke에 들어있는 질문을, context에는 질문과 관련있는 docs의 조각들을 담은 다음에
#이를 prompt에 전달하고, 그렇게 완성된 prompt가 llm에 전달되고, 하는 방식으로 진행됨
chain = ( 
        {
            "input" : RunnablePassthrough(),
            "context" : retriever
        }
        | prompt 
        | llm 
        | StrOutputParser())

result = chain.invoke("""입력하는 교과, 역량, 성취기준을 보고 깊이 있는 수업 지도안을 작성해줘
                       교과: 국어
                       역량: 의사소통역량
                       성취기준: 상황에 어울리는 대화를 할 수 있다.
                       """)
print(result)