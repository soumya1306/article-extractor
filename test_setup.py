"""
Simple test script to verify all components work correctly
Run this before starting the Streamlit app to check your setup
"""

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✓ Streamlit installed")
    except ImportError:
        print("✗ Streamlit not installed. Run: pip install streamlit")
        return False
    
    try:
        import pypdf
        print("✓ PyPDF installed")
    except ImportError:
        print("✗ PyPDF not installed. Run: pip install pypdf")
        return False
    
    try:
        import google.generativeai
        print("✓ Google Generative AI installed")
    except ImportError:
        print("✗ Google Generative AI not installed. Run: pip install google-generativeai")
        return False
    
    try:
        import openai
        print("✓ OpenAI installed")
    except ImportError:
        print("✗ OpenAI not installed. Run: pip install openai")
        return False
    
    print("\n✓ All required packages are installed!\n")
    return True


def test_module_structure():
    """Test if project structure is correct"""
    print("Testing module structure...")
    
    import os
    
    required_files = [
        'app.py',
        'requirements.txt',
        'utils/__init__.py',
        'utils/pdf_extractor.py',
        'utils/ai_processor.py',
        'utils/output_formatter.py',
        'config/__init__.py',
        'config/prompts.py'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    if all_exist:
        print("\n✓ All required files are present!\n")
    else:
        print("\n✗ Some files are missing. Please check the project structure.\n")
    
    return all_exist


def test_module_imports():
    """Test if custom modules can be imported"""
    print("Testing custom module imports...")
    
    try:
        from config.prompts import EXTRACTION_SYSTEM_PROMPT, EXTRACTION_USER_PROMPT_TEMPLATE
        print("✓ Prompts module imported")
    except ImportError as e:
        print(f"✗ Failed to import prompts: {e}")
        return False
    
    try:
        from utils.pdf_extractor import extract_text_from_pdf, extract_text_from_abstract
        print("✓ PDF extractor module imported")
    except ImportError as e:
        print(f"✗ Failed to import pdf_extractor: {e}")
        return False
    
    try:
        from utils.ai_processor import AIProcessor
        print("✓ AI processor module imported")
    except ImportError as e:
        print(f"✗ Failed to import ai_processor: {e}")
        return False
    
    try:
        from utils.output_formatter import format_as_json, format_as_markdown
        print("✓ Output formatter module imported")
    except ImportError as e:
        print(f"✗ Failed to import output_formatter: {e}")
        return False
    
    print("\n✓ All custom modules imported successfully!\n")
    return True


def test_text_extraction():
    """Test text extraction with sample text"""
    print("Testing text extraction...")
    
    try:
        from utils.pdf_extractor import extract_text_from_abstract, estimate_tokens
        
        sample_text = """
        CRISPR-Cas9 in Cancer Treatment
        
        Background: Cancer is a major health challenge.
        Methods: We used CRISPR-Cas9 gene editing.
        Results: 85% efficiency was achieved.
        Conclusions: This approach shows promise.
        """
        
        result = extract_text_from_abstract(sample_text)
        if result['success']:
            print("✓ Text extraction working")
            tokens = estimate_tokens(sample_text)
            print(f"  Sample text: ~{tokens} tokens")
        else:
            print(f"✗ Text extraction failed: {result['error']}")
            return False
        
    except Exception as e:
        print(f"✗ Text extraction test failed: {e}")
        return False
    
    print("\n✓ Text extraction is working!\n")
    return True


def test_output_formatting():
    """Test output formatting"""
    print("Testing output formatting...")
    
    try:
        from utils.output_formatter import format_as_json, format_as_markdown
        
        sample_data = {
            "title": "Test Article",
            "authors": "Test Author",
            "journal": "Test Journal",
            "year": "2024",
            "background": {
                "summary": "Test background",
                "key_points": ["Point 1", "Point 2"]
            },
            "methods": {
                "summary": "Test methods",
                "key_points": ["Method 1", "Method 2"]
            }
        }
        
        json_output = format_as_json(sample_data)
        if json_output and '"title"' in json_output:
            print("✓ JSON formatting working")
        else:
            print("✗ JSON formatting failed")
            return False
        
        md_output = format_as_markdown(sample_data)
        if md_output and "# Test Article" in md_output:
            print("✓ Markdown formatting working")
        else:
            print("✗ Markdown formatting failed")
            return False
        
    except Exception as e:
        print(f"✗ Output formatting test failed: {e}")
        return False
    
    print("\n✓ Output formatting is working!\n")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Research Article Extractor - Setup Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Package Installation", test_imports),
        ("File Structure", test_module_structure),
        ("Module Imports", test_module_imports),
        ("Text Extraction", test_text_extraction),
        ("Output Formatting", test_output_formatting),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with error: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the application.")
        print("\nRun: streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running the app.")
        print("\nCheck:")
        print("1. All packages installed: pip install -r requirements.txt")
        print("2. All files in correct locations")
        print("3. __init__.py files exist in utils/ and config/ directories")
    
    print()


if __name__ == "__main__":
    main()
