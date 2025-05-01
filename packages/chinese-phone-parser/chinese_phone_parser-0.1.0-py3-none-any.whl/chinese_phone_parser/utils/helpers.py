 """
Helper functions for working with Chinese phone numbers.
"""

import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from typing import Dict, List, Optional, Any, Union

from cn_phone_parser.cleaner import clean_phone_number, normalize_phone
from cn_phone_parser.extractor import extract_area_code
from cn_phone_parser.validator import categorize_phone_format
from cn_phone_parser.data.area_codes import area_code_to_city


def analyze_phone_patterns(phones: List[str]) -> Dict[str, Any]:
    """
    Analyze phone number patterns in a list of phone numbers.
    
    Parameters
    ----------
    phones : list of str
        The list of phone numbers to analyze
        
    Returns
    -------
    dict
        Dictionary containing pattern analysis results
    """
    phone_patterns = []
    
    for phone in phones:
        if pd.isna(phone):
            continue
            
        phone_str = str(phone)
        
        # Count the number of digits
        digit_count = sum(c.isdigit() for c in phone_str)
        
        # Check if it contains extensions
        has_extension = '转' in phone_str or 'ext' in phone_str.lower() or '-0' in phone_str
        
        # Check if it has multiple numbers
        has_multiple = ',' in phone_str or ';' in phone_str or '/' in phone_str
        
        # Check if it's international format
        is_international = '+86' in phone_str or '0086' in phone_str or phone_str.startswith('86')
        
        # Check if it has missing area code (starts with a dash)
        missing_area_code = phone_str.startswith('-')
        
        # Check if it's a concatenated number (unusually long)
        is_concatenated = digit_count > 15
        
        # Check if it's a mobile number (starts with 1 and has 11 digits)
        is_mobile = bool(re.match(r'^1\d{10}$', phone_str.replace('-', '').replace(' ', '')))
        
        # Check if it's a mixed format (area code + mobile)
        is_mixed_format = bool(re.search(r'0\d{2,3}[-/]?1\d{10}', phone_str))
        
        # Check if it's a toll-free number (starting with 400 or 800)
        is_tollfree = bool(re.match(r'^[48]00', phone_str.replace('-', '')))
        
        # Check if it has no area code (just 7-8 digits)
        has_no_area_code = bool(re.match(r'^\d{7,8}$', phone_str))
        
        pattern = {
            'digit_count': digit_count,
            'has_extension': has_extension,
            'has_multiple': has_multiple,
            'is_international': is_international,
            'missing_area_code': missing_area_code,
            'is_concatenated': is_concatenated,
            'is_mobile': is_mobile,
            'is_mixed_format': is_mixed_format,
            'is_tollfree': is_tollfree,
            'has_no_area_code': has_no_area_code
        }
        phone_patterns.append(pattern)
    
    # Convert to DataFrame for analysis
    phone_pattern_df = pd.DataFrame(phone_patterns)
    
    # Compile results
    results = {}
    
    # Count occurrences of different patterns
    if not phone_pattern_df.empty:
        results['digit_counts'] = phone_pattern_df['digit_count'].value_counts().to_dict()
        results['extension_count'] = phone_pattern_df['has_extension'].sum()
        results['multiple_count'] = phone_pattern_df['has_multiple'].sum()
        results['international_count'] = phone_pattern_df['is_international'].sum()
        results['missing_area_count'] = phone_pattern_df['missing_area_code'].sum()
        results['concatenated_count'] = phone_pattern_df['is_concatenated'].sum()
        results['mobile_count'] = phone_pattern_df['is_mobile'].sum()
        results['mixed_format_count'] = phone_pattern_df['is_mixed_format'].sum()
        results['tollfree_count'] = phone_pattern_df['is_tollfree'].sum()
        results['no_area_code_count'] = phone_pattern_df['has_no_area_code'].sum()
    
    return results


def analyze_phone_dataset(df: pd.DataFrame, phone_column: str) -> pd.DataFrame:
    """
    Analyze a dataset containing phone numbers.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing phone numbers
    phone_column : str
        The name of the column containing phone numbers
        
    Returns
    -------
    pandas.DataFrame
        The dataframe with additional phone analysis columns
    """
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    # Clean phone numbers
    result_df['clean_phone'] = result_df[phone_column].apply(clean_phone_number)
    
    # Normalize phone numbers
    result_df['normalized_phone'] = result_df['clean_phone'].apply(normalize_phone)
    
    # Extract area codes
    result_df['area_code'] = result_df['normalized_phone'].apply(extract_area_code)
    
    # Map area codes to cities
    result_df['city'] = result_df['area_code'].map(lambda x: area_code_to_city.get(x, 'Unknown') if pd.notna(x) else 'Unknown')
    
    # Categorize phone formats
    result_df['phone_format'] = result_df['normalized_phone'].apply(categorize_phone_format)
    
    return result_df


def get_phone_stats(df: pd.DataFrame, phone_column: str) -> Dict[str, Any]:
    """
    Get statistics about phone numbers in a dataset.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing phone numbers
    phone_column : str
        The name of the column containing phone numbers
        
    Returns
    -------
    dict
        Dictionary containing phone number statistics
    """
    # Count total and unique phone numbers
    total_phones = df[phone_column].count()
    unique_phones = df[phone_column].nunique()
    
    # Analyze phone formats
    analyzed_df = analyze_phone_dataset(df, phone_column)
    format_counts = analyzed_df['phone_format'].value_counts().to_dict()
    
    # Get area code distribution
    area_code_counts = analyzed_df['area_code'].dropna().value_counts().to_dict()
    
    # Get city distribution
    city_counts = analyzed_df['city'].value_counts().to_dict()
    
    # Get pattern analysis
    patterns = analyze_phone_patterns(df[phone_column].dropna().tolist())
    
    # Compile results
    results = {
        'total_count': total_phones,
        'unique_count': unique_phones,
        'unique_percentage': (unique_phones / total_phones * 100) if total_phones > 0 else 0,
        'format_counts': format_counts,
        'area_code_counts': area_code_counts,
        'city_counts': city_counts,
        'patterns': patterns
    }
    
    return results


def plot_phone_formats(df: pd.DataFrame, phone_column: str, color_scheme: Dict[str, str] = None) -> go.Figure:
    """
    Create a bar chart of phone number formats.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing phone numbers
    phone_column : str
        The name of the column containing phone numbers
    color_scheme : dict, optional
        Color scheme to use for the plot
        
    Returns
    -------
    plotly.graph_objects.Figure
        The plotly figure object
    """
    # Default color scheme
    if color_scheme is None:
        color_scheme = {
            'primary': '#1E3765',
            'secondary': '#4F6898',
            'tertiary': '#8F9FBF'
        }
    
    # Analyze phone formats
    analyzed_df = analyze_phone_dataset(df, phone_column)
    format_counts = analyzed_df['phone_format'].value_counts().reset_index()
    format_counts.columns = ['format', 'count']
    
    # Sort by count
    format_counts = format_counts.sort_values(by='count', ascending=False)
    
    # Create bar chart
    fig = px.bar(
        format_counts, 
        x='format', 
        y='count',
        title='Phone Number Format Distribution',
        color_discrete_sequence=[color_scheme['primary']]
    )
    
    fig.update_layout(
        xaxis_title='Format',
        yaxis_title='Count',
        template='plotly_white'
    )
    
    return fig


def plot_area_code_map(df: pd.DataFrame, phone_column: str, top_n: int = 10, color_scheme: Dict[str, str] = None) -> go.Figure:
    """
    Create a bar chart of the top area codes.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing phone numbers
    phone_column : str
        The name of the column containing phone numbers
    top_n : int, optional
        Number of top area codes to display
    color_scheme : dict, optional
        Color scheme to use for the plot
        
    Returns
    -------
    plotly.graph_objects.Figure
        The plotly figure object
    """
    # Default color scheme
    if color_scheme is None:
        color_scheme = {
            'primary': '#1E3765',
            'secondary': '#4F6898',
            'tertiary': '#8F9FBF'
        }
    
    # Analyze area codes
    analyzed_df = analyze_phone_dataset(df, phone_column)
    
    # Get top area codes with their cities
    area_codes = analyzed_df.dropna(subset=['area_code'])
    area_code_counts = area_codes.groupby(['area_code', 'city']).size().reset_index(name='count')
    area_code_counts = area_code_counts.sort_values(by='count', ascending=False).head(top_n)
    
    # Create bar chart
    fig = px.bar(
        area_code_counts, 
        x='area_code', 
        y='count',
        title=f'Top {top_n} Area Codes',
        hover_data=['city'],
        color_discrete_sequence=[color_scheme['primary']]
    )
    
    fig.update_layout(
        xaxis_title='Area Code',
        yaxis_title='Count',
        template='plotly_white'
    )
    
    return fig