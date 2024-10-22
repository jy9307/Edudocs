import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key="sk-proj-p6i01xc1aEXcJuDQK4NrT3BlbkFJUECFk0uxAI7YoBtTAHvh", 
)

prompt = ChatPromptTemplate.from_messages([("system",
                                            """
    너는 내가 교육과정 지도안 만드는 것을 도와줘.

    대답할 때는 무조건 아래 양식에 맞춰서 만들어줘야해.

    핵심 역량: 
    성취 기준: 
    학습 활동: 
    평가 방법: 
    """), ("human", "{input}")])

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"input": f"{input()}"})
print(result)
