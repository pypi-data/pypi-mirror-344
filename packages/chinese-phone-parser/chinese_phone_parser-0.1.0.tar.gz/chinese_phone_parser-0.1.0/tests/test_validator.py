"""
Tests for the validator module.
"""

import unittest
from chinese_phone_parser.validator import (
    validate_phone, 
    categorize_phone_format, 
    is_mobile_number, 
    is_landline_number
)


class TestValidator(unittest.TestCase):
    """Test cases for the validator module."""
    
    def test_validate_phone(self):
        """Test the validate_phone function."""
        test_cases = [
            # Input, Expected Valid, Expected Error Message
            ("+86-010-12345678", True, ""),
            ("01012345678", True, ""),
            ("13812345678", True, ""),
            ("4001234567", True, ""),
            ("123", False, "Invalid phone number format"),
            ("", False, "Phone number is empty"),
            (None, False, "Phone number is empty"),
        ]
        
        for input_val, expected_valid, expected_msg in test_cases:
            with self.subTest(input_val=input_val):
                is_valid, error_msg = validate_phone(input_val)
                self.assertEqual(is_valid, expected_valid)
                self.assertEqual(error_msg, expected_msg)
    
    def test_categorize_phone_format(self):
        """Test the categorize_phone_format function."""
        test_cases = [
            # Input, Expected Category
            ("+86-010-12345678", "International (+86)"),
            ("0086-010-12345678", "International (0086)"),
            ("86-010-12345678", "International (86)"),
            ("010-12345678", "Domestic (0XX)"),
            ("13812345678", "Mobile"),
            ("400-123-4567", "Toll-Free (400)"),
            ("800-123-4567", "Toll-Free (800)"),
            ("12345678", "No Area Code"),
            ("-12345678", "Missing Area Code"),
            ("01012345678139********", "Concatenated"),
            ("010-12345678/13812345678", "Landline/Mobile Mix"),
            (None, "Missing"),
            ("", "Missing"),
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = categorize_phone_format(input_val)
                self.assertEqual(result, expected)
    
    def test_is_mobile_number(self):
        """Test the is_mobile_number function."""
        test_cases = [
            # Input, Expected Result
            ("13812345678", True),
            ("15912345678", True),
            ("18612345678", True),
            ("+8613812345678", True),
            ("8613812345678", True),
            ("010-12345678", False),
            ("400-123-4567", False),
            ("12345678", False),
            (None, False),
            ("", False),
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = is_mobile_number(input_val)
                self.assertEqual(result, expected)
    
    def test_is_landline_number(self):
        """Test the is_landline_number function."""
        test_cases = [
            # Input, Expected Result
            ("010-12345678", True),
            ("01012345678", True),
            ("0755-12345678", True),
            ("+86-010-12345678", True),
            ("13812345678", False),
            ("400-123-4567", False),
            ("12345678", False),
            (None, False),
            ("", False),
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = is_landline_number(input_val)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()