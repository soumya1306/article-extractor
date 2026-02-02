# Life Science Research Article Extractor

A Python-based GenAI application that extracts structured information from life science research papers and outputs organized summaries in JSON or Markdown format.

## Features

- 📄 **PDF Text Extraction**: Extract full text from scientific papers using PyPDF
- 🤖 **Dual AI Support**: Switch between Google Gemini and OpenAI GPT-4o-mini
- 📊 **Structured Output**: Automatically extracts Background, Methods, Results, and Conclusions
- 🎨 **Interactive UI**: Built with Streamlit for easy use
- 💾 **Export Options**: Download results as JSON or Markdown
- 🔑 **API Key Management**: Secure API key input with session management

## Project Structure

```
research-article-extractor/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── pdf_extractor.py       # PDF text extraction logic
│   ├── ai_processor.py        # GenAI processing with Gemini/GPT
│   └── output_formatter.py    # JSON/Markdown formatting
├── config/
│   └── prompts.py             # System prompts for AI models
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.9+
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

## Configuration

### API Keys

You'll need API keys for the AI models you want to use:

**Google Gemini API:**
- Get your key from: https://makersuite.google.com/app/apikey
- Free tier includes 15 requests per minute

**OpenAI API:**
- Get your key from: https://platform.openai.com/api-keys
- GPT-4o-mini pricing: $0.15/1M input tokens, $0.60/1M output tokens

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

## Example Output

### JSON Format
```json
{
  "title": "Novel Approach to Cancer Treatment Using CRISPR",
  "authors": "Smith, J., et al.",
  "journal": "Nature Medicine",
  "year": "2026",
  "doi": "10.1038/nm.2026.1234",
  "background": {
    "summary": "Cancer treatment faces challenges...",
    "key_points": [
      "Current limitations of chemotherapy",
      "CRISPR technology advancement"
    ]
  },
  "methods": {
    "summary": "The study employed...",
    "key_points": [
      "CRISPR-Cas9 gene editing",
      "In vitro cell culture experiments"
    ]
  },
  "results": {
    "summary": "Significant tumor reduction observed...",
    "key_points": [
      "85% reduction in tumor size",
      "Minimal off-target effects"
    ]
  },
  "conclusions": {
    "summary": "This approach shows promise...",
    "key_points": [
      "Potential for clinical trials",
      "Further validation needed"
    ]
  }
}
```

### Markdown Format
```markdown
# Novel Approach to Cancer Treatment Using CRISPR

**Authors:** Smith, J., et al.
**Journal:** Nature Medicine
**Year:** 2026
**DOI:** 10.1038/nm.2026.1234

## Background
Cancer treatment faces challenges...

**Key Points:**
- Current limitations of chemotherapy
- CRISPR technology advancement

## Methods
The study employed...
...
```

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

## Troubleshooting

### Common Issues

**"PDF extraction failed"**
- Ensure PDF is text-based, not a scanned image
- Try a different PDF viewer to verify file integrity

**"API key invalid"**
- Double-check your API key
- Ensure you've activated the API in Google Cloud Console or OpenAI dashboard

**"Token limit exceeded"**
- Try extracting only specific sections
- Use a model with larger context window (Gemini 1.5 Pro has 1M tokens)

## Future Enhancements

- [ ] OCR support for scanned PDFs
- [ ] Batch processing multiple papers
- [ ] Citation extraction and reference parsing
- [ ] Figure and table extraction
- [ ] PubMed integration for direct paper retrieval
- [ ] Support for additional AI models (Claude, Llama)
- [ ] Export to CSV for dataset creation
- [ ] Keyword and entity extraction
- [ ] Research paper similarity comparison

## Contributing

This is an educational project. Feel free to fork and enhance!

## License

MIT License - feel free to use and modify for your projects.

## Credits

Built with:
- Streamlit for the UI framework
- PyPDF for PDF processing
- Google Gemini and OpenAI GPT for AI extraction

## Contact

For questions or suggestions, open an issue on the GitHub repository.

---

**Last Updated:** February 2026
**Version:** 1.0.0
