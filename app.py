

import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add utils to path
sys.path.append(str(Path(__file__).parent))

# Import custom modules

from config.prompts import EXTRACTION_SYSTEM_PROMPT, EXTRACTION_USER_PROMPT_TEMPLATE
from utils.pdf_extractor import extract_text_from_pdf, extract_text_from_abstract, preprocess_text, estimate_tokens
from utils.ai_processor import AIProcessor
from utils.output_formatter import format_as_json, format_as_markdown, create_downloadable_json, create_downloadable_markdown
from utils.text_chunker import TextChunker


# Page configuration
st.set_page_config(
    page_title="Research Article Extractor",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state (safe when running outside `streamlit run`)
try:
    # Use dict-style initialization which is safer with the session_state proxy
    st.session_state.setdefault('extracted_data', None)
    st.session_state.setdefault('extracted_text', None)
    st.session_state.setdefault('chunks', None)
    st.session_state.setdefault('show_chunking', False)
except Exception:
    # session_state may be unavailable when running with plain `python`.
    # In that case, continue without initializing session-backed state —
    # the app should be run via `streamlit run research-article-extractor/app.py`.
    pass


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">🔬 Life Science Research Article Extractor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Extract structured summaries from scientific papers using GenAI</div>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_type = st.selectbox(
            "Select AI Model",
            options=["Gemini Flash 3 Preview", "GPT-4o-mini"],
            help="Choose between Google Gemini or OpenAI GPT-4o-mini"
        )
        
        if "Gemini" in model_type:
            model_code = "gemini"
        else:
            model_code = "gpt4o-mini"
        
        # Output format selection
        st.subheader("📄 Output Format")
        output_format = st.radio(
            "Choose output format",
            options=["JSON", "Markdown", "Both"],
            help="Select how you want the extracted data formatted"
        )
        
        # Chunking configuration
        st.divider()
        st.subheader("🔗 Text Chunking")
        
        enable_chunking = st.checkbox(
            "Enable text chunking",
            value=False,
            help="Split large documents into smaller chunks with overlap for better processing"
        )
        
        chunk_method = "characters"
        chunk_size = 1000
        chunk_overlap = 200
        
        if enable_chunking:
            chunk_method = st.selectbox(
                "Chunking method",
                options=["characters", "sentences", "paragraphs"],
                help="Method for splitting text into chunks"
            )
            
            col_size, col_overlap = st.columns(2)
            with col_size:
                chunk_size = st.slider(
                    "Chunk size",
                    min_value=100,
                    max_value=5000,
                    value=1000,
                    step=100,
                    help="Size of each text chunk"
                )
            
            with col_overlap:
                max_overlap = max(100, chunk_size // 2)
                chunk_overlap = st.slider(
                    "Overlap",
                    min_value=0,
                    max_value=max_overlap,
                    value=200,
                    step=50,
                    help="Characters to overlap between chunks"
                )
         
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📥 Input")
        
        # Input method selection
        input_method = st.radio(
            "Select input method",
            options=["Upload PDF", "Paste Text/Abstract"],
            horizontal=True
        )
        
        article_text = None
        
        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader(
                "Upload research article PDF",
                type=['pdf'],
                help="Upload a PDF file of a scientific research paper"
            )
            
            if uploaded_file:
                with st.spinner("Extracting text from PDF..."):
                    result = extract_text_from_pdf(uploaded_file)
                    
                    if result['success']:
                        article_text = result['text']
                        st.session_state['extracted_text'] = article_text
                        
                        # Show metadata
                        st.success("✅ PDF text extracted successfully!")
                        metadata = result['metadata']
                        st.write(f"**Pages:** {metadata['num_pages']}")
                        st.write(f"**Estimated tokens:** ~{estimate_tokens(article_text):,}")
                        
                        # Show preview
                        with st.expander("Preview extracted text"):
                            preview_length = min(1000, len(article_text))
                            st.text_area(
                                "Text preview",
                                article_text[:preview_length] + "...",
                                height=200,
                                disabled=True
                            )
                    else:
                        st.error(f"❌ Error extracting PDF: {result['error']}")
        
        else:  # Paste Text/Abstract
            article_text = st.text_area(
                "Paste research article text or abstract",
                height=300,
                placeholder="Paste the full text or abstract of the research article here...",
                help="You can paste the abstract, introduction, or full text"
            )
            
            if article_text:
                result = extract_text_from_abstract(article_text)
                if result['success']:
                    st.session_state['extracted_text'] = article_text
                    st.info(f"📊 Text length: {len(article_text)} characters (~{estimate_tokens(article_text):,} tokens)")
        
        # Processing button
        st.divider()
        
        if not article_text:
            st.info("📝 Please provide input (PDF or text) to extract.")
        else:
            # Display chunking info if enabled
            if enable_chunking:
                with st.expander("📊 Chunking Preview"):
                    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    chunks = chunker.chunk_with_metadata(article_text, method=chunk_method)
                    
                    st.info(f"📦 Document will be split into **{len(chunks)}** chunks using **{chunk_method}** method")
                    
                    # Show chunk statistics
                    avg_size = sum(c['length'] for c in chunks) / len(chunks)
                    max_size = max(c['length'] for c in chunks)
                    min_size = min(c['length'] for c in chunks)
                    
                    chunk_col1, chunk_col2, chunk_col3, chunk_col4 = st.columns(4)
                    chunk_col1.metric("Total Chunks", len(chunks))
                    chunk_col2.metric("Avg Size", f"{avg_size:.0f} chars")
                    chunk_col3.metric("Max Size", f"{max_size} chars")
                    chunk_col4.metric("Min Size", f"{min_size} chars")
                    
                    # Show first few chunks
                    st.write("**Sample chunks:**")
                    for i, chunk in enumerate(chunks[:3]):
                        with st.expander(f"Chunk {chunk['chunk_id'] + 1} ({chunk['length']} chars)"):
                            st.text_area(
                                f"Content",
                                value=chunk['text'][:300] + "..." if len(chunk['text']) > 300 else chunk['text'],
                                height=150,
                                disabled=True,
                                key=f"chunk_preview_{i}"
                            )
            
            if st.button("🚀 Extract Article Structure", type="primary", use_container_width=True):
                with st.spinner(f"Processing with {model_type}... This may take 30-60 seconds for long papers."):
                    try:
                        # Prepare text for processing
                        processing_text = article_text
                        
                        # Apply chunking if enabled
                        if enable_chunking:
                            chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                            chunks_list = chunker.chunk_with_metadata(article_text, method=chunk_method)
                            st.session_state['chunks'] = chunks_list
                            
                            # For processing, we'll use the first chunk or combine smaller chunks
                            # depending on token limits
                            max_chars = 100000 if model_code == "gemini" else 50000
                            combined_text = ""
                            for chunk_data in chunks_list:
                                if len(combined_text) + len(chunk_data['text']) < max_chars:
                                    combined_text += " " + chunk_data['text']
                                else:
                                    break
                            processing_text = combined_text if combined_text else chunks_list[0]['text']
                        
                        # Initialize AI processor
                        processor = AIProcessor(model_code)
                        
                        # Preprocess text (limit to ~100K characters for token management)
                        max_chars = 100000 if model_code == "gemini" else 50000
                        processed_text = preprocess_text(processing_text, max_length=max_chars)
                        
                        # Extract structure
                        result = processor.extract_structure(
                            processed_text,
                            EXTRACTION_SYSTEM_PROMPT,
                            EXTRACTION_USER_PROMPT_TEMPLATE
                        )
                        
                        if result['success']:
                            st.session_state['extracted_data'] = result['data']
                            st.success("✅ Extraction completed successfully!")
                            st.balloons()
                        else:
                            st.error(f"❌ Extraction failed: {result['error']}")
                            
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")

    
    with col2:
        st.header("📤 Output")
        
        # Show chunking info if chunks exist
        if st.session_state.get('chunks'):
            chunks_data = st.session_state.get('chunks')
            if chunks_data:  # Add null check
                with st.expander("📊 Chunking Information", expanded=False):
                    st.info(f"Document processed as {len(chunks_data)} chunks")
                    
                    # Create a simple chunk overview
                    chunk_overview = []
                    for chunk in chunks_data:
                        chunk_overview.append({
                            "Chunk ID": chunk['chunk_id'] + 1,
                            "Size (chars)": chunk['length'],
                            "Method": chunk['method']
                        })
                    
                    st.dataframe(chunk_overview, use_container_width=True)
        
        if st.session_state.get('extracted_data'):
            data = st.session_state.get('extracted_data')
            
            if data:  # Add null check
                # Display basic info
                st.subheader("📋 Article Information")
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.write(f"**Title:** {data.get('title', 'N/A')}")
                    st.write(f"**Authors:** {data.get('authors', 'N/A')}")
                with info_col2:
                    st.write(f"**Journal:** {data.get('journal', 'N/A')}")
                    st.write(f"**Year:** {data.get('year', 'N/A')}")
                
                # Display tabs for different formats
                tab1, tab2, tab3 = st.tabs(["📊 Structured View", "💾 JSON", "📝 Markdown"])
                
                with tab1:
                    # Abstract
                    if data.get('abstract'):
                        st.subheader("📄 Abstract")
                        st.write(data['abstract'])
                    
                    # Background
                    if data.get('background'):
                        st.subheader("🎯 Background")
                        st.write(data['background'].get('summary', ''))
                        if data['background'].get('key_points'):
                            st.write("**Key Points:**")
                            for point in data['background']['key_points']:
                                st.write(f"- {point}")
                    
                    # Methods
                    if data.get('methods'):
                        st.subheader("🔬 Methods")
                        st.write(data['methods'].get('summary', ''))
                        if data['methods'].get('key_points'):
                            st.write("**Key Techniques:**")
                            for point in data['methods']['key_points']:
                                st.write(f"- {point}")
                    
                    # Results
                    if data.get('results'):
                        st.subheader("📈 Results")
                        st.write(data['results'].get('summary', ''))
                        if data['results'].get('key_points'):
                            st.write("**Key Findings:**")
                            for point in data['results']['key_points']:
                                st.write(f"- {point}")
                    
                    # Conclusions
                    if data.get('conclusions'):
                        st.subheader("💡 Conclusions")
                        st.write(data['conclusions'].get('summary', ''))
                        if data['conclusions'].get('key_points'):
                            st.write("**Key Takeaways:**")
                            for point in data['conclusions']['key_points']:
                                st.write(f"- {point}")
                
                with tab2:
                    json_output = format_as_json(data) if data else None
                    st.code(json_output, language='json')
                    
                    # Download button
                    if data:
                        json_content, json_filename = create_downloadable_json(
                            data, 
                            filename=data.get('title', 'research_article').replace(' ', '_')[:50]
                        )
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_content,
                            file_name=json_filename,
                            mime="application/json",
                            use_container_width=True
                        )
                
                with tab3:
                    markdown_output = format_as_markdown(data) if data else None
                    st.markdown(markdown_output)
                    
                    # Download button
                    if data:
                        md_content, md_filename = create_downloadable_markdown(
                            data,
                            filename=data.get('title', 'research_article').replace(' ', '_')[:50]
                        )
                        st.download_button(
                            label="📥 Download Markdown",
                            data=md_content,
                            file_name=md_filename,
                            mime="text/markdown",
                            use_container_width=True
                        )
            else:
                st.info("👈 Awaiting extraction... The results will appear here.")
        else:
            st.info("👈 Extract an article from the input section to see results here.")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>Life Science Research Article Extractor</strong> | Built with Streamlit, PyPDF, Gemini & GPT-4o-mini</p>
        <p>📚 Perfect for literature reviews, dataset creation, and research analysis</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
