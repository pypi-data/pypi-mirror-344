"""
ACACE Compression Engine Module

This module handles semantic compression of text while preserving key information.
"""

from typing import List, Dict, Union
import re

def compress_text(text: Union[str, List[str]]) -> str:
    """
    Compress text while preserving key semantic elements.
    
    Args:
        text: Input text to compress (string or list of tokens)
        
    Returns:
        Compressed text with preserved key concepts
    """
    # Convert list of tokens to string if needed
    if isinstance(text, list):
        text = ' '.join(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove common filler words and phrases
    filler_words = [
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'as', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'shall', 'should', 'may', 'might', 'must', 'can', 'could', 'that',
        'which', 'who', 'whom', 'whose', 'when', 'where', 'why', 'how',
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'just', 'it', 'its', 'this', 'these',
        'that', 'those', 'i', 'you', 'he', 'she', 'we', 'they', 'across',
        'along', 'around', 'before', 'behind', 'below', 'beneath', 'beside',
        'between', 'beyond', 'during', 'except', 'inside', 'into', 'through',
        'under', 'within', 'without', 'about', 'above', 'after', 'among',
        'from', 'like', 'near', 'off', 'out', 'over', 'since', 'till',
        'until', 'upon', 'while', 'yet'
    ]
    
    # Common phrases to remove
    phrases_to_remove = [
        'in order to',
        'due to the fact that',
        'for the purpose of',
        'in spite of the fact that',
        'with regard to',
        'in terms of',
        'in the event that',
        'in the case of',
        'it is important to note that',
        'it should be noted that',
        'it is worth noting that',
        'in addition to',
        'in light of',
        'in the process of',
        'in view of',
        'with respect to',
        'on the basis of',
        'in relation to',
        'in connection with',
        'in accordance with',
        'with reference to',
        'for the reason that',
        'on account of',
        'in spite of',
        'regardless of',
        'notwithstanding',
        'nevertheless',
        'consequently',
        'therefore',
        'furthermore',
        'moreover',
        'however',
        'although',
        'whereas'
    ]
    
    # Remove phrases
    for phrase in phrases_to_remove:
        text = text.replace(phrase, '')
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Process each sentence
    compressed_sentences = []
    for sentence in sentences:
        # Remove filler words
        words = sentence.split()
        filtered_words = [word for word in words if word.lower() not in filler_words]
        
        # Remove redundant information in parentheses if main concept is mentioned
        filtered_words = [w for w in filtered_words if not (
            w.startswith('(') and w.endswith(')') and
            any(w[1:-1] in other_w for other_w in filtered_words if w != other_w)
        )]
        
        # Remove redundant words (case-insensitive)
        seen_words = set()
        unique_words = []
        for word in filtered_words:
            lower_word = word.lower()
            if lower_word not in seen_words:
                seen_words.add(lower_word)
                unique_words.append(word)
        
        # Join words back into a sentence
        if unique_words:
            compressed_sentences.append(' '.join(unique_words))
    
    # Join sentences back into text
    compressed_text = ' '.join(compressed_sentences)
    
    # Remove any remaining multiple spaces
    compressed_text = re.sub(r'\s+', ' ', compressed_text).strip()
    
    return compressed_text

def get_compression_ratio(original_text: str, compressed_text: str) -> float:
    """
    Calculate the compression ratio between original and compressed text.
    
    Args:
        original_text: Original text
        compressed_text: Compressed text
        
    Returns:
        Compression ratio (0.0 to 1.0)
    """
    if not original_text:
        return 0.0
    
    original_length = len(original_text)
    compressed_length = len(compressed_text)
    
    return 1.0 - (compressed_length / original_length) 