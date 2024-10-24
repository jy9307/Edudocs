from dotenv import load_dotenv
import streamlit as st
from typing import List
from langchain_core.runnables import RunnablePassthrough
from langchain.memory.buffer_window import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.base import BaseCallbackHandler
from app.set_documents import load_Document
from app.set_prompt import el_prompt
from langchain_openai import ChatOpenAI

class MessageHandler() :
    def __init__(self) :
        return

    def save_message(self, message, role, page):
        self.page_name = f"{page}_messages"
        st.session_state[self.page_name].append({"message": message, "role": role})

    def send_message(self, message, role, page, save=True):
        with st.chat_message(role):
            st.markdown(message)
        if save:
            self.save_message(message, role, page)


class ChatCallbackHandler(BaseCallbackHandler):
    def __init__(self, mh_instance,page_name):
        self.message = ""
        self.page_name = page_name
        self.mh = mh_instance

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        self.mh.save_message(self.message, "ai", self.page_name)

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


class BasicChatbotPageTemplate() :

    def __init__(self, mh_instance, llm, page_name) :

        self.message_cache_name = page_name+"_messages"

        if self.message_cache_name not in st.session_state:
            st.session_state[self.message_cache_name] = []

        self.llm = llm
        self.page_name = page_name
        self.mh = mh_instance
        return


    def paint_history(self):
        

        for message in st.session_state[self.message_cache_name]:
            self.mh.send_message(
                message["message"],
                message["role"],
                self.page_name,
                save=False,
            )

    def set_title(self, title, emoji) :
        st.set_page_config(
            page_title=title,
            page_icon=emoji,
        )

        st.title(title)


    def set_chat_ui(self, 
                    prompt_name, 
                    basic_message, 
                    search_type='similarity') :

        docs = load_Document()
        #기본 출력 메세지 설정(AI가 제공) 
        self.mh.send_message(basic_message, "ai", self.page_name, save=False)
        
        self.paint_history() 

        message = st.chat_input("찾고싶은 내용을 입력하세요")
        if message :
            self.mh.send_message(message, "human", self.page_name)
            chain = (
                {
                "context" : docs.select_document(self.page_name).as_retriever(search_type=search_type,
                                                                search_kwargs={'k':6}),
                "input" : RunnablePassthrough()
                }
                | prompt_name
                | self.llm
                | StrOutputParser()
            )
            with st.chat_message("ai"):
                chain.invoke(message)
        
    def set_chat_ui_with_retriever(self,
                                   prompt_name,
                                   basic_message,
                                   retriever) :
        
        #기본 출력 메세지 설정(AI가 제공) 
        self.mh.send_message(basic_message, "ai", self.page_name, save=False)
        
        self.paint_history() 

        message = st.chat_input("찾고싶은 내용을 입력하세요")
        if message :
            self.mh.send_message(message, "human", self.page_name)
            chain = (
                {
                "context" : retriever,
                "input" : RunnablePassthrough()
                }
                | prompt_name
                | self.llm
                | StrOutputParser()
            )
            with st.chat_message("ai"):
                chain.invoke(message)
        
class BasicInputBoxPageTemplate() :

    def __init__(self, llm, page_name, mh_instance) :

        self.message_cache_name = page_name+"_messages"

        if self.message_cache_name not in st.session_state:
            st.session_state[self.message_cache_name] = []

        self.llm = llm
        self.page_name = page_name
        self.mh = mh_instance

    def input_box(self, items: List[str]) : 

        inputs = []
        n = len(items)
        for i,n in enumerate(items):
            user_input = st.text_input(f"{n} 입력창", key= i)
            inputs.append(user_input)

    def run_button(self, button_name) :
        if st.button(button_name):
            st.write("입력된 내용:")
        return
   
    def set_title(self, title, emoji) :
        st.set_page_config(
            page_title=title,
            page_icon=emoji,
        )

        st.title(title)