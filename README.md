# Web Research Assistant

A Streamlit-based web application that helps users conduct research by automatically searching the web, extracting relevant information, and generating well-structured reports using AI.

## Features

- Web search using Google (via SerpAPI)
- Automatic content extraction from web pages
- AI-powered report generation using OpenAI's GPT-3.5
- Multiple report length options (Short, Medium, Detailed)
- Export reports as PDF or DOCX
- Clean and intuitive user interface

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd web-research-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Create a `.env` file in the project root
- Add your API keys:
```
SERPAPI_KEY=your_serpapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
your_project_name/
├── app.py                    # Main Streamlit application
├── utils/                    # Utility modules
│   ├── search_utils.py       # Web search functions
│   ├── content_extractor.py  # Web content extraction
│   ├── llm_handler.py        # OpenAI API integration
│   └── document_generator.py # PDF/DOCX generation
├── .streamlit/               # Streamlit configuration
├── assets/                   # Static assets
├── requirements.txt          # Python dependencies
└── .env                      # API keys (not in version control)
```

## Usage

1. Enter your API keys in the sidebar
2. Type your research query
3. Select desired report length
4. Click "Generate Report"
5. Download the report in PDF or DOCX format

## Dependencies

- streamlit
- openai
- beautifulsoup4
- requests
- python-docx
- reportlab
- serpapi
- python-dotenv

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.