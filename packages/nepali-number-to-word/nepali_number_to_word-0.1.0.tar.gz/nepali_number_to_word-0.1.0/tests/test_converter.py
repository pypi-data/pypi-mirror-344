"""
Test cases for Nepali number converter
"""

from nepali_number_to_word.converter import NepaliNumberConverter


def test_convert_to_nepali_words():
    converter = NepaliNumberConverter()

    # Test cases
    test_cases = [
        (0, "शून्य रूपैयाँ मात्र"),
        (1, "एक रूपैयाँ मात्र"),
        (10, "दस रूपैयाँ मात्र"),
        (100, "एक सय रूपैयाँ मात्र"),
        (1000, "एक हजार रूपैयाँ मात्र"),
        (10000, "दस हजार रूपैयाँ मात्र"),
        (100000, "एक लाख रूपैयाँ मात्र"),
        (1000000, "दस लाख रूपैयाँ मात्र"),
        (10000000, "एक करोड रूपैयाँ मात्र"),
        (123, "एक सय बीस तीन रूपैयाँ मात्र"),
        (1234, "एक हजार दुई सय तीस चार रूपैयाँ मात्र"),
        (-1000, "ऋणात्मक एक हजार रूपैयाँ मात्र"),
    ]

    for number, expected in test_cases:
        assert converter.convert_to_nepali_words(number) == expected


def test_convert_to_nepali_numerals():
    converter = NepaliNumberConverter()

    # Test cases
    test_cases = [
        (0, "० /-"),
        (1, "१ /-"),
        (10, "१० /-"),
        (100, "१०० /-"),
        (1000, "१००० /-"),
        (10000, "१०००० /-"),
        (100000, "१००००० /-"),
        (1000000, "१०००००० /-"),
        (10000000, "१००००००० /-"),
        (123, "१२३ /-"),
        (1234, "१२३४ /-"),
        (-1000, "-१००० /-"),
    ]

    for number, expected in test_cases:
        assert converter.convert_to_nepali_numerals(number) == expected
