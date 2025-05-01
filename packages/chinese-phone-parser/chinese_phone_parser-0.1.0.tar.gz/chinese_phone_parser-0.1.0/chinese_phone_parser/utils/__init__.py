"""
Utility functions and constants for the Chinese phone number parser.
"""

from cn_phone_parser.utils.constants import PATTERNS, DEFAULT_CONFIG, PLOT_COLORS
from cn_phone_parser.utils.helpers import (
    analyze_phone_patterns,
    analyze_phone_dataset,
    get_phone_stats,
    plot_phone_formats,
    plot_area_code_map
)

__all__ = [
    'PATTERNS',
    'DEFAULT_CONFIG',
    'PLOT_COLORS',
    'analyze_phone_patterns',
    'analyze_phone_dataset',
    'get_phone_stats',
    'plot_phone_formats',
    'plot_area_code_map'
]