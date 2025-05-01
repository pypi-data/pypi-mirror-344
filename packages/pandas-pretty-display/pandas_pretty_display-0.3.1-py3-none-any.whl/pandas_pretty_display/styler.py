"""
Module for styling pandas DataFrames with alternating colors and improved formatting.
"""

try:
    from IPython.display import display, HTML
except ImportError:
    try:
        from IPython.core.display import display, HTML
    except ImportError:
        raise ImportError("Could not import display and HTML from IPython. Please ensure IPython is installed correctly.")

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
    # Universal approach to target headers across different Jupyter environments
    header_css = """
    <style>
    /* Universal selector for h1 headers across different Jupyter environments */
    h1 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 3px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 15px !important;
        margin: 10px 0px !important;
        font-size: 24px !important;
    }
    
    /* Universal selector for h2 headers */
    h2 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 12px !important;
        margin: 10px 0px !important;
        font-size: 20px !important;
    }
    
    /* Universal selector for h3 headers */
    h3 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 10px !important;
        margin: 10px 0px !important;
        font-size: 18px !important;
    }
    
    /* Additional selectors for specific Jupyter environments */
    .rendered_html h1, .jp-RenderedMarkdown h1, .markdown h1, div[data-mime-type="text/markdown"] h1 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 3px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 15px !important;
        margin: 10px 0px !important;
        font-size: 24px !important;
    }
    
    .rendered_html h2, .jp-RenderedMarkdown h2, .markdown h2, div[data-mime-type="text/markdown"] h2 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 12px !important;
        margin: 10px 0px !important;
        font-size: 20px !important;
    }
    
    .rendered_html h3, .jp-RenderedMarkdown h3, .markdown h3, div[data-mime-type="text/markdown"] h3 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 10px !important;
        margin: 10px 0px !important;
        font-size: 18px !important;
    }
    </style>
    """
    display(HTML(header_css))
    
    # Add a direct script injection for more complex environments
    script_injection = """
    <script>
    // This script will run after the page loads and apply styling to headers
    (function() {
        // Function to apply styles to headers
        function applyHeaderStyles() {
            // Style for h1
            const h1Style = {
                'background-color': '#ffcc00',
                'color': '#000080',
                'border': '3px solid #ff0000',
                'border-radius': '5px',
                'padding': '15px',
                'margin': '10px 0px',
                'font-size': '24px'
            };
            
            // Style for h2
            const h2Style = {
                'background-color': '#ffcc00',
                'color': '#000080',
                'border': '2px solid #ff0000',
                'border-radius': '5px',
                'padding': '12px',
                'margin': '10px 0px',
                'font-size': '20px'
            };
            
            // Style for h3
            const h3Style = {
                'background-color': '#ffcc00',
                'color': '#000080',
                'border': '1px solid #ff0000',
                'border-radius': '5px',
                'padding': '10px',
                'margin': '10px 0px',
                'font-size': '18px'
            };
            
            // Apply styles to all h1 elements
            document.querySelectorAll('h1').forEach(h1 => {
                Object.assign(h1.style, h1Style);
            });
            
            // Apply styles to all h2 elements
            document.querySelectorAll('h2').forEach(h2 => {
                Object.assign(h2.style, h2Style);
            });
            
            // Apply styles to all h3 elements
            document.querySelectorAll('h3').forEach(h3 => {
                Object.assign(h3.style, h3Style);
            });
        }
        
        // Apply styles immediately
        applyHeaderStyles();
        
        // Set up a mutation observer to apply styles to new headers
        const observer = new MutationObserver(mutations => {
            applyHeaderStyles();
        });
        
        // Start observing the document body for changes
        observer.observe(document.body, { 
            childList: true,
            subtree: true
        });
    })();
    </script>
    """
    display(HTML(script_injection))

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
