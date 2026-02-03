# Life Science Research Article Extractor

A Python-based GenAI application that extracts structured information from life science research papers and outputs organized summaries in JSON or Markdown format.

## Features

- 📄 **PDF Text Extraction**: Extract full text from scientific papers using PyPDF
- 🤖 **Dual AI Support**: Switch between Google Gemini and OpenAI GPT-4o-mini
- 📊 **Structured Output**: Automatically extracts Background, Methods, Results, and Conclusions
- 🎨 **Interactive UI**: Built with Streamlit for easy use
- 💾 **Export Options**: Download results as JSON or Markdown
- 🔑 **API Key Management**: Secure API key input with session management

## Installation

### Prerequisites

- Python 3.13+
- pip package manager

### Setup

1. Clone or download the project:
```bash
cd research-article-extractor
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the application:**
```bash
streamlit run app.py
```

2. **In the web interface:**
   - Enter your API key(s) in the sidebar
   - Select your preferred AI model (Gemini or GPT-4o-mini)
   - Upload a PDF research paper or paste text/abstract
   - Choose output format (JSON or Markdown)
   - Click "Extract Article Structure"
   - Download the results

## How It Works

### 1. PDF Text Extraction
- Uses `pypdf` library to extract text from PDF files
- Handles multi-page scientific papers
- Preserves text structure and formatting

### 2. AI Processing
The application sends the extracted text to your chosen AI model with a specialized prompt that:
- Identifies paper structure (Background, Methods, Results, Conclusions)
- Extracts key information from each section
- Generates concise summaries
- Maintains scientific accuracy

### 3. Output Formatting
Results are formatted in your choice of:
- **JSON**: Structured data for programmatic use
- **Markdown**: Human-readable format with clear sections

## Tech Stack

### Core Libraries
- **Streamlit** (1.30.0+): Web UI framework
- **pypdf** (4.0.0+): PDF text extraction
- **google-generativeai** (0.3.0+): Gemini API client
- **openai** (1.10.0+): OpenAI API client

### AI Models
- **Google Gemini 1.5 Flash**: Fast, cost-effective ($0.075/$0.30 per 1M tokens)
- **OpenAI GPT-4o-mini**: Balanced performance ($0.15/$0.60 per 1M tokens)

## Limitations

- PDF extraction works best with text-based PDFs (not scanned images)
- OCR is not included for image-based PDFs
- AI extraction accuracy depends on paper structure quality
- API rate limits apply based on your subscription tier
- Maximum paper length: ~50 pages (varies by model token limits)

