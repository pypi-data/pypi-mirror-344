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
pip install cn-phone-parser
```

## Quick Start

```python
from cn_phone_parser import PhoneParser

# Parse a single phone number
parser = PhoneParser()
result = parser.parse("+86-010-12345678")
print(result)
# Output: {'normalized': '01012345678', 'type': 'landline', 'area_code': '010', 'city': 'Beijing'}

# Clean and analyze a dataset
import pandas as pd
from cn_phone_parser import analyze_phone_dataset

df = pd.read_csv('your_data.csv')
result_df = analyze_phone_dataset(df, phone_column='phone_number')
```

## Common Phone Number Formats Handled

- **Mobile Numbers**: `13812345678`, `+86 138 1234 5678`
- **Landline Numbers**: `010-12345678`, `0755-87654321`
- **International Format**: `+86 10 1234 5678`, `0086-755-12345678`
- **Numbers with Extensions**: `010-12345678-123`, `0755-87654321 转 456`
- **Multiple Numbers**: `010-12345678 / 13812345678`
- **Toll-Free Numbers**: `400-123-4567`, `800-123-4567`

## Documentation

For detailed usage and API documentation, please refer to the [documentation](docs/usage.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.