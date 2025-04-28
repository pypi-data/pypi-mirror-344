"""
Core number to Nepali word conversion logic
"""

from .constants import (
    UNITS,
    TENS,
    HUNDREDS,
    SPECIAL_NUMBERS,
    NEPALI_NUMERALS,
)


class NepaliNumberConverter:
    """Converter for numbers to Nepali words and numerals following proper OOP principles"""

    KHARAB = 100000000000
    ARAB = 1000000000
    CRORE = 10000000
    LAKH = 100000
    THOUSAND = 1000
    MAX_SUPPORTED_VALUE = 999999999999999

    UNITS = [
        (KHARAB, "खर्ब"),
        (ARAB, "अरब"),
        (CRORE, "करोड"),
        (LAKH, "लाख"),
        (THOUSAND, "हजार"),
    ]

    @classmethod
    def convert_to_nepali_words(cls, number: int) -> str:
        """
        Convert a number to Nepali words (class method)
        Args:
            number: The number to convert
        Returns:
            Nepali words representation of the number
        Raises:
            ValueError: If number exceeds maximum supported value
        """
        cls._validate_number_range(number)

        if number == 0:
            return "शून्य"
        if number < 0:
            return "ऋणात्मक " + cls.convert_to_nepali_words(abs(number))

        words: list[str] = []
        remaining = abs(number)

        for unit_value, unit_name in cls.UNITS:
            if remaining >= unit_value:
                unit_count = remaining // unit_value
                words.append(cls._convert_number_part(unit_count) + " " + unit_name)
                remaining %= unit_value

        if remaining > 0:
            words.append(cls._convert_number_part(remaining))

        return " ".join(filter(None, words)) + " रूपैयाँ मात्र"

    @staticmethod
    def convert_to_nepali_numerals(number: int) -> str:
        """
        Convert a number to Nepali numerals with formatting (static method)
        Args:
            number: The number to convert
        Returns:
            Formatted Nepali numerals string
        Raises:
            ValueError: If number exceeds maximum supported value
        """
        NepaliNumberConverter._validate_number_range(number)

        if number < 0:
            return "-" + NepaliNumberConverter.convert_to_nepali_numerals(abs(number))

        nepali_digits = "".join(NEPALI_NUMERALS[d] for d in str(abs(number)))
        formatted = NepaliNumberConverter._format_with_commas(nepali_digits)
        return f"{formatted} /-"

    @classmethod
    def _validate_number_range(cls, number: int) -> None:
        """Validate that number is within supported range"""
        if abs(number) > cls.MAX_SUPPORTED_VALUE:
            raise ValueError(
                f"Numbers beyond {cls.MAX_SUPPORTED_VALUE:,} (99 खर्ब) are not supported"
            )

    @staticmethod
    def _format_with_commas(number_str: str) -> str:
        """
        Format a number string with Nepali-style commas
        Args:
            number_str: The number string to format
        Returns:
            Formatted string with commas
        """
        if len(number_str) <= 3:
            return number_str

        parts: list[str] = [number_str[-3:]]
        remaining = number_str[:-3]

        while remaining:
            parts.append(remaining[-2:] if len(remaining) >= 2 else remaining)
            remaining = remaining[:-2]

        return ",".join(reversed(parts))

    @staticmethod
    def _convert_number_part(number: int) -> str:
        """
        Convert any number part to Nepali words
        Args:
            number: The number to convert (0-999)
        Returns:
            Nepali words representation
        """
        if number < 100:
            return NepaliNumberConverter._convert_two_digits(number)
        return NepaliNumberConverter._convert_three_digits(number)

    @staticmethod
    def _convert_two_digits(number: int) -> str:
        """
        Convert a two-digit number to Nepali words
        Args:
            number: The number to convert (0-99)
        Returns:
            Nepali words representation
        """
        if number < 10:
            return UNITS[number]

        if 10 <= number < len(SPECIAL_NUMBERS) + 10:
            return SPECIAL_NUMBERS[number - 10]

        ten, unit = divmod(number, 10)
        return TENS[ten] + (f" {UNITS[unit]}" if unit > 0 else "")

    @staticmethod
    def _convert_three_digits(number: int) -> str:
        """
        Convert a three-digit number to Nepali words
        Args:
            number: The number to convert (100-999)
        Returns:
            Nepali words representation
        """
        hundred, remaining = divmod(number, 100)
        parts = []
        if hundred > 0:
            parts.append(HUNDREDS[hundred])
        if remaining > 0:
            parts.append(NepaliNumberConverter._convert_two_digits(remaining))
        return " ".join(filter(None, parts))
