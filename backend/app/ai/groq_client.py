"""
Groq LLM Client
Handles communication with Groq API for LLM operations
"""

import json
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings


class GroqClient:
    """
    Client for interacting with Groq API
    """
    
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    def __init__(self):
        """Initialize Groq client with API key from settings"""
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL_NAME
        self.timeout = settings.LLM_TIMEOUT
        self.max_tokens = settings.LLM_MAX_TOKENS
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY not configured in environment variables")
    
    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a completion using Groq LLM
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Sampling temperature (0-1, higher = more random)
            max_tokens: Maximum tokens to generate (overrides default)
            
        Returns:
            Generated text response
            
        Raises:
            httpx.HTTPError: If API request fails
            ValueError: If response parsing fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "top_p": 1,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    self.BASE_URL,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract the generated text
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    raise ValueError("Unexpected response structure from Groq API")
                    
            except httpx.TimeoutException:
                raise Exception(f"LLM request timed out after {self.timeout} seconds")
            except httpx.HTTPStatusError as e:
                raise Exception(f"LLM API error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                raise Exception(f"LLM request failed: {str(e)}")
    
    async def generate_json_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a JSON completion and parse it
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Parsed JSON object as dictionary
            
        Raises:
            Exception: If JSON parsing fails
        """
        response_text = await self.generate_completion(prompt, temperature, max_tokens)
        
        # Try to extract JSON from the response
        try:
            # Sometimes LLM adds markdown code blocks, strip them
            if "```json" in response_text:
                # Extract content between ```json and ```
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                # Extract content between ``` and ```
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            
            # Parse JSON with strict=False to allow control characters
            return json.loads(response_text, strict=False)
            
        except json.JSONDecodeError as e:
            # If parsing fails, try to find the last complete JSON object
            try:
                # Remove any trailing incomplete content
                last_brace = response_text.rfind('}')
                if last_brace > 0:
                    truncated = response_text[:last_brace + 1]
                    return json.loads(truncated, strict=False)
            except:
                pass
            
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}. Response: {response_text[:200]}")


# Global instance
groq_client = GroqClient()
