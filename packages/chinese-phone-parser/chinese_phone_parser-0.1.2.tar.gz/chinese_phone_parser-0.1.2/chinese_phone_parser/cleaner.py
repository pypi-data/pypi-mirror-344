"""
Functions for cleaning and normalizing Chinese phone numbers.
"""

import re
import pandas as pd
from typing import Optional, Union


def clean_phone_number(phone: Union[str, int, float]) -> Optional[str]:
    """
    Clean a phone number string by handling non-string inputs and
    removing duplicate whitespace.
    
    Parameters
    ----------
    phone : str, int, float
        The phone number to clean
        
    Returns
    -------
    str or None
        The cleaned phone number string or None if input is invalid
    """
    # Handle NaN, None, etc.
    if pd.isna(phone):
        return None
        
    # Convert to string if not already
    phone_str = str(phone).strip()
    
    # Handle empty strings
    if not phone_str:
        return None
    
    # Remove any non-essential whitespace
    phone_str = re.sub(r'\s+', ' ', phone_str)
    
    # Handle multiple phone numbers - take the first one
    if ',' in phone_str:
        phone_str = phone_str.split(',')[0].strip()
    elif ';' in phone_str:
        phone_str = phone_str.split(';')[0].strip()
    elif '/' in phone_str:
        phone_str = phone_str.split('/')[0].strip()
    
    return phone_str if phone_str else None


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Normalize a phone number by removing all non-digit characters except
    for the '+' sign at the beginning.
    
    Parameters
    ----------
    phone : str or None
        The phone number to normalize
        
    Returns
    -------
    str or None
        The normalized phone number string or None if input is invalid
    """
    if not phone:
        return None
        
    # Keep the + sign if it exists
    if phone.startswith('+'):
        # Remove the + sign temporarily and then add it back
        plus_sign = True
        phone = phone[1:]
    else:
        plus_sign = False
    
    # Remove all non-digit characters
    normalized = re.sub(r'\D', '', phone)
    
    # Add back the + sign if needed
    if plus_sign and normalized:
        normalized = '+' + normalized
        
    return normalized if normalized else None


def convert_to_standard_format(phone: str) -> str:
    """Convert a phone number to a standardized format.
    
    Parameters
    ----------
    phone : str
        The phone number to format
        
    Returns
    -------
    str
        The formatted phone number
    """
    if not phone:
        return ""
    
    # Remove any non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Handle international format with +86
    if cleaned.startswith('+86'):
        base = cleaned[3:]  # Remove +86
        if base.startswith('1'):  # Mobile
            return f"+86 {base[:3]} {base[3:7]} {base[7:]}"
        else:  # Landline
            area_code = base[:3] if base[:3] in ['010', '020', '021', '022', '023', '024', '025', '027', '028', '029'] else base[:4]
            return f"+86 {area_code} {base[len(area_code):]}"
    
    # Handle mobile numbers
    if cleaned.startswith('1') and len(cleaned) == 11:
        return f"{cleaned[:3]} {cleaned[3:7]} {cleaned[7:]}"
    
    # Handle toll-free numbers
    if cleaned.startswith(('400', '800')):
        return f"{cleaned[:3]}-{cleaned[3:6]}-{cleaned[6:]}"
    
    # Handle landline numbers
    if cleaned.startswith('0'):
        area_code = cleaned[:3] if cleaned[:3] in ['010', '020', '021', '022', '023', '024', '025', '027', '028', '029'] else cleaned[:4]
        return f"{area_code}-{cleaned[len(area_code):]}"
    
    return cleaned