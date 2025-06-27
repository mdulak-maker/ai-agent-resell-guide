# Zendesk ISV Resell Assistant

A specialized AI assistant designed to help Zendesk sales representatives navigate the process and paperwork required to resell third-party ISVs (Independent Software Vendors) on Zendesk sales orders. Built with LangChain, Streamlit, and ChromaDB for RAG (Retrieval-Augmented Generation).

## 🎯 Purpose

This assistant serves as an internal sales operations tool that helps Zendesk sales reps:
- Navigate complex ISV reselling processes
- Complete required paperwork and documentation
- Understand approval workflows and requirements
- Access up-to-date procedures and guidelines
- Get quick answers to common ISV reselling questions

## ✨ Features

- 🤖 **Intelligent Chat Interface**: Powered by OpenAI GPT-4 or Anthropic Claude
- 📚 **RAG-powered Responses**: Retrieves relevant information from your knowledge base
- 💬 **Conversation Memory**: Maintains context across chat sessions
- 🎨 **Beautiful UI**: Modern Streamlit interface with Zendesk branding
- 📊 **Source Attribution**: Shows which documents were used to generate responses
- 🔧 **Flexible Configuration**: Support for multiple AI providers
- ⚡ **Quick Questions**: Pre-built common questions for faster access
- 📋 **Process Guidance**: Step-by-step guidance for ISV reselling workflows

## 📁 Project Structure

```
my-chatbot/
├── main.py                 # CLI version of the assistant
├── streamlit_app.py        # Web interface using Streamlit
├── index_documents.py      # Document indexing script
├── .env                    # Environment variables and API keys
├── rag_index/              # ChromaDB vector store (created after indexing)
├── docs/                   # Knowledge base documents
│   └── TechResellChatbotRAG/
│       ├── zendesk_isv_resell_process.txt
│       ├── sales_order_requirements.txt
│       ├── pricing_guidelines.txt
│       └── quoting_steps.txt
└── README.md               # This file
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install langchain langchain-openai langchain-anthropic streamlit chromadb python-dotenv
```

### 2. Configure API Keys

Edit the `.env` file and add your API keys:

```env
# OpenAI API Key (required for embeddings and GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (alternative to OpenAI)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Configuration
MODEL_NAME=gpt-4
TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 3. Add Your Knowledge Base

Place your Zendesk ISV reselling documents in the `docs/TechResellChatbotRAG/` folder. The assistant comes with sample documents covering:

- **ISV Resell Process Guide**: Complete workflow for ISV reselling
- **Sales Order Requirements**: Documentation and paperwork requirements
- **Pricing Guidelines**: Pricing strategies and discount structures
- **Quoting Steps**: Step-by-step quoting process

Supported formats:
- Text files (.txt)
- PDF files (.pdf)
- Word documents (.docx)

### 4. Index Your Documents

Run the document indexing script:

```bash
python index_documents.py
```

### 5. Run the Application

#### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```

#### Command Line Interface
```bash
python main.py
```

## 💼 Use Cases

### Common Questions the Assistant Can Help With:

**📋 Process Questions:**
- "What are the steps for ISV reselling?"
- "How do I create a sales order for an ISV?"
- "What approvals do I need for ISV deals?"
- "What documentation is required?"

**💰 Pricing & Billing:**
- "How do I price ISV products?"
- "What discount structure applies?"
- "What are the billing options?"
- "How do I handle implementation costs?"

**📄 Documentation:**
- "What forms do I need to complete?"
- "What's included in the ISV addendum?"
- "How do I handle contract terms?"
- "What compliance requirements apply?"

**🔧 Technical & Implementation:**
- "How do I validate ISV compatibility?"
- "What are the implementation requirements?"
- "How do I coordinate with ISV partners?"
- "What support is available?"

**📞 Support & Troubleshooting:**
- "How do I escalate ISV issues?"
- "What's the approval workflow?"
- "How do I handle customer complaints?"
- "What are common problems and solutions?"

## 🎨 Interface Features

### Web Interface
- **Modern Chat Interface**: Clean, professional design with Zendesk branding
- **Quick Questions Sidebar**: Pre-built common questions for faster access
- **Source Attribution**: View which documents were used for each response
- **Configuration Panel**: Check API key status and system health
- **Chat History**: Maintains conversation context across sessions

### Command Line Interface
- **Interactive Chat**: Simple text-based interface
- **Help System**: Built-in guidance and examples
- **Source Display**: View source documents for responses
- **Easy Navigation**: Simple commands for help and exit

## ⚙️ Configuration Options

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for embeddings)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (alternative LLM)
- `MODEL_NAME`: AI model to use (default: gpt-4)
- `TEMPERATURE`: Response creativity (0.0-1.0, default: 0.7)
- `CHUNK_SIZE`: Document chunk size for indexing (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)

### Customization

You can customize the assistant by:
- Adding more Zendesk-specific documents to the `docs/` folder
- Modifying the prompt templates in the code
- Adjusting the retrieval parameters
- Changing the UI styling in `streamlit_app.py`
- Adding new quick questions to the sidebar

## 🔧 Troubleshooting

### Common Issues

1. **"No API key found"**
   - Make sure you've added your API keys to the `.env` file
   - Ensure the `.env` file is in the correct location

2. **"RAG index not found"**
   - Run the document indexing script first: `python index_documents.py`
   - Check that documents exist in the `docs/` folder

3. **Import errors**
   - Make sure all dependencies are installed
   - Check your Python environment

4. **Streamlit not working**
   - Ensure Streamlit is installed: `pip install streamlit`
   - Try running with: `streamlit run streamlit_app.py --server.port 8501`

## 📈 Best Practices

### For Sales Representatives:
- Ask specific questions about your ISV deals
- Use the quick questions for common scenarios
- Review source documents for detailed information
- Keep the knowledge base updated with new procedures
- Provide feedback on assistant responses

### For Administrators:
- Regularly update the knowledge base with new procedures
- Monitor assistant usage and feedback
- Update quick questions based on common inquiries
- Ensure API keys are properly configured
- Maintain document organization in the `docs/` folder

## 🔄 Maintenance

### Regular Updates:
- Update ISV reselling procedures as they change
- Add new ISV products and requirements
- Update pricing and discount information
- Refresh approval workflows
- Add new compliance requirements

### Knowledge Base Management:
- Keep documents organized and up-to-date
- Use descriptive filenames for easy identification
- Regularly re-index documents when adding new content
- Archive outdated procedures
- Maintain version control for important documents

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with Zendesk ISV scenarios
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the documentation
3. Contact your system administrator
4. Open an issue on the repository

---

**Note**: This assistant is specifically designed for Zendesk sales representatives handling ISV reselling. Make sure your knowledge base contains current Zendesk procedures, ISV partner information, and internal policies. 