
from google import genai
from openai import OpenAI, AzureOpenAI
import json
import os


class AIProcessor:
    
    def __init__(self, model_type):

        self.model_type = model_type.lower()
        
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

        try:
            user_prompt = user_prompt_template.format(article_text=article_text)
            
            if self.model_type == 'gemini':
                response = self._call_gemini(system_prompt, user_prompt)
            else:
                response = self._call_gpt(system_prompt, user_prompt)
            
            result = self._parse_json_response(response) or {}
            
            return {
                'success': True,
                'data': result,
                'raw_response': response,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'raw_response': None,
                'error': str(e)
            }
    

    def _call_gemini(self, system_prompt, user_prompt):

        # Combine system and user prompts for Gemini
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = self.model.models.generate_content(
            contents=full_prompt,
            model="gemini-3-flash-preview",
        )
        
        return response.text
    

    def _call_gpt(self, system_prompt, user_prompt):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Low temperature for consistent extraction
            max_tokens=4096,
            response_format={"type": "json_object"}  # Request JSON format
        )
        
        return response.choices[0].message.content
    

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

        if self.model_type == 'gemini':
            return {
                'name': 'Gemini 3 Flash Preview',
                'provider': 'Google',
                'context_window': '1M tokens',
                'pricing': 'Free tier available, paid plans start at $0.002 per 1K tokens'
            }
        else:
            return {
                'name': 'GPT-4o-mini',
                'provider': 'OpenAI',
                'context_window': '128K tokens',
                'pricing': '$0.15 per 1M input tokens, $0.60 per 1M output tokens'
            }
