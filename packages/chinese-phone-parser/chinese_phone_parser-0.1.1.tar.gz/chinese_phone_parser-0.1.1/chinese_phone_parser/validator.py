 """
Functions for validating and categorizing Chinese phone numbers.
"""

import re
from typing import Optional, Tuple, Union


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate if a string is a valid Chinese phone number.
    
    Parameters
    ----------
    phone : str
        The phone number to validate
        
    Returns
    -------
    tuple
        (is_valid, error_message)
    """
    if not phone:
        return False, "Phone number is empty"
        
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's a mobile number
    if re.match(r'^1\d{10}$', digits_only):
        return True, ""
        
    # Check if it's a landline with area code
    if re.match(r'^0\d{2,3}\d{7,8}$', digits_only):
        return True, ""
        
    # Check if it's a toll-free number
    if re.match(r'^[48]00\d{7}$', digits_only):
        return True, ""
        
    # Check international format with +86
    if re.match(r'^\+?86\d{10,12}$', digits_only) or re.match(r'^0086\d{10,12}$', digits_only):
        return True, ""
        
    # If it doesn't match any known format
    return False, "Invalid phone number format"


def categorize_phone_format(phone: Optional[str]) -> str:
    """
    Categorize a phone number into different format types.
    
    Parameters
    ----------
    phone : str or None
        The phone number to categorize
        
    Returns
    -------
    str
        The category of the phone number
    """
    if not phone:
        return 'Missing'
    
    digits_only = re.sub(r'\D', '', phone)
    
    # Check for international formats
    if phone.startswith('+86'):
        return 'International (+86)'
    elif phone.startswith('0086'):
        return 'International (0086)'
    elif phone.startswith('86') and not phone.startswith('86-'):
        return 'International (86)'
        
    # Check for mobile numbers
    if phone.startswith('1') and len(digits_only) == 11:
        return 'Mobile'
        
    # Check for toll-free numbers
    if phone.startswith('400') or re.match(r'^400-', phone):
        return 'Toll-Free (400)'
    elif phone.startswith('800') or re.match(r'^800-', phone):
        return 'Toll-Free (800)'
        
    # Check for landline with area code
    if phone.startswith('0'):
        if re.search(r'0\d{2,3}[-/]?1\d{10}', phone):
            return 'Area Code + Mobile'
        return 'Domestic (0XX)'
        
    # Check for missing area code
    if phone.startswith('-'):
        return 'Missing Area Code'
        
    # Check for no area code
    if re.match(r'^\d{7,8}$', phone):
        return 'No Area Code'
        
    # Check for concatenated numbers
    if len(digits_only) > 15:
        return 'Concatenated'
        
    # If multiple numbers are separated by slash
    if '/' in phone and any(c.isdigit() and len(c) == 11 and c.startswith('1') for c in phone.split('/')):
        return 'Landline/Mobile Mix'
        
    # Default case
    return 'Other'


def is_mobile_number(phone: str) -> bool:
    """
    Check if a phone number is a Chinese mobile number.
    
    Parameters
    ----------
    phone : str
        The phone number to check
        
    Returns
    -------
    bool
        True if it's a mobile number, False otherwise
    """
    if not phone:
        return False
        
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check international prefix
    if digits_only.startswith('86'):
        digits_only = digits_only[2:]
        
    # Check if it starts with 1 and has 11 digits
    return bool(re.match(r'^1\d{10}$', digits_only))


def is_landline_number(phone: str) -> bool:
    """
    Check if a phone number is a Chinese landline number.
    
    Parameters
    ----------
    phone : str
        The phone number to check
        
    Returns
    -------
    bool
        True if it's a landline number, False otherwise
    """
    if not phone:
        return False
        
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Remove international prefix if present
    if digits_only.startswith('86'):
        digits_only = digits_only[2:]
        
    # Check for landline pattern (area code + 7-8 digits)
    return bool(re.match(r'^0\d{2,3}\d{7,8}$', digits_only))