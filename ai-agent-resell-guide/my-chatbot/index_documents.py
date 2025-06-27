"""
Document indexing script for AI Agent Resell Guide Chatbot
Processes documents in the docs folder and creates a ChromaDB vector store
"""

import os
import glob
from dotenv import load_dotenv
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredFileLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Load environment variables
load_dotenv()

def load_documents(docs_path):
    """Load documents from the specified path"""
    documents = []
    
    # Supported file extensions
    supported_extensions = {
        '.txt': TextLoader,
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
    }
    
    # Find all files in the docs directory
    for file_path in glob.glob(os.path.join(docs_path, "**/*"), recursive=True):
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in supported_extensions:
                try:
                    print(f"Loading: {file_path}")
                    loader_class = supported_extensions[file_ext]
                    loader = loader_class(file_path)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
            else:
                print(f"Skipping unsupported file: {file_path}")
    
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    return text_splitter.split_documents(documents)

def create_vectorstore(chunks, persist_directory="rag_index"):
    """Create and persist the vector store"""
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is required for creating embeddings")
    
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # Persist the vector store
    vectorstore.persist()
    
    return vectorstore

def main():
    """Main function to index documents"""
    print("🤖 AI Agent Resell Guide - Document Indexing")
    print("=" * 50)
    
    # Configuration
    docs_path = "docs/TechResellChatbotRAG"
    rag_index_path = "rag_index"
    chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))
    
    # Check if docs directory exists
    if not os.path.exists(docs_path):
        print(f"❌ Docs directory not found: {docs_path}")
        print("Please create the docs directory and add your documents.")
        return
    
    # Load documents
    print(f"📚 Loading documents from: {docs_path}")
    documents = load_documents(docs_path)
    
    if not documents:
        print("❌ No documents found to index")
        return
    
    print(f"✅ Loaded {len(documents)} documents")
    
    # Split documents into chunks
    print(f"✂️  Splitting documents (chunk_size={chunk_size}, overlap={chunk_overlap})")
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Create vector store
    print(f"🔍 Creating vector store in: {rag_index_path}")
    try:
        vectorstore = create_vectorstore(chunks, rag_index_path)
        print("✅ Vector store created successfully!")
        
        # Test the vector store
        print("🧪 Testing vector store...")
        test_query = "pricing guidelines"
        results = vectorstore.similarity_search(test_query, k=1)
        if results:
            print(f"✅ Test query successful: Found {len(results)} results")
        else:
            print("⚠️  Test query returned no results")
            
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        return
    
    print("\n🎉 Document indexing completed successfully!")
    print(f"📁 Vector store saved to: {rag_index_path}")
    print("\nYou can now run the chatbot:")
    print("  • Web interface: streamlit run streamlit_app.py")
    print("  • CLI interface: python main.py")

if __name__ == "__main__":
    main() 