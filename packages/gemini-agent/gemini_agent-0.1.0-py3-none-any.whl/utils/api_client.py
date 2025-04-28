import os
import base64
import json
import requests
from typing import Dict, Any, Optional, List, Union


class GeminiClient:
    """
    Client for interacting with Google's Gemini API, handling both text and image inputs.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini API client.
        
        Args:
            api_key: Google Gemini API key. If None, it will try to get from environment variable.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set it via constructor or GEMINI_API_KEY environment variable.")
        
        # Base URL for Gemini API
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
        # Default model - we use gemini-2.0-flash for efficiency but can be changed
        self.model = "gemini-2.0-flash"
    
    def _encode_image(self, image_bytes: bytes) -> str:
        """
        Encode image bytes to base64.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Base64 encoded image string
        """
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def generate_content(self, 
                         text: str, 
                         image_bytes: Optional[bytes] = None,
                         temperature: float = 0.4,
                         max_output_tokens: int = 2048) -> Dict[str, Any]:
        """
        Generate content from Gemini API with text and optional image.
        
        Args:
            text: Text prompt
            image_bytes: Optional image bytes
            temperature: Sampling temperature (0.0 to 1.0)
            max_output_tokens: Maximum tokens to generate
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        # Prepare the content parts
        parts = [{"text": text}]
        
        # Add image if provided
        if image_bytes:
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": self._encode_image(image_bytes)
                }
            })
        
        # Construct the request payload
        payload = {
            "contents": [{
                "parts": parts
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens
            }
        }
        
        # Make the API request
        response = requests.post(url, json=payload)
        
        # Handle potential errors
        if response.status_code != 200:
            error_msg = f"API request failed with status code {response.status_code}: {response.text}"
            raise Exception(error_msg)
        
        return response.json()
    
    def extract_text_from_response(self, response: Dict[str, Any]) -> str:
        """
        Extract the generated text from the API response.
        
        Args:
            response: The API response dictionary
            
        Returns:
            Generated text content
        """
        try:
            return response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise ValueError(f"Failed to extract text from response: {e}")