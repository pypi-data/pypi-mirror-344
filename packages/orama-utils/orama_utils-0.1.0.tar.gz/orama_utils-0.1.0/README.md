# Orama Utils

A collection of utility functions for data processing and feature engineering.

## Features

- Date feature generation
- Holiday feature generation (supporting ES and IT countries)

## Installation

You can install the package using pip:

```bash
pip install orama-utils
```

For development installation:

```bash
git clone https://github.com/Orama-Solutions/utils.git
cd utils
pip install -e .[dev]
```

## Usage

### Holiday Features

Add holiday-related features to your DataFrame:

```python
import pandas as pd
from orama_utils import add_holiday_features

# Create your DataFrame
df = pd.DataFrame({
    'date': ['2023-01-01', '2023-12-25'],
    'country': ['ES', 'ES'],
    'county': ['ES-MD', 'ES-CT']
})

# Add holiday features
result = add_holiday_features(df)
```

The function adds three columns:
- `is_public_holiday`: True for national holidays
- `is_local_holiday`: True for county-specific holidays
- `many_counties_holiday`: True when multiple counties celebrate the holiday

You can customize the threshold for many counties:
```python
result = add_holiday_features(df, county_threshold=5)
```

### Date Features

Add date-related features to your DataFrame:

```python
from orama_utils import add_date_features

result = add_date_features(df, date_column='date')
```

## Development

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.