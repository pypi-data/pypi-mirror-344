# Pandas Pretty Display

A simple Python package to make your pandas DataFrames look beautiful in Jupyter notebooks with alternating colors and improved formatting. Now with support for styled markdown headers!

## Installation

You can install the package via pip:

```bash
pip install pandas-pretty-display
```

## Usage

### DataFrame Styling

```python
from pandas_pretty_display import style_dataframe
import pandas as pd

# Create or load your DataFrame
df = pd.DataFrame(...)

# Apply the styling
style_dataframe()

# Display your DataFrame - it will now have the pretty styling
display(df)
```

### Markdown Header Styling

```python
from pandas_pretty_display import header1, header2, header3, style_notebook

# Apply all styling at once (DataFrame + usage info)
style_notebook()

# Or use individual header functions
header1("This is a Level 1 Header")
header2("This is a Level 2 Header")
header3("This is a Level 3 Header")
```

## Features

### DataFrame Styling
- Alternating gold and light blue row colors
- Black text in table cells
- Red text in table headers
- Black borders around cells
- 18px font size
- Full-width container
- Scrollable output up to 1000px height

### Header Styling
- Level 1, 2, and 3 headers with consistent styling
- Red border (thickness varies by level)
- Gold background (#ffcc00)
- Dark blue text (#000080)
- Responsive sizing based on header level
- Rounded corners for modern appearance

## Requirements

- Python >= 3.6
- pandas >= 1.0.0
- IPython >= 7.0.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.
