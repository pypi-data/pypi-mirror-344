"""
Chinese Phone Number Parser
==========================

A Python package for cleaning, normalizing, and analyzing Chinese phone numbers.
"""

from cn_phone_parser.cleaner import clean_phone_number, normalize_phone
from cn_phone_parser.extractor import extract_area_code, extract_phone_numbers
from cn_phone_parser.validator import validate_phone, categorize_phone_format
from cn_phone_parser.utils.helpers import analyze_phone_dataset

__version__ = '0.1.0'
__all__ = [
    'clean_phone_number',
    'normalize_phone',
    'extract_area_code',
    'extract_phone_numbers',
    'validate_phone',
    'categorize_phone_format',
    'analyze_phone_dataset',
]

class PhoneParser:
    """Main class for parsing Chinese phone numbers."""
    
    def __init__(self):
        """Initialize the parser with default settings."""
        pass
        
    def parse(self, phone_string):
        """
        Parse a phone string and return structured information.
        
        Parameters
        ----------
        phone_string : str
            The phone string to parse
            
        Returns
        -------
        dict
            A dictionary containing the parsed phone information
        """
        if not phone_string:
            return None
            
        # Clean the phone number
        cleaned = clean_phone_number(phone_string)
        
        # Normalize the phone number
        normalized = normalize_phone(cleaned)
        
        # Extract area code
        area_code = extract_area_code(normalized)
        
        # Get the city from area code
        from cn_phone_parser.data.area_codes import area_code_to_city
        city = area_code_to_city.get(area_code, 'Unknown')
        
        # Categorize the phone format
        phone_type = categorize_phone_format(normalized)
        
        return {
            'original': phone_string,
            'normalized': normalized,
            'type': phone_type,
            'area_code': area_code,
            'city': city
        }