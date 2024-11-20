from typing import List
from app.set_page import BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_prompt import as_prompt
from app.set_documents import load_Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import  PromptTemplate
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv

load_dotenv()

class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return list(filter(None, lines))  # Remove empty lines

output_parser = LineListOutputParser()

mh = MessageHandler()

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(mh,"achievement_standard"),
    ],
)


## -------- Variables for SelfQueryRetriever --------- ##

# llm_selfquery = ChatOpenAI(
#     temperature=0,
#     model='gpt-4o-mini',
# )

# metadata_field_info = [
#     AttributeInfo(
#         name="subject",
#         description="""The subject of achievement standards. 
#         One of [국어, 수학, 사회, 과학, 영어, 음악, 도덕, 실과, 체육, 미술]""",
#         type='string'
#     ),
#     AttributeInfo(
#         name="grade",
#         description="""The grade to which achievement standards would be applied. 
#         One of ['1학년,2학년', '3학년,4학년', '5학년,6학년']""",
#         type='string'
#     ),
#     AttributeInfo(
#     name="area",
#     description="""Area distinguish different parts of the subjects.""",
#     type='string'
#     ),
# ]

# document_content_description = "Achievement standards of 2022 revised national curriculum"

# retriever = SelfQueryRetriever.from_llm(
#     llm_selfquery,
#     vectorstore,
#     document_content_description,
#     metadata_field_info,
#     verbose= True
# )

# ## -------- Variables for MultiQueryRetriever --------- ##

# llm_multiquery = ChatOpenAI(
#     temperature=0,
#     model='gpt-4o-mini',
# )

# multiquery_prompt = PromptTemplate(
#     input_variables=["question"],
#     template="""You are an AI language model assistant helping users find specific achievement standards. User questions should be composed by grade, subject and area.  Your task is to generate three different versions of the given user question to retrieve relevant documents from a vector database. 
#     Original question: {question}""",
# )

# multiquery_chain = multiquery_prompt | llm_multiquery | output_parser

# retriever_from_llm = MultiQueryRetriever(
#     retriever=vectorstore.as_retriever(), llm_chain=multiquery_chain, parser_key="lines"
# )



page_template = BasicChatbotPageTemplate(mh, llm, "achievement_standard")
page_template.set_title("성취기준","🎓")

page_info = """본 페이지에서는 2022 개정 교육과정 성취기준을 확인할 수 있습니다. \n
성취기준 검색시에는 '과목'-'학년'-'원하는 키워드' 순으로 검색하면 좋습니다.\n
ex) 수학 3학년 분수"""

page_template.set_chat_ui(as_prompt,
                          page_info,
                          )