
from google import genai
from openai import OpenAI, AzureOpenAI
import json
import os
import time
from typing import Dict, Any, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result
)


class AIProcessor:
    
    def __init__(self, model_type, max_retries=3, initial_wait_time=1, max_tokens=4096, temperature=0.1):
        """
        Initialize AIProcessor with retry and model configuration.
        
        Args:
            model_type: Type of model ('gemini' or 'gpt4o-mini')
            max_retries: Maximum number of retry attempts (default: 3)
            initial_wait_time: Initial wait time in seconds for exponential backoff (default: 1)
            max_tokens: Maximum tokens in response (default: 4096)
            temperature: Model temperature for response randomness (default: 0.1 - low for consistency)
        """
        self.model_type = model_type.lower()
        self.max_retries = max_retries
        self.initial_wait_time = initial_wait_time
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        if self.model_type == 'gemini': 
            api_key = os.getenv("GEMINI_API_KEY") or ""
            self.model = genai.Client(api_key=api_key)
        elif self.model_type == 'gpt4o-mini':
            
            #use this if you are using vanilla OpenAI
            #self.client = OpenAI(api_key=api_key) 
            
            #use this if you are using Azure OpenAI
            self.api_key = os.getenv("AZURE_API_KEY") or ""
            azure_endpoint = os.getenv("AZURE_ENDPOINT") or ""
            api_version = "2024-12-01-preview"
                
            self.client = AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=azure_endpoint,
                api_version=api_version
                )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    

    def extract_structure(self, article_text, system_prompt, user_prompt_template):
        """
        Extract structure from article text with automatic retry on failure.
        
        Args:
            article_text: The article text to extract from
            system_prompt: System prompt for the LLM
            user_prompt_template: User prompt template
            
        Returns:
            Dictionary with success status, extracted data, and error details
        """
        try:
            user_prompt = user_prompt_template.format(article_text=article_text)
            
            # Call appropriate LLM with retry logic
            if self.model_type == 'gemini':
                response = self._call_gemini_with_retry(system_prompt, user_prompt)
            else:
                response = self._call_gpt_with_retry(system_prompt, user_prompt)
            
            result = self._parse_json_response(response) or {}
            
            return {
                'success': True,
                'data': result,
                'raw_response': response,
                'error': None,
                'retry_count': 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'raw_response': None,
                'error': str(e),
                'retry_count': self.max_retries
            }
    
    def _call_gemini_with_retry(self, system_prompt, user_prompt):
        """
        Call Gemini API with exponential backoff retry logic.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            
        Returns:
            API response text
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                # Combine system and user prompts for Gemini
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                
                response = self.model.models.generate_content(
                    contents=full_prompt,
                    model="gemini-3-flash-preview",
                )
                
                return response.text
                
            except Exception as e:
                last_exception = e
                
                # Check if error is retryable (connection, timeout, rate limit)
                error_str = str(e).lower()
                is_retryable = any(
                    keyword in error_str 
                    for keyword in ['timeout', 'connection', 'rate', '429', '500', '503', '502']
                )
                
                if not is_retryable or attempt == self.max_retries - 1:
                    raise
                
                # Exponential backoff: wait_time = initial_wait_time * (2 ^ attempt)
                wait_time = self.initial_wait_time * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
        
        if last_exception:
            raise last_exception
        raise RuntimeError("Maximum retry attempts failed for Gemini API")
    
    def _call_gpt_with_retry(self, system_prompt, user_prompt):
        """
        Call GPT API with exponential backoff retry logic.
        
        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            
        Returns:
            API response text
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    response_format={"type": "json_object"},  # Request JSON format
                    timeout=60  # 60 second timeout per request
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                last_exception = e
                
                # Check if error is retryable (connection, timeout, rate limit)
                error_str = str(e).lower()
                is_retryable = any(
                    keyword in error_str 
                    for keyword in ['timeout', 'connection', 'rate', '429', '500', '503', '502', 'temporarily']
                )
                
                if not is_retryable or attempt == self.max_retries - 1:
                    raise
                
                # Exponential backoff: wait_time = initial_wait_time * (2 ^ attempt)
                wait_time = self.initial_wait_time * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
        
        if last_exception:
            raise last_exception
        raise RuntimeError("Maximum retry attempts failed for GPT API")
    

    def _parse_json_response(self, response):

        # Remove markdown code block formatting if present
        cleaned = response.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            import re
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Failed to parse JSON response: {str(e)}")
    
    def get_model_info(self):
        """Get information about the configured model and parameters"""
        
        base_info = {
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'max_retries': self.max_retries,
            'initial_wait_time': self.initial_wait_time,
        }
        
        if self.model_type == 'gemini':
            return {
                **base_info,
                'name': 'Gemini Flash 3 Preview',
                'provider': 'Google',
                'context_window': '1M tokens',
                'pricing': 'Free tier available, paid plans start at $0.002 per 1K tokens'
            }
        else:
            return {
                **base_info,
                'name': 'GPT-4o-mini',
                'provider': 'OpenAI',
                'context_window': '128K tokens',
                'pricing': '$0.15 per 1M input tokens, $0.60 per 1M output tokens'
            }
