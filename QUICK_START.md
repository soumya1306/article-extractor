# Quick Start Guide

## Installation Steps

### 1. Project Structure
Create the following directory structure:

```
research-article-extractor/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
│
├── utils/                      # Utility modules
│   ├── __init__.py            # Empty file to make it a package
│   ├── pdf_extractor.py       # PDF text extraction
│   ├── ai_processor.py        # AI model integration
│   └── output_formatter.py    # JSON/Markdown formatting
│
└── config/                     # Configuration files
    ├── __init__.py            # Empty file to make it a package
    └── prompts.py             # AI prompts
```

### 2. Create Empty __init__.py Files
```bash
# In the project root
mkdir utils config
touch utils/__init__.py
touch config/__init__.py
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get API Keys

**For Gemini:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

**For OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage Examples

### Example 1: Extract from PDF
1. Select "Gemini 1.5 Flash" or "GPT-4o-mini" in sidebar
2. Enter your API key
3. Choose "Upload PDF" as input method
4. Upload a research paper PDF
5. Click "Extract Article Structure"
6. Download results as JSON or Markdown

### Example 2: Extract from Abstract
1. Select your AI model
2. Enter API key
3. Choose "Paste Text/Abstract"
4. Paste this example abstract:

```
CRISPR-Cas9 Gene Editing in Cancer Treatment

Background: Cancer remains one of the leading causes of death globally. 
Traditional treatments like chemotherapy have limitations including toxicity 
and drug resistance. CRISPR-Cas9 technology offers precise gene editing 
capabilities that could revolutionize cancer treatment.

Methods: We employed CRISPR-Cas9 to target oncogenes in human cancer cell 
lines. In vitro experiments were conducted using HeLa and MCF-7 cells. 
Gene editing efficiency was measured using flow cytometry and western blot 
analysis. Cell viability was assessed using MTT assays over 7 days.

Results: CRISPR-Cas9 successfully knocked out target oncogenes with 85% 
efficiency. Treated cells showed a 70% reduction in proliferation compared 
to controls (p<0.001). Off-target effects were minimal (<2%) as confirmed 
by whole-genome sequencing. Cell death increased by 60% in edited cells.

Conclusions: CRISPR-Cas9 gene editing shows significant promise as a cancer 
therapy. The high specificity and efficiency observed warrant further 
investigation in animal models and eventually clinical trials. Future work 
should focus on delivery mechanisms and long-term safety profiles.
```

5. Click "Extract Article Structure"
6. View structured results

## Expected Output

### JSON Format
```json
{
  "title": "CRISPR-Cas9 Gene Editing in Cancer Treatment",
  "authors": "Not specified",
  "journal": "Not specified",
  "year": "2024",
  "background": {
    "summary": "Cancer is a global health challenge with traditional treatments having significant limitations...",
    "key_points": [
      "Cancer is a leading cause of death globally",
      "Traditional chemotherapy has limitations",
      "CRISPR-Cas9 offers precise gene editing"
    ]
  },
  "methods": {
    "summary": "The study used CRISPR-Cas9 technology to target oncogenes...",
    "key_points": [
      "CRISPR-Cas9 gene editing",
      "HeLa and MCF-7 cell lines",
      "Flow cytometry and western blot analysis"
    ]
  },
  "results": {
    "summary": "High editing efficiency with minimal off-target effects...",
    "key_points": [
      "85% gene knockout efficiency",
      "70% reduction in cell proliferation",
      "Minimal off-target effects (<2%)"
    ]
  },
  "conclusions": {
    "summary": "CRISPR-Cas9 shows promise for cancer therapy...",
    "key_points": [
      "High specificity and efficiency observed",
      "Further animal model studies needed",
      "Clinical trials warranted"
    ]
  }
}
```

## Troubleshooting

### Issue: Module not found errors
**Solution:** Make sure you have `__init__.py` files in both `utils/` and `config/` directories:
```bash
touch utils/__init__.py
touch config/__init__.py
```

### Issue: PDF extraction returns empty text
**Problem:** PDF might be scanned images
**Solution:** The PDF must be text-based (not scanned). Try:
- Opening the PDF and checking if you can select text
- Using a different PDF
- Converting scanned PDFs using OCR software first

### Issue: API rate limit exceeded
**Solution:**
- Wait a few minutes and try again
- Upgrade your API plan for higher limits
- Use shorter text inputs

### Issue: Token limit exceeded
**Solution:**
- For Gemini: Can handle up to 1M tokens (very long papers)
- For GPT-4o-mini: Limited to 128K tokens (~50 pages)
- Extract only specific sections if needed

## Tips for Best Results

1. **Use complete papers when possible** - Full text gives better extraction than abstracts alone

2. **Choose the right model:**
   - Use **Gemini** for very long papers (100+ pages)
   - Use **GPT-4o-mini** for shorter papers with faster response

3. **Clean PDFs work best** - Papers with clear structure and formatting

4. **Check extracted text preview** - Verify PDF extraction worked before processing

5. **Save your results** - Download JSON for programmatic use, Markdown for reading

## Cost Estimates

### Gemini 1.5 Flash
- Typical research paper (10-20 pages): ~$0.01-0.03
- Long review paper (50 pages): ~$0.10-0.15
- Free tier: 15 requests per minute

### GPT-4o-mini
- Typical research paper (10-20 pages): ~$0.02-0.05
- Long paper (30 pages): ~$0.10-0.15
- Pay as you go: No free tier

## Next Steps

Once you have structured data:
1. **Create datasets** - Batch process multiple papers for meta-analysis
2. **Extract trends** - Analyze methods and results across papers
3. **Build literature databases** - Organize research by topic
4. **Compare studies** - Identify patterns in methodologies
5. **Generate insights** - Use structured data for further AI analysis

## Advanced Features to Add

Consider enhancing the project with:
- Batch processing for multiple PDFs
- Citation extraction and reference parsing
- Figure and table extraction
- Database integration (SQLite, PostgreSQL)
- PubMed API integration for automatic paper retrieval
- Export to CSV for spreadsheet analysis
- Search and filter functionality

## Support Resources

- **PyPDF Documentation:** https://pypdf.readthedocs.io/
- **Streamlit Documentation:** https://docs.streamlit.io/
- **Gemini API:** https://ai.google.dev/docs
- **OpenAI API:** https://platform.openai.com/docs
- **Python JSON:** https://docs.python.org/3/library/json.html

---

**Happy Researching! 🔬📚**
