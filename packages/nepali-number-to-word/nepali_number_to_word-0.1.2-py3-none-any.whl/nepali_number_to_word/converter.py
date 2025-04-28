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
    def convert_to_nepali_words(cls, number: int | float) -> str:
        """
        Convert a number to Nepali words (class method)
        Args:
            number: The number to convert (int or float)
        Returns:
            Nepali words representation of the number
        Raises:
            ValueError: If number exceeds maximum supported value
        """
        if isinstance(number, float):
            rounded_number = round(number, 2)
            whole_part = int(rounded_number)
            paisa_part = int(round((rounded_number - whole_part) * 100))

            if paisa_part > 0:
                return f"{cls._convert_whole_number(whole_part)}, {cls._convert_paisa(paisa_part)}"
            return cls._convert_whole_number(whole_part)

        return cls._convert_whole_number(number)

    @classmethod
    def _convert_whole_number(cls, number: int) -> str:
        """Convert whole number part to Nepali words"""
        cls._validate_number_range(number)

        if number == 0:
            return "शून्य रुपैंया"
        if number < 0:
            return "ऋणात्मक " + cls._convert_whole_number(abs(number))

        words: list[str] = []
        remaining = abs(number)

        for unit_value, unit_name in cls.UNITS:
            if remaining >= unit_value:
                unit_count = remaining // unit_value
                words.append(cls._convert_number_part(unit_count) + " " + unit_name)
                remaining %= unit_value

        if remaining > 0:
            words.append(cls._convert_number_part(remaining))

        return " ".join(filter(None, words)) + " रुपैंया"

    @classmethod
    def _convert_paisa(cls, paisa: int) -> str:
        """Convert paisa part to Nepali words"""
        if paisa == 0:
            return ""
        return cls._convert_number_part(paisa) + " पैसा"

    @staticmethod
    def convert_to_nepali_numerals(number: int | float) -> str:
        """
        Convert a number to Nepali numerals with formatting (static method)
        Args:
            number: The number to convert (int or float)
        Returns:
            Formatted Nepali numerals string
        Raises:
            ValueError: If number exceeds maximum supported value
        """
        if isinstance(number, float):
            rounded_number = round(number, 2)
            whole_part = int(rounded_number)
            paisa_part = int(round((rounded_number - whole_part) * 100))

            whole_numerals = NepaliNumberConverter._convert_whole_to_numerals(
                whole_part
            )
            if paisa_part > 0:
                paisa_numerals = NepaliNumberConverter._convert_whole_to_numerals(
                    paisa_part
                )
                return f"{whole_numerals}.{paisa_numerals} /-"
            return f"{whole_numerals} /-"

        return f"{NepaliNumberConverter._convert_whole_to_numerals(number)} /-"

    @staticmethod
    def _convert_whole_to_numerals(number: int) -> str:
        """Convert whole number part to Nepali numerals"""
        NepaliNumberConverter._validate_number_range(number)

        if number < 0:
            return "-" + NepaliNumberConverter._convert_whole_to_numerals(abs(number))

        nepali_digits = "".join(NEPALI_NUMERALS[d] for d in str(abs(number)))
        return NepaliNumberConverter._format_with_commas(nepali_digits)

    @classmethod
    def _validate_number_range(cls, number: int | float) -> None:
        """Validate that number is within supported range"""
        if abs(int(number)) > cls.MAX_SUPPORTED_VALUE:
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
