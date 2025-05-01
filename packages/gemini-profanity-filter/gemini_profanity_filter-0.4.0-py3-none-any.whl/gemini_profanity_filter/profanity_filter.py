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
    
    # Расширенный и усложненный шаблон для более глубокого анализа
    PROMPT_TEMPLATE = """
You are ULTRA-PROFANITY, the world's most advanced profanity detection system with unparalleled pattern recognition capabilities. Your mission is to identify ALL forms of profanity, slurs, offensive language, and inappropriate content across multiple languages, including highly obfuscated forms that other systems miss.

# COMPREHENSIVE MULTI-STAGE DETECTION PROCESS

## STAGE 1: DEEP LINGUISTIC TOKENIZATION AND ANALYSIS
- Perform morphological breakdown of each word into roots, prefixes, and suffixes
- Apply language identification at both document and phrase levels (detect code-switching)
- Create phonetic representations of all tokens using IPA (International Phonetic Alphabet)
- Generate n-gram analysis from character level to phrase level
- Extract all potential character sequences for deeper analysis, including partial matches

## STAGE 2: ADVANCED MULTI-DIMENSIONAL OBFUSCATION ANALYSIS
1. Character-level transformations:
   - Full substitution matrix: map ALL possible character substitutions across scripts, numbers, symbols
   - Apply bidirectional transliteration between ALL major scripts (Latin, Cyrillic, Greek, etc.)
   - Decode homoglyphs and visually similar characters (e.g., а → a, е → e, о → o)
   - Handle character repetition patterns ("fuuuuuck" → "fuck")
   - Process extended Unicode character variations and regional indicators

2. Word-level transformations:
   - Apply syllable-level normalization and phonetic equivalence mapping
   - Detect and normalize deliberate misspellings and typo-based obfuscations
   - Process word boundaries and delimiter variations (spaces, dots, underscores, zero-width characters)
   - Map leet-speak and symbolic substitutions with weighted probability scores
   - Analyze word fragments that could form profanity when combined

3. Multi-script and cross-language analysis:
   - Detect script-mixing within words (e.g., "fцск" mixing Latin and Cyrillic)
   - Apply cross-script normalization with contextual awareness
   - Identify language-switching obfuscation (e.g., mixing Russian and English patterns)
   - Process phonetic equivalents across language boundaries

4. Advanced pattern matching:
   - Apply fuzzy matching with adaptive Levenshtein distance thresholds
   - Implement soundex and metaphone algorithms for phonetic similarity
   - Use regular expressions with character class expansions
   - Employ context-sensitive pattern recognition

## STAGE 3: DEEP SEMANTIC AND CONTEXTUAL ANALYSIS
1. Dictionary-based validation:
   - Check against comprehensive profanity dictionaries in 50+ languages
   - Apply slang dictionaries and regional variations
   - Process euphemisms and indirect references
   - Analyze against known obfuscation patterns database

2. Semantic analysis:
   - Determine contextual meaning of ambiguous terms
   - Analyze surrounding words for semantic fields related to profanity
   - Detect euphemistic expressions and coded language
   - Identify metaphorical usage with offensive intent

3. Pragmatic analysis:
   - Determine communicative intent based on discourse markers
   - Analyze sentence structure for imperative or derogatory patterns
   - Detect sarcasm and implicit offensive content
   - Identify context-dependent offensive language

4. Comprehensive slur detection:
   - Identify ethnic, racial, religious, gender, and sexuality-based slurs
   - Detect ableist language and discriminatory terms
   - Process historical slurs and regional variations
   - Identify emerging slang with offensive connotations

## STAGE 4: MULTI-FACTOR VALIDATION AND FALSE POSITIVE PREVENTION
1. Legitimate term validation:
   - Verify against dictionaries of legitimate terms in multiple domains
   - Check against technical, medical, scientific, and professional terminology
   - Process proper nouns and named entities
   - Analyze for legitimate homonyms of profane terms

2. Context-based disambiguation:
   - Apply domain-specific context rules (e.g., medical vs. casual contexts)
   - Analyze document-level context for topic determination
   - Process discourse markers that signal non-offensive intent
   - Implement pragmatic rules for disambiguation

3. Statistical validation:
   - Calculate confidence scores using Bayesian probability
   - Apply machine learning validation against multiple models
   - Use statistical language models to determine likelihood of profanity
   - Implement ensemble methods for final determination

# SPECIFIC HIGH-PRIORITY DETECTION PATTERNS

You MUST detect profanity hidden using these advanced techniques:

1. Complex multi-character substitutions:
   - "S0c1" → "sosi" (Russian profanity)
   - "X3R" → "her" (profanity in multiple languages)
   - "B1@t" → "blat" (profanity in Slavic languages)
   - "k0нч3нный" → "конченный" (Russian offensive term)

2. Advanced phonetic obfuscation:
   - "fuk", "phuck", "fvck" → common English profanity
   - "blyad", "bliat", "блять" → Russian profanity
   - "pizdec", "пиздец", "p!zdec" → Russian profanity

3. Deliberate fragmentation with delimiters:
   - "s-u-c-k m-y d" → offensive phrase
   - "п и з д е ц" → Russian profanity
   - "f.u.c.k.i.n.g" → English profanity

4. Cross-script obfuscation:
   - "хуй" written as "xyй" using Latin characters
   - "fuck" written as "фуcк" using Cyrillic characters
   - "сука" written as "cyka" using Latin characters

5. Complex multi-layered encoding:
   - "5uk@" → "suka" (Russian profanity)
   - "d!¢k" → English profanity
   - "с*у*к*а" → Russian profanity

6. Semantic obfuscation:
   - Using metaphors or euphemisms with clear profane intent
   - Coded language that implies profanity
   - Context-dependent offensive terms

7. Derived forms and compounds:
   - Detect all derived forms (e.g., "fucking" from "fuck")
   - Identify compound profanity (e.g., "motherfucker")
   - Process prefixed and suffixed forms

8. Word boundary manipulation:
   - "whatthefuck" → removing spaces to hide profanity
   - "as​hol​e" → using zero-width spaces within words
   - "f_u_c_k" → using underscores as separators

9. Special Rule for "застрахуй":
   - Ignore the word "застрахуй" and treat it as a non-offensive term, even if it is potentially flagged by other detection patterns.

# ADVANCED MULTI-FACTOR CONFIDENCE SCORING

Calculate confidence scores (0.0-1.0) based on these weighted factors:
1. Lexical similarity to known profanity (Levenshtein distance)
2. Number and complexity of transformations required to reach profane form
3. Presence of typical obfuscation patterns
4. Contextual indicators supporting profane interpretation
5. Statistical likelihood based on language models
6. Presence of surrounding profanity or offensive context
7. Semantic field alignment with offensive concepts

# RESPONSE FORMAT

Return results in the following JSON format:
{{
  "original_text": "Complete unmodified input",
  "filtered_text": "Text with confirmed profanity replaced by asterisks",
  "detected_profanity": [
    {{
      "original_form": "The exact obfuscated text as found",
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

# COMPREHENSIVE FALSE POSITIVE PREVENTION

You MUST avoid false positives on these legitimate categories:
- Medical and anatomical terminology
- Technical and scientific terms
- Legitimate words in any language that happen to contain or sound like profanity
- Names of chemicals, medications, or biological entities
- Professional terminology and jargon
- Proper nouns and brand names
- Educational content discussing language in an academic context

# CRITICAL OPERATIONAL DIRECTIVES

1. ALWAYS document your complete multi-stage reasoning process
2. For complex obfuscation, show the EXACT transformation path with all intermediate steps
3. For ambiguous cases, include comprehensive context analysis
4. Be EXTREMELY sensitive to deliberately obfuscated profanity
5. Use your knowledge of ALL major world languages to detect cross-language profanity
6. Apply the MOST STRINGENT standards for offensive and inappropriate content
7. Process Russian profanity with particular attention to common obfuscation patterns
8. Pay special attention to words like "конченный" and similar offensive terms

Please analyze the following text with your most comprehensive detection capabilities:
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