"""
Module for styling pandas DataFrames and markdown headers with improved formatting.
"""

from IPython.core.display import display, HTML

def style_dataframe():
    """
    Apply a custom style to pandas DataFrames with alternating gold and light blue colors.
    
    This function applies the following styling:
    - Alternating gold and light blue row colors
    - Black text in table cells
    - Red text in table headers
    - Black borders around cells
    - 18px font size
    - Full-width container
    - Scrollable output up to 1000px height
    
    Returns:
        None
    """
    display(HTML("<style>.container { width:100% !important; }</style>"))
    display(HTML("<style>div.output_scroll { height: 1000px; }</style>"))
    display(HTML("<style>.output {color: #7df9ff;}</style>"))
    display(HTML("<style>table.dataframe, .dataframe td {border: 1px solid black; color:black;font-size:18px;}</style>"))
    display(HTML("<style>table.dataframe tr:nth-child(even) {background-color: rgb(253,253,201);}</style>"))
    display(HTML("<style>table.dataframe tr:nth-child(odd) {background-color: rgb(162,255,255);}</style>"))
    display(HTML("<style>.dataframe th {background-color: rgb(253,253,201); border: 1px solid black;color:red;}</style>"))

def style_headers():
    """
    Apply custom styling to markdown headers (h1, h2, h3) in Jupyter notebooks.
    
    This function applies the following styling to markdown headers:
    - Red border (thickness varies by level)
    - Gold background (#ffcc00)
    - Dark blue text (#000080)
    - Rounded corners
    - Appropriate padding and margins
    
    Returns:
        None
    """
    # CSS for styling markdown headers
    header_css = """
    <style>
    /* Level 1 Header Styling */
    .rendered_html h1 {
        background-color: #ffcc00;
        color: #000080;
        border: 3px solid #ff0000;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0px;
        font-size: 24px;
    }
    
    /* Level 2 Header Styling */
    .rendered_html h2 {
        background-color: #ffcc00;
        color: #000080;
        border: 2px solid #ff0000;
        border-radius: 5px;
        padding: 12px;
        margin: 10px 0px;
        font-size: 20px;
    }
    
    /* Level 3 Header Styling */
    .rendered_html h3 {
        background-color: #ffcc00;
        color: #000080;
        border: 1px solid #ff0000;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0px;
        font-size: 18px;
    }
    </style>
    """
    display(HTML(header_css))

def style_notebook():
    """
    Apply all custom styling to the notebook.
    
    This function applies both DataFrame styling and header styling to the notebook.
    After running this function, all markdown headers (h1, h2, h3) will be styled with
    red borders, gold backgrounds, and dark blue text, and DataFrames will have the
    pretty display styling.
    
    Returns:
        None
    """
    # Apply DataFrame styling
    style_dataframe()
    
    # Apply header styling
    style_headers()
    
    # Display usage information
    display(HTML("""
    <div style="margin: 10px; padding: 10px; border-radius: 5px; border: 1px solid #cccccc; background-color: #f9f9f9;">
    <p><strong>Notebook styling applied!</strong></p>
    <p>All markdown headers and pandas DataFrames will now be styled automatically.</p>
    <p>Examples of markdown headers:</p>
    <pre>
    # Level 1 Header
    ## Level 2 Header
    ### Level 3 Header
    </pre>
    </div>
    """))

def header1(text):
    """
    Display a level 1 header with red border, gold background, and dark blue text.
    
    Args:
        text (str): The header text to display
        
    Returns:
        None
    """
    html = f"""
    <div style="margin: 10px; padding: 15px; border-radius: 5px; border: 3px solid #ff0000; 
    background-color: #ffcc00; color: #000080; font-size: 24px; font-weight: bold;">
    {text}
    </div>
    """
    display(HTML(html))

def header2(text):
    """
    Display a level 2 header with red border, gold background, and dark blue text.
    
    Args:
        text (str): The header text to display
        
    Returns:
        None
    """
    html = f"""
    <div style="margin: 10px; padding: 12px; border-radius: 5px; border: 2px solid #ff0000; 
    background-color: #ffcc00; color: #000080; font-size: 20px; font-weight: bold;">
    {text}
    </div>
    """
    display(HTML(html))

def header3(text):
    """
    Display a level 3 header with red border, gold background, and dark blue text.
    
    Args:
        text (str): The header text to display
        
    Returns:
        None
    """
    html = f"""
    <div style="margin: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ff0000; 
    background-color: #ffcc00; color: #000080; font-size: 18px; font-weight: bold;">
    {text}
    </div>
    """
    display(HTML(html))
