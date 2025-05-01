 """
Functions for extracting phone numbers and their components from strings.
"""

import re
from typing import Optional, List, Dict, Any, Union


def extract_area_code(phone: Optional[str]) -> Optional[str]:
    """
    Extract the area code from a phone number.
    
    Parameters
    ----------
    phone : str or None
        The phone number to extract from
        
    Returns
    -------
    str or None
        The extracted area code or None if not found
    """
    if not phone:
        return None
    
    # Handle international format with +86
    if phone.startswith('+86'):
        phone = phone[3:]  # Remove +86
        
    # Handle international format with 0086
    if phone.startswith('0086'):
        phone = phone[4:]  # Remove 0086
        
    # Handle 86 prefix without + sign
    if phone.startswith('86'):
        phone = phone[2:]  # Remove 86
    
    # Check if it's a mobile number
    if phone.startswith('1') and len(phone) == 11:
        return None  # Mobile numbers don't have area codes
    
    # Check if it's a toll-free number
    if phone.startswith('400') or phone.startswith('800'):
        return phone[:3]  # Return 400 or 800 as the "area code"
    
    # Standard Chinese landline format: 0XXX-XXXXXXX or 0XX-XXXXXXXX
    if phone.startswith('0'):
        # Special cases for major cities with 2-digit area codes
        if phone.startswith('010') or phone.startswith('020'):
            return phone[:3]
            
        # For other cities, area codes are usually 3-4 digits
        match = re.search(r'^0(\d{2,4})', phone)
        if match:
            # Check for common patterns
            if phone[:3] in ['010', '020', '021', '022', '023', '024', '025', '027', '028', '029']:
                return phone[:3]  # Major cities with 3-digit codes
            elif phone.startswith('0'):
                # Other cities with 4-digit area codes
                return phone[:4] if len(phone) >= 4 else None
    
    return None


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract all phone numbers from a text string.
    
    Parameters
    ----------
    text : str
        The text containing phone numbers
        
    Returns
    -------
    list of str
        List of extracted phone numbers
    """
    if not text:
        return []
    
    # Define patterns for different types of phone numbers
    patterns = [
        # International format with +86
        r'\+86[-\s]?(\d{2,4})[-\s]?(\d{7,8})',
        # International format with 0086
        r'0086[-\s]?(\d{2,4})[-\s]?(\d{7,8})',
        # Mobile numbers (11 digits starting with 1)
        r'1\d{10}',
        # Landline with area code
        r'0\d{2,4}[-\s]?\d{7,8}',
        # Toll-free numbers
        r'[48]00[-\s]?\d{3}[-\s]?\d{4}',
        # Fallback for digits-only strings of right length
        r'\b\d{7,12}\b'
    ]
    
    # Extract all matches
    all_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            if isinstance(matches[0], tuple):
                # If the pattern has capturing groups, join them
                for match in matches:
                    joined = ''.join(match)
                    if joined not in all_matches:
                        all_matches.append(joined)
            else:
                # Otherwise add them directly
                for match in matches:
                    if match not in all_matches:
                        all_matches.append(match)
    
    return all_matches


def extract_extension(phone: str) -> Dict[str, Any]:
    """
    Extract the extension from a phone number.
    
    Parameters
    ----------
    phone : str
        The phone number to extract from
        
    Returns
    -------
    dict
        A dictionary with 'main' and 'extension' keys
    """
    extension = None
    main_number = phone
    
    # Check for common extension separators
    ext_patterns = [
        r'(.+)[\s-]转[\s-](\d+)',  # Chinese
        r'(.+)[\s-]ext[\s-.](\d+)',  # English
        r'(.+)[\s-]分机[\s-](\d+)',  # Chinese
        r'(.+)[-](\d{1,5})$'  # Simple dash
    ]
    
    for pattern in ext_patterns:
        match = re.match(pattern, phone, re.IGNORECASE)
        if match:
            main_number = match.group(1)
            extension = match.group(2)
            break
    
    return {
        'main': main_number,
        'extension': extension
    }