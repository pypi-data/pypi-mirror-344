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

def style_notebook():
    """
    Apply custom styling to the notebook.
    
    This function sets up the styling for the notebook, including the DataFrame styling
    and makes the header functions available for use.
    
    Returns:
        None
    """
    # Apply DataFrame styling
    style_dataframe()
    
    # Display usage information
    display(HTML("""
    <div style="margin: 10px; padding: 10px; border-radius: 5px; border: 1px solid #cccccc; background-color: #f9f9f9;">
    <p><strong>Notebook styling applied!</strong></p>
    <p>You can now use the following functions to create styled headers:</p>
    <ul>
        <li><code>header1("Your Level 1 Header")</code></li>
        <li><code>header2("Your Level 2 Header")</code></li>
        <li><code>header3("Your Level 3 Header")</code></li>
    </ul>
    </div>
    """))
