"""
Tests for the cleaner module.
"""

import unittest
import pandas as pd
import numpy as np
from chinese_phone_parser.cleaner import clean_phone_number, normalize_phone, convert_to_standard_format


class TestCleaner(unittest.TestCase):
    """Test cases for the cleaner module."""
    
    def test_clean_phone_number(self):
        """Test the clean_phone_number function."""
        # Test with various inputs
        test_cases = [
            # Input, Expected Output
            ("+86-010-12345678", "+86-010-12345678"),
            ("010-12345678", "010-12345678"),
            ("010 12345678", "010 12345678"),
            ("010-12345678, 13812345678", "010-12345678"),
            ("010-12345678; 13812345678", "010-12345678"),
            ("010-12345678 / 13812345678", "010-12345678"),
            (13812345678, "13812345678"),  # Integer input
            (np.nan, None),  # NaN input
            (None, None),  # None input
            ("", None),  # Empty string
            ("   ", None),  # Whitespace only
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = clean_phone_number(input_val)
                self.assertEqual(result, expected)
    
    def test_normalize_phone(self):
        """Test the normalize_phone function."""
        test_cases = [
            # Input, Expected Output
            ("+86-010-12345678", "+8601012345678"),
            ("010-12345678", "01012345678"),
            ("010 12345678", "01012345678"),
            ("13812345678", "13812345678"),
            ("400-123-4567", "4001234567"),
            (None, None),  # None input
            ("", None),  # Empty string
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = normalize_phone(input_val)
                self.assertEqual(result, expected)
    
    def test_convert_to_standard_format(self):
        """Test the convert_to_standard_format function."""
        test_cases = [
            # Input, Expected Output
            ("+8601012345678", "+86 010 12345678"),
            ("+8613812345678", "+86 138 1234 5678"),
            ("01012345678", "010-12345678"),
            ("075512345678", "0755-12345678"),
            ("13812345678", "138 1234 5678"),
            ("4001234567", "400-123-4567"),
            ("", ""),  # Empty string
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = convert_to_standard_format(input_val)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()