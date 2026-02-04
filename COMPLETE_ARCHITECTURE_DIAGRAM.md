# Research Article Extractor - Complete Architecture Diagram

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          RESEARCH ARTICLE EXTRACTOR                         │
│                         (Streamlit Web Application)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            ┌───────▼─────┐  ┌───────▼────────┐  ┌──▼────────────┐
            │ Input Layer │  │ Processing     │  │ Output Layer  │
            │             │  │ Pipeline       │  │               │
            └─────┬───────┘  └────────┬────────┘  └────┬──────────┘
                  │                   │                 │
        ┌─────────┴──────┐  ┌─────────┴──────────┐  ┌──┴──────────────┐
        │   PDF Upload   │  │  AI Processing    │  │  JSON Export    │
        │   Text Input   │  │  Chunking Logic   │  │  Markdown       │
        └────────────────┘  │  Retry Logic      │  │  Web Display    │
                            └───────┬───────────┘  └─────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼──────┐  ┌────▼──────┐  ┌────▼──────────┐
            │   Gemini     │  │ GPT-4o    │  │ Error Handler │
            │   API        │  │ mini API  │  │ & Logging     │
            └──────────────┘  └───────────┘  └───────────────┘
```

---

## 2. Detailed Component Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI LAYER                                │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                      SIDEBAR CONFIGURATION                         │  │
│  │  • Model Selection (Gemini / GPT-4o-mini)                         │  │
│  │  • Output Format (JSON / Markdown / Both)                         │  │
│  │  • Chunking Settings (Enable/Method/Size/Overlap)                 │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│  ┌─────────────────────────────┐    ┌──────────────────────────────────┐ │
│  │  INPUT COLUMN (Left)        │    │  OUTPUT COLUMN (Right)          │ │
│  │                             │    │                                  │ │
│  │ • PDF Uploader              │    │ • Article Information           │ │
│  │ • Text Area                 │    │ • Chunking Info (if enabled)    │ │
│  │ • Preview                   │    │ • Tabbed Results:               │ │
│  │ • Extraction Button         │    │   - Structured View             │ │
│  │ • Chunking Preview          │    │   - JSON Output                 │ │
│  │                             │    │   - Markdown Output             │ │
│  │                             │    │ • Download Buttons              │ │
│  └─────────────────────────────┘    └──────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
                                     │
                         ┌───────────▼───────────┐
                         │  Session State Cache  │
                         │                       │
                         │ • extracted_text      │
                         │ • extracted_data      │
                         │ • chunks              │
                         │ • show_chunking       │
                         └───────────────────────┘
```

---

## 3. Processing Pipeline Architecture

```
┌──────────────┐
│  User Input  │
│  PDF / Text  │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────┐
│   PDF/TEXT EXTRACTION MODULE    │
│   (utils/pdf_extractor.py)      │
│                                 │
│ • extract_text_from_pdf()       │
│ • extract_text_from_abstract()  │
│ • preprocess_text()             │
│ • estimate_tokens()             │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  TEXT CHUNKING MODULE (OPTIONAL)│
│  (utils/text_chunker.py)        │
│                                 │
│ TextChunker Class:              │
│ • chunk_by_characters()         │
│ • chunk_by_sentences()          │
│ • chunk_by_paragraphs()         │
│ • chunk_with_metadata()         │
│ • estimate_tokens()             │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│   AI PROCESSING MODULE          │
│   (utils/ai_processor.py)       │
│                                 │
│ AIProcessor Class:              │
│ ┌────────────────────────────┐  │
│ │ extract_structure()        │  │
│ │ ┌──────────────────────┐   │  │
│ │ │ Gemini Path:         │   │  │
│ │ │ • _call_gemini_with  │   │  │
│ │ │   _retry()           │   │  │
│ │ └──────────────────────┘   │  │
│ │ ┌──────────────────────┐   │  │
│ │ │ GPT-4o Path:         │   │  │
│ │ │ • _call_gpt_with     │   │  │
│ │ │   _retry()           │   │  │
│ │ │ • Config:            │   │  │
│ │ │   - max_tokens       │   │  │
│ │ │   - temperature      │   │  │
│ │ │   - timeout          │   │  │
│ │ └──────────────────────┘   │  │
│ │ ┌──────────────────────┐   │  │
│ │ │ Retry Logic:         │   │  │
│ │ │ • max_retries        │   │  │
│ │ │ • exponential backoff│   │  │
│ │ │ • error detection    │   │  │
│ │ └──────────────────────┘   │  │
│ └────────────────────────────┘  │
│                                 │
│ • _parse_json_response()        │
│ • get_model_info()              │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  OUTPUT FORMATTING MODULE       │
│  (utils/output_formatter.py)    │
│                                 │
│ • format_as_json()              │
│ • format_as_markdown()          │
│ • create_downloadable_json()    │
│ • create_downloadable_markdown()│
└──────────┬──────────────────────┘
           │
           ▼
┌──────────────────┐
│  Final Output    │
│  Display/Download│
└──────────────────┘
```

---

## 4. API Integration Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    AI PROCESSOR MODULE                              │
│              (Handles API Calls & Retry Logic)                      │
└────────────────────────────────────────────────────────────────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
      ┌──────▼──────┐  ┌────▼──────┐  ┌───▼─────────┐
      │   GEMINI    │  │ GPT-4O    │  │  FALLBACK   │
      │   API       │  │ MINI API  │  │  & ERRORS   │
      └──────┬──────┘  └────┬──────┘  └───┬─────────┘
             │               │              │
      ┌──────▼──────────┐   │              │
      │ google-genai    │   │              │
      │ SDK             │   │              │
      │                 │   │              │
      │ • API Key:      │   │              │
      │   GEMINI_API_   │   │              │
      │   KEY           │   │              │
      │ • Model:        │   │              │
      │   gemini-3-     │   │              │
      │   flash-preview │   │              │
      │ • Features:     │   │              │
      │   - Text input  │   │              │
      │   - Streaming   │   │              │
      │   - Retries     │   │              │
      └────────────────┘   │              │
                           │              │
                      ┌────▼──────────┐   │
                      │ Azure OpenAI  │   │
                      │ SDK           │   │
                      │               │   │
                      │ • API Key:    │   │
                      │   AZURE_API_  │   │
                      │   KEY         │   │
                      │ • Endpoint:   │   │
                      │   AZURE_      │   │
                      │   ENDPOINT    │   │
                      │ • Model:      │   │
                      │   gpt-4o-mini │   │
                      │ • Features:   │   │
                      │   - JSON mode │   │
                      │   - Retries   │   │
                      │   - Timeout   │   │
                      └───────────────┘   │
                                          │
                      ┌───────────────────▼───┐
                      │  Error Handling       │
                      │  & Retry Mechanism    │
                      │                       │
                      │ • Transient Errors:   │
                      │   - Timeout           │
                      │   - Rate Limit (429)  │
                      │   - 5xx errors        │
                      │   → Retry with backoff│
                      │                       │
                      │ • Permanent Errors:   │
                      │   - Invalid key       │
                      │   - Bad request       │
                      │   - Auth failure      │
                      │   → Fail immediately  │
                      └───────────────────────┘
```

---

## 5. Data Flow Architecture

```
USER INTERACTION
       │
       ▼
┌─────────────────────────┐
│ Upload PDF / Paste Text │
└──────────┬──────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ Extract Text & Metadata          │
│ • Pages count                    │
│ • Character count               │
│ • Estimated tokens              │
└──────────┬───────────────────────┘
           │
           ▼
        ┌──┴──┐
        │     │
   NO   │     │ YES
   ┌────▼─┐ ┌─┴────────────────────┐
   │      │ │ Apply Text Chunking  │
   │      │ │ • Select method      │
   │      │ │ • Set chunk size     │
   │      │ │ • Set overlap        │
   │      │ │ • Generate metadata  │
   │      │ └─┬────────────────────┘
   │      │   │
   │      └───┤
   │          │
   ▼          ▼
┌────────────────────────────────┐
│ Create LLM Prompts             │
│ • System Prompt (from config)  │
│ • User Prompt (formatted text) │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Call AI Model (with Retry)   │
│ • Attempt 1 (immediate)      │
│ • Attempt 2 (wait 1s)        │
│ • Attempt 3 (wait 2s)        │
│ • Attempt 4 (wait 4s)        │
└────────┬─────────────────────┘
         │
         ├─ SUCCESS ─────────┐
         │                   │
         └─ TRANSIENT ERROR  │
             (Retry)         │
             │               │
             └─ PERMANENT    │
                 ERROR       │
                 (Fail)      │
         │
         ▼
┌───────────────────────────┐
│ Parse JSON Response       │
│ • Clean markdown blocks   │
│ • Extract JSON            │
│ • Validate structure      │
└────────┬────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Format Output                │
│ • JSON Format                │
│ • Markdown Format            │
│ • Structured Display         │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Store in Session State   │
│ • extracted_data         │
│ • chunks (if applied)    │
│ • retry_count            │
└────────┬─────────────────┘
         │
         ▼
┌────────────────────────┐
│ Display & Download     │
│ • Show results         │
│ • Download JSON        │
│ • Download Markdown    │
└────────────────────────┘
```

---

## 6. Configuration & Secrets Architecture

```
┌─────────────────────────────────────────────────┐
│         ENVIRONMENT CONFIGURATION               │
│                                                 │
│ ┌───────────────────────────────────────────┐  │
│ │  .env File (Local, NOT in Git)            │  │
│ │                                           │  │
│ │  GEMINI_API_KEY=xxx...                    │  │
│ │  AZURE_API_KEY=xxx...                     │  │
│ │  AZURE_ENDPOINT=https://xxx.openai...     │  │
│ └───────────────────────────────────────────┘  │
│                    │                            │
│                    ▼                            │
│ ┌───────────────────────────────────────────┐  │
│ │  python-dotenv (load environment vars)    │  │
│ │                                           │  │
│ │  load_dotenv()                            │  │
│ └───────────────────────────────────────────┘  │
│                    │                            │
│                    ▼                            │
│ ┌───────────────────────────────────────────┐  │
│ │  AIProcessor Initialization               │  │
│ │                                           │  │
│ │  • Retrieve API keys from env             │  │
│ │  • Initialize clients:                    │  │
│ │    - genai.Client (Gemini)                │  │
│ │    - AzureOpenAI (GPT)                    │  │
│ │  • Set configuration:                     │  │
│ │    - max_tokens                           │  │
│ │    - temperature                          │  │
│ │    - retry settings                       │  │
│ └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 7. File Structure & Module Organization

```
research-article-extractor/
│
├── app.py                          ◄─ Main Streamlit Application
│   ├── Sidebar Configuration
│   ├── Input Column (PDF/Text)
│   └── Output Column (Results)
│
├── config/
│   ├── __init__.py
│   └── prompts.py                  ◄─ System & User Prompts
│       ├── EXTRACTION_SYSTEM_PROMPT
│       └── EXTRACTION_USER_PROMPT_TEMPLATE
│
├── utils/
│   ├── __init__.py
│   ├── pdf_extractor.py            ◄─ PDF Text Extraction
│   │   ├── extract_text_from_pdf()
│   │   ├── extract_text_from_abstract()
│   │   ├── preprocess_text()
│   │   └── estimate_tokens()
│   │
│   ├── ai_processor.py             ◄─ AI Model Integration
│   │   ├── AIProcessor Class
│   │   ├── extract_structure()
│   │   ├── _call_gemini_with_retry()
│   │   ├── _call_gpt_with_retry()
│   │   ├── _parse_json_response()
│   │   └── get_model_info()
│   │
│   ├── text_chunker.py             ◄─ Text Chunking
│   │   ├── TextChunker Class
│   │   ├── chunk_by_characters()
│   │   ├── chunk_by_sentences()
│   │   ├── chunk_by_paragraphs()
│   │   └── chunk_with_metadata()
│   │
│   └── output_formatter.py         ◄─ Output Formatting
│       ├── format_as_json()
│       ├── format_as_markdown()
│       ├── create_downloadable_json()
│       └── create_downloadable_markdown()
│
├── .env                            ◄─ Environment Variables (NOT in git)
│   ├── GEMINI_API_KEY
│   ├── AZURE_API_KEY
│   └── AZURE_ENDPOINT
│
├── requirements.txt                ◄─ Python Dependencies
│
├── README.md
│
└── Documentation/
    ├── RETRY_MECHANISM.md
    ├── RETRY_IMPLEMENTATION_SUMMARY.md
    ├── RETRY_FLOW_DIAGRAMS.md
    ├── MAX_TOKENS_IMPLEMENTATION.md
    └── ARCHITECTURE.md (this file)
```

---

## 8. Technology Stack Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ FRONTEND LAYER                                           │ │
│  │ • Streamlit 1.30.0      (Web UI Framework)              │ │
│  │ • Python 3.13           (Runtime)                        │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ PROCESSING LAYER                                         │ │
│  │ • PyPDF 4.0.0           (PDF text extraction)            │ │
│  │ • Python built-ins:     (JSON, regex, file I/O)         │ │
│  │   - json                                                 │ │
│  │   - re                                                   │ │
│  │   - time                                                 │ │
│  │   - os                                                   │ │
│  │ • tenacity 8.2.0        (Retry patterns)                │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ AI/LLM LAYER                                             │ │
│  │ • google-generativeai    (Google Gemini API SDK)        │ │
│  │ • openai 1.10.0          (Azure OpenAI SDK)             │ │
│  │   - AzureOpenAI client                                  │ │
│  │   - Chat completions API                                │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ CONFIGURATION LAYER                                      │ │
│  │ • python-dotenv 1.0.0   (Environment variable loading)  │ │
│  │ • .env file             (Local secrets storage)         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 9. Deployment Architecture (Optional)

```
┌──────────────────────────────────────────────────────────────┐
│              POTENTIAL DEPLOYMENT OPTIONS                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Option 1: LOCAL DEVELOPMENT                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ $ streamlit run app.py                                 │ │
│  │ → Runs on localhost:8501                               │ │
│  │ → Access via browser                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Option 2: STREAMLIT CLOUD                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ • GitHub repo with app.py                              │ │
│  │ • secrets.toml for API keys                            │ │
│  │ • Deploy via Streamlit Cloud dashboard                 │ │
│  │ → Public URL access                                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Option 3: DOCKER CONTAINER                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Dockerfile:                                            │ │
│  │ • Base: python:3.13-slim                              │ │
│  │ • Install: pip install -r requirements.txt            │ │
│  │ • Expose: port 8501                                   │ │
│  │ • CMD: streamlit run app.py                           │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Option 4: CLOUD RUN / AZURE CONTAINER INSTANCES           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ • Push Docker image to registry                        │ │
│  │ • Deploy to Google Cloud Run or Azure ACI             │ │
│  │ • Scale automatically based on load                    │ │
│  │ • Managed secrets through cloud platform              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 10. Security & Error Handling Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               SECURITY ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API KEY MANAGEMENT                                 │  │
│  │                                                      │  │
│  │  ✓ Keys stored in .env (NOT in git)                │  │
│  │  ✓ .gitignore includes .env                        │  │
│  │  ✓ Loaded via python-dotenv at startup             │  │
│  │  ✓ Never logged or displayed to user               │  │
│  │  ✓ Session-scoped (fresh load per run)             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ERROR HANDLING & LOGGING                            │  │
│  │                                                      │  │
│  │  • User-friendly error messages                     │  │
│  │  • API errors caught and wrapped                    │  │
│  │  • Retry logic prevents cascade failures            │  │
│  │  • Timeout protection (60s per request)             │  │
│  │  • File upload validation                           │  │
│  │                                                      │  │
│  │  Error Types:                                       │  │
│  │  ├─ Network Errors (retried)                        │  │
│  │  ├─ API Errors (logged + user feedback)             │  │
│  │  ├─ JSON Parse Errors (handled gracefully)          │  │
│  │  ├─ File Errors (validation + feedback)             │  │
│  │  └─ Timeout Errors (retry with backoff)             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DATA PRIVACY                                        │  │
│  │                                                      │  │
│  │  ✓ No persistent storage of user documents          │  │
│  │  ✓ Session-based (cleared on session end)           │  │
│  │  ✓ No data sent to third-party services             │  │
│  │  ✓ Only LLM APIs receive extracted content          │  │
│  │  ✓ User controls what to download                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 11. Processing Flow - Detailed Sequence

```
USER ──────────────────────┐
                          │
    ┌─────────────────────┴────────────────┐
    │   1. Open Application                │
    │   ├─ Load environment variables      │
    │   ├─ Initialize Streamlit UI         │
    │   └─ Setup session state             │
    │                                      │
    ▼                                      ▼
    2. Configure Settings            3. Provide Input
    ├─ Select Model                  ├─ Upload PDF
    ├─ Choose Output Format          ├─ Paste Text
    ├─ Enable Chunking (optional)    └─ View Preview
    ├─ Set Parameters
    └─ Configure Chunk Strategy
                                      │
                                      ▼
                        4. Click Extract Button
                        │
                        ▼
                    5. Process Input
                    ├─ Extract PDF/Text
                    ├─ Calculate tokens
                    ├─ Apply chunking (if enabled)
                    └─ Create prompts
                        │
                        ▼
                    6. Call AI Model
                    ├─ Prepare request
                    ├─ Send to API
                    ├─ Receive response
                    └─ Retry on error (up to 3x)
                        │
                        ├─ Success
                        │   ├─ Parse JSON
                        │   ├─ Store in session
                        │   └─ Display results
                        │
                        └─ Failure
                            ├─ Show error message
                            └─ Suggest retry
                        
                        ▼
                    7. Display Results
                    ├─ Show metadata
                    ├─ Display in tabs
                    │   ├─ Structured view
                    │   ├─ JSON code
                    │   └─ Markdown text
                    └─ Offer downloads
                        │
                        ▼
                    8. User Actions
                    ├─ Review Results
                    ├─ Download JSON
                    ├─ Download Markdown
                    ├─ Extract Another Article
                    └─ Close Application
```

---

## 12. Configuration & Parameter Summary

```
┌────────────────────────────────────────────────────┐
│          CONFIGURABLE PARAMETERS                   │
├────────────────────────────────────────────────────┤
│                                                    │
│  AI Model Parameters:                              │
│  ├─ max_tokens: 1-8000 (default: 4096)           │
│  ├─ temperature: 0.0-2.0 (default: 0.1)          │
│  ├─ max_retries: 1-10 (default: 3)               │
│  └─ initial_wait_time: 0.1-10s (default: 1s)     │
│                                                    │
│  Chunking Parameters:                              │
│  ├─ Enable: true/false (default: false)          │
│  ├─ Method: 'characters', 'sentences',           │
│  │   'paragraphs' (default: 'characters')         │
│  ├─ Chunk size: 100-5000 (default: 1000)         │
│  └─ Overlap: 0-2500 (default: 200)               │
│                                                    │
│  Output Parameters:                                │
│  ├─ Format: JSON, Markdown, Both                  │
│  └─ Download: JSON file, Markdown file            │
│                                                    │
│  API Parameters:                                   │
│  ├─ Timeout: 60 seconds (fixed)                   │
│  ├─ Response format: JSON object (fixed)          │
│  └─ Model: Gemini or GPT-4o-mini (user choice)   │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## Summary

This architecture provides:

✅ **Modular Design**: Each component has a single responsibility
✅ **Scalable**: Easy to add new AI models or processing techniques
✅ **Reliable**: Retry logic and error handling throughout
✅ **Secure**: API keys protected, no data persistence
✅ **User-Friendly**: Intuitive Streamlit UI
✅ **Extensible**: Well-documented, configurable parameters
✅ **Production-Ready**: Error handling, logging, timeouts

**Total System: Fully integrated, tested, and ready for deployment!**
