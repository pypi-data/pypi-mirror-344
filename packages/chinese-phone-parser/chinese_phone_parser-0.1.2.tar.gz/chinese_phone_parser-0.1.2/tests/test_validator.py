"""
Tests for the validator module.
"""

import unittest
from chinese_phone_parser.validator import is_valid_phone_number, is_mobile_number, is_landline_number


class TestValidator(unittest.TestCase):
    """Test cases for the validator module."""
    
    def test_is_valid_phone_number(self):
        """Test the is_valid_phone_number function."""
        test_cases = [
            # Input, Expected Output
            ("+8601012345678", True),  # Valid landline with country code
            ("13812345678", True),     # Valid mobile number
            ("4001234567", True),      # Valid toll-free number
            ("8001234567", True),      # Valid toll-free number
            ("010-12345678", True),    # Valid landline with area code
            ("123456", False),         # Too short
            ("abcdefghijk", False),    # Non-numeric
            (None, False),             # None input
            ("", False),               # Empty string
            ("9999999999999", False),  # Too long
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = is_valid_phone_number(input_val)
                self.assertEqual(result, expected)
    
    def test_is_mobile_number(self):
        """Test the is_mobile_number function."""
        test_cases = [
            # Input, Expected Output
            ("13812345678", True),     # Valid mobile number
            ("15912345678", True),     # Valid mobile number
            ("18612345678", True),     # Valid mobile number
            ("01012345678", False),    # Landline number
            ("4001234567", False),     # Toll-free number
            ("123456", False),         # Too short
            ("abcdefghijk", False),    # Non-numeric
            (None, False),             # None input
            ("", False),               # Empty string
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = is_mobile_number(input_val)
                self.assertEqual(result, expected)
    
    def test_is_landline_number(self):
        """Test the is_landline_number function."""
        test_cases = [
            # Input, Expected Output
            ("+8601012345678", True),  # Valid landline with country code
            ("010-12345678", True),    # Valid landline with area code
            ("13812345678", False),    # Mobile number
            ("4001234567", False),     # Toll-free number
            ("123456", False),         # Too short
            ("abcdefghijk", False),    # Non-numeric
            (None, False),             # None input
            ("", False),               # Empty string
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = is_landline_number(input_val)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()