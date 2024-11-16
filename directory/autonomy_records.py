from dotenv import load_dotenv
import streamlit as st
from langchain_core.runnables import RunnablePassthrough
from langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.base import BaseCallbackHandler
from app.set_page import BasicChatbotPageTemplate, MessageHandler, ChatCallbackHandler
from app.set_documents import load_Document
from app.set_prompt import aac_prompt
from langchain_openai import ChatOpenAI

st.set_page_config(
    page_title="EduDocs",
    page_icon="📃",
)
#autonomy accumulative records
if 'aac_messages' not in st.session_state:
    st.session_state['aac_messages'] = []

load_dotenv()

class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        ms.save_message(self.message, "ai",'aac')

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)

ms = MessageHandler()

memory = ConversationBufferWindowMemory(
    return_messages=True,
    k=4,
    memory_key='chat_history'
)

llm = ChatOpenAI(
    temperature=0,
    model='gpt-4o-mini',
    streaming= True,
    callbacks=[
        ChatCallbackHandler(),
    ],
)

def paint_history():
    for message in st.session_state["aac_messages"]:
        ms.send_message(
            message["message"],
            message["role"],
            'aac',
            save=False,
        )

st.title("학생부 기재요령 검색")

docs = load_Document()

paint_history()  

message = st.chat_input("찾고싶은 내용을 입력하세요")

if message :
    ms.send_message(message, "human",'aac')
    chain = (
        {
        "context" : docs.aac_select_document().as_retriever(search_type="mmr",
                                                        search_kargs={'k':2}),
        "input" : RunnablePassthrough()
        }
        | aac_prompt
        | llm
        | StrOutputParser()
    )
    with st.chat_message("ai"):
        chain.invoke(message)
