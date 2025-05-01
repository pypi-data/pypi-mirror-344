"""
Data files for the Chinese phone number parser.
"""

from cn_phone_parser.data.area_codes import (
    area_code_to_city,
    short_area_codes,
    mobile_prefix_to_carrier,
    get_carrier
)

__all__ = [
    'area_code_to_city',
    'short_area_codes',
    'mobile_prefix_to_carrier',
    'get_carrier'
]