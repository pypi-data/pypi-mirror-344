"""
Tests for the extractor module.
"""

import unittest
from chinese_phone_parser.extractor import extract_area_code, extract_phone_numbers, extract_extension


class TestExtractor(unittest.TestCase):
    """Test cases for the extractor module."""
    
    def test_extract_area_code(self):
        """Test the extract_area_code function."""
        test_cases = [
            # Input, Expected Output
            ("+8601012345678", "010"),
            ("+8602112345678", "021"),
            ("01012345678", "010"),
            ("075512345678", "0755"),
            ("13812345678", None),  # Mobile number, no area code
            ("4001234567", "400"),  # Toll-free
            ("8001234567", "800"),  # Toll-free
            ("86010-12345678", "010"),  # Without + sign
            ("0086-010-12345678", "010"),  # International format
            (None, None),  # None input
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = extract_area_code(input_val)
                self.assertEqual(result, expected)
    
    def test_extract_phone_numbers(self):
        """Test the extract_phone_numbers function."""
        test_cases = [
            # Input, Expected Result Length
            ("Contact us at +86-010-12345678 or 13812345678", 2),
            ("Our number is 010-12345678", 1),
            ("Call 400-123-4567 for service", 1),
            ("No phone numbers here", 0),
            ("Multiple formats: +86 138 1234 5678, 0755-87654321, 0086-010-12345678", 3),
            (None, 0),  # None input
        ]
        
        for input_val, expected_len in test_cases:
            with self.subTest(input_val=input_val):
                result = extract_phone_numbers(input_val)
                self.assertEqual(len(result), expected_len)
    
    def test_extract_extension(self):
        """Test the extract_extension function."""
        test_cases = [
            # Input, Expected Main, Expected Extension
            ("010-12345678-123", "010-12345678", "123"),
            ("010-12345678 转 456", "010-12345678", "456"),
            ("010-12345678 ext 789", "010-12345678", "789"),
            ("010-12345678 分机 321", "010-12345678", "321"),
            ("13812345678", "13812345678", None),  # No extension
            (None, None, None),  # None input
        ]
        
        for input_val, expected_main, expected_ext in test_cases:
            with self.subTest(input_val=input_val):
                if input_val is None:
                    continue
                result = extract_extension(input_val)
                self.assertEqual(result['main'], expected_main)
                self.assertEqual(result['extension'], expected_ext)


if __name__ == '__main__':
    unittest.main()