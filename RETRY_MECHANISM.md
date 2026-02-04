# Retry Mechanism Implementation

## Overview
A comprehensive retry mechanism has been implemented in the `AIProcessor` class to handle transient failures and improve reliability when calling external LLM APIs (Gemini and GPT-4o-mini).

## Features

### 1. **Exponential Backoff Strategy**
- Initial wait time: 1 second (configurable)
- Wait time doubles with each retry: 1s → 2s → 4s
- Formula: `wait_time = initial_wait_time * (2 ^ attempt)`

### 2. **Configurable Retry Parameters**
```python
AIProcessor(model_type, max_retries=3, initial_wait_time=1)
```
- `max_retries`: Maximum retry attempts (default: 3)
- `initial_wait_time`: Starting wait duration in seconds (default: 1)

### 3. **Intelligent Error Classification**
Only retries on **transient errors**:
- Connection timeouts
- Rate limiting (429, 503, 502, 500)
- Temporary service unavailability
- Network connectivity issues

**Does NOT retry** on permanent errors:
- Invalid API keys
- Malformed requests
- Authentication failures
- Invalid models

### 4. **Retry Flow**

#### For Gemini API (`_call_gemini_with_retry`):
```
Attempt 1 → Failure (transient) → Wait 1s
Attempt 2 → Failure (transient) → Wait 2s
Attempt 3 → Failure (transient) → Wait 4s
Attempt 4 → Failure → Raise Exception (max retries reached)
```

#### For GPT API (`_call_gpt_with_retry`):
```
Similar exponential backoff with timeout=60 seconds per request
```

### 5. **Implementation Details**

**Key Methods:**
- `_call_gemini_with_retry()`: Handles Gemini API calls with retry logic
- `_call_gpt_with_retry()`: Handles Azure OpenAI GPT-4o-mini calls with retry logic
- `extract_structure()`: Orchestrates the extraction with automatic retry

**Error Handling:**
```python
# Detects retryable errors
is_retryable = any(
    keyword in error_str 
    for keyword in ['timeout', 'connection', 'rate', '429', '500', '503', '502']
)

# Only retries if error is transient
if not is_retryable or attempt == self.max_retries - 1:
    raise  # Immediate raise for non-retryable errors
```

### 6. **Response Structure**
```python
{
    'success': True/False,
    'data': {...},  # Extracted data if successful
    'raw_response': '...',  # Raw API response
    'error': None or 'error message',
    'retry_count': 0-3  # Number of retries attempted
}
```

## Benefits

✅ **Increased Reliability**: Handles transient network issues automatically  
✅ **Cost Optimization**: Avoids redundant API calls for permanent errors  
✅ **Better User Experience**: Graceful degradation instead of immediate failures  
✅ **Configurable**: Retry strategy can be customized per use case  
✅ **Logging**: Console output shows retry attempts and wait times  
✅ **Timeout Protection**: 60-second timeout on GPT requests prevents hanging  

## Example Usage

```python
processor = AIProcessor(model_type='gpt4o-mini', max_retries=3, initial_wait_time=1)

result = processor.extract_structure(
    article_text,
    system_prompt,
    user_prompt_template
)

if result['success']:
    print(f"Extraction successful after {result['retry_count']} retries")
    print(result['data'])
else:
    print(f"Extraction failed: {result['error']}")
```

## Configuration

Adjust retry behavior by modifying initialization:
```python
# Aggressive retries (up to 5 attempts, 0.5s initial wait)
processor = AIProcessor('gemini', max_retries=5, initial_wait_time=0.5)

# Conservative retries (up to 2 attempts, 2s initial wait)
processor = AIProcessor('gpt4o-mini', max_retries=2, initial_wait_time=2)
```

## Testing

To test the retry mechanism:
1. Simulate network timeouts or rate limiting
2. Observe console output showing retry attempts
3. Verify successful extraction after transient failures

## Dependencies

Added to requirements.txt:
- `tenacity>=8.2.0` (for decorator-based retry patterns, future enhancement)

## Future Enhancements

- Implement circuit breaker pattern for cascading failures
- Add metrics/telemetry for retry success rates
- Support for custom retry predicates
- Integration with monitoring systems
