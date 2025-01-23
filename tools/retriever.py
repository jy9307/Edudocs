from langchain_openai import ChatOpenAI
from typing import List
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever

# -------- Variables for SelfQueryRetriever --------- ##

class LoadSelfQueryRetriever() :

    def __init__( self, vectorstore, temperature=0.5 ):
        self.llm_selfquery = ChatOpenAI(
            temperature=temperature,
            model='gpt-4o-mini',
        )
        self.vectorstore = vectorstore

    def metadata_info(self, metadata_info : List[AttributeInfo]) -> None:
        """
        Initializes metadata field information for achievement standards.
        
        Returns:
            None
        """

        self.metadata_field_info = metadata_info

    def docs_info(self, txt) :  
        self.document_content_description = txt

    def retriever_load(self) :
        retriever = SelfQueryRetriever.from_llm(
            self.llm_selfquery,
            self.vectorstore,
            self.document_content_description,
            self.metadata_field_info,
            verbose= True
        )

        return retriever