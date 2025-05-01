import json
import traceback
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("profanity_filter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ProfanityFilter")

try:
    import google.generativeai as genai
except ImportError:
    logger.critical("Google Generative AI package not found")
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
    reasoning: str  # Added field for detection reasoning
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProfanityInstance':
        """Create a ProfanityInstance from a dictionary."""
        try:
            return cls(
                original_form=data.get('original_form', ''),
                detection_method=data.get('detection_method', ''),
                confidence_score=data.get('confidence_score', 0.0),
                normalized_form=data.get('normalized_form', ''),
                reasoning=data.get('reasoning', '')
            )
        except Exception as e:
            logger.error(f"Failed to create ProfanityInstance from data: {e}")
            logger.debug(f"Data: {data}")
            raise ValueError(f"Failed to create ProfanityInstance: {e}")

@dataclass
class FilterResult:
    """Data class representing the result of a profanity filtering operation."""
    original_text: str
    filtered_text: str
    detected_profanity: List[ProfanityInstance]
    languages_detected: List[str]
    detected_count: int
    analysis_steps: List[str]  # Added field for analysis steps
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FilterResult':
        """Create a FilterResult from a dictionary."""
        try:
            detected_instances = []
            for item in data.get('detected_profanity', []):
                try:
                    instance = ProfanityInstance.from_dict(item)
                    detected_instances.append(instance)
                except Exception as e:
                    logger.warning(f"Failed to parse profanity instance: {e}")
                    logger.debug(f"Instance data: {item}")
            
            metadata = data.get('metadata', {})
            
            return cls(
                original_text=data.get('original_text', ''),
                filtered_text=data.get('filtered_text', ''),
                detected_profanity=detected_instances,
                languages_detected=metadata.get('languages_detected', []),
                detected_count=metadata.get('total_instances', 0),
                analysis_steps=metadata.get('analysis_steps', [])
            )
        except Exception as e:
            logger.error(f"Failed to create FilterResult from data: {e}")
            logger.debug(f"Data: {data}")
            raise ValueError(f"Failed to create FilterResult: {e}")

class ProfanityFilter:
    """
    A class for detecting and filtering profanity in text using Google's Gemini API.
    
    This filter can detect standard and obfuscated profanity across multiple languages
    and provides detailed information about each detected instance.
    """
    
    # Default configuration
    DEFAULT_MODEL = "gemini-2.5-pro-exp-03-25"
    DEFAULT_TEMPERATURE = 0.1
    
    # Исправленный шаблон с экранированными фигурными скобками в JSON примере
    PROMPT_TEMPLATE = """
You are an advanced profanity detection system with sophisticated pattern recognition capabilities. Your task is to identify both obvious and highly obfuscated profanity while avoiding false positives on legitimate words.

# Multi-Stage Detection Process

You must follow this step-by-step process for EVERY potential profanity detection, documenting your reasoning at each stage:

## STAGE 1: Initial Text Processing
- Break down input text into tokens and analyze each token
- Identify language(s) present in the text
- Normalize text by converting to lowercase
- Extract potential suspicious patterns for deeper analysis

## STAGE 2: Advanced Obfuscation Analysis
For each suspicious pattern, apply these techniques:
1. Character substitution decoding:
   - Replace numbers with visually similar letters (1→i, 3→e, 4→a, 5→s, 0→o, etc.)
   - Replace special characters with similar letters (@→a, $→s, etc.)
   - Convert Cyrillic characters to Latin equivalents and vice versa

2. Pattern normalization:
   - Remove or consolidate separators (spaces, dots, underscores)
   - Remove repeated characters (e.g., "sooooosi" → "sosi")
   - Apply phonetic normalization (e.g., "xa-xa" → "haha")

3. Leetspeak decoding:
   - Convert complex leetspeak like "S0c1" to potential word forms ("soci", "sosi")
   - Apply multiple transformation rules and check all resulting variants

4. Cross-script analysis:
   - Detect mixing of scripts (Latin, Cyrillic, etc.) to obfuscate words
   - Normalize across scripts to detect hybrid profanity

## STAGE 3: Linguistic Analysis
For each normalized pattern:
1. Check against profanity dictionaries in detected languages
2. Apply fuzzy matching with Levenshtein distance threshold
3. Check for phonetic equivalence (how it sounds when pronounced)
4. Analyze for partial matches and common obfuscation patterns
5. Check for word fragments that could be parts of profanity

## STAGE 4: Context Validation & False Positive Prevention
For each potential match:
1. Verify if the normalized form is actually profanity in any detected language
2. Check if it's a legitimate word that happens to match profanity patterns
3. Analyze surrounding context to determine intent
4. Apply higher confidence thresholds for ambiguous cases
5. Check against list of known false positives

# Specific Obfuscation Techniques to Detect

You must be able to detect profanity hidden using these techniques:

1. Numeric/symbol substitutions:
   - "S0c1" → "sosi" (Russian profanity)
   - "X3R" → "her" (profanity in multiple languages)
   - "B1@t" → "blat" (profanity in Slavic languages)

2. Phonetic obfuscation:
   - "fuk" or "phuck" → common English profanity
   - "blyad" or "bliat" → Russian profanity

3. Deliberate fragmentation:
   - "s u c k m y d" → offensive phrase
   - "п и з д е ц" → Russian profanity

4. Mixed script obfuscation:
   - "хуй" written as "xyй" using Latin characters
   - "fuck" written as "фуcк" using Cyrillic characters

5. Complex encoding:
   - "5uk@" → "suka" (Russian profanity)
   - "d!¢k" → English profanity

# Confidence Scoring System

Calculate confidence scores based on:
1. Closeness to known profanity (Levenshtein distance)
2. Number of transformations required to reach profane form
3. Contextual indicators of intent to use profanity
4. Presence of surrounding profanity or offensive context

# Response Format

Return results in the following JSON format:
{{
  "original_text": "Complete unmodified input",
  "filtered_text": "Text with confirmed profanity replaced by asterisks",
  "detected_profanity": [
    {{
      "original_form": "The obfuscated text as found",
      "detection_method": "Detailed method used (transformation rules applied)",
      "confidence_score": 0.XX,
      "normalized_form": "The actual profanity it represents",
      "reasoning": "Step-by-step explanation of how this was detected"
    }}
  ],
  "metadata": {{
    "total_instances": X,
    "languages_detected": ["en", "ru", etc.],
    "analysis_steps": [
      "Step 1: Initial tokenization results",
      "Step 2: Suspicious patterns identified",
      "Step 3: Transformation rules applied",
      "Step 4: Matching results against profanity dictionaries",
      "Step 5: Context validation process"
    ]
  }}
}}

# False Positive Prevention

While being thorough in detection, you must still avoid false positives on:
- Legitimate words in any language (e.g., "застрахуй" in Russian)
- Technical or scientific terms (e.g., "скипидар")
- Names of chemicals, medications, or maritime terms
- Professional terminology

# Critical Instructions

1. Always document your complete reasoning process for each detection
2. For complex obfuscation like "S0c1", show the exact transformation path to "sosi"
3. For ambiguous cases, include additional context analysis
4. Be extremely sensitive to highly obfuscated profanity
5. Use your knowledge of multiple languages to detect cross-language profanity

Please analyze the following text, showing your complete detection process:
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
            logger.error("API key not provided")
            raise ValueError("API key must be provided")
            
        self.api_key = api_key
        
        # Set model name
        self.model_name = model_name or self.DEFAULT_MODEL
        logger.info(f"Initializing ProfanityFilter with model: {self.model_name}")
        
        # Configure the Gemini API
        try:
            logger.debug("Configuring Google GenAI API")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info("Successfully initialized Gemini API")
        except Exception as e:
            error_msg = f"Failed to configure Google GenAI: {e}"
            logger.critical(error_msg)
            logger.debug(traceback.format_exc())
            raise RuntimeError(error_msg)
    
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
            logger.warning("Empty text provided to filter_text")
            return None
            
        try:
            logger.info(f"Filtering text (length: {len(text)})")
            logger.debug(f"Input text: {text}")
            
            # Format the prompt with the input text
            final_prompt = self.PROMPT_TEMPLATE.format(text_to_filter=text)
            
            # Configure generation parameters
            temperature_value = temperature if temperature is not None else self.DEFAULT_TEMPERATURE
            logger.debug(f"Using temperature: {temperature_value}")
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature_value
            )
            
            # Send request to the API
            logger.debug("Sending request to Gemini API")
            try:
                response = self.model.generate_content(
                    final_prompt,
                    generation_config=generation_config
                )
                logger.debug("Received response from Gemini API")
            except genai.types.BlockedPromptException as e:
                logger.error(f"Prompt was blocked by safety filters: {e}")
                return None
            except Exception as e:
                logger.error(f"API request failed: {e}")
                logger.debug(traceback.format_exc())
                return None
            
            # Check for valid response
            if not response.candidates:
                error_msg = ""
                if hasattr(response, 'prompt_feedback'):
                    error_msg = f"No response from model: {response.prompt_feedback}"
                else:
                    error_msg = "No response from model (no candidates returned)"
                
                logger.error(error_msg)
                return None
            
            # Extract text response
            response_text = response.text
            logger.debug(f"Raw response text: {response_text[:200]}...")
            
            # Parse JSON from response
            # Handle cases where JSON is wrapped in code blocks
            if response_text.strip().startswith("```json"):
                logger.debug("Detected JSON code block with language identifier")
                response_text = response_text.strip()[7:-3].strip()
            elif response_text.strip().startswith("```"):
                logger.debug("Detected generic code block")
                response_text = response_text.strip()[3:-3].strip()
            
            try:
                logger.debug("Parsing JSON response")
                result_json = json.loads(response_text)
                
                # Validate expected keys
                required_keys = ["original_text", "filtered_text", "detected_profanity", "metadata"]
                missing_keys = [key for key in required_keys if key not in result_json]
                
                if missing_keys:
                    error_msg = f"API response missing expected keys: {', '.join(missing_keys)}"
                    logger.error(error_msg)
                    logger.debug(f"Response JSON: {result_json}")
                    return None
                
                # Convert to FilterResult object
                logger.debug("Creating FilterResult from JSON")
                result = FilterResult.from_dict(result_json)
                logger.info(f"Successfully filtered text. Found {result.detected_count} instances of profanity.")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from API response: {e}")
                logger.debug(f"Response text causing JSON error: {response_text}")
                return None
                
        except Exception as e:
            logger.error(f"Unexpected error in filter_text: {e}")
            logger.debug(traceback.format_exc())
            return None
    
    def __str__(self) -> str:
        """Return string representation of the filter."""
        return f"ProfanityFilter(model={self.model_name})"