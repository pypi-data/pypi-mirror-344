import json
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "Google Generative AI package not found. Please install it with: pip install google-generativeai"
    )

@dataclass
class ProfanityInstance:
    """Data class representing a detected profanity instance."""
    original_form: str
    detection_method: str
    confidence_score: float
    normalized_form: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProfanityInstance':
        """Create a ProfanityInstance from a dictionary."""
        return cls(
            original_form=data.get('original_form', ''),
            detection_method=data.get('detection_method', ''),
            confidence_score=data.get('confidence_score', 0.0),
            normalized_form=data.get('normalized_form', '')
        )

@dataclass
class FilterResult:
    """Data class representing the result of a profanity filtering operation."""
    original_text: str
    filtered_text: str
    detected_profanity: List[ProfanityInstance]
    languages_detected: List[str]
    detected_count: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FilterResult':
        """Create a FilterResult from a dictionary."""
        detected_instances = [
            ProfanityInstance.from_dict(item) 
            for item in data.get('detected_profanity', [])
        ]
        
        metadata = data.get('metadata', {})
        
        return cls(
            original_text=data.get('original_text', ''),
            filtered_text=data.get('filtered_text', ''),
            detected_profanity=detected_instances,
            languages_detected=metadata.get('languages_detected', []),
            detected_count=metadata.get('total_instances', 0)
        )

class ProfanityFilter:
    """
    A class for detecting and filtering profanity in text using Google's Gemini API.
    
    This filter can detect standard and obfuscated profanity across multiple languages
    and provides detailed information about each detected instance.
    """
    
    # Default configuration
    DEFAULT_MODEL = "gemini-2.5-pro-exp-03-25"
    DEFAULT_TEMPERATURE = 0.1
    
    # Prompt template for the Gemini model
    PROMPT_TEMPLATE = """
You are a sophisticated profanity detection system with advanced pattern recognition capabilities. Your primary function is to identify and censor all forms of offensive language, including highly obfuscated profanity that uses complex encoding techniques.

Your detection algorithm must identify:

1. Standard profanity in any language
2. Obfuscated profanity using character substitutions (e.g., @ for a, 3 for e)
3. Stretched or repeated characters (e.g., "fuuuuuck" → "f***k")
4. Deliberately fragmented words with separators (spaces, underscores, dots, etc.)
5. Mixed case patterns designed to evade detection
6. Leetspeak and numeric substitutions
7. Phonetic equivalents and homoglyphs
8. Reversed or scrambled profanity
9. Context-sensitive profanity where meaning emerges from combinations
10. Language-specific profanity patterns including Cyrillic, Asian scripts, etc.

For complex obfuscation patterns like "XuE_s0S EbaNUUUUI", implement a multi-stage detection:

1. Normalize the text by:
   - Removing or consolidating separators (spaces, underscores, dots)
   - Standardizing character stretching (e.g., multiple 'U's become single 'U')
   - Converting leetspeak/numeric substitutions to standard characters
   - Analyzing phonetic patterns across language boundaries

2. Apply fuzzy matching algorithms with profanity dictionaries
   - Calculate Levenshtein distance to known profanity
   - Use n-gram analysis for partial matches
   - Apply phonetic algorithms (Soundex, Metaphone) for sound-alike detection
   - Implement sliding window analysis for fragmented profanity

3. Contextual analysis:
   - Evaluate surrounding words for semantic indicators of profanity
   - Check for known euphemisms and coded language
   - Identify language-mixing techniques (e.g., Russian-English hybrid profanity)

For each detected instance, replace the entire profane construction with asterisks matching the original length.

Return results in the following JSON format:
{{
  "original_text": "Complete unmodified input",
  "filtered_text": "Text with profanity replaced by asterisks",
  "detected_profanity": [
    {{
      "original_form": "The obfuscated text as found",
      "detection_method": "How it was identified (pattern/fuzzy/contextual)",
      "confidence_score": 0.XX,
      "normalized_form": "What the system believes it represents"
    }}
  ],
  "metadata": {{
    "total_instances": X,
    "languages_detected": ["en", "ru", etc.]
  }}
}}

If no profanity is detected, return the original text with empty detection arrays.

Please filter the following text:
[{text_to_filter}]
"""
    
    def __init__(self, api_key: str, model_name: str = None):
        """
        Initialize the ProfanityFilter.
        
        Args:
            api_key: The Google Gemini API key.
            model_name: The Gemini model to use. Defaults to DEFAULT_MODEL.
        
        Raises:
            ValueError: If no API key is provided.
            RuntimeError: If Gemini configuration fails.
        """
        # Validate API key
        if not api_key:
            raise ValueError("API key must be provided")
            
        self.api_key = api_key
        
        # Set model name
        self.model_name = model_name or self.DEFAULT_MODEL
        
        # Configure the Gemini API
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to configure Google GenAI: {e}")
    
    def filter_text(self, text: str, temperature: float = None) -> Optional[FilterResult]:
        """
        Filter profanity from the input text.
        
        Args:
            text: The text to filter.
            temperature: The temperature setting for generation (lower for more consistent results).
                        Defaults to DEFAULT_TEMPERATURE.
        
        Returns:
            A FilterResult object containing the filtered text and detection information,
            or None if an error occurred.
        """
        if not text:
            return None
            
        try:
            # Format the prompt with the input text
            final_prompt = self.PROMPT_TEMPLATE.format(text_to_filter=text)
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature if temperature is not None else self.DEFAULT_TEMPERATURE
            )
            
            # Send request to the API
            response = self.model.generate_content(
                final_prompt,
                generation_config=generation_config
            )
            
            # Check for valid response
            if not response.candidates:
                if hasattr(response, 'prompt_feedback'):
                    raise RuntimeError(f"No response from model: {response.prompt_feedback}")
                else:
                    raise RuntimeError("No response from model")
            
            # Extract text response
            response_text = response.text
            
            # Parse JSON from response
            # Handle cases where JSON is wrapped in code blocks
            if response_text.strip().startswith("```json"):
                response_text = response_text.strip()[7:-3].strip()
            elif response_text.strip().startswith("```"):
                response_text = response_text.strip()[3:-3].strip()
            
            try:
                result_json = json.loads(response_text)
                
                # Validate expected keys
                if not all(key in result_json for key in ["original_text", "filtered_text", "detected_profanity", "metadata"]):
                    raise ValueError("API response missing expected keys")
                
                # Convert to FilterResult object
                return FilterResult.from_dict(result_json)
                
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse JSON from API response: {response_text}")
                
        except Exception as e:
            # Just return None on error, let the caller handle it
            return None
    
    def __str__(self) -> str:
        """Return string representation of the filter."""
        return f"ProfanityFilter(model={self.model_name})"