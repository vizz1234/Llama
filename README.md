# RAG and Text-to-SQL Query System

A versatile, interactive system that combines SQL databases and LlamaIndex for natural language querying of both structured and unstructured data. The system features Retrieval-Augmented Generation (RAG) capabilities and Text-to-SQL conversion, supporting both predefined datasets and custom data uploads.

## 🌟 Features

### Default Mode
- **Text-to-SQL Conversion**: Query structured data using natural language
- **RAG Integration**: Enhanced responses using LlamaIndex for comprehensive information retrieval
- **Pre-loaded Database**: Example dataset demonstrating system capabilities

### Custom Mode
- **CSV Data Upload**: Import any structured data for Text-to-SQL queries
- **PDF Document Processing**: Upload documents for RAG-powered queries
- **Dynamic Tool Creation**: Automatic configuration of query tools based on uploaded data

## 🚀 Getting Started

### Prerequisites
```
python >= 3.8
streamlit
llama-index
pandas
sqlalchemy
python-dotenv
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/rag-sql-query-system.git
cd rag-sql-query-system
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up your environment variables
Create a `.streamlit/secrets.toml` file:
```toml
[api_keys]
OPENAI_API_KEY = "your-openai-key"
PHOENIX_API_KEY = "your-phoenix-key"
LLAMA_CLOUD_API_KEY = "your-llama-cloud-key"
ORGANIZATION_ID = "your-org-id"

[llama_cloud]
INDEX_NAME = "your-index-name"
PROJECT_NAME = "your-project-name"
```

4. Run the application
```bash
streamlit run app.py
```

## 💡 Usage

### Default Mode
1. Enter your natural language query
2. System automatically determines whether to use SQL or RAG
3. View results formatted in markdown

### Custom Mode
1. Toggle "Use Custom Data" in the sidebar
2. Upload structured data (CSV) for Text-to-SQL functionality
3. Upload unstructured documents (PDF) for RAG capabilities
4. Query your custom data using natural language
5. Reset anytime using the "Reset Custom Tools" button

### Sample Queries
- Structured Data: "What are the highest values in the dataset?"
- Unstructured Data: "Summarize the key points from the documents."
- Combined: "Compare the statistical data with the contextual information."

## 🏗 Project Structure

```
rag-sql-query-system/
├── app.py                 # Main Streamlit application
├── sql_router.py          # Router and tool definitions
├── .streamlit/
│   └── secrets.toml       # API keys and configurations
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## 🔒 Security

- API keys and sensitive information are stored in `.streamlit/secrets.toml`
- The secrets file is excluded from version control
- Environment variables are used for deployment
- Different keys should be used for development and production

## 🛠 Technical Details

### Components
- **Streamlit**: Web interface and user interaction
- **SQLAlchemy**: Database management and SQL queries
- **LlamaIndex**: RAG implementation and document processing
- **OpenAI**: Natural language understanding and generation

### Tools
1. **Text-to-SQL Tool**
   - Converts natural language to SQL queries
   - Handles structured data queries
   - Supports dynamic schema adaptation

2. **RAG Tool**
   - Implements Retrieval-Augmented Generation
   - Processes unstructured documents
   - Provides contextual information retrieval

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LlamaIndex for RAG capabilities
- OpenAI for language processing
- Streamlit for the interactive interface

## 📧 Contact

Your Name - your.email@example.com
Project Link: [https://github.com/yourusername/rag-sql-query-system](https://github.com/yourusername/rag-sql-query-system)
```

The key changes include:
- Updated project name and description to focus on RAG and Text-to-SQL capabilities
- Modified feature descriptions to be more general and technical
- Updated sample queries to be domain-agnostic
- Enhanced technical details section to highlight RAG and Text-to-SQL components
- Updated repository names and links to reflect the new focus