"""
Token weighting functionality for the ACACE pipeline.
"""

import re
import math
import importlib.util
from typing import List, Dict, Union, Optional, Any, Tuple, Set
from collections import Counter


class TokenWeightor:
    """
    Assigns semantic weights to tokens based on various criteria.
    
    This class analyzes tokens and assigns them weight values that represent their
    semantic importance in the text. Weights are used to prioritize tokens during
    compression and filtering.
    """
    
    def __init__(self, 
                 strategy: str = "tfidf",
                 pos_weights: Optional[Dict[str, float]] = None,
                 custom_weights: Optional[Dict[str, float]] = None,
                 min_weight: float = 0.0,
                 max_weight: float = 1.0,
                 use_spacy: bool = False,
                 language: str = "en",
                 **kwargs: Any):
        """
        Initialize the TokenWeightor with configuration options.
        
        Args:
            strategy (str): Weighting strategy to use ('tfidf', 'pos', 'custom', or 'hybrid')
            pos_weights (Dict[str, float], optional): Weights for different parts of speech
            custom_weights (Dict[str, float], optional): Custom weights for specific tokens
            min_weight (float): Minimum weight value (for normalization)
            max_weight (float): Maximum weight value (for normalization)
            use_spacy (bool): Whether to use spaCy for enhanced linguistic analysis
            language (str): Language code for language-specific processing (ISO 639-1)
            **kwargs: Additional options for specific weighting strategies
        """
        self.strategy = strategy.lower()
        self.pos_weights = pos_weights or {
            'NOUN': 1.0,
            'PROPN': 1.0,
            'VERB': 0.8,
            'ADJ': 0.6,
            'ADV': 0.4,
            'NUM': 0.4,
            'PRON': 0.3,
            'DET': 0.1,
            'ADP': 0.1,
            'CONJ': 0.1,
            'CCONJ': 0.1,
            'SCONJ': 0.1,
            'PUNCT': 0.0,
            'SYM': 0.2,
            'X': 0.0,
        }
        self.custom_weights = custom_weights or {}
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.use_spacy = use_spacy
        self.language = language
        self.options = kwargs
        
        # Initialize spaCy if requested
        if self.use_spacy:
            self._initialize_spacy()
        
        # Validate strategy
        self._validate_strategy()
    
    def _validate_strategy(self) -> None:
        """Validate the selected weighting strategy."""
        valid_strategies = ["tfidf", "pos", "custom", "hybrid"]
        if self.strategy not in valid_strategies:
            raise ValueError(f"Invalid weighting strategy: {self.strategy}. "
                           f"Must be one of {valid_strategies}")
    
    def _initialize_spacy(self) -> None:
        """Initialize spaCy for enhanced linguistic analysis."""
        if not self._check_module_installed("spacy"):
            raise ImportError("spaCy is not installed. Please install it using: pip install spacy")
        
        import spacy
        try:
            # Load the appropriate language model
            language_code = self.language
            if language_code == "en":
                model = "en_core_web_sm"
            else:
                model = f"{language_code}_core_news_sm"
            
            # Check if the model is installed
            if not spacy.util.is_package(model):
                raise ImportError(f"spaCy model '{model}' is not installed. "
                                f"Please install it using: python -m spacy download {model}")
            
            self.nlp = spacy.load(model)
        except Exception as e:
            raise ImportError(f"Failed to load spaCy model: {str(e)}")
    
    @staticmethod
    def _check_module_installed(module_name: str) -> bool:
        """Check if a Python module is installed."""
        return importlib.util.find_spec(module_name) is not None
    
    def assign_weights(self, tokens: List[str], context: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Assign weights to the input tokens based on the configured strategy.
        
        Args:
            tokens (List[str]): List of tokens to assign weights to
            context (str, optional): Original text for context-based weighting
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries with tokens and their weights
                Each dictionary contains:
                - token (str): The token text
                - weight (float): The assigned weight
                - metadata (Dict): Additional metadata about the token
        """
        if not tokens:
            return []
        
        # Choose weighting method based on strategy
        if self.strategy == "tfidf":
            weighted_tokens = self._tfidf_weighting(tokens, context)
        elif self.strategy == "pos":
            weighted_tokens = self._pos_weighting(tokens, context)
        elif self.strategy == "custom":
            weighted_tokens = self._custom_weighting(tokens)
        elif self.strategy == "hybrid":
            weighted_tokens = self._hybrid_weighting(tokens, context)
        else:
            weighted_tokens = self._tfidf_weighting(tokens, context)  # Default to TF-IDF
        
        # Apply any custom overrides
        if self.custom_weights:
            for i, item in enumerate(weighted_tokens):
                token = item["token"]
                if token in self.custom_weights:
                    weighted_tokens[i]["weight"] = self.custom_weights[token]
        
        # Normalize weights to the specified range
        self._normalize_weights(weighted_tokens)
        
        return weighted_tokens
    
    def _tfidf_weighting(self, tokens: List[str], context: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Assign weights using TF-IDF (Term Frequency-Inverse Document Frequency).
        
        Args:
            tokens (List[str]): List of tokens to assign weights to
            context (str, optional): Original text for context-based weighting
            
        Returns:
            List[Dict[str, Any]]: Tokens with TF-IDF weights
        """
        # Convert to lowercase for case-insensitive frequency calculation
        lowercase_tokens = [token.lower() for token in tokens]
        
        # Count token frequencies (Term Frequency)
        token_counter = Counter(lowercase_tokens)
        total_tokens = len(lowercase_tokens)
        
        # Calculate TF (Term Frequency) for each token
        tf_values = {token: count / total_tokens for token, count in token_counter.items()}
        
        # We can't calculate true IDF without a corpus, but we can approximate
        # by treating common tokens (stopwords) as having lower weight
        stopwords = self._get_stopwords()
        
        weighted_tokens = []
        for i, token in enumerate(tokens):
            lowercase = token.lower()
            
            # Base TF value
            tf = tf_values[lowercase]
            
            # Approximate IDF by reducing weight of stopwords
            idf_factor = 0.1 if lowercase in stopwords else 1.0
            
            # Calculate TF-IDF-like weight
            weight = tf * idf_factor
            
            # Create metadata
            metadata = {
                "tf": tf,
                "idf_factor": idf_factor,
                "is_stopword": lowercase in stopwords
            }
            
            weighted_tokens.append({
                "token": token,
                "weight": weight,
                "metadata": metadata
            })
        
        return weighted_tokens
    
    def _pos_weighting(self, tokens: List[str], context: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Assign weights based on part-of-speech tags.
        
        Args:
            tokens (List[str]): List of tokens to assign weights to
            context (str, optional): Original text for context analysis
            
        Returns:
            List[Dict[str, Any]]: Tokens with POS-based weights
        """
        # Construct full text for spaCy if context isn't provided
        if context is None:
            context = " ".join(tokens)
        
        # Process with spaCy if available
        if self.use_spacy:
            doc = self.nlp(context)
            
            # Extract POS tags and create a mapping from token text to POS
            # This handles the case where the same token appears multiple times with different POS
            token_to_pos = {}
            for token in doc:
                if token.text in token_to_pos:
                    # If the token already exists, keep the highest-weighted POS
                    current_weight = self.pos_weights.get(token_to_pos[token.text], 0.0)
                    new_weight = self.pos_weights.get(token.pos_, 0.0)
                    if new_weight > current_weight:
                        token_to_pos[token.text] = token.pos_
                else:
                    token_to_pos[token.text] = token.pos_
            
            # Assign weights based on POS
            weighted_tokens = []
            for token in tokens:
                pos = token_to_pos.get(token, "X")  # Default to "X" (unknown) if not found
                weight = self.pos_weights.get(pos, 0.0)
                
                weighted_tokens.append({
                    "token": token,
                    "weight": weight,
                    "metadata": {"pos": pos}
                })
            
            return weighted_tokens
        
        # Fallback to basic weighting if spaCy is not available
        return self._fallback_pos_weighting(tokens)
    
    def _fallback_pos_weighting(self, tokens: List[str]) -> List[Dict[str, Any]]:
        """
        Fallback POS weighting when spaCy is not available.
        Uses basic heuristics to approximate POS values.
        """
        weighted_tokens = []
        for token in tokens:
            # Estimate POS based on simple patterns
            if token.isalpha():
                if token[0].isupper() and tokens.index(token) > 0:
                    # Likely a proper noun
                    pos = "PROPN"
                elif token.lower() in self._get_stopwords():
                    # Likely a function word (determiner, preposition, etc.)
                    pos = "DET"  # Simplified approximation
                else:
                    # Default to noun for unknown words
                    pos = "NOUN"
            elif token.isdigit():
                pos = "NUM"
            elif not token.isalnum():
                pos = "PUNCT"
            else:
                pos = "X"  # Unknown
            
            weight = self.pos_weights.get(pos, 0.0)
            
            weighted_tokens.append({
                "token": token,
                "weight": weight,
                "metadata": {"pos": pos, "estimated": True}
            })
        
        return weighted_tokens
    
    def _custom_weighting(self, tokens: List[str]) -> List[Dict[str, Any]]:
        """
        Assign weights based on custom weight dictionary.
        
        Args:
            tokens (List[str]): List of tokens to assign weights to
            
        Returns:
            List[Dict[str, Any]]: Tokens with custom weights
        """
        weighted_tokens = []
        for token in tokens:
            # Check if the token has a custom weight
            token_lower = token.lower()
            weight = self.custom_weights.get(token, self.custom_weights.get(token_lower, 0.5))
            
            weighted_tokens.append({
                "token": token,
                "weight": weight,
                "metadata": {"custom_weight": True if token in self.custom_weights else False}
            })
        
        return weighted_tokens
    
    def _hybrid_weighting(self, tokens: List[str], context: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Combine multiple weighting strategies for better results.
        
        Args:
            tokens (List[str]): List of tokens to assign weights to
            context (str, optional): Original text for context analysis
            
        Returns:
            List[Dict[str, Any]]: Tokens with hybrid weights
        """
        # Get weights from different strategies
        tfidf_weights = self._tfidf_weighting(tokens, context)
        pos_weights = self._pos_weighting(tokens, context)
        
        # Combine weights (default: 0.6 * TF-IDF + 0.4 * POS)
        tfidf_factor = self.options.get("tfidf_factor", 0.6)
        pos_factor = self.options.get("pos_factor", 0.4)
        
        weighted_tokens = []
        for i, token in enumerate(tokens):
            tfidf_weight = tfidf_weights[i]["weight"]
            pos_weight = pos_weights[i]["weight"]
            
            # Combine weights
            combined_weight = (tfidf_weight * tfidf_factor) + (pos_weight * pos_factor)
            
            # Combine metadata
            combined_metadata = {
                **tfidf_weights[i]["metadata"],
                **pos_weights[i]["metadata"],
                "tfidf_weight": tfidf_weight,
                "pos_weight": pos_weight,
                "tfidf_factor": tfidf_factor,
                "pos_factor": pos_factor
            }
            
            weighted_tokens.append({
                "token": token,
                "weight": combined_weight,
                "metadata": combined_metadata
            })
        
        return weighted_tokens
    
    def _normalize_weights(self, weighted_tokens: List[Dict[str, Any]]) -> None:
        """
        Normalize weights to the specified range.
        
        Args:
            weighted_tokens (List[Dict[str, Any]]): Tokens with weights to normalize
        """
        if not weighted_tokens:
            return
        
        # Find min and max weights
        weights = [item["weight"] for item in weighted_tokens]
        min_val = min(weights)
        max_val = max(weights)
        
        # Skip normalization if all weights are the same
        if max_val == min_val:
            norm_weight = (self.min_weight + self.max_weight) / 2
            for item in weighted_tokens:
                item["weight"] = norm_weight
            return
        
        # Normalize to [min_weight, max_weight]
        range_old = max_val - min_val
        range_new = self.max_weight - self.min_weight
        
        for item in weighted_tokens:
            normalized = ((item["weight"] - min_val) / range_old) * range_new + self.min_weight
            item["weight"] = normalized
    
    def _get_stopwords(self) -> Set[str]:
        """Get a set of stopwords for the current language."""
        # English stopwords as a fallback
        english_stopwords = {
            "a", "an", "the", "and", "or", "but", "if", "then", "else", "when",
            "at", "by", "for", "with", "about", "against", "between", "into",
            "through", "during", "before", "after", "above", "below", "to",
            "from", "up", "down", "in", "out", "on", "off", "over", "under",
            "again", "further", "then", "once", "here", "there", "when",
            "where", "why", "how", "all", "any", "both", "each", "few", "more",
            "most", "other", "some", "such", "no", "nor", "not", "only", "own",
            "same", "so", "than", "too", "very", "s", "t", "can", "will",
            "just", "don", "should", "now", "d", "ll", "m", "o", "re", "ve",
            "y", "ain", "aren", "couldn", "didn", "doesn", "hadn", "hasn",
            "haven", "isn", "ma", "mightn", "mustn", "needn", "shan", "shouldn",
            "wasn", "weren", "won", "wouldn", "am", "is", "are", "was", "were",
            "be", "been", "being", "have", "has", "had", "having", "do", "does",
            "did", "doing", "would", "should", "could", "ought", "i'm", "you're",
            "he's", "she's", "it's", "we're", "they're", "i've", "you've",
            "we've", "they've", "i'd", "you'd", "he'd", "she'd", "we'd",
            "they'd", "i'll", "you'll", "he'll", "she'll", "we'll", "they'll",
            "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't", "hadn't",
            "doesn't", "don't", "didn't", "won't", "wouldn't", "shan't", "shouldn't",
            "can't", "cannot", "couldn't", "mustn't", "let's", "that's", "who's",
            "what's", "here's", "there's", "when's", "where's", "why's", "how's",
            "of", "that", "who", "this", "these", "those", "which", "whose",
            "whom", "mine", "ours", "yours", "his", "hers", "its", "theirs",
            "myself", "yourself", "himself", "herself", "itself", "ourselves",
            "yourselves", "themselves"
        }
        
        # Try to get language-specific stopwords if spaCy is available
        if self.use_spacy:
            try:
                spacy_stopwords = self.nlp.Defaults.stop_words
                return spacy_stopwords
            except:
                pass
        
        # Try to get stopwords from NLTK if available
        if self._check_module_installed("nltk"):
            try:
                import nltk
                from nltk.corpus import stopwords
                try:
                    nltk.data.find(f'corpora/stopwords')
                except LookupError:
                    nltk.download('stopwords')
                
                try:
                    lang = self.language if self.language in stopwords.fileids() else 'english'
                    return set(stopwords.words(lang))
                except:
                    pass
            except:
                pass
        
        # Return the fallback stopwords
        return english_stopwords


def assign_weights(tokens: List[str], **kwargs: Any) -> List[Dict[str, Any]]:
    """
    Utility function to assign weights to tokens without explicitly creating a TokenWeightor instance.
    
    Args:
        tokens (List[str]): List of tokens to assign weights to
        **kwargs: Configuration options for TokenWeightor
        
    Returns:
        List[Dict[str, Any]]: A list of dictionaries with tokens and their weights
    """
    weightor = TokenWeightor(**kwargs)
    return weightor.assign_weights(tokens)
