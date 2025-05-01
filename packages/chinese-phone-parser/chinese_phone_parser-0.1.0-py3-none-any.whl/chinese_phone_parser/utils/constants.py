 """
Constants used in the Chinese phone number parser.
"""

# Regular expressions for pattern matching
PATTERNS = {
    # Mobile number patterns
    'MOBILE': r'^1\d{10}$',
    'MOBILE_FORMATTED': r'^1[3-9]\d{9}$',
    
    # Landline patterns
    'LANDLINE': r'^0\d{2,3}[\s-]?\d{7,8}$',
    'BEIJING_LANDLINE': r'^010[\s-]?\d{7,8}$',
    'SHANGHAI_LANDLINE': r'^021[\s-]?\d{7,8}$',
    
    # International format patterns
    'INTL_PLUS86': r'^\+86[\s-]?',
    'INTL_0086': r'^0086[\s-]?',
    'INTL_86': r'^86[\s-]?',
    
    # Extension patterns
    'EXT_CHINESE': r'转[\s-]?\d+$',
    'EXT_ENGLISH': r'ext[\s-.]?\d+$',
    'EXT_DASH': r'-\d{1,5}$',
    
    # Toll-free patterns
    'TOLLFREE_400': r'^400[\s-]?\d{3}[\s-]?\d{4}$',
    'TOLLFREE_800': r'^800[\s-]?\d{3}[\s-]?\d{4}$',
    
    # Multiple number patterns
    'MULTIPLE_SLASH': r'/',
    'MULTIPLE_COMMA': r',',
    'MULTIPLE_SEMICOLON': r';',
    
    # No area code pattern
    'NO_AREA_CODE': r'^\d{7,8}$',
    
    # Missing area code pattern
    'MISSING_AREA_CODE': r'^-\d+$',
    
    # Concatenated numbers
    'CONCATENATED': r'^\d{15,}$',
}

# Default configuration
DEFAULT_CONFIG = {
    'handle_extensions': True,
    'handle_multiple': True,
    'normalize_output': True,
    'take_first_number': True,
    'map_area_codes': True,
    'detect_format': True,
}

# Plot colors
PLOT_COLORS = {
    'uoft_blue': '#1E3765',
    'light_blue': '#4F6898',
    'lighter_blue': '#8F9FBF',
    'gray': '#CCCCCC',
    'dark_gray': '#666666',
}

# Format display names
FORMAT_DISPLAY_NAMES = {
    'Mobile': 'Mobile Number',
    'Domestic (0XX)': 'Landline with Area Code',
    'International (+86)': 'International Format (+86)',
    'International (0086)': 'International Format (0086)',
    'International (86)': 'International Format (86)',
    'Area Code + Mobile': 'Area Code + Mobile Mix',
    'Landline/Mobile Mix': 'Landline/Mobile Mix',
    'Missing Area Code': 'Missing Area Code',
    'No Area Code': 'No Area Code (7-8 digits)',
    'Concatenated': 'Concatenated Numbers',
    'Toll-Free (400)': 'Toll-Free (400)',
    'Toll-Free (800)': 'Toll-Free (800)',
    'Other': 'Other Format',
    'Missing': 'Missing Number',
}

# Mobile carrier prefixes
MOBILE_PREFIXES = {
    # China Mobile
    'CMCC': ['134', '135', '136', '137', '138', '139', '147', '150', 
             '151', '152', '157', '158', '159', '178', '182', '183', 
             '184', '187', '188', '198'],
    # China Unicom
    'CUCC': ['130', '131', '132', '145', '155', '156', '166', '175', 
             '176', '185', '186'],
    # China Telecom
    'CTCC': ['133', '153', '177', '180', '181', '189', '191', '199'],
    # Virtual Operators
    'VIRTUAL': ['170', '171', '172', '173'],
}