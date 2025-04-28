# Nepali Number to Word Converter

A Python package that converts numbers to Nepali words and numerals following proper OOP principles.

## Features

- Convert numbers to Nepali words (up to 99 खर्ब)
- Convert numbers to Nepali numerals with proper formatting (१,२३,४५६ /-)
- Support for positive and negative numbers
- No instance required - all methods are class/static methods
- No external dependencies
- Proper error handling for unsupported numbers

## Installation

1. Clone the repository:
```bash
git clone git@github.com:manisha841/nepali_number_to_word.git
cd nepali-number-to-word
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package:
```bash
pip install nepali_number_to_word.
```

## Usage

```python
from nepali_number_to_word import NepaliNumberConverter

# Convert numbers to Nepali words (class method)
result = NepaliNumberConverter.convert_to_nepali_words(1000)
print(result)  # Output: एक हजार रूपैयाँ मात्र

# Convert numbers to Nepali numerals (static method)
result = NepaliNumberConverter.convert_to_nepali_numerals(1000)
print(result)  # Output: १,००० /-

# Examples
print(NepaliNumberConverter.convert_to_nepali_words(123))      # एक सय तेइस रूपैयाँ मात्र
print(NepaliNumberConverter.convert_to_nepali_numerals(123))   # १,२३ /-

# Error handling
try:
    NepaliNumberConverter.convert_to_nepali_words(1000000000000000)  # Raises ValueError
except ValueError as e:
    print(e)  # Numbers beyond 999,999,999,999,999 (99 खर्ब) are not supported
```

## Number Units

The converter supports the following Nepali number units:
- खर्ब (Kharab) = 100,000,000,000
- अरब (Arab) = 1,000,000,000
- करोड (Crore) = 10,000,000
- लाख (Lakh) = 100,000
- हजार (Thousand) = 1,000

## Testing

Run the tests using pytest:
```bash
pytest
```

## License

MIT License
