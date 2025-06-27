"""
Zendesk ISV Resell Assistant - Streamlit Web Application
A helpful assistant for Zendesk sales representatives to navigate ISV reselling processes
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


import os
import glob
from dotenv import load_dotenv


# Disable LangChain telemetry
os.environ["LANGCHAIN_API_KEY"] = ""
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""
# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Zendesk ISV Resell Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #03363d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #174a5c;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .quick-question {
        background-color: #f0f8ff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .quick-question:hover {
        background-color: #e3f2fd;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-success {
        background-color: #4caf50;
    }
    .status-warning {
        background-color: #ff9800;
    }
    .status-error {
        background-color: #f44336;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitApp:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        # Initialize Embeddings and Vectorstore
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        self.vectorstore = Chroma(
            persist_directory="rag_index",
            embedding_function=embeddings
        )
        # Initialize Memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        # Initialize QA Chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=True,
            output_key="answer"
        )

    def get_response(self, user_input):
        result = self.qa_chain.invoke({"question": user_input})
        response = result["answer"]
        source_docs = result.get("source_documents", [])
        return response, source_docs

def main():
    """Main Streamlit application"""
    st.markdown('<h1 class="main-header">🤖 Zendesk ISV Resell Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your helpful guide for navigating ISV reselling processes and paperwork</p>', unsafe_allow_html=True)
    
    # Initialize assistant
    if 'assistant' not in st.session_state:
        st.session_state.assistant = StreamlitApp()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for configuration and quick actions
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key status
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if openai_key:
            st.success("✅ OpenAI API Key configured")
        elif anthropic_key:
            st.success("✅ Anthropic API Key configured")
        else:
            st.error("❌ No API key found")
        
        # Vector store status
        if os.path.exists("rag_index"):
            st.success("✅ RAG index found")
        else:
            st.warning("⚠️ RAG index not found")
        
        st.divider()
        
        # Quick Questions
        st.header("💡 Quick Questions")
        st.markdown("Click any question to ask it:")
        
        quick_questions = [
            "What are the steps for ISV reselling?",
            "How do I create a sales order for an ISV?",
            "What approvals do I need for ISV deals?",
            "How do I price ISV products?",
            "What documentation is required?",
            "How do I handle implementation costs?",
            "What's the approval workflow?",
            "How do I validate ISV compatibility?"
        ]
        
        for question in quick_questions:
            if st.button(question, key=f"quick_{question[:20]}"):
                st.session_state.messages.append({"role": "user", "content": question})
                with st.spinner("Getting response..."):
                    response, sources = st.session_state.assistant.get_response(question)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                st.rerun()
        
        st.divider()
        
        # Actions
        st.header("⚡ Actions")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("Show Help"):
            st.info("""
            **How to use this assistant:**
            
            • Ask questions about ISV reselling processes
            • Use the quick questions above for common topics
            • View source documents for detailed information
            • Clear chat history when needed
            
            **Common topics:**
            • Sales order requirements
            • Approval workflows
            • Pricing and billing
            • Documentation needs
            • Implementation processes
            """)
    
    # Main chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander(f"📚 Sources ({len(message['sources'])})"):
                        for i, doc in enumerate(message["sources"]):
                            source = doc.metadata.get('source', 'Unknown')
                            st.write(f"**Source {i+1}:** {source}")
                            # Show preview of content
                            content_preview = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                            st.text_area(
                                f"Content preview {i+1}:",
                                content_preview,
                                height=100,
                                key=f"preview_{id(message)}_{i}"
                            )
        
        # Chat input
        if prompt := st.chat_input("Ask about ISV reselling processes..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Thinking..."):
                    response, sources = st.session_state.assistant.get_response(prompt)
                    st.markdown(response)
                    
                    # Display sources if available
                    if sources:
                        with st.expander(f"📚 Sources ({len(sources)})"):
                            for i, doc in enumerate(sources):
                                source = doc.metadata.get('source', 'Unknown')
                                st.write(f"**Source {i+1}:** {source}")
                                # Show preview of content
                                content_preview = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                                st.text_area(
                                    f"Content preview {i+1}:",
                                    content_preview,
                                    height=100,
                                    key=f"preview_current_{id(response)}_{i}"
                                )
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "sources": sources
            })
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🤖 Zendesk ISV Resell Assistant | Built for Zendesk Sales Representatives
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 