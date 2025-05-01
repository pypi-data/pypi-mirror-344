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
    
    # Remove any non-essential whitespace
    phone_str = re.sub(r'\s+', ' ', phone_str)
    
    # Handle multiple phone numbers - take the first one
    if ',' in phone_str:
        phone_str = phone_str.split(',')[0].strip()
    elif ';' in phone_str:
        phone_str = phone_str.split(';')[0].strip()
    elif '/' in phone_str:
        phone_str = phone_str.split('/')[0].strip()
    
    return phone_str


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
    """
    Convert a normalized phone number to a standard display format.
    
    Parameters
    ----------
    phone : str
        The normalized phone number
        
    Returns
    -------
    str
        The phone number in standard display format
    """
    if not phone:
        return ''
        
    # Handle international format with +86
    if phone.startswith('+86'):
        # +86 + area code + number
        if len(phone) > 11 and not phone[3:].startswith('1'):
            # Try to determine area code length (2-4 digits)
            area_code_length = 2
            area_code_candidate = phone[3:3+area_code_length]
            
            if area_code_candidate.startswith('0'):
                if area_code_candidate == '01':
                    area_code_length = 3  # Beijing (010)
                elif area_code_candidate in ['02', '03', '04', '05', '07', '08', '09']:
                    area_code_length = 3  # Other major cities
                else:
                    area_code_length = 4  # Smaller cities
                    
            return f"+86 {phone[3:3+area_code_length]} {phone[3+area_code_length:]}"
        
        # Mobile number
        if len(phone) == 14 and phone[3:].startswith('1'):
            return f"+86 {phone[3:6]} {phone[6:10]} {phone[10:14]}"
            
        return phone
    
    # Handle domestic format
    if phone.startswith('0'):
        # Landline
        if not phone[1:].startswith('1'):
            # Determine area code length
            if phone.startswith('010') or phone.startswith('020'):
                return f"{phone[:3]}-{phone[3:]}"
            elif phone[:2] in ['01', '02', '03', '04', '05', '07', '08', '09']:
                return f"{phone[:4]}-{phone[4:]}"
            else:
                return f"{phone[:5]}-{phone[5:]}"
    
    # Mobile number
    if phone.startswith('1') and len(phone) == 11:
        return f"{phone[:3]} {phone[3:7]} {phone[7:11]}"
        
    # Toll-free number
    if phone.startswith('400') or phone.startswith('800'):
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        
    # Default: return as is
    return phone