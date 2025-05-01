"""
Module for styling pandas DataFrames with alternating colors and improved formatting.
"""

try:
    from IPython.display import display, HTML
    from IPython import get_ipython
except ImportError:
    try:
        from IPython.core.display import display, HTML
        from IPython import get_ipython
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
    - Level 1 headers are bold and centered
    - Level 2 headers are bold
    
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
        font-weight: bold !important;
        text-align: center !important;
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
        font-weight: bold !important;
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
    .rendered_html h1, .jp-RenderedMarkdown h1, .markdown h1, div[data-mime-type="text/markdown"] h1,
    .cm-header-1, .cm-header.cm-header-1, .CodeMirror-line .cm-header-1 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 3px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 15px !important;
        margin: 10px 0px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    .rendered_html h2, .jp-RenderedMarkdown h2, .markdown h2, div[data-mime-type="text/markdown"] h2,
    .cm-header-2, .cm-header.cm-header-2, .CodeMirror-line .cm-header-2 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 12px !important;
        margin: 10px 0px !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    
    .rendered_html h3, .jp-RenderedMarkdown h3, .markdown h3, div[data-mime-type="text/markdown"] h3,
    .cm-header-3, .cm-header.cm-header-3, .CodeMirror-line .cm-header-3 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 5px !important;
        padding: 10px !important;
        margin: 10px 0px !important;
        font-size: 18px !important;
    }
    
    /* VS Code specific selectors */
    .vscode-dark h1, .vscode-light h1, .vscode h1,
    .vscode-dark h2, .vscode-light h2, .vscode h2,
    .vscode-dark h3, .vscode-light h3, .vscode h3 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border-radius: 5px !important;
        margin: 10px 0px !important;
    }
    
    .vscode-dark h1, .vscode-light h1, .vscode h1 {
        border: 3px solid #ff0000 !important;
        padding: 15px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    .vscode-dark h2, .vscode-light h2, .vscode h2 {
        border: 2px solid #ff0000 !important;
        padding: 12px !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    
    .vscode-dark h3, .vscode-light h3, .vscode h3 {
        border: 1px solid #ff0000 !important;
        padding: 10px !important;
        font-size: 18px !important;
    }
    
    /* Windsurf specific selectors */
    .markdown-cell h1, .markdown-cell h2, .markdown-cell h3,
    .markdown-body h1, .markdown-body h2, .markdown-body h3 {
        background-color: #ffcc00 !important;
        color: #000080 !important;
        border-radius: 5px !important;
        margin: 10px 0px !important;
    }
    
    .markdown-cell h1, .markdown-body h1 {
        border: 3px solid #ff0000 !important;
        padding: 15px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    
    .markdown-cell h2, .markdown-body h2 {
        border: 2px solid #ff0000 !important;
        padding: 12px !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    
    .markdown-cell h3, .markdown-body h3 {
        border: 1px solid #ff0000 !important;
        padding: 10px !important;
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
                'font-size': '24px',
                'font-weight': 'bold',
                'text-align': 'center'
            };
            
            // Style for h2
            const h2Style = {
                'background-color': '#ffcc00',
                'color': '#000080',
                'border': '2px solid #ff0000',
                'border-radius': '5px',
                'padding': '12px',
                'margin': '10px 0px',
                'font-size': '20px',
                'font-weight': 'bold'
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
    background-color: #ffcc00; color: #000080; font-size: 24px; font-weight: bold; text-align: center;">
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
    
    # Use a safer approach to hide output that doesn't rely on 'this.element'
    display(HTML("""
    <script>
    // Safer approach to hide output
    (function() {
        try {
            // Try to find the current output area in various ways
            var outputs = document.querySelectorAll('.output_area, .jp-OutputArea');
            if (outputs.length > 0) {
                // Get the most recently created output (likely to be from this cell)
                var lastOutput = outputs[outputs.length - 1];
                
                // Check if this is the right output (from the current cell)
                var currentCell = lastOutput.closest('.cell, .jp-Cell');
                if (currentCell) {
                    // Hide text output but keep any styling that was applied
                    var textOutputs = currentCell.querySelectorAll('.output_text, .jp-OutputArea-output');
                    textOutputs.forEach(function(output) {
                        if (output.textContent.includes('Notebook styling applied') || 
                            output.textContent.includes('All markdown headers') ||
                            output.textContent.includes('Examples of markdown headers')) {
                            output.style.display = 'none';
                        }
                    });
                }
            }
        } catch (e) {
            // Silently fail if there's an error - we don't want to break the notebook
            console.log('Note: Could not hide output message, but styling is still applied.');
        }
    })();
    </script>
    """))
