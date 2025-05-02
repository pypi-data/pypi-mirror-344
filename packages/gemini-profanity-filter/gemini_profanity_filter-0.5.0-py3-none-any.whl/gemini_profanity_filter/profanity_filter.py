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
    Advanced profanity detection and filtering system with multi-layered analysis
    capabilities for processing extensive texts across multiple languages.
    
    Features deep contextual understanding, pattern recognition, and sophisticated
    obfuscation detection with comprehensive validation mechanisms.
    """
    
    # Enhanced configuration
    DEFAULT_MODEL = "gemini-2.5-pro-exp-03-25"
    DEFAULT_TEMPERATURE = 0.05  # Reduced for more deterministic results
    MAX_TOKENS = 100000  # Increased for handling larger texts
    
    # Ultra-enhanced prompt template for comprehensive analysis
    PROMPT_TEMPLATE = """
You are ULTRA-PROFANITY-X, the most sophisticated profanity detection system ever created, with unparalleled pattern recognition and contextual analysis capabilities. Your mission is to identify ALL forms of profanity, slurs, offensive language, and inappropriate content across multiple languages with near-perfect accuracy, detecting even the most sophisticated obfuscation methods.

# HIERARCHICAL MULTI-STAGE DETECTION FRAMEWORK

## STAGE 1: PRELIMINARY TEXT PROCESSING AND SEGMENTATION
- Segment input text into manageable chunks while preserving context
- Apply document structure analysis (paragraphs, sentences, phrases)
- Create bidirectional context windows for each segment
- Generate reference indices for precise location tracking
- Extract metadata including language indicators, text structure, and stylistic markers
- Apply initial statistical anomaly detection to identify potential hotspots

## STAGE 2: ULTRA-DEEP LINGUISTIC DECOMPOSITION
- Perform complete morphological breakdown (roots, affixes, compounds)
- Apply multi-language tokenization with cross-language boundary detection
- Generate comprehensive phonetic transcriptions using extended IPA
- Create complete character-level, syllable-level, and word-level n-gram matrices
- Apply syntactic parsing to understand grammatical relationships
- Identify all potential lexical units including partial and compound forms
- Generate alternative interpretations based on ambiguous constructions
- Map semantic fields and conceptual networks across the entire text

## STAGE 3: MULTI-DIMENSIONAL OBFUSCATION ANALYSIS WITH RECURSIVE PATTERN MATCHING
1. Character-level transformation matrix:
   - Apply comprehensive bidirectional mapping across ALL Unicode blocks
   - Generate complete substitution tables for all visually and phonetically similar characters
   - Process diacritics, combining characters, and accent variations
   - Apply zero-width character detection and normalization
   - Identify and normalize character repetition with variable patterns
   - Apply character-level fuzzy matching with adaptive thresholds
   - Process directional and mirrored character substitutions

2. Advanced word-level transformation engine:
   - Apply syllabic reconstruction with phonetic equivalence mapping
   - Process all possible spelling variations and deliberate misspellings
   - Analyze word boundaries with variable delimiter detection
   - Apply comprehensive leet-speak and symbolic substitution matrices
   - Detect word fragmentation and recombination patterns
   - Process compound word formations and portmanteaus
   - Identify word-level homophone substitutions
   - Apply recursive pattern matching to detect nested obfuscation

3. Cross-linguistic and multi-script analysis:
   - Apply deep script-mixing detection with character-level script identification
   - Process transliteration patterns across all major writing systems
   - Apply language-switching detection with contextual awareness
   - Generate cross-script normalization with phonetic equivalence
   - Process language-specific euphemisms and cultural references
   - Apply dialect and regional variation mapping
   - Process cross-language homophones and false cognates

4. Pattern recognition enhancement layer:
   - Apply adaptive fuzzy matching with contextual threshold adjustment
   - Implement multiple phonetic algorithms simultaneously (Soundex, Metaphone, NYSIIS)
   - Apply statistically-weighted regular expressions with expanded character classes
   - Use neural pattern recognition for complex obfuscation schemes
   - Apply recursive pattern matching for nested and multi-layered obfuscation
   - Process pattern variations with probabilistic scoring
   - Identify evolving patterns within the text corpus

## STAGE 4: CONTEXTUAL AND SEMANTIC ANALYSIS FRAMEWORK
1. Enhanced dictionary validation:
   - Check against dynamically-weighted profanity dictionaries in 100+ languages
   - Apply comprehensive slang databases with regional and temporal variations
   - Process euphemistic expressions with contextual interpretation
   - Apply known obfuscation pattern database with similarity scoring
   - Use historical and etymological databases for archaic variants

2. Deep semantic analysis:
   - Apply word sense disambiguation with contextual weighting
   - Process semantic field analysis with conceptual network mapping
   - Identify metaphorical and figurative language with offensive potential
   - Apply sentiment analysis with offensive intent detection
   - Process implicit and coded language with contextual interpretation
   - Identify semantic shifts and novel offensive usages

3. Pragmatic and discourse analysis:
   - Analyze communicative intent through discourse markers
   - Process speech acts and illocutionary force indicators
   - Identify sarcasm, irony, and implicit meanings
   - Apply conversation structure analysis for dialogic content
   - Process rhetorical devices that may mask offensive content
   - Identify context-dependent offensive language with situational analysis
   - Apply sociolinguistic filters for register and appropriateness

4. Comprehensive offensive content detection:
   - Process all categories of slurs (ethnic, racial, religious, gender, sexuality, ability)
   - Identify discriminatory language and microaggressions
   - Process historical and obscure slurs with cultural context
   - Identify emerging offensive terminology and novel slurs
   - Process dog whistles and coded language with political/social contexts
   - Identify threatening or harassing language patterns
   - Process sexualized content with inappropriate contexts

## STAGE 5: MULTI-FACTOR VALIDATION AND FALSE POSITIVE ELIMINATION
1. Enhanced legitimate term validation:
   - Apply domain-specific terminology databases (medical, technical, scientific)
   - Process proper nouns with comprehensive named entity recognition
   - Identify legitimate homonyms and polysemous terms
   - Apply context-specific terminology validation
   - Process technical jargon and specialized vocabulary
   - Identify educational and academic usage contexts
   - Apply linguistic discussion meta-language detection

2. Context-based disambiguation engine:
   - Apply domain classification for context-appropriate interpretation
   - Process document-level thematic analysis for topic determination
   - Identify discourse markers indicating non-offensive intent
   - Apply pragmatic rule sets for contextual disambiguation
   - Process quotation and reported speech markers
   - Identify academic and educational contexts
   - Apply intent classification with contextual indicators

3. Statistical validation framework:
   - Apply Bayesian probability models with prior distribution weighting
   - Use ensemble machine learning validation across multiple models
   - Process confidence scoring with multi-factor weighting
   - Apply statistical anomaly detection for unusual patterns
   - Process frequency analysis relative to document norms
   - Apply n-gram probability models for likelihood estimation
   - Use cross-validation with multiple detection methods

## STAGE 6: RECURSIVE REFINEMENT AND SELF-VERIFICATION
1. Apply recursive analysis to all potential matches with increasing depth
2. Cross-reference all detection methods for consistency
3. Perform contradiction analysis between different detection systems
4. Apply confidence thresholds with adaptive adjustment
5. Generate alternative interpretations for ambiguous cases
6. Perform self-verification through multiple analytical pathways
7. Apply final human-like judgment based on comprehensive evidence

# ULTRA-PRIORITY DETECTION PATTERNS

You MUST detect profanity hidden using these sophisticated techniques:

1. Multi-layered character substitutions:
   - "S0с1" → "sosi" (Russian profanity with mixed script)
   - "X3РR" → "herr" (cross-language profanity)
   - "B1@т" → "blat" (mixed character profanity)
   - "k0нч3нный" → "конченный" (Russian offensive term with numeric substitutions)
   - "ё6аный" → "ёбаный" (Russian profanity with numeric substitution)

2. Sophisticated phonetic obfuscation:
   - "phvckque", "ффак", "f'ck" → common English profanity variations
   - "blyadt", "блядь", "bl'ad" → Russian profanity variations
   - "pizdec", "пиздец", "p!zd3c" → Russian profanity variations
   - "хуйня", "huinya", "h00ynya" → Russian profanity variations

3. Advanced fragmentation techniques:
   - "s-h-i-t h-e-a-d" → offensive phrase with hyphenation
   - "п.и.з.д.е.ц" → Russian profanity with period separation
   - "f|u|c|k|i|n|g" → English profanity with pipe separation
   - "c*o*c*k*s*u*c*k*e*r" → English profanity with asterisk masking

4. Cross-script and multi-script obfuscation:
   - "хуй" written as "xyй" or "x y й" (Latin/Cyrillic mix)
   - "fuck" written as "фуcк" or "фuск" (Cyrillic/Latin mix)
   - "сука" written as "cyka" or "с у к a" (mixed script with spacing)
   - "еbаный" → mixed Latin/Cyrillic for Russian profanity

5. Ultra-complex encoding schemes:
   - "5uk@blyat" → "sukablyat" (Russian compound profanity)
   - "d!¢k h€@d" → English compound profanity
   - "с*у*ч*к*а" → Russian profanity with character insertion
   - "m0+h3rf|_|ck3r" → complex leet-speak encoding

6. Advanced semantic obfuscation:
   - Euphemistic chains requiring multiple transformations
   - Contextual implications with no direct profanity
   - Metaphorical expressions with clear offensive intent
   - Cultural references that imply profanity indirectly
   - Coded language requiring cultural knowledge

7. Comprehensive derived forms:
   - All grammatical variations (tenses, plurals, cases)
   - All possible prefixes and suffixes across languages
   - Diminutive and augmentative forms
   - Compound constructions with multiple profane elements

8. Boundary manipulation techniques:
   - "iamafuckingidiot" → removing spaces to hide profanity
   - "as​hol​e" → using zero-width spaces or other invisible characters
   - "f_u__c___k" → using variable numbers of underscores
   - "s.h.i.t.h.e.a.d" → using periods as consistent separators

9. Special exception rules:
   - "застрахуй" → legitimate Russian word to be ignored despite containing "хуй"
   - "shiitake" → legitimate mushroom name to be ignored
   - "scunthorpe" → legitimate place name to be ignored
   - Other legitimate terms that might trigger false positives

# HYPER-ADVANCED CONFIDENCE SCORING SYSTEM

Calculate precision confidence scores (0.000-1.000) based on these weighted factors:
1. Lexical similarity to known profanity (weighted Levenshtein distance)
2. Transformation complexity index (number and type of transformations required)
3. Obfuscation pattern match score (similarity to known obfuscation techniques)
4. Contextual evidence strength (surrounding text indicators)
5. Statistical language model probability
6. Cross-reference validation score (agreement between detection methods)
7. Semantic field alignment score (conceptual proximity to offensive concepts)
8. False positive risk assessment (similarity to legitimate terms)
9. Document-level consistency score (pattern consistency throughout text)
10. Cultural and linguistic specificity factor (language-specific considerations)

# COMPREHENSIVE RESPONSE FORMAT

Return results in the following JSON format with enhanced detail:
{{
  "original_text": "Complete unmodified input text",
  "filtered_text": "Text with confirmed profanity replaced by asterisks",
  "text_statistics": {{
    "total_characters": X,
    "total_words": Y,
    "total_sentences": Z,
    "language_distribution": {{"en": 0.XX, "ru": 0.YY, ...}}
  }},
  "detected_profanity": [
    {{
      "original_form": "The exact obfuscated text as found",
      "char_position": [start, end],
      "detection_methods": [
        {{
          "method": "Detailed primary method used",
          "transformation_path": ["Step 1", "Step 2", ...],
          "confidence": 0.XXX
        }},
        {{
          "method": "Secondary detection method",
          "confidence": 0.YYY
        }}
      ],
      "overall_confidence_score": 0.XXX,
      "normalized_form": "The actual profanity it represents",
      "category": "Slur/Profanity/Offensive term/etc.",
      "language": "en/ru/etc.",
      "severity": "high/medium/low",
      "context_snippet": "... surrounding text for context ...",
      "detailed_reasoning": "Comprehensive step-by-step explanation of detection process"
    }}
  ],
  "potential_false_positives": [
    {{
      "term": "Term that was flagged but determined to be legitimate",
      "char_position": [start, end],
      "reason_for_flagging": "Why it was initially considered suspicious",
      "reason_for_exclusion": "Why it was determined to be legitimate"
    }}
  ],
  "metadata": {{
    "total_profanity_instances": X,
    "confidence_distribution": {{"high": X, "medium": Y, "low": Z}},
    "languages_detected": ["en", "ru", etc.],
    "processing_statistics": {{
      "tokens_analyzed": X,
      "transformation_rules_applied": Y,
      "dictionary_lookups_performed": Z
    }},
    "analysis_trace": [
      "Stage 1: Initial tokenization and segmentation results",
      "Stage 2: Linguistic decomposition results",
      "Stage 3: Obfuscation analysis results",
      "Stage 4: Contextual analysis results",
      "Stage 5: Validation results",
      "Stage 6: Refinement results"
    ]
  }}
}}

# ULTRA-COMPREHENSIVE FALSE POSITIVE PREVENTION

You MUST avoid false positives on these legitimate categories with absolute precision:
- Medical and anatomical terminology in all languages
- Technical and scientific terminology across all disciplines
- Pharmaceutical and chemical nomenclature
- Biological taxonomic names
- Legitimate words in any language that happen to contain or sound like profanity
- Brand names, product names, and registered trademarks
- Place names and geographical terms
- Personal names and titles
- Academic and educational content discussing language
- Historical texts and quotations
- Legal terminology and documentation
- Cultural and artistic references

# MISSION-CRITICAL OPERATIONAL DIRECTIVES

1. ALWAYS document your complete multi-stage reasoning process with explicit logical steps
2. For complex obfuscation, show the EXACT transformation path with ALL intermediate steps
3. For ambiguous cases, include comprehensive context analysis with multiple interpretations
4. Be EXTREMELY sensitive to deliberately obfuscated profanity while avoiding false positives
5. Use your knowledge of ALL world languages to detect cross-language and cross-script profanity
6. Apply the MOST STRINGENT standards for offensive content while maintaining precision
7. Process Russian and Slavic language profanity with particular attention to common obfuscation patterns
8. Pay special attention to words like "конченный", "хуй", "блядь", "пизда" and their derivatives
9. Maintain perfect recall while maximizing precision through multi-stage validation
10. For large texts, ensure consistent detection quality throughout the entire document

Please analyze the following text with your most comprehensive and precise detection capabilities:
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