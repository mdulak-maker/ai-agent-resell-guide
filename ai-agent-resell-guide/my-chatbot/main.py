"""
Zendesk ISV Resell Assistant - CLI Version
A helpful assistant for Zendesk sales representatives to navigate ISV reselling processes
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

class ZendeskISVAssistant:
    def __init__(self):
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None
        self.setup_llm()
        self.setup_vectorstore()
    
    def setup_llm(self):
        """Initialize the language model"""
        # Try OpenAI first, fallback to Anthropic
        if os.getenv("OPENAI_API_KEY"):
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif os.getenv("ANTHROPIC_API_KEY"):
            self.llm = ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=0.7,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError("No API key found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    def setup_vectorstore(self):
        """Initialize the vector store with RAG index"""
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Check if RAG index exists
        if os.path.exists("rag_index"):
            self.vectorstore = Chroma(
                persist_directory="rag_index",
                embedding_function=embeddings
            )
            
            # Setup conversation chain
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(),
                memory=memory,
                return_source_documents=True,
                output_key="answer"
            )
        else:
            print("RAG index not found. Please run indexing first.")
            self.vectorstore = None
    
    def get_response(self, user_input: str):
        """Get response from the assistant"""
        if not self.qa_chain:
            return "Vector store not initialized. Please run indexing first.", []
        
        try:
            result = self.qa_chain({"question": user_input})
            response = result["answer"]
            source_docs = result.get("source_documents", [])
            return response, source_docs
        except Exception as e:
            return f"Error generating response: {e}", []
    
    def show_help(self):
        """Display help information"""
        help_text = """
🤖 Zendesk ISV Resell Assistant - Help Guide

This assistant helps Zendesk sales representatives navigate ISV reselling processes.

COMMON QUESTIONS YOU CAN ASK:

📋 Process Questions:
- "What are the steps for ISV reselling?"
- "How do I create a sales order for an ISV?"
- "What approvals do I need for ISV deals?"
- "What documentation is required?"

💰 Pricing & Billing:
- "How do I price ISV products?"
- "What discount structure applies?"
- "What are the billing options?"
- "How do I handle implementation costs?"

📄 Documentation:
- "What forms do I need to complete?"
- "What's included in the ISV addendum?"
- "How do I handle contract terms?"
- "What compliance requirements apply?"

🔧 Technical & Implementation:
- "How do I validate ISV compatibility?"
- "What are the implementation requirements?"
- "How do I coordinate with ISV partners?"
- "What support is available?"

📞 Support & Troubleshooting:
- "How do I escalate ISV issues?"
- "What's the approval workflow?"
- "How do I handle customer complaints?"
- "What are common problems and solutions?"

COMMANDS:
- Type 'help' to see this message
- Type 'sources' to see source documents for the last response
- Type 'quit' to exit

TIPS:
- Be specific in your questions for better answers
- Ask about specific ISV products or scenarios
- Request step-by-step guidance for complex processes
"""
        print(help_text)
    
    def show_sources(self, source_docs):
        """Display source documents"""
        if not source_docs:
            print("No source documents available for the last response.")
            return
        
        print("\n📚 Source Documents:")
        print("=" * 50)
        for i, doc in enumerate(source_docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            print(f"{i}. {source}")
            # Show first 200 characters of content
            content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            print(f"   Preview: {content_preview}")
            print()

def main():
    """Main function to run the assistant"""
    print("🤖 Zendesk ISV Resell Assistant")
    print("=" * 50)
    
    try:
        assistant = ZendeskISVAssistant()
        print("✅ Assistant initialized successfully!")
        
        # Show help
        assistant.show_help()
        
        # Track last response for sources
        last_response = None
        last_sources = []
        
        print("\n💬 Ready to help! Type 'help' for guidance or 'quit' to exit.")
        print("-" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye! Thank you for using the Zendesk ISV Resell Assistant.")
                break
            elif user_input.lower() == 'help':
                assistant.show_help()
                continue
            elif user_input.lower() == 'sources':
                assistant.show_sources(last_sources)
                continue
            elif not user_input:
                continue
            
            # Get response
            response, sources = assistant.get_response(user_input)
            last_response = response
            last_sources = sources
            
            print(f"\n🤖 Assistant: {response}")
            
            if sources:
                print(f"\n📚 Sources: {len(sources)} document(s) referenced")
                print("   Type 'sources' to see details")
    
    except Exception as e:
        print(f"❌ Error initializing assistant: {e}")
        print("Please check your API keys and ensure the RAG index is created.")

if __name__ == "__main__":
    main() 