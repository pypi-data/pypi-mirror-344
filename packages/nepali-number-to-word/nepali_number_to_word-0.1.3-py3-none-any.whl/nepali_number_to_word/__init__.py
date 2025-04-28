"""
Nepali Number to Word Converter
A package to convert numbers to Nepali words
"""

from .converter import (
    convert_to_nepali_words,
    convert_to_nepali_numerals,
)

__version__ = "0.1.3"
__all__ = [
    "convert_to_nepali_words",
    "convert_to_nepali_numerals",
]
