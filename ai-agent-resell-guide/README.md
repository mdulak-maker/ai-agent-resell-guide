# Zendesk ISV Resell Assistant Chatbot

An intelligent chatbot assistant that helps with Zendesk ISV (Independent Software Vendor) resell processes, powered by LangChain, OpenAI, and Streamlit.

## Features

- **RAG-powered responses**: Uses Retrieval-Augmented Generation to provide accurate answers based on your documentation
- **Document processing**: Supports PDF and DOCX files for knowledge base
- **Conversational memory**: Maintains context across chat sessions
- **Modern UI**: Clean, responsive Streamlit interface
- **Source citations**: Shows which documents were used to generate responses

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Your Zendesk ISV resell documentation (PDFs, DOCX files)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-agent-resell-guide/my-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the `my-chatbot` directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Or for Streamlit Cloud deployment, create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

## Setup

1. **Add your documents**
   
   Place your Zendesk ISV resell documentation (PDFs, DOCX files) in the `docs/TechResellChatbotRAG/` directory.

2. **Index your documents**
   ```bash
   python index_documents.py
   ```

3. **Run the chatbot**
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

1. Open your browser and navigate to the Streamlit app (usually `http://localhost:8501`)
2. Start chatting with the assistant about Zendesk ISV resell processes
3. The chatbot will provide answers based on your uploaded documentation
4. View source citations to see which documents were referenced

## Project Structure

```
my-chatbot/
├── docs/
│   └── TechResellChatbotRAG/     # Your documentation files
├── rag_index/                    # Vector store (auto-generated)
├── streamlit_app.py             # Main Streamlit application
├── index_documents.py           # Document indexing script
├── main.py                      # Core chatbot logic
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (not in git)
└── README.md                    # This file
```

## Customization

### Adding New Documents
1. Place new PDF or DOCX files in `docs/TechResellChatbotRAG/`
2. Run `python index_documents.py` to update the knowledge base
3. Restart the Streamlit app

### Modifying the Chatbot
- Edit `main.py` to change the chatbot's behavior and prompts
- Modify `streamlit_app.py` to customize the UI
- Update the system prompt in `main.py` to change the assistant's personality

## Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Add your OpenAI API key in the Streamlit Cloud secrets management
4. Deploy!

### Local Deployment
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your OpenAI API key is correctly set in `.env` or Streamlit secrets
2. **Document Indexing Issues**: Delete the `rag_index/` directory and re-run `index_documents.py`
3. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

### Reset Everything
```bash
rm -rf rag_index/
python index_documents.py
streamlit run streamlit_app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the Streamlit and LangChain documentation
- Open an issue in the repository 