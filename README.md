# City Information Query System

A powerful, interactive system that combines SQL databases and LlamaIndex for querying information about cities. The system supports both predefined city data and custom data uploads, allowing users to query structured databases and unstructured documents seamlessly.

## 🌟 Features

### Default Mode
- **City Database**: Pre-loaded information about major US cities including:
  - Population statistics
  - State information
  - Location details
- **LlamaCloud Integration**: Access to comprehensive city information through LlamaIndex

### Custom Mode
- **CSV Data Upload**: Import your own structured data
- **PDF Document Processing**: Upload and query multiple PDF documents
- **Dynamic Tool Creation**: Automatic creation of query tools based on uploaded data

## 🚀 Getting Started

### Prerequisites
bash
python >= 3.8
streamlit
llama-index
pandas
sqlalchemy
python-dotenv
nest-asyncio
openai
ipython

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/city-query-system.git
cd city-query-system
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
1. Enter your query in the text input
2. Click "Get Answer" to receive information about US cities
3. View results formatted in markdown

### Custom Mode
1. Toggle "Use Custom Data" in the sidebar
2. Upload your CSV file with structured data
3. Upload PDF documents for unstructured data
4. Enter queries about your custom data
5. Reset tools anytime using the "Reset Custom Tools" button

### Sample Queries
- "Which city has the highest population?"
- "List all places to visit in Miami."
- "How do people in Chicago get around?"
- "What is the historical name of Los Angeles?"

## 🏗 Project Structure

```
city-query-system/
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
- **LlamaIndex**: Document processing and semantic search
- **OpenAI**: Natural language processing

### Tools
1. **SQL Query Tool**
   - Handles structured data queries
   - Supports both default and custom databases

2. **LlamaIndex Tool**
   - Processes unstructured text from PDFs
   - Enables semantic search capabilities

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LlamaIndex for document processing capabilities
- OpenAI for natural language processing
- Streamlit for the interactive web interface

## 📧 Contact

Your Name - your.email@example.com
Project Link: [https://github.com/yourusername/city-query-system](https://github.com/yourusername/city-query-system)
