from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_core.memory import ConversationBufferMemory

class QAModel:
    def __init__(self, llm, vectorstore):
        self.llm = llm
        self.vectorstore = vectorstore
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=True,
            output_key="answer"
        ) 

    def ask(self, user_input):
        result = self.qa_chain.invoke({"question": user_input})
        return result 