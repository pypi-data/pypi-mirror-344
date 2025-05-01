# Chinese Phone Number Parser

A Python package for cleaning, parsing, and analyzing Chinese phone numbers in various formats.

## Features

- Clean and normalize phone numbers from various formats
- Extract area codes and map them to corresponding cities
- Detect different phone number formats (mobile, landline, international, etc.)
- Handle multiple phone numbers in a single string
- Support for extensions and special number formats
- Comprehensive analysis of phone number patterns

## Installation

```bash
pip install chinese-phone-parser
```

## Quick Start

```python
from chinese_phone_parser import PhoneParser

# Parse a single phone number
parser = PhoneParser()
result = parser.parse("+86-010-12345678")
print(result)
# Output: {
#     'original': '+86-010-12345678',
#     'normalized': '+8601012345678',
#     'type': 'landline',
#     'area_code': '010',
#     'city': 'Beijing'
# }

# Analyze a dataset with phone numbers
import pandas as pd
from chinese_phone_parser.utils.helpers import analyze_phone_dataset, get_phone_stats, plot_phone_formats

# Load your data
df = pd.read_csv('your_data.csv')

# Analyze the dataset
analyzed_df = analyze_phone_dataset(df, phone_column='phone')

# Get comprehensive statistics
stats = get_phone_stats(df, phone_column='phone')

# Create visualizations
fig = plot_phone_formats(df, phone_column='phone')
fig.show()
```

## Supported Phone Number Formats

### 1. Mobile Numbers (11 digits)
- Standard: `13812345678`
- International: `+86 138 1234 5678`
- With prefix: `0086-13812345678`

### 2. Landline Numbers
- Local: `010-12345678`
- With area code: `0755-87654321`
- International: `+86 10 1234 5678`

### 3. Toll-Free Numbers (10 digits)
- 400 numbers: `400-123-4567`
- 800 numbers: `800-123-4567`

### 4. Special Formats
- With extensions: 
  - `010-12345678-123`
  - `0755-87654321 转 456`
  - `010-12345678 ext 789`
  - `010-12345678 分机 321`
- Multiple numbers:
  - `010-12345678 / 13812345678`
  - `0755-87654321, 400-123-4567`
- Concatenated numbers:
  - `0101234567813812345678`
- Missing area codes:
  - `12345678`
  - `-12345678`
- Service numbers:
  - `110` (Police)
  - `12345` (Government hotline)

## Advanced Features

### Pattern Analysis
```python
from chinese_phone_parser.utils.helpers import analyze_phone_patterns

patterns = analyze_phone_patterns(phone_numbers)
print(patterns)
# Output includes:
# - Digit count distribution
# - Extension presence
# - Multiple number detection
# - International format detection
# - Area code analysis
# - Mobile/landline classification
```

### Visualization
```python
from chinese_phone_parser.utils.helpers import plot_area_code_map

# Create a visualization of area code distribution
fig = plot_area_code_map(df, phone_column='phone', top_n=10)
fig.show()
```

## Documentation

For detailed usage and API documentation, please refer to the [documentation](docs/usage.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.