"""
Colab Print - Enhanced display utilities for Jupyter/Colab notebooks.

This module provides a comprehensive set of display utilities for creating beautiful, 
customizable HTML outputs in Jupyter and Google Colab notebooks. It transforms plain
data into visually appealing, styled content to improve notebook readability and presentation.

Features:
- 🎨 Rich text styling with 20+ predefined styles (headers, titles, cards, quotes, etc.)
- 📊 Beautiful DataFrame display with extensive customization options
- 📑 Customizable tables with header/row styling and cell highlighting
- 📜 Formatted lists and nested structures with ordered/unordered options
- 📖 Structured dictionary display with customizable key/value styling
- 🎭 Extensible theming system for consistent visual styling
- 📏 Smart row/column limiting for large DataFrames
- 🔍 Targeted highlighting for specific rows, columns, or individual cells
- 🔄 Graceful fallbacks when used outside of notebook environments

Content Display Methods:
- text: printer.display(text, style="default", **inline_styles)
- tables: printer.display_table(headers, rows, style="default", **table_options)
- DataFrames: printer.display_df(df, style="default", highlight_cols=[], **options)
- lists: printer.display_list(items, ordered=False, style="default", **options)
- dictionaries: printer.display_dict(data, style="default", **options)

Convenience Functions:
- Text styling: header(), title(), subtitle(), highlight(), info(), success(), etc.
- Content display: dfd(), table(), list_(), dict_()

Basic Usage:
    from colab_print import Printer, header, success, dfd
    
    # Object-oriented style
    printer = Printer()
    printer.display("Hello World!", style="highlight")
    
    # Shortcut functions
    header("Main Section")
    success("Operation completed successfully")
    
    # Content-specific display
    df = pandas.DataFrame(...)
    dfd(df, highlight_cols=["important_column"], max_rows=20)

See documentation for complete style list and customization options.
"""

from IPython.display import display as ip_display, HTML, Javascript
import pandas as pd
from dataclasses import dataclass
from typing import Callable, Optional, Union, Dict, List, Any, Tuple
import abc
import warnings
import uuid
import re
import json
import html
from colab_print._exception import (ColabPrintError, TextError, ColorError,
                                    DisplayEnvironmentError, InvalidParameterError,
                                    DisplayMethodError, DisplayUpdateError, ListError, StyleNotFoundError, StyleError,
                                    StyleConflictError, StyleParsingError, TableError, DictError,
                                    IPythonNotAvailableError, ProgressError, ConversionError, ArrayConversionError,
                                    FormattingError, HTMLGenerationError, HTMLRenderingError, DataFrameError,
                                    MatrixDetectionError, NestedStructureError, MermaidError, ContentTypeError,
                                    CodeError, CodeParsingError, SyntaxHighlightingError)

__version__ = "0.3.0"
__author__ = "alaamer12"
__email__ = "ahmedmuhmmed239@gmail.com"
__license__ = "MIT"
__keywords__ = ["jupyter",
                "colab",
                "display",
                "dataframe",
                "styling",
                "html",
                "visualization",
                "notebook",
                "formatting",
                "presentation",
                "rich-text",
                "tables",
                "pandas",
                "output",
                "ipython",
                "data-science"
                ]
__description__ = "Enhanced display utilities for Jupyter/Colab notebooks."
__url__ = "https://github.com/alaamer12/colab-print"
__author_email__ = "ahmedmuhmmed239@gmail.com"
__all__ = [
    # Main classes
    "Printer",

    # Display shortcuts
    "header", "title", "subtitle", "section_divider", "subheader",
    "code", "card", "quote", "badge", "data_highlight", "footer",
    "highlight", "info", "success", "warning", "error", "muted", "primary", "secondary",
    "dfd", "table", "list_", "dict_", "progress", "mermaid",
]
__dir__ = sorted(__all__)

# Define the theme types
DEFAULT_THEMES = {
    'default': 'color: #000000; font-size: 16px; font-family: Arial, sans-serif; letter-spacing: 0.3px; line-height: 1.5; padding: 4px 6px; border-radius: 2px;',
    'highlight': 'color: #E74C3C; font-size: 18px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 3px rgba(231, 76, 60, 0.3); letter-spacing: 0.6px; background-color: rgba(231, 76, 60, 0.05); padding: 6px 10px; border-radius: 4px; border-left: 3px solid #E74C3C;',
    'info': 'color: #3498DB; font-size: 16px; font-style: italic; font-family: Arial, sans-serif; border-bottom: 1px dotted #3498DB; letter-spacing: 0.3px; background-color: rgba(52, 152, 219, 0.05); padding: 4px 8px; border-radius: 3px;',
    'success': 'color: #27AE60; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(39, 174, 96, 0.2); letter-spacing: 0.3px; background-color: rgba(39, 174, 96, 0.05); padding: 4px 8px; border-radius: 3px; border-left: 2px solid #27AE60;',
    'warning': 'color: #F39C12; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(243, 156, 18, 0.2); letter-spacing: 0.3px; background-color: rgba(243, 156, 18, 0.05); padding: 4px 8px; border-radius: 3px; border-left: 2px solid #F39C12;',
    'error': 'color: #C0392B; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(192, 57, 43, 0.2); letter-spacing: 0.3px; background-color: rgba(192, 57, 43, 0.05); padding: 4px 8px; border-radius: 3px; border-left: 2px solid #C0392B;',
    'muted': 'color: #7F8C8D; font-size: 14px; font-family: Arial, sans-serif; font-style: italic; letter-spacing: 0.2px; opacity: 0.85; padding: 2px 4px;',
    'code': 'color: #2E86C1; font-size: 14px; font-family: Arial, sans-serif; background-color: rgba(46, 134, 193, 0.07); padding: 2px 6px; border-radius: 3px; border: 1px solid rgba(46, 134, 193, 0.2); letter-spacing: 0.2px;',
    'primary': 'color: #3498DB; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; letter-spacing: 0.3px; background-color: rgba(52, 152, 219, 0.08); padding: 6px 10px; border-radius: 4px; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);',
    'secondary': 'color: #9B59B6; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; letter-spacing: 0.3px; background-color: rgba(155, 89, 182, 0.08); padding: 6px 10px; border-radius: 4px; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);',
}

# Define specialized style variables for easy access
SPECIAL_STYLES = {
    'header': 'color: #1A237E; font-size: 24px; font-weight: bold; font-family: Arial, sans-serif; text-align: center; letter-spacing: 1px; padding: 16px 10px; border-top: 2px dashed #1A237E; border-bottom: 2px dashed #1A237E; margin: 30px 0; background-color: rgba(26, 35, 126, 0.05); display: block; clear: both;',

    'subheader': 'color: #283593; font-size: 20px; font-weight: bold; font-family: Arial, sans-serif; letter-spacing: 0.7px; padding: 8px 10px; border-left: 4px solid #283593; margin: 25px 0; background-color: rgba(40, 53, 147, 0.03); display: block; clear: both;',

    'title': 'color: #3F51B5; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif; text-align: center; text-shadow: 1px 1px 1px rgba(63, 81, 181, 0.2); letter-spacing: 1.2px; padding: 10px; margin: 35px 0 25px 0; display: block; clear: both;',

    'subtitle': 'color: #5C6BC0; font-size: 18px; font-weight: 600; font-style: italic; font-family: Arial, sans-serif; text-align: center; letter-spacing: 0.5px; margin: 20px 0 30px 0; display: block; clear: both;',

    'code_block': 'color: #424242; font-size: 14px; font-family: Arial, sans-serif; background-color: #F5F5F5; padding: 15px; border-radius: 5px; border-left: 4px solid #9E9E9E; margin: 25px 0; overflow-x: auto; white-space: pre-wrap; display: block; clear: both;',

    'quote': 'color: #455A64; font-size: 16px; font-style: italic; font-family: Arial, sans-serif; background-color: #ECEFF1; padding: 15px 20px; border-left: 5px solid #78909C; margin: 30px 0; letter-spacing: 0.3px; line-height: 1.6; display: block; clear: both;',

    'card': 'color: #333333; font-size: 16px; font-family: Arial, sans-serif; background-color: #FFFFFF; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); margin: 30px 0; border: 1px solid #E0E0E0; display: block; clear: both;',

    'notice': 'color: #004D40; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; background-color: #E0F2F1; padding: 15px; border-radius: 5px; border: 1px solid #80CBC4; margin: 25px 0; letter-spacing: 0.2px; display: block; clear: both;',

    'badge': 'color: #FFFFFF; font-size: 12px; font-weight: bold; font-family: Arial, sans-serif; background-color: #00897B; padding: 3px 8px; border-radius: 12px; display: inline-block; letter-spacing: 0.5px; margin: 5px 5px 5px 0;',

    'footer': 'color: #757575; font-size: 13px; font-style: italic; font-family: Arial, sans-serif; text-align: center; border-top: 1px solid #E0E0E0; padding-top: 10px; margin: 35px 0 15px 0; letter-spacing: 0.3px; display: block; clear: both;',

    'data_highlight': 'color: #0D47A1; font-size: 18px; font-weight: bold; font-family: Arial, sans-serif; background-color: rgba(13, 71, 161, 0.08); padding: 5px 8px; border-radius: 4px; letter-spacing: 0.3px; text-align: center; display: block; margin: 25px 0; clear: both;',

    'section_divider': 'color: #212121; font-size: 18px; font-weight: bold; font-family: Arial, sans-serif; border-bottom: 2px solid #BDBDBD; padding-bottom: 5px; margin: 35px 0 25px 0; letter-spacing: 0.4px; display: block; clear: both;',

    'df': 'color: #000000; font-size: 14px; font-family: Arial, sans-serif; background-color: #FFFFFF; border-collapse: collapse; width: 100%; margin: 15px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);',

    'table': 'color: #0f67A9; font-size: 15px; font-family: Arial, sans-serif; width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 1px 4px rgba(0,0,0,0.15); border-radius: 4px; overflow: hidden;',

    'list': 'color: #000000; font-size: 16px; font-family: Arial, sans-serif; padding-left: 20px; line-height: 1.6; margin: 25px 0; display: block; clear: both;',

    'dict': 'color: #000000; font-size: 16px; font-family: Arial, sans-serif; background-color: rgba(0,0,0,0.02); padding: 12px; border-radius: 4px; margin: 25px 0; border-left: 3px solid #607D8B; display: block; clear: both;',

    'highlight': 'color: #E74C3C; font-size: 18px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 3px rgba(231, 76, 60, 0.3); letter-spacing: 0.6px; background-color: rgba(231, 76, 60, 0.05); padding: 6px 10px; border-radius: 4px; border-left: 3px solid #E74C3C; display: block; margin: 25px 0; clear: both;',

    'info': 'color: #3498DB; font-size: 16px; font-style: italic; font-family: Arial, sans-serif; border-bottom: 1px dotted #3498DB; letter-spacing: 0.3px; background-color: rgba(52, 152, 219, 0.05); padding: 8px; border-radius: 3px; display: block; margin: 25px 0; clear: both;',

    'success': 'color: #27AE60; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(39, 174, 96, 0.2); letter-spacing: 0.3px; background-color: rgba(39, 174, 96, 0.05); padding: 8px; border-radius: 3px; border-left: 2px solid #27AE60; display: block; margin: 25px 0; clear: both;',

    'warning': 'color: #F39C12; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(243, 156, 18, 0.2); letter-spacing: 0.3px; background-color: rgba(243, 156, 18, 0.05); padding: 8px; border-radius: 3px; border-left: 2px solid #F39C12; display: block; margin: 25px 0; clear: both;',

    'error': 'color: #C0392B; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; text-shadow: 1px 1px 2px rgba(192, 57, 43, 0.2); letter-spacing: 0.3px; background-color: rgba(192, 57, 43, 0.05); padding: 8px; border-radius: 3px; border-left: 2px solid #C0392B; display: block; margin: 25px 0; clear: both;',

    'muted': 'color: #7F8C8D; font-size: 14px; font-family: Arial, sans-serif; font-style: italic; letter-spacing: 0.2px; opacity: 0.85; padding: 4px; display: block; margin: 20px 0; clear: both;',

    'primary': 'color: #3498DB; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; letter-spacing: 0.3px; background-color: rgba(52, 152, 219, 0.08); padding: 6px 10px; border-radius: 4px; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); display: block; margin: 25px 0; clear: both;',

    'secondary': 'color: #9B59B6; font-size: 16px; font-weight: 600; font-family: Arial, sans-serif; letter-spacing: 0.3px; background-color: rgba(155, 89, 182, 0.08); padding: 6px 10px; border-radius: 4px; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); display: block; margin: 25px 0; clear: both;',

    'progress': 'color: #2C3E50; font-size: 14px; font-weight: 500; font-family: "Segoe UI", Roboto, sans-serif; background: linear-gradient(to right, #f7f9fc, #edf2f7); padding: 18px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.04), 0 0 1px rgba(0,0,0,0.1); margin: 24px 0; border: none; display: block; clear: both;',
}


@dataclass
class DFDisplayParams:
    """Parameters for DataFrame display styling."""
    style: str = 'default'
    max_rows: Optional[int] = None
    max_cols: Optional[int] = None
    precision: int = 2
    header_style: Optional[str] = None
    odd_row_style: Optional[str] = None
    even_row_style: Optional[str] = None
    index: bool = True
    width: str = '100%'
    caption: Optional[str] = None
    highlight_cols: Optional[Union[List, Dict]] = None
    highlight_rows: Optional[Union[List, Dict]] = None
    highlight_cells: Optional[Dict] = None


@dataclass
class TableDisplayParams:
    """Parameters for table display styling."""
    style: str = 'default'
    width: str = '100%'
    header_style: Optional[str] = None
    row_style: Optional[str] = None
    caption: Optional[str] = None


class Displayer(abc.ABC):
    """
    Abstract base class for display components.
    
    All display components should extend this class and implement
    the display method according to their specific requirements.
    """

    def __init__(self, styles: Dict[str, str]):
        """
        Initialize a displayer with styles.
        
        Args:
            styles: Dictionary of named styles
        """
        self.styles = styles

    def _process_inline_styles(self, inline_styles: Dict[str, str]) -> str:
        """
        Convert Python-style keys to CSS style format and join them.
        
        Args:
            inline_styles: Dictionary of style attributes
            
        Returns:
            Formatted CSS string
            
        Raises:
            ConversionError: If there's an error converting Python-style keys to CSS format
        """
        try:
            corrected_styles = {k.replace('_', '-') if '_' in k else k: v for k, v in inline_styles.items()}
            return "; ".join([f"{key}: {value}" for key, value in corrected_styles.items()])
        except Exception as e:
            raise ConversionError(
                from_type="Dict[str, str]", 
                to_type="CSS string", 
                message=f"Failed to convert inline styles to CSS format: {str(e)}"
            )

    @abc.abstractmethod
    def display(self, *args, **kwargs):
        """Display content with the specified styling."""
        pass


class TextDisplayer(Displayer):
    """Displays styled text content."""

    def display(self, text: str, *, style: str = 'default', **inline_styles) -> None:
        """
        Display styled text.
        
        Args:
            text: The text to display
            style: Named style from the available styles
            **inline_styles: Additional CSS styles to apply
            
        Raises:
            TextError: If text is not a string
            StyleNotFoundError: If specified style is not found
            StyleParsingError: If there's an error parsing inline styles
            HTMLRenderingError: If HTML content cannot be rendered
        """
        if not isinstance(text, str):
            received_type = type(text).__name__
            raise TextError(f"Text must be a string, received {received_type}")

        if style not in self.styles:
            raise StyleNotFoundError(style_name=style,
                                     message=f"Style '{style}' not found. Available styles: {', '.join(self.styles.keys())}")

        try:
            base_style = self.styles.get(style)
            inline_style_string = self._process_inline_styles(inline_styles)
            final_style = f"{base_style} {inline_style_string}" if inline_style_string else base_style
            formatted_text = f'<span style="{final_style}">{text}</span>'

            self._display_html(formatted_text)
        except ValueError as e:
            raise StyleParsingError(style_value=str(inline_styles), message=f"Error parsing styles: {str(e)}")

    def _process_inline_styles(self, inline_styles: Dict[str, str]) -> str:
        """
        Convert Python-style keys to CSS style format and join them.
        
        Args:
            inline_styles: Dictionary of style attributes
            
        Returns:
            Formatted CSS string
            
        Raises:
            StyleParsingError: If there's an error parsing the styles
        """
        try:
            corrected_styles = {k.replace('_', '-') if '_' in k else k: v for k, v in inline_styles.items()}
            return "; ".join([f"{key}: {value}" for key, value in corrected_styles.items()])
        except Exception as e:
            raise StyleParsingError(style_value=str(inline_styles),
                                    message=f"Failed to process inline styles: {str(e)}")

    @staticmethod
    def _display_html(html_content: str) -> None:
        """
        Display HTML content safely.
        
        Args:
            html_content: HTML content to display
            
        Raises:
            IPythonNotAvailableError: If IPython environment is not detected
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. HTML output will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render HTML content: {str(e)}")


class CodeDisplayer(Displayer):
    """Displays code with syntax highlighting and special formatting for Python prompts."""
    
    def __init__(self, styles: Dict[str, str]):
        """
        Initialize a code displayer with styles.
        
        Args:
            styles: Dictionary of named styles
        """
        super().__init__(styles)
        self.default_colors = [
            "#3498DB",  # Blue
            "#9B59B6",  # Purple
            "#2ECC71",  # Green
            "#F1C40F",  # Yellow
            "#E74C3C",  # Red
            "#1ABC9C",  # Turquoise
        ]
    
    def _parse_python_prompts(self, code: str) -> List[Dict[str, Any]]:
        """
        Parse Python code and identify prompt markers (>, >>>, ...).
        
        Args:
            code: Python code text
            
        Returns:
            List of dictionaries containing line info and prompt type
            
        Raises:
            CodeParsingError: If there's an error parsing the code
        """
        try:
            lines = code.split('\n')
            parsed_lines = []
            
            for i, line in enumerate(lines):
                line_info = {
                    'number': i + 1,
                    'text': line,
                    'prompt_type': None,
                    'indentation': 0
                }
                
                stripped = line.lstrip()
                line_info['indentation'] = len(line) - len(stripped)
                
                if stripped.startswith('>>> '):
                    line_info['prompt_type'] = 'primary'
                    line_info['text'] = stripped[4:]
                elif stripped.startswith('... '):
                    line_info['prompt_type'] = 'continuation'
                    line_info['text'] = stripped[4:]
                elif stripped.startswith('> '):
                    line_info['prompt_type'] = 'shell'
                    line_info['text'] = stripped[2:]
                
                parsed_lines.append(line_info)
            
            return parsed_lines
        except Exception as e:
            raise CodeParsingError(message=f"Failed to parse code: {str(e)}")
    
    def _calculate_gradient_color(self, line_number: int, total_lines: int, 
                                  start_color: str = "#3498DB", end_color: str = "#9B59B6") -> str:
        """
        Calculate a gradient color based on the line position.
        
        Args:
            line_number: Current line number (1-based)
            total_lines: Total number of lines
            start_color: Starting color in the gradient
            end_color: Ending color in the gradient
            
        Returns:
            Hex color string
            
        Raises:
            ColorError: If there's an error parsing or calculating colors
        """
        try:
            # Parse start and end colors
            if not start_color.startswith('#') or not end_color.startswith('#'):
                raise ColorError(color_value=f"{start_color} or {end_color}", 
                                message="Colors must be hex values starting with #")
                
            start_r = int(start_color[1:3], 16)
            start_g = int(start_color[3:5], 16)
            start_b = int(start_color[5:7], 16)
            
            end_r = int(end_color[1:3], 16)
            end_g = int(end_color[3:5], 16)
            end_b = int(end_color[5:7], 16)
            
            # Calculate position in gradient (0 to 1)
            if total_lines <= 1:
                position = 0
            else:
                position = (line_number - 1) / (total_lines - 1)
            
            # Calculate new color
            r = int(start_r + position * (end_r - start_r))
            g = int(start_g + position * (end_g - start_g))
            b = int(start_b + position * (end_b - start_b))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except ColorError:
            raise  # Re-raise existing ColorError
        except Exception as e:
            raise ColorError(color_value=f"{start_color} to {end_color}", 
                           message=f"Failed to calculate gradient color: {str(e)}")
    
    def _get_block_level_color(self, indentation: int) -> str:
        """
        Get a color based on the indentation level.
        
        Args:
            indentation: Number of spaces at the beginning of the line
            
        Returns:
            Hex color string
        """
        # Normalize indentation to a block level
        block_level = indentation // 4  # Assuming 4 spaces per indentation level
        color_index = block_level % len(self.default_colors)
        return self.default_colors[color_index]
    
    def _apply_syntax_highlighting(self, parsed_lines: List[Dict[str, Any]], 
                                   highlighting_mode: str = 'block', 
                                   base_style: str = "") -> str:
        """
        Apply syntax highlighting to parsed code lines.
        
        Args:
            parsed_lines: List of dictionaries containing line info
            highlighting_mode: 'block' for indentation-based coloring, 'gradient' for gradient coloring
            base_style: Base CSS style string
            
        Returns:
            HTML string with highlighted code
            
        Raises:
            SyntaxHighlightingError: If there's an error applying syntax highlighting
            InvalidParameterError: If an invalid highlighting mode is provided
        """
        try:
            if highlighting_mode not in ['block', 'gradient']:
                raise InvalidParameterError(param_name="highlighting_mode",
                                         expected="'block' or 'gradient'",
                                         received=highlighting_mode)
            
            total_lines = len(parsed_lines)
            html_lines = []
            
            # Start with a pre tag for proper code formatting
            pre_style = f"font-family: monospace; padding: 15px; border-radius: 5px; {base_style}"
            html_lines.append(f'<pre style="{pre_style}">')
            
            for i, line_info in enumerate(parsed_lines):
                line_number = line_info['number']
                text = html.escape(line_info['text'])
                indentation = line_info['indentation']
                prompt_type = line_info['prompt_type']
                
                # Determine line color based on the highlighting mode
                if highlighting_mode == 'gradient':
                    line_color = self._calculate_gradient_color(line_number, total_lines)
                else:  # block level
                    line_color = self._get_block_level_color(indentation)
                
                # Format based on prompt type
                if prompt_type == 'primary':
                    prompt_style = "color: #E67E22; font-weight: bold;"
                    line_html = f'<span style="{prompt_style}">>>></span> <span style="color: {line_color};">{text}</span>'
                elif prompt_type == 'continuation':
                    prompt_style = "color: #E67E22; font-weight: bold;"
                    line_html = f'<span style="{prompt_style}>...</span> <span style="color: {line_color};">{text}</span>'
                elif prompt_type == 'shell':
                    prompt_style = "color: #16A085; font-weight: bold;"
                    line_html = f'<span style="{prompt_style}">></span> <span style="color: {line_color};">{text}</span>'
                else:
                    line_html = f'<span style="color: {line_color};">{text}</span>'
                
                html_lines.append(line_html)
            
            html_lines.append('</pre>')
            return '\n'.join(html_lines)
        except (InvalidParameterError, ColorError):
            raise  # Re-raise specific exceptions
        except Exception as e:
            raise SyntaxHighlightingError(highlighting_mode=highlighting_mode,
                                        message=f"Failed to apply syntax highlighting: {str(e)}")
    
    def display(self, code: str, *, 
                style: str = 'code_block', 
                highlighting_mode: str = 'block',
                background_color: Optional[str] = None,
                prompt_style: Optional[str] = None,
                **inline_styles) -> None:
        """
        Display code with syntax highlighting and prompt formatting.
        
        Args:
            code: Code to display
            style: Named style from the available styles
            highlighting_mode: 'block' for indentation-based coloring or 'gradient' for gradient coloring
            background_color: Optional background color override
            prompt_style: Optional style for prompt markers
            **inline_styles: Additional CSS styles to apply
            
        Raises:
            CodeError: If code is not a string or other code display issues occur
            StyleNotFoundError: If specified style is not found
            StyleParsingError: If there's an error parsing inline styles
            CodeParsingError: If there's an error parsing the code
            SyntaxHighlightingError: If there's an error applying syntax highlighting
            HTMLRenderingError: If HTML content cannot be rendered
        """
        if not isinstance(code, str):
            received_type = type(code).__name__
            raise CodeError(f"Code must be a string, received {received_type}")

        if style not in self.styles:
            raise StyleNotFoundError(style_name=style,
                                    message=f"Style '{style}' not found. Available styles: {', '.join(self.styles.keys())}")

        try:
            # Get the base style
            base_style = self.styles.get(style)
            
            # Process inline styles
            inline_style_string = self._process_inline_styles(inline_styles)
            
            # Combine styles
            final_style = f"{base_style} {inline_style_string}" if inline_style_string else base_style
            
            # Override background color if specified
            if background_color:
                final_style = final_style.replace("background-color: #f5f5f5;", f"background-color: {background_color};")
            
            # Parse the code for Python prompts
            parsed_lines = self._parse_python_prompts(code)
            
            # Apply syntax highlighting
            html_content = self._apply_syntax_highlighting(parsed_lines, highlighting_mode, final_style)
            
            # Display the HTML
            self._display_html(html_content)
            
        except ValueError as e:
            raise StyleParsingError(style_value=str(inline_styles), message=f"Error parsing styles: {str(e)}")
        except (CodeParsingError, SyntaxHighlightingError, ColorError, InvalidParameterError):
            raise  # Re-raise specific exceptions
        except Exception as e:
            raise CodeError(f"Error displaying code: {str(e)}")

    @staticmethod
    def _display_html(html_content: str) -> None:
        """
        Display HTML content safely.
        
        Args:
            html_content: HTML content to display
            
        Raises:
            IPythonNotAvailableError: If IPython environment is not detected
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. HTML output will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render HTML content: {str(e)}")


class TableDisplayer(Displayer):
    """Displays HTML tables with customizable styling."""

    def _get_table_styles(self, style: str = 'default', width: str = '100%') -> tuple:
        """
        Generate the CSS styles for the table, headers, and cells.
        
        Args:
            style: Named style from the available styles
            width: Width of the table (CSS value)
            
        Returns:
            Tuple of (table_style, th_style, td_style)
        """
        base_style = self.styles.get(style, self.styles['default'])

        # Ensure width is explicitly included to take full notebook width
        table_style = f"{base_style} border-collapse: collapse; width: {width} !important;"
        th_style = "background-color: #f2f2f2; padding: 8px; border: 1px solid #ddd; text-align: left;"
        td_style = "padding: 8px; border: 1px solid #ddd;"

        return table_style, th_style, td_style

    @staticmethod
    def _generate_table_caption(caption: Optional[str], style_base: str) -> List[str]:
        """
        Generate HTML for the table caption if provided.
        
        Args:
            caption: Caption text
            style_base: Base CSS style string
            
        Returns:
            List of HTML caption elements or empty list
        """
        if not caption:
            return []

        caption_style = f"caption-side: top; text-align: left; font-weight: bold; margin-bottom: 10px; {style_base}"
        return [f'<caption style="{caption_style}">{caption}</caption>']

    @staticmethod
    def _generate_table_header(headers: List[str], th_style: str) -> List[str]:
        """
        Generate HTML for the table header row.
        
        Args:
            headers: List of header texts
            th_style: CSS style for header cells
            
        Returns:
            List of HTML elements for the header row
        """
        html = ['<tr>']
        for header in headers:
            html.append(f'<th style="{th_style}">{header}</th>')
        html.append('</tr>')
        return html

    @staticmethod
    def _generate_table_rows(rows: List[List[Any]], td_style: str) -> List[str]:
        """
        Generate HTML for the table data rows.
        
        Args:
            rows: List of rows, each row being a list of cell values
            td_style: CSS style for data cells
            
        Returns:
            List of HTML elements for data rows
        """
        html = []
        for row in rows:
            html.append('<tr>')
            for cell in row:
                html.append(f'<td style="{td_style}">{cell}</td>')
            html.append('</tr>')
        return html

    def _process_styles(self, style: str, width: str, custom_header_style: Optional[str],
                        custom_row_style: Optional[str], inline_styles_dict: Dict[str, str]) -> Tuple[
                        str, str, str, str]:
        """
        Process and prepare all styles for the table.
        
        Args:
            style: Named style from the available styles
            width: Width of the table (CSS value)
            custom_header_style: Optional custom CSS for header cells
            custom_row_style: Optional custom CSS for data cells
            inline_styles_dict: Dictionary of additional CSS styles
            
        Returns:
            Tuple of (table_style, th_style, td_style, inline_style_string)
            
        Raises:
            StyleNotFoundError: If specified style is not found
            StyleConflictError: If there are conflicts between styles
            ConversionError: If there's an error converting styles
        """
        try:
            # Process inline styles
            inline_style_string = self._process_inline_styles(inline_styles_dict)

            # Get base styles for table components
            if style not in self.styles:
                raise StyleNotFoundError(style_name=style)
                
            table_style, th_style, td_style = self._get_table_styles(style, width)

            # Check for conflicting styles
            if custom_header_style and 'text-align:' in custom_header_style and 'text-align:' in th_style:
                raise StyleConflictError(
                    style1="default header style",
                    style2="custom header style",
                    message="Conflicting text-align properties in header styles"
                )
                
            if custom_row_style and 'text-align:' in custom_row_style and 'text-align:' in td_style:
                raise StyleConflictError(
                    style1="default row style",
                    style2="custom row style",
                    message="Conflicting text-align properties in row styles"
                )

            # Apply custom styles if provided
            if custom_header_style:
                th_style = custom_header_style
            if custom_row_style:
                td_style = custom_row_style

            # Add inline styles to the table style
            if inline_style_string:
                table_style = f"{table_style} {inline_style_string}"

            return table_style, th_style, td_style, inline_style_string
            
        except (StyleNotFoundError, StyleConflictError, ConversionError):
            raise
        except Exception as e:
            raise StyleError(f"Error processing table styles: {str(e)}")

    def _build_table_html(self, headers: List[str], rows: List[List[Any]],
                          table_style: str, th_style: str, td_style: str,
                          caption: Optional[str], inline_style_string: str) -> List[str]:
        """
        Build the HTML components for the table.
        
        Args:
            headers: List of column headers
            rows: List of rows, each row being a list of cell values
            table_style: CSS style for the table
            th_style: CSS style for header cells
            td_style: CSS style for data cells
            caption: Optional table caption
            inline_style_string: Additional CSS styles
            
        Returns:
            List of HTML elements for the complete table
            
        Raises:
            HTMLGenerationError: If HTML generation fails
        """
        try:
            html = [f'<table style="{table_style}">']

            # Add caption if provided
            html.extend(self._generate_table_caption(caption, inline_style_string))

            # Add header row
            html.extend(self._generate_table_header(headers, th_style))

            # Add data rows
            html.extend(self._generate_table_rows(rows, td_style))

            # Close the table
            html.append('</table>')

            return html
        except Exception as e:
            raise HTMLGenerationError(
                component="table", 
                message=f"Failed to generate table HTML: {str(e)}"
            )

    @staticmethod
    def _display_html(html: List[str], headers: List[str], rows: List[List[Any]]) -> None:
        """
        Display the HTML table or fallback to text representation.
        
        Args:
            html: List of HTML elements for the table
            headers: List of column headers (for fallback display)
            rows: List of rows (for fallback display)
            
        Raises:
            IPythonNotAvailableError: If IPython environment is not detected
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            ip_display(HTML(''.join(html)))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. Table will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render HTML table: {str(e)}") from e

    def display(self, headers: List[str], rows: List[List[Any]], *,
                style: str = 'default', width: str = '100%',
                caption: Optional[str] = None,
                custom_header_style: Optional[str] = None,
                custom_row_style: Optional[str] = None,
                **inline_styles) -> None:
        """
        Display a table with the given headers and rows.
        
        Args:
            headers: List of column headers
            rows: List of rows, each row being a list of cell values
            style: Named style from the available styles
            width: Width of the table (CSS value)
            caption: Optional table caption
            custom_header_style: Optional custom CSS for header cells
            custom_row_style: Optional custom CSS for data cells
            **inline_styles: Additional CSS styles to apply to the table
        """
        # Process inline styles (but don't let them override the width)
        inline_styles_dict = dict(inline_styles)
        if 'width' in inline_styles_dict:
            del inline_styles_dict['width']  # Ensure our width parameter takes precedence

        # Process all styles
        table_style, th_style, td_style, inline_style_string = self._process_styles(
            style, width, custom_header_style, custom_row_style, inline_styles_dict
        )

        # Build HTML components
        html = self._build_table_html(
            headers, rows, table_style, th_style, td_style, caption, inline_style_string
        )

        # Display the final HTML
        self._display_html(html, headers, rows)


class DFDisplayer(Displayer):
    """Displays pandas DataFrames with extensive styling options."""

    def __init__(self, styles: Dict[str, str], df: pd.DataFrame):
        """
        Initialize a DataFrame displayer.
        
        Args:
            styles: Dictionary of named styles
            df: The DataFrame to display
        """
        super().__init__(styles)
        self.df = df

    @staticmethod
    def _extract_base_color(base_style: str) -> str:
        """
        Extract the text color from a base style string.
        
        Args:
            base_style: CSS style string
            
        Returns:
            CSS color property or empty string
        """
        base_color = ""
        for part in base_style.split(';'):
            if 'color:' in part and 'background-color:' not in part:
                base_color = part.strip()
                break
        return base_color

    def _prepare_table_styles(self, style: str, width: str, inline_style_string: str,
                              base_color: str, header_style: Optional[str],
                              odd_row_style: Optional[str], even_row_style: Optional[str]) -> tuple:
        """
        Prepare all the styles needed for the table.
        
        Args:
            style: Named style from the available styles
            width: Table width (CSS value)
            inline_style_string: Processed inline CSS styles
            base_color: Extracted text color
            header_style: Custom CSS for header cells
            odd_row_style: Custom CSS for odd rows
            even_row_style: Custom CSS for even rows
            
        Returns:
            Tuple of (table_style, th_style, odd_td_style, even_td_style)
        """
        # Base styles
        base_style = self.styles.get(style, self.styles['default'])

        # Table element styles - ensure width is important to override any other styles
        table_only_styles = f"border-collapse: collapse; width: {width} !important;"
        table_style = f"{base_style} {table_only_styles}"

        # Cell styles base
        cell_style_base = inline_style_string if inline_style_string else ""

        # Default styles with inline styles
        default_header = f"background-color: #f2f2f2; padding: 8px; border: 1px solid #ddd; text-align: left; font-weight: bold; {base_color}; {cell_style_base}"
        default_odd_row = f"background-color: #ffffff; padding: 8px; border: 1px solid #ddd; {base_color}; {cell_style_base}"
        default_even_row = f"background-color: #f9f9f9; padding: 8px; border: 1px solid #ddd; {base_color}; {cell_style_base}"

        # Apply custom styles if provided
        th_style = f"{header_style} {cell_style_base}" if header_style else default_header
        odd_td_style = f"{odd_row_style} {cell_style_base}" if odd_row_style else default_odd_row
        even_td_style = f"{even_row_style} {cell_style_base}" if even_row_style else default_even_row

        return table_style, th_style, odd_td_style, even_td_style

    @staticmethod
    def _prepare_dataframe(df: pd.DataFrame, max_rows: Optional[int],
                           max_cols: Optional[int], precision: int) -> pd.DataFrame:
        """
        Prepare the DataFrame for display with limits and formatting.
        
        Args:
            df: DataFrame to prepare
            max_rows: Maximum number of rows to display
            max_cols: Maximum number of columns to display
            precision: Decimal precision for float values
            
        Returns:
            Prepared DataFrame copy
            
        Raises:
            FormattingError: If there's an error formatting the DataFrame
            DataFrameError: If there's an issue with the DataFrame structure
        """
        try:
            # Validate inputs
            if max_rows is not None and max_rows <= 0:
                raise FormattingError("max_rows must be a positive integer")
                
            if max_cols is not None and max_cols <= 0:
                raise FormattingError("max_cols must be a positive integer")
                
            if precision < 0:
                raise FormattingError("precision must be a non-negative integer")
            
            if not isinstance(df, pd.DataFrame):
                raise DataFrameError(f"Expected pandas DataFrame, got {type(df).__name__}")
            
            df_copy = df.copy()

            # Handle row limits
            if max_rows is not None and len(df_copy) > max_rows:
                half_rows = max_rows // 2
                df_copy = pd.concat([df_copy.head(half_rows), df_copy.tail(half_rows)])

            # Handle column limits
            if max_cols is not None and len(df_copy.columns) > max_cols:
                half_cols = max_cols // 2
                first_cols = df_copy.columns[:half_cols].tolist()
                last_cols = df_copy.columns[-half_cols:].tolist()
                df_copy = df_copy[first_cols + last_cols]

            # Format numbers
            for col in df_copy.select_dtypes(include=['float']).columns:
                try:
                    df_copy[col] = df_copy[col].apply(lambda x: f"{x:.{precision}f}" if pd.notnull(x) else "")
                except Exception as e:
                    raise FormattingError(f"Error formatting column '{col}': {str(e)}")

            return df_copy
            
        except (FormattingError, DataFrameError):
            raise
        except Exception as e:
            raise FormattingError(f"Error preparing DataFrame: {str(e)}")

    @staticmethod
    def _generate_table_caption(caption: Optional[str], cell_style_base: str) -> List[str]:
        """
        Generate HTML for the table caption if provided.
        
        Args:
            caption: Caption text
            cell_style_base: Base CSS style string
            
        Returns:
            List of HTML caption elements or empty list
        """
        if not caption:
            return []

        caption_style = f"caption-side: top; text-align: left; font-weight: bold; margin-bottom: 10px; {cell_style_base}"
        return [f'<caption style="{caption_style}">{caption}</caption>']

    @staticmethod
    def _generate_header_row(df_copy: pd.DataFrame, th_style: str,
                             highlight_cols: Optional[Union[List, Dict]],
                             index: bool) -> List[str]:
        """
        Generate HTML for the table header row.
        
        Args:
            df_copy: Prepared DataFrame
            th_style: CSS style for header cells
            highlight_cols: Columns to highlight
            index: Whether to show DataFrame index
            
        Returns:
            List of HTML elements for the header row
        """
        html = ['<tr>']

        # Add index header if showing index
        if index:
            html.append(f'<th style="{th_style}"></th>')

        # Add column headers
        for col in df_copy.columns:
            col_style = th_style

            # Apply highlighting to columns if specified
            if highlight_cols:
                if isinstance(highlight_cols, dict) and col in highlight_cols:
                    col_style = f"{th_style} {highlight_cols[col]}"
                elif isinstance(highlight_cols, list) and col in highlight_cols:
                    col_style = f"{th_style} background-color: #FFEB3B !important;"

            html.append(f'<th style="{col_style}">{col}</th>')

        html.append('</tr>')
        return html

    def _generate_data_rows(self, df_copy: pd.DataFrame, even_td_style: str,
                            odd_td_style: str, highlight_rows: Optional[Union[List, Dict]],
                            highlight_cells: Optional[Dict], index: bool) -> List[str]:
        """
        Generate HTML for the table data rows.
        
        Args:
            df_copy: Prepared DataFrame
            even_td_style: CSS style for even rows
            odd_td_style: CSS style for odd rows
            highlight_rows: Rows to highlight
            highlight_cells: Cells to highlight
            index: Whether to show DataFrame index
            
        Returns:
            List of HTML elements for data rows
        """
        html = []

        for i, (idx, row) in enumerate(df_copy.iterrows()):
            row_style = self._get_row_style(i, idx, even_td_style, odd_td_style, highlight_rows)
            html.extend(self._generate_single_row(i, idx, row, row_style, df_copy.columns, highlight_cells, index))

        return html

    @staticmethod
    def _get_row_style(row_index: int, idx, even_td_style: str, odd_td_style: str,
                       highlight_rows: Optional[Union[List, Dict]]) -> str:
        """
        Determine the style for a table row.
        
        Args:
            row_index: Zero-based index of the row
            idx: DataFrame index value for the row
            even_td_style: CSS style for even rows
            odd_td_style: CSS style for odd rows
            highlight_rows: Rows to highlight
            
        Returns:
            CSS style string for the row
        """
        # Base style alternates between even and odd
        row_style = even_td_style if row_index % 2 == 0 else odd_td_style

        # Apply row highlighting if specified
        if highlight_rows:
            if isinstance(highlight_rows, dict) and idx in highlight_rows:
                row_style = f"{row_style} {highlight_rows[idx]}"
            elif isinstance(highlight_rows, list) and idx in highlight_rows:
                row_style = f"{row_style} background-color: #FFEB3B !important;"

        return row_style

    def _generate_single_row(self, row_index: int, idx, row, row_style: str, columns,
                             highlight_cells: Optional[Dict], index: bool) -> List[str]:
        """
        Generate HTML for a single table row.
        
        Args:
            row_index: Zero-based index of the row
            idx: DataFrame index value for the row
            row: Row data
            row_style: Base CSS style for the row
            columns: DataFrame columns
            highlight_cells: Cells to highlight
            index: Whether to show DataFrame index
            
        Returns:
            List of HTML elements for the row
        """
        html_row = ['<tr>']

        # Add index cell if showing index
        if index:
            html_row.append(f'<td style="{row_style} font-weight: bold;">{idx}</td>')

        # Add data cells
        for col in columns:
            cell_style = self._get_cell_style(row_index, idx, col, row_style, highlight_cells)
            cell_value = row[col]
            html_row.append(f'<td style="{cell_style}">{cell_value}</td>')

        html_row.append('</tr>')
        return html_row

    @staticmethod
    def _get_cell_style(row_index: int, idx, col, row_style: str,
                        highlight_cells: Optional[Dict]) -> str:
        """
        Determine the style for a table cell.
        
        Args:
            row_index: Zero-based index of the row
            idx: DataFrame index value for the row
            col: Column name
            row_style: Base CSS style for the row
            highlight_cells: Cells to highlight
            
        Returns:
            CSS style string for the cell
        """
        cell_style = row_style

        # Apply cell highlighting if specified
        if highlight_cells:
            # Try different ways to match the cell coordinates
            if (idx, col) in highlight_cells:
                cell_style = f"{cell_style} {highlight_cells[(idx, col)]}"
            elif (row_index, col) in highlight_cells:
                cell_style = f"{cell_style} {highlight_cells[(row_index, col)]}"
            elif (str(row_index), col) in highlight_cells:
                cell_style = f"{cell_style} {highlight_cells[(str(row_index), col)]}"

        return cell_style

    def display(self, *,
                style: str = 'default',
                max_rows: Optional[int] = None,
                max_cols: Optional[int] = None,
                precision: int = 2,
                header_style: Optional[str] = None,
                odd_row_style: Optional[str] = None,
                even_row_style: Optional[str] = None,
                index: bool = True,
                width: str = '100%',
                caption: Optional[str] = None,
                highlight_cols: Optional[Union[List, Dict]] = None,
                highlight_rows: Optional[Union[List, Dict]] = None,
                highlight_cells: Optional[Dict] = None,
                **inline_styles) -> None:
        """
        Display a pandas DataFrame with customizable styling.

        Args:
            style: Named style from the available styles
            max_rows: Maximum number of rows to display
            max_cols: Maximum number of columns to display
            precision: Decimal precision for float values
            header_style: Custom CSS for header cells
            odd_row_style: Custom CSS for odd rows
            even_row_style: Custom CSS for even rows
            index: Whether to show DataFrame index
            width: Table width (CSS value)
            caption: Table caption
            highlight_cols: Columns to highlight (list) or {col: style} mapping
            highlight_rows: Rows to highlight (list) or {row: style} mapping
            highlight_cells: Cell coordinates to highlight {(row, col): style}
            **inline_styles: Additional CSS styles for all cells
        """
        # Process styles (but don't let them override the width)
        inline_styles_dict = dict(inline_styles)
        if 'width' in inline_styles_dict:
            del inline_styles_dict['width']  # Ensure our width parameter takes precedence

        inline_style_string = self._process_inline_styles(inline_styles_dict)
        base_style = self.styles.get(style, self.styles['default'])
        base_color = self._extract_base_color(base_style)

        # Prepare all styles
        table_style, th_style, odd_td_style, even_td_style = self._prepare_table_styles(
            style, width, inline_style_string, base_color,
            header_style, odd_row_style, even_row_style
        )

        # Prepare the DataFrame
        df_copy = self._prepare_dataframe(self.df, max_rows, max_cols, precision)

        # Build HTML components
        html = [f'<table style="{table_style}">']

        # Add caption if provided
        html.extend(self._generate_table_caption(caption, inline_style_string))

        # Add header row
        html.extend(self._generate_header_row(df_copy, th_style, highlight_cols, index))

        # Add data rows
        html.extend(self._generate_data_rows(df_copy, even_td_style, odd_td_style,
                                             highlight_rows, highlight_cells, index))

        html.append('</table>')

        # Display the final HTML
        try:
            ip_display(HTML(''.join(html)))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. DataFrame will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render DataFrame HTML: {str(e)}") from e


class ListDisplayer(Displayer):
    """Displays Python lists or tuples as HTML lists with enhanced styling for nested structures and matrices."""

    def __init__(self, styles: Dict[str, str]):
        """
        Initialize a list displayer with styles.
        
        Args:
            styles: Dictionary of named styles
        """
        super().__init__(styles)
        # Default color scheme for nested lists - can be customized
        self.nesting_colors = [
            "#3498DB",  # Level 0 - Blue
            "#9B59B6",  # Level 1 - Purple
            "#16A085",  # Level 2 - Teal
            "#F39C12",  # Level 3 - Orange
            "#E74C3C",  # Level 4 - Red
        ]

    def _generate_list_html(self, items: Union[List, Tuple, Any], ordered: bool, style: str,
                            item_style: Optional[str], nesting_level: int = 0,
                            is_matrix: bool = False, **inline_styles) -> str:
        """
        Recursively generate HTML for a list or tuple with enhanced styling.
        
        Args:
            items: The list or tuple to display
            ordered: True for ordered list (<ol>), False for unordered (<ul>)
            style: Base style name for the list container
            item_style: Optional custom CSS for list items
            nesting_level: Current nesting level for applying different styles
            is_matrix: Whether to render as a matrix (2D array)
            **inline_styles: Additional inline styles for list items
            
        Returns:
            HTML string for the list
            
        Raises:
            StyleNotFoundError: If the specified style is not found
            NestedStructureError: If there's an error processing nested structures
            HTMLGenerationError: If HTML generation fails
        """
        try:
            # Handle NumPy arrays or other array-like objects
            items = self._convert_to_list(items)

            # Check if this is a matrix (2D array) and wasn't already flagged
            if not is_matrix and self._is_matrix(items):
                return self._generate_matrix_html(items, style, **inline_styles)

            # Validate style and prepare list styling
            self._validate_style(style)
            list_style = self._prepare_list_style(style, nesting_level)

            # Process item styling
            final_item_style = self._prepare_item_style(item_style, inline_styles, nesting_level)

            # Generate the HTML
            return self._build_list_html(items, ordered, list_style, final_item_style, nesting_level, inline_styles)

        except StyleNotFoundError:
            raise
        except Exception as e:
            raise NestedStructureError(f"Error generating HTML for list at nesting level {nesting_level}: {str(e)}")

    def _validate_style(self, style: str) -> None:
        """
        Validate that the requested style exists.
        
        Args:
            style: Style name to validate
            
        Raises:
            StyleNotFoundError: If the style is not found
        """
        if style not in self.styles:
            raise StyleNotFoundError(style_name=style)

    def _prepare_list_style(self, style: str, nesting_level: int) -> str:
        """
        Prepare the CSS style for the list container based on nesting level.
        
        Args:
            style: Base style name
            nesting_level: Current nesting level
            
        Returns:
            CSS style string for the list container
        """
        style_base = self.styles.get(style)

        # Determine nesting color
        color_idx = min(nesting_level, len(self.nesting_colors) - 1)
        nesting_color = self.nesting_colors[color_idx]

        # Apply nesting-specific style enhancements
        if nesting_level > 0:
            # Add some visual differentiation based on nesting level
            indent = nesting_level * 5  # Slightly increase indent for deeper nesting
            return f"{style_base}; border-left: 2px solid {nesting_color}; padding-left: {indent}px; margin-left: {indent}px;"
        else:
            return style_base

    def _prepare_item_style(self, item_style: Optional[str], inline_styles: Dict[str, str], nesting_level: int) -> str:
        """
        Prepare the CSS style for list items.
        
        Args:
            item_style: Optional custom CSS for list items
            inline_styles: Additional inline styles
            nesting_level: Current nesting level
            
        Returns:
            CSS style string for list items
        """
        list_item_inline_style = self._process_inline_styles(inline_styles)
        final_item_style = item_style if item_style else ""

        if list_item_inline_style:
            final_item_style = f"{final_item_style}; {list_item_inline_style}".strip('; ')

        # Add color to items based on nesting level
        if not final_item_style or "color:" not in final_item_style:
            color_idx = min(nesting_level, len(self.nesting_colors) - 1)
            nesting_color = self.nesting_colors[color_idx]
            final_item_style = f"{final_item_style}; color: {nesting_color}".strip('; ')

        return final_item_style

    def _build_list_html(self, items: List, ordered: bool, list_style: str,
                         item_style: str, nesting_level: int, inline_styles: Dict[str, str]) -> str:
        """
        Build the HTML for the list.
        
        Args:
            items: List items to render
            ordered: Whether to use ordered or unordered list
            list_style: CSS style for the list container
            item_style: CSS style for list items
            nesting_level: Current nesting level
            inline_styles: Additional inline styles
            
        Returns:
            HTML string for the list
        """
        tag = 'ol' if ordered else 'ul'
        html = [f'<{tag} style="{list_style}">']

        for item in items:
            item_content = self._process_list_item(item, ordered, item_style, nesting_level, inline_styles)
            html.append(f'<li style="{item_style}">{item_content}</li>')

        html.append(f'</{tag}>')
        return ''.join(html)

    def _process_list_item(self, item: Any, ordered: bool, item_style: str,
                           nesting_level: int, inline_styles: Dict[str, str]) -> str:
        """
        Process a single list item, handling nested structures.
        
        Args:
            item: The item to process
            ordered: Whether to use ordered or unordered list for nested lists
            item_style: CSS style for the item
            nesting_level: Current nesting level
            inline_styles: Additional inline styles
            
        Returns:
            HTML string for the item content
        """
        if isinstance(item, (list, tuple)) or self._is_array_like(item):
            # Recursively handle nested lists/tuples with increased nesting level
            return self._generate_list_html(
                item, ordered, "list", item_style, nesting_level=nesting_level + 1, **inline_styles
            )
        elif isinstance(item, dict):
            # Handle dictionaries more elegantly
            return self._generate_dict_html(item, nesting_level)
        else:
            return str(item)

    @staticmethod
    def _is_array_like(obj: Any) -> bool:
        """
        Check if an object is array-like.
        
        Args:
            obj: Object to check
            
        Returns:
            True if the object is array-like, False otherwise
        """
        # Quick checks for common Python types
        if isinstance(obj, (list, tuple)):
            return True
            
        if isinstance(obj, (str, dict, bytes, bool, int, float)):
            return False
        
        # Check common array library types by name
        obj_type = str(type(obj))
        if any(lib in obj_type for lib in ['numpy', 'pandas', 'torch', 'tensorflow', 'tf.', 'jax']):
            return True
            
        # Check for common array-like interfaces
        if hasattr(obj, '__iter__'):
            # Try to access basic sequence operations
            try:
                # Check if object supports indexing
                if hasattr(obj, '__getitem__'):
                    return True
                    
                # Check if it has a length
                len(obj)
                return True
            except (TypeError, AttributeError):
                pass

            # Check if it's a generator or iterator without len()
            try:
                # Just getting the iterator is enough to confirm it's iterable
                iter(obj)
                return True
            except TypeError:
                pass
                
        # Check for array or buffer protocol
        if hasattr(obj, '__array__') or hasattr(obj, 'buffer_info'):
            return True
            
        return False

    def _convert_to_list(self, obj: Any) -> List:
        """
        Convert array-like objects to lists for display.
        
        Args:
            obj: Object to convert
            
        Returns:
            List representation of the object
            
        Raises:
            ArrayConversionError: If array-like object conversion fails
        """
        try:
            # Already a list or tuple, return as is
            if isinstance(obj, (list, tuple)):
                return obj
                
            # Handle NumPy arrays specifically
            if 'numpy' in str(type(obj)):
                try:
                    return obj.tolist() if hasattr(obj, 'tolist') else list(obj)
                except (AttributeError, TypeError):
                    return list(obj)

            # Handle pandas Series or DataFrame
            if 'pandas' in str(type(obj)):
                try:
                    return obj.values.tolist() if hasattr(obj, 'values') else list(obj)
                except (AttributeError, TypeError):
                    return list(obj)

            # Handle torch tensors
            if 'torch' in str(type(obj)):
                try:
                    return obj.cpu().numpy().tolist() if hasattr(obj, 'numpy') else list(obj)
                except (AttributeError, TypeError):
                    return list(obj)
                    
            # Handle tensorflow tensors
            if 'tensorflow' in str(type(obj)) or 'tf.' in str(type(obj)):
                try:
                    return obj.numpy().tolist() if hasattr(obj, 'numpy') else list(obj)
                except (AttributeError, TypeError):
                    return list(obj)

            # Handle JAX arrays
            if 'jax' in str(type(obj)):
                try:
                    return obj.tolist() if hasattr(obj, 'tolist') else list(obj)
                except (AttributeError, TypeError):
                    return list(obj)

            # Handle other array-like objects
            if self._is_array_like(obj):
                try:
                    # Try direct conversion
                    return list(obj)
                except (TypeError, ValueError):
                    # Last resort: try to convert items one by one
                    result = []
                    for item in obj:
                        result.append(item)
                    return result
            
            # Single item, not an array-like - wrap in a list
            return [obj]

        except Exception as e:
            obj_type = type(obj).__name__
            raise ArrayConversionError(array_type=obj_type,
                                       message=f"Failed to convert object of type {obj_type}: {str(e)}")

    @staticmethod
    def _is_matrix(items: List) -> bool:
        """
        Check if a list represents a matrix (2D array with consistent row lengths).
        
        Args:
            items: List to check
            
        Returns:
            True if the list is a matrix, False otherwise
            
        Raises:
            MatrixDetectionError: If matrix detection fails
        """
        try:
            if not items or not isinstance(items, (list, tuple)):
                return False

            # Check if all items are lists/tuples of the same length
            if all(isinstance(row, (list, tuple)) for row in items):
                try:
                    row_lengths = [len(row) for row in items]
                    return len(row_lengths) > 1 and all(length == row_lengths[0] for length in row_lengths)
                except (TypeError, AttributeError):
                    return False

            return False

        except Exception as e:
            raise MatrixDetectionError(f"Failed to detect if structure is a matrix: {str(e)}")

    def _generate_matrix_html(self, matrix: List[List], style: str, **inline_styles) -> str:
        """
        Generate HTML for a matrix-like structure.
        
        Args:
            matrix: 2D list/array to display as a matrix
            style: Base style name
            **inline_styles: Additional inline styles
            
        Returns:
            HTML string for the matrix
            
        Raises:
            StyleNotFoundError: If the specified style is not found
            MatrixDetectionError: If matrix processing fails
        """
        try:
            if style not in self.styles:
                raise StyleNotFoundError(style_name=style)

            style_base = self.styles.get(style)
            matrix_style = f"{style_base}; border-collapse: collapse; margin: 10px 0;"
            cell_style = "border: 1px solid #ddd; padding: 6px 10px; text-align: center;"

            html = [f'<table style="{matrix_style}">']

            for row in matrix:
                html.append('<tr>')
                for cell in row:
                    if isinstance(cell, (list, tuple)) or self._is_array_like(cell):
                        # Handle nested structures within matrix cells
                        cell_content = self._generate_list_html(
                            cell, False, style, None, nesting_level=1, **inline_styles
                        )
                    elif isinstance(cell, dict):
                        # Handle dictionaries within matrix cells
                        cell_content = self._generate_dict_html(cell, 1)
                    else:
                        cell_content = str(cell)

                    html.append(f'<td style="{cell_style}">{cell_content}</td>')

                html.append('</tr>')

            html.append('</table>')
            return ''.join(html)

        except StyleNotFoundError:
            raise
        except Exception as e:
            raise MatrixDetectionError(f"Failed to generate HTML for matrix: {str(e)}")

    def _generate_dict_html(self, data: Dict, nesting_level: int) -> str:
        """
        Generate HTML for dictionary inside a list.
        
        Args:
            data: Dictionary to display
            nesting_level: Current nesting level
            
        Returns:
            HTML string for the dictionary
            
        Raises:
            DictError: If dictionary processing fails
            ColorError: If color processing fails
        """
        try:
            if not isinstance(data, dict):
                raise DictError(f"Expected dictionary, received {type(data).__name__}")

            # Simple but nicer dictionary representation than just str(dict)
            color_idx = min(nesting_level, len(self.nesting_colors) - 1)
            nesting_color = self.nesting_colors[color_idx]
            bg_color = self._lighten_color(nesting_color, 0.9)  # Very light background based on nesting color

            html = [
                f'<div style="background-color: {bg_color}; padding: 6px; border-radius: 4px; border-left: 2px solid {nesting_color}; margin: 4px 0;">']

            for key, value in data.items():
                key_style = f"font-weight: bold; color: {nesting_color};"
                html.append(f'<div><span style="{key_style}">{key}</span>: ')

                if isinstance(value, (list, tuple)) or self._is_array_like(value):
                    html.append(self._generate_list_html(
                        value, False, "default", None, nesting_level=nesting_level + 1
                    ))
                elif isinstance(value, dict):
                    html.append(self._generate_dict_html(value, nesting_level + 1))
                else:
                    html.append(str(value))

                html.append('</div>')

            html.append('</div>')
            return ''.join(html)

        except ColorError:
            raise
        except Exception as e:
            raise DictError(f"Failed to generate HTML for dictionary: {str(e)}")

    @staticmethod
    def _lighten_color(color: str, factor: float = 0.5) -> str:
        """
        Lighten a hex color by the given factor.
        
        Args:
            color: Hex color string (#RRGGBB)
            factor: Factor to lighten (0-1, where 1 is white)
            
        Returns:
            Lightened hex color
            
        Raises:
            ColorError: If color processing fails
        """
        try:
            # Handle colors with or without #
            if color.startswith('#'):
                color = color[1:]

            # Handle both 3 and 6 digit hex
            if len(color) == 3:
                r = int(color[0] + color[0], 16)
                g = int(color[1] + color[1], 16)
                b = int(color[2] + color[2], 16)
            elif len(color) == 6:
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
            else:
                raise ColorError(color_value=color, message=f"Invalid hex color format: {color}")

            # Lighten
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)

            # Convert back to hex
            return f"#{r:02x}{g:02x}{b:02x}"

        except ValueError as e:
            raise ColorError(color_value=color, message=f"Invalid color value: {color}") from e
        except Exception as e:
            raise ColorError(color_value=color, message=f"Error processing color: {str(e)}") from e

    def display(self, items: Union[List, Tuple, Any], *,
                ordered: bool = False, style: str = 'default',
                item_style: Optional[str] = None,
                matrix_mode: Optional[bool] = None,
                nesting_colors: Optional[List[str]] = None,
                **inline_styles) -> None:
        """
        Display a list, tuple, or array-like object as an HTML list or matrix.
        
        Args:
            items: The list, tuple, or array-like object to display
            ordered: If True, use an ordered list (<ol>), otherwise unordered (<ul>)
            style: Named style for the list container
            item_style: Optional custom CSS style for list items
            matrix_mode: Force matrix display mode for 2D arrays (default: auto-detect)
            nesting_colors: Optional list of colors to use for different nesting levels
            **inline_styles: Additional CSS styles to apply to list items
            
        Raises:
            ListError: If the input cannot be displayed as a list
            StyleNotFoundError: If the specified style is not found
            ColorError: If color validation fails
            DisplayEnvironmentError: If display environment is not available
            InvalidParameterError: If invalid parameters are provided
        """
        try:
            self._validate_and_set_nesting_colors(nesting_colors)
            display_items = self._prepare_items_for_display(items)
            is_matrix = self._determine_matrix_mode(display_items, matrix_mode)
            html_content = self._generate_appropriate_html(display_items, is_matrix, ordered, style, item_style,
                                                           **inline_styles)
            self._display_html(html_content, display_items)
        except (ListError, StyleNotFoundError, ColorError, DisplayEnvironmentError, InvalidParameterError):
            raise
        except Exception as e:
            raise ListError(f"Error displaying list: {str(e)}")

    def _validate_and_set_nesting_colors(self, nesting_colors: Optional[List[str]]) -> None:
        """
        Validate and set nesting colors if provided.
        
        Args:
            nesting_colors: Optional list of colors to use for different nesting levels
            
        Raises:
            InvalidParameterError: If nesting_colors is not a list
            ColorError: If any color in the list is invalid
        """
        if not nesting_colors:
            return

        if not isinstance(nesting_colors, list):
            raise InvalidParameterError("nesting_colors", "a list of color strings",
                                        received=type(nesting_colors).__name__)

        for color in nesting_colors:
            if not isinstance(color, str):
                raise ColorError(color_value=str(color),
                                 message=f"Invalid color in nesting_colors: {color}")

        self.nesting_colors = nesting_colors

    def _prepare_items_for_display(self, items: Union[List, Tuple, Any]) -> Union[List, Tuple]:
        """
        Convert input to a displayable list format.
        
        Args:
            items: The list, tuple, or array-like object to display
            
        Returns:
            Converted list or tuple ready for display
            
        Raises:
            ListError: If the input cannot be converted or is invalid
            ContentTypeError: If the input is of an incompatible type
        """
        try:
            display_items = self._convert_to_list(items)
            return display_items
        except ArrayConversionError as e:
            # Provide more helpful error message
            raise ListError(f"Failed to convert array-like object to displayable format: {str(e)}. "
                           f"The object type '{type(items).__name__}' is supported but an error occurred during conversion.")
        except Exception as e:
            raise ListError(f"Unable to display object of type '{type(items).__name__}': {str(e)}")

    def _determine_matrix_mode(self, items: Union[List, Tuple], matrix_mode: Optional[bool]) -> bool:
        """
        Determine if the items should be displayed as a matrix.
        
        Args:
            items: The list or tuple to display
            matrix_mode: Force matrix display mode if provided
            
        Returns:
            Boolean indicating whether to use matrix display mode
        """
        return matrix_mode if matrix_mode is not None else self._is_matrix(items)

    def _generate_appropriate_html(self, items: Union[List, Tuple], is_matrix: bool,
                                   ordered: bool, style: str, item_style: Optional[str],
                                   **inline_styles) -> str:
        """
        Generate the appropriate HTML based on whether the display is a matrix or list.
        
        Args:
            items: The list or tuple to display
            is_matrix: Whether to display as a matrix
            ordered: If True, use an ordered list (<ol>), otherwise unordered (<ul>)
            style: Named style for the list container
            item_style: Optional custom CSS style for list items
            **inline_styles: Additional CSS styles to apply to list items
            
        Returns:
            Generated HTML content
        """
        if is_matrix:
            return self._generate_matrix_html(items, style, **inline_styles)
        else:
            return self._generate_list_html(items, ordered, style, item_style, **inline_styles)

    @staticmethod
    def _display_html(html_content: str, items: Union[List, Tuple]) -> None:
        """
        Display HTML content safely, with fallback.
        
        Args:
            html_content: HTML content to display
            items: Original list/tuple (for fallback)
            
        Raises:
            IPythonNotAvailableError: If IPython environment is not detected
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. List will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render HTML content: {str(e)}")


class DictDisplayer(Displayer):
    """Displays Python dictionaries as HTML definition lists or tables."""

    def _generate_dict_html_dl(self, data: Dict, style: str,
                               key_style: Optional[str], value_style: Optional[str],
                               **inline_styles) -> str:
        """
        Recursively generate HTML definition list for a dictionary.
        
        Args:
            data: The dictionary to display
            style: Base style name for the list container
            key_style: Optional custom CSS for keys (<dt>)
            value_style: Optional custom CSS for values (<dd>)
            **inline_styles: Additional inline styles for list items
        
        Returns:
            HTML string for the definition list
        """
        dl_style = self.styles.get(style, self.styles['default'])
        html = [f'<dl style="{dl_style}">']

        inline_style_string = self._process_inline_styles(inline_styles)
        final_key_style = key_style if key_style else "font-weight: bold;"
        final_value_style = value_style if value_style else "margin-left: 20px;"

        if inline_style_string:
            final_key_style = f"{final_key_style}; {inline_style_string}".strip('; ')
            final_value_style = f"{final_value_style}; {inline_style_string}".strip('; ')

        for key, value in data.items():
            key_content = str(key)
            value_content = ""

            if isinstance(value, dict):
                # Recursively handle nested dictionaries
                value_content = self._generate_dict_html_dl(value, style, key_style, value_style, **inline_styles)
            elif isinstance(value, (list, tuple)):
                # Delegate nested lists to ListDisplayer (if available)
                # For simplicity here, we'll just convert to string
                value_content = str(value)  # Placeholder - ideally use ListDisplayer
            else:
                value_content = str(value)

            html.append(f'<dt style="{final_key_style}">{key_content}</dt>')
            html.append(f'<dd style="{final_value_style}">{value_content}</dd>')

        html.append('</dl>')
        return ''.join(html)

    def display(self, data: Dict, *, style: str = 'default',
                key_style: Optional[str] = None,
                value_style: Optional[str] = None,
                **inline_styles) -> None:
        """
        Display a dictionary as an HTML definition list.
        
        Args:
            data: The dictionary to display
            style: Named style for the definition list container
            key_style: Optional custom CSS style for keys (<dt>)
            value_style: Optional custom CSS style for values (<dd>)
            **inline_styles: Additional CSS styles to apply to list items
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")

        html_content = self._generate_dict_html_dl(data, style, key_style, value_style, **inline_styles)
        self._display_html(html_content, data)

    @staticmethod
    def _display_html(html_content: str, data: Dict) -> None:
        """
        Display HTML content safely, with fallback.
        
        Args:
            html_content: HTML content to display
            data: Original dictionary (for fallback)
            
        Raises:
            IPythonNotAvailableError: If IPython environment is not detected
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. Dictionary will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render dictionary HTML: {str(e)}") from e


class MermaidDisplayer(Displayer):
    """Displays Mermaid diagrams using the Mermaid JavaScript library."""

    def display(self, diagram: str, *, 
                style: str = 'default', 
                theme: str = 'default',
                custom_css: Optional[Dict[str, str]] = None,
                **inline_styles) -> None:
        """
        Display a Mermaid diagram.
        
        Args:
            diagram: The Mermaid diagram definition/code or a file path
            style: Named style from the available styles
            theme: Mermaid theme ('default', 'forest', 'dark', 'neutral')
            custom_css: Optional dictionary mapping Mermaid CSS selectors to style properties
            **inline_styles: Additional CSS styles to apply to the container
            
        Raises:
            MermaidError: If there's an issue with the diagram
            StyleNotFoundError: If specified style is not found
            InvalidParameterError: If invalid parameters are provided
            DisplayEnvironmentError: If display environment is not available
            DisplayMethodError: If there's an issue with the display method
        """
        try:
            # Check if diagram is a file path and attempt to read from file
            diagram_content = self._read_diagram_from_path_or_use_directly(diagram)
            
            if not isinstance(diagram_content, str):
                received_type = type(diagram_content).__name__
                raise MermaidError(f"Diagram must be a string, received {received_type}")

            if style not in self.styles:
                raise StyleNotFoundError(style_name=style)
                
            if theme not in ['default', 'forest', 'dark', 'neutral']:
                raise InvalidParameterError("theme", 
                                        "one of: 'default', 'forest', 'dark', 'neutral'", 
                                        received=theme)

            base_style = self.styles.get(style)
            inline_style_string = self._process_inline_styles(inline_styles)
            container_style = f"{base_style} {inline_style_string}" if inline_style_string else base_style
            
            # Create HTML with Mermaid diagram
            html_content = self._generate_mermaid_html(diagram_content, container_style, theme, custom_css)
            
            # Display the diagram
            self._display_html(html_content)
        except (MermaidError, StyleNotFoundError, InvalidParameterError, 
                DisplayEnvironmentError, HTMLGenerationError, ConversionError):
            # Pass through specific exceptions
            raise
        except Exception as e:
            # Wrap other exceptions with DisplayMethodError
            raise DisplayMethodError(
                method_name="display_mermaid", 
                message=f"Error displaying Mermaid diagram: {str(e)}"
            )
    
    @staticmethod
    def _read_diagram_from_path_or_use_directly(diagram_input: str) -> str:
        """
        Check if input is a file path and read content if it is.
        
        Args:
            diagram_input: Either a Mermaid diagram string or a file path
            
        Returns:
            The Mermaid diagram content
            
        Raises:
            MermaidError: If there's an issue reading the file
        """
        # Skip empty strings
        if not diagram_input or not diagram_input.strip():
            return diagram_input
            
        # Check if diagram looks like a file path
        if (diagram_input.endswith('.md') or 
            diagram_input.endswith('.mmd') or 
            diagram_input.endswith('.mermaid') or
            ('/' in diagram_input or '\\' in diagram_input)):
            try:
                with open(diagram_input, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                # If it looks like a file path but reading fails, assume it's either
                # a diagram with slashes, or raise an error if it clearly ends with a file extension
                if (diagram_input.endswith('.md') or 
                    diagram_input.endswith('.mmd') or 
                    diagram_input.endswith('.mermaid')):
                    raise MermaidError(f"Failed to read Mermaid diagram from file: {diagram_input}. Error: {str(e)}")
                # Otherwise, treat it as a diagram string
                return diagram_input
        
        # If not a file path, return the original string
        return diagram_input

    def _generate_mermaid_html(self, diagram: str, container_style: str, theme: str, 
                               custom_css: Optional[Dict[str, str]] = None) -> str:
        """
        Generate HTML for displaying a Mermaid diagram.
        
        Args:
            diagram: The Mermaid diagram definition/code
            container_style: CSS style for the container
            theme: Mermaid theme
            custom_css: Optional dictionary mapping Mermaid CSS selectors to style properties
            
        Returns:
            HTML content string
        """
        diagram_id = f"mermaid_{str(uuid.uuid4()).replace('-', '')}"
        
        # Prepare custom CSS if provided
        custom_css_string = ""
        if custom_css and isinstance(custom_css, dict):
            css_rules = []
            for selector, properties in custom_css.items():
                # Add a proper prefix for the current diagram if it doesn't already target .mermaid
                if not selector.startswith('.mermaid'):
                    prefixed_selector = f"#{diagram_id} {selector}"
                else:
                    prefixed_selector = f"#{diagram_id}{selector[8:]}"
                
                css_rules.append(f"{prefixed_selector} {{ {properties} }}")
            
            custom_css_string = f"<style>{' '.join(css_rules)}</style>"
        
        html = f"""
        <div style="{container_style}">
            {custom_css_string}
            <div class="mermaid" id="{diagram_id}">
            {diagram}
            </div>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
            <script>
                // Initialize Mermaid with specified theme
                mermaid.initialize({{ startOnLoad: true, theme: '{theme}' }});
                mermaid.run();
            </script>
        </div>
        """
        return html

    @staticmethod
    def _display_html(html_content: str) -> None:
        """
        Display HTML content safely.
        
        Args:
            html_content: HTML content to display
            
        Raises:
            IPythonNotAvailableError: If IPython environment is not detected
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. Mermaid diagram will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render Mermaid diagram: {str(e)}")


class ProgressDisplayer(Displayer):
    """Displays customizable progress bars using JavaScript or SVG."""

    def __init__(self, styles: Dict[str, str]):
        """Initialize a progress displayer with styles."""
        super().__init__(styles)

    def display(self, total: Optional[int] = None, *,
                desc: str = "",
                style: str = "default",
                color: str = "#3498DB",
                height: str = "20px",
                animated: bool = True,
                **inline_styles) -> str:
        """
        Display a progress bar with either determined or undetermined progress.
        
        Args:
            total: Total number of steps (None for undetermined progress)
            desc: Description text to display with the progress bar
            style: Named style from available styles
            color: Color of the progress bar
            height: Height of the progress bar
            animated: Whether to animate the progress bar
            **inline_styles: Additional CSS styles to apply
            
        Returns:
            Progress bar ID that can be used to update the progress
        """
        # Generate a unique ID for this progress bar
        progress_id = f"progress_{str(uuid.uuid4()).replace('-', '')}"
        container_id = f"container_{progress_id}"

        # Process styles
        base_style = self.styles.get(style, self.styles['default'])
        inline_style_string = self._process_inline_styles(inline_styles)

        # Create the progress bar HTML
        if total is None:
            # Undetermined progress (loading animation)
            html_content = self._create_undetermined_progress(
                progress_id, container_id, desc, base_style,
                inline_style_string, color, height, animated
            )
        else:
            # Determined progress (with total)
            html_content = self._create_determined_progress(
                progress_id, container_id, desc, base_style,
                inline_style_string, color, height, animated, total
            )

        # Display the progress bar
        self._display_html(html_content)

        return progress_id

    @staticmethod
    def update(progress_id: str, value: int, total: Optional[int] = None) -> None:
        """
        Update the progress of a displayed progress bar.
        
        Args:
            progress_id: ID of the progress bar to update
            value: Current progress value
            total: Optional new total (if changed)
            
        Raises:
            DisplayUpdateError: If update fails
            IPythonNotAvailableError: If IPython environment is not detected
        """
        # Validate inputs
        if not isinstance(progress_id, str):
            raise InvalidParameterError("progress_id", "string", received=type(progress_id).__name__)

        if not isinstance(value, int):
            raise InvalidParameterError("value", "integer", received=type(value).__name__)

        if total is not None and not isinstance(total, int):
            raise InvalidParameterError("total", "integer or None", received=type(total).__name__)

        # Create JavaScript to update the progress
        if total is not None:
            if value >= total:  # Check if complete
                # For completed progress, stop any animation and show 100%
                js_code = f"""
                (function() {{
                    var progressBar = document.getElementById('{progress_id}');
                    var container = document.getElementById('container_{progress_id}');
                    if (progressBar) {{
                        // Handle both determined and undetermined progress bars
                        if (progressBar.tagName === 'PROGRESS') {{
                            progressBar.max = {total};
                            progressBar.value = {value};
                            var label = document.getElementById('label_{progress_id}');
                            if (label) {{
                                label.textContent = '100%';
                            }}
                        }} else {{
                            // This is an undetermined progress bar, replace with completed state
                            progressBar.style.animation = 'none';
                            progressBar.style.background = '#27AE60';  // Success green color
                            var label = document.createElement('span');
                            label.textContent = 'Complete';
                            label.style.position = 'absolute';
                            label.style.top = '50%';
                            label.style.left = '50%';
                            label.style.transform = 'translate(-50%, -50%)';
                            label.style.color = 'white';
                            label.style.fontWeight = 'bold';
                            label.style.fontSize = '12px';
                            progressBar.appendChild(label);
                        }}
                    }}
                }})();
                """
            else:
                # Regular update with new total
                js_code = f"""
                (function() {{
                    var progressBar = document.getElementById('{progress_id}');
                    if (progressBar) {{
                        progressBar.max = {total};
                        progressBar.value = {value};
                        var percent = Math.round(({value} / {total}) * 100);
                        var label = document.getElementById('label_{progress_id}');
                        if (label) {{
                            label.textContent = percent + '%';
                        }}
                    }}
                }})();
                """
        else:
            # Regular update without changing total
            js_code = f"""
            (function() {{
                var progressBar = document.getElementById('{progress_id}');
                if (progressBar) {{
                    progressBar.value = {value};
                    var percent = Math.round(({value} / progressBar.max) * 100);
                    var label = document.getElementById('label_{progress_id}');
                    if (label) {{
                        label.textContent = percent + '%';
                    }}
                }}
            }})();
            """

        try:
            ip_display(Javascript(js_code))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. Progress update will not be applied."
            )
        except Exception as e:
            raise DisplayUpdateError(
                element_id=progress_id,
                message=f"Failed to update progress bar: {str(e)}"
            ) from e

    @staticmethod
    def _create_determined_progress(progress_id: str, container_id: str,
                                    desc: str, base_style: str, inline_style_string: str,
                                    color: str, height: str, animated: bool, total: int) -> str:
        """
        Create HTML for a determined progress bar.
        
        Args:
            progress_id: Unique ID for the progress element
            container_id: Unique ID for the container element
            desc: Description text
            base_style: Base CSS style
            inline_style_string: Additional inline CSS
            color: Progress bar color
            height: Progress bar height
            animated: Whether to animate
            total: Total number of steps
            
        Returns:
            HTML string for the progress bar
        """
        # Define CSS styles
        container_style = f"display: flex; align-items: center; margin: 10px 0; {base_style}"
        if inline_style_string:
            container_style = f"{container_style}; {inline_style_string}"

        desc_style = "margin-right: 10px; min-width: 120px; color: #3498DB;"
        progress_container_style = "flex-grow: 1; position: relative; height: 100%;"
        progress_style = f"""
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: {height};
            border: none;
            border-radius: 4px;
            background-color: #f0f0f0;
        """

        progress_value_style = f"""
            ::-webkit-progress-value {{
                background-color: {color};
                border-radius: 4px;
                transition: width 0.3s ease;
            }}
            ::-moz-progress-bar {{
                background-color: {color};
                border-radius: 4px;
                transition: width 0.3s ease;
            }}
        """

        label_style = """
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 12px;
            font-weight: bold;
            color: #333;
            text-shadow: 0 0 2px white, 0 0 2px white, 0 0 2px white, 0 0 2px white;
        """

        # Build HTML
        html = f"""
        <div id="{container_id}" style="{container_style}">
            <span style="{desc_style}">{desc}</span>
            <div style="{progress_container_style}">
                <progress id="{progress_id}" value="0" max="{total}" style="{progress_style}"></progress>
                <style>{progress_value_style}</style>
                <span id="label_{progress_id}" style="{label_style}">0%</span>
            </div>
        </div>
        """

        return html

    def _create_undetermined_progress(self, progress_id: str, container_id: str,
                                      desc: str, base_style: str, inline_style_string: str,
                                      color: str, height: str, animated: bool) -> str:
        """
        Create HTML for an undetermined progress bar (loading animation).
        
        Args:
            progress_id: Unique ID for the progress element
            container_id: Unique ID for the container element
            desc: Description text
            base_style: Base CSS style
            inline_style_string: Additional inline CSS
            color: Progress bar color
            height: Progress bar height
            animated: Whether to animate
            
        Returns:
            HTML string for the progress bar
        """
        # Define CSS styles
        container_style = f"display: flex; align-items: center; margin: 10px 0; {base_style}"
        if inline_style_string:
            container_style = f"{container_style}; {inline_style_string}"

        desc_style = "margin-right: 10px; min-width: 120px; color: #3498DB;"
        progress_container_style = "flex-grow: 1; position: relative; height: 100%;"

        # More elegant gradient with lighter colors for better visual effect
        lighter_color = self._lighten_color(color, 0.7)
        mid_color = self._lighten_color(color, 0.4)

        loading_style = f"""
            width: 100%;
            height: {height};
            position: relative;
            background: linear-gradient(90deg, 
                {lighter_color} 0%, 
                {color} 25%, 
                {mid_color} 50%, 
                {color} 75%, 
                {lighter_color} 100%);
            background-size: 400% 100%;
            border-radius: 4px;
            animation: loading_{progress_id} 2s ease infinite;
            overflow: hidden;
        """

        animation_style = f"""
            @keyframes loading_{progress_id} {{
                0% {{
                    background-position: 100% 50%;
                }}
                100% {{
                    background-position: 0% 50%;
                }}
            }}
        """

        shine_effect = f"""
            position: absolute;
            content: '';
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(255,255,255,0.3), 
                transparent);
            animation: shine_{progress_id} 1.5s infinite;
        """

        shine_animation = f"""
            @keyframes shine_{progress_id} {{
                0% {{
                    transform: translateX(-100%);
                }}
                100% {{
                    transform: translateX(100%);
                }}
            }}
        """

        # Build HTML with a more structured approach that's easier to modify via JS
        html = f"""
        <div id="{container_id}" style="{container_style}">
            <span style="{desc_style}">{desc}</span>
            <div style="{progress_container_style}">
                <div id="{progress_id}" style="{loading_style}">
                    <div style="{shine_effect}"></div>
                </div>
                <style>
                    {animation_style}
                    {shine_animation}
                </style>
            </div>
        </div>
        """

        return html

    @staticmethod
    def _display_html(html_content: str) -> None:
        """
        Display HTML content safely.
        
        Args:
            html_content: HTML content to display
            
        Raises:
            IPythonNotAvailableError: If IPython environment is not detected
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            ip_display(HTML(html_content))
        except NameError:
            raise IPythonNotAvailableError(
                "IPython environment not detected. Progress bar will not be rendered properly."
            )
        except Exception as e:
            raise HTMLRenderingError(f"Failed to render progress bar HTML: {str(e)}") from e

    @staticmethod
    def _lighten_color(color: str, factor: float = 0.5) -> str:
        """
        Lighten a hex color by the given factor.
        
        Args:
            color: Hex color string (#RRGGBB)
            factor: Factor to lighten (0-1, where 1 is white)
            
        Returns:
            Lightened hex color
        """
        # Handle colors with or without #
        if color.startswith('#'):
            color = color[1:]

        # Handle both 3 and 6 digit hex
        if len(color) == 3:
            r = int(color[0] + color[0], 16)
            g = int(color[1] + color[1], 16)
            b = int(color[2] + color[2], 16)
        else:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)

        # Lighten
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)

        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"


class Printer:
    """
    Main class for displaying text, tables, and DataFrames with stylized HTML.
    
    This class provides a unified interface for all display operations,
    delegating to specialized displayers for each type of content.
    """

    def __init__(self, additional_styles: Optional[Dict[str, str]] = None):
        """
        Initialize the printer with default and optional additional styles.
        
        Args:
            additional_styles: Optional dictionary of additional styles to add
            
        Raises:
            StyleError: If there's an issue with the provided styles
        """
        try:
            # Set up styles with defaults and any additional styles
            self.styles = DEFAULT_THEMES.copy()
            # Add special styles
            self.styles.update(SPECIAL_STYLES)
            if additional_styles:
                if not isinstance(additional_styles, dict):
                    raise StyleError(f"additional_styles must be a dictionary, got {type(additional_styles).__name__}")
                self.styles.update(additional_styles)

            # Create displayers for different content types
            self.text_displayer = TextDisplayer(self.styles)
            self.code_displayer = CodeDisplayer(self.styles)
            self.table_displayer = TableDisplayer(self.styles)
            self.list_displayer = ListDisplayer(self.styles)
            self.dict_displayer = DictDisplayer(self.styles)
            self.progress_displayer = ProgressDisplayer(self.styles)
            self.mermaid_displayer = MermaidDisplayer(self.styles)
        except Exception as e:
            raise ColabPrintError(f"Error initializing Printer: {str(e)}")

    def display(self, text: str, *, style: str = 'default', **inline_styles) -> None:
        """
        Display text with the specified styling.
        
        Args:
            text: Text to display
            style: Named style from available styles
            **inline_styles: Additional CSS styles to apply
            
        Raises:
            TextError: If text is not a string
            StyleNotFoundError: If specified style is not found
            StyleParsingError: If there's an error parsing inline styles
            DisplayEnvironmentError: If display environment is not available
        """
        try:
            # Validate inputs
            if not isinstance(text, str):
                raise TextError(f"Text must be a string, received {type(text).__name__}")

            if style not in self.styles:
                available_styles = ', '.join(list(self.styles.keys())[:10]) + "..." if len(
                    self.styles) > 10 else ', '.join(self.styles.keys())
                raise StyleNotFoundError(style_name=style,
                                         message=f"Style '{style}' not found. Available styles: {available_styles}")

            self.text_displayer.display(text, style=style, **inline_styles)
        except (TextError, StyleNotFoundError, StyleParsingError, DisplayEnvironmentError) as e:
            # Pass through known exceptions
            raise
        except Exception as e:
            # Wrap unknown exceptions
            raise TextError(f"Error displaying text: {str(e)}") from e

    def display_table(self, headers: List[str], rows: List[List[Any]], *,
                      style: str = 'default', **table_options) -> None:
        """
        Display a table with the given headers and rows.
        
        Args:
            headers: List of column headers
            rows: List of rows, each row being a list of cell values
            style: Named style from available styles
            **table_options: Additional table styling options
            
        Raises:
            TableError: If there's an issue with the table data
            StyleNotFoundError: If specified style is not found
            DisplayEnvironmentError: If display environment is not available
        """
        try:
            # Validate input
            if not isinstance(headers, list):
                raise TableError(f"Headers must be a list, got {type(headers).__name__}")

            if not isinstance(rows, list):
                raise TableError(f"Rows must be a list, got {type(rows).__name__}")

            for i, row in enumerate(rows):
                if not isinstance(row, list):
                    raise TableError(f"Row {i} must be a list, got {type(row).__name__}")

            self.table_displayer.display(headers, rows, style=style, **table_options)
        except (TableError, StyleNotFoundError, DisplayEnvironmentError) as e:
            # Pass through known exceptions
            raise
        except Exception as e:
            # Wrap unknown exceptions
            raise TableError(f"Error displaying table: {str(e)}")

    def display_df(self, df: pd.DataFrame, *,
                   style: str = 'default',
                   max_rows: Optional[int] = None,
                   max_cols: Optional[int] = None,
                   precision: int = 2,
                   header_style: Optional[str] = None,
                   odd_row_style: Optional[str] = None,
                   even_row_style: Optional[str] = None,
                   index: bool = True,
                   width: str = '100%',
                   caption: Optional[str] = None,
                   highlight_cols: Optional[Union[List, Dict]] = None,
                   highlight_rows: Optional[Union[List, Dict]] = None,
                   highlight_cells: Optional[Dict] = None,
                   **inline_styles) -> None:
        """
        Display a pandas DataFrame with customizable styling.
        
        Args:
            df: DataFrame to display
            style: Named style from available styles
            max_rows: Maximum number of rows to display
            max_cols: Maximum number of columns to display
            precision: Decimal precision for float values
            header_style: Custom CSS for header cells
            odd_row_style: Custom CSS for odd rows
            even_row_style: Custom CSS for even rows
            index: Whether to show DataFrame index
            width: Table width (CSS value)
            caption: Table caption
            highlight_cols: Columns to highlight (list) or {col: style} mapping
            highlight_rows: Rows to highlight (list) or {row: style} mapping
            highlight_cells: Cell coordinates to highlight {(row, col): style}
            **inline_styles: Additional CSS styles for all cells
            
        Raises:
            DataFrameError: If df is not a pandas DataFrame or there's an issue with the data
            StyleNotFoundError: If specified style is not found
            InvalidParameterError: If invalid parameters are provided
            DisplayEnvironmentError: If display environment is not available
        """
        try:
            # Check if pandas is available
            if 'pandas.core.frame.DataFrame' not in str(type(df)):
                raise DataFrameError("The 'df' parameter must be a pandas DataFrame")

            # Validate numeric parameters
            if max_rows is not None and not isinstance(max_rows, int):
                raise InvalidParameterError("max_rows", "integer", received=type(max_rows).__name__)

            if max_cols is not None and not isinstance(max_cols, int):
                raise InvalidParameterError("max_cols", "integer", received=type(max_cols).__name__)

            if not isinstance(precision, int):
                raise InvalidParameterError("precision", "integer", received=type(precision).__name__)

            # Create the displayer and use it
            displayer = DFDisplayer(self.styles, df)
            displayer.display(
                style=style,
                max_rows=max_rows,
                max_cols=max_cols,
                precision=precision,
                header_style=header_style,
                odd_row_style=odd_row_style,
                even_row_style=even_row_style,
                index=index,
                width=width,
                caption=caption,
                highlight_cols=highlight_cols,
                highlight_rows=highlight_rows,
                highlight_cells=highlight_cells,
                **inline_styles
            )
        except (DataFrameError, StyleNotFoundError, InvalidParameterError, DisplayEnvironmentError) as e:
            # Pass through known exceptions
            raise
        except Exception as e:
            # Wrap unknown exceptions
            raise DataFrameError(f"Error displaying DataFrame: {str(e)}")

    def display_list(self, items: Union[List, Tuple, Any], *,
                     ordered: bool = False, style: str = 'default',
                     item_style: Optional[str] = None,
                     matrix_mode: Optional[bool] = None,
                     nesting_colors: Optional[List[str]] = None,
                     **inline_styles) -> None:
        """
        Display a list or tuple as an HTML list.

        Args:
            items: The list, tuple, or array-like object to display
            ordered: If True, use an ordered list (<ol>), otherwise unordered (<ul>)
            style: Named style for the list container
            item_style: Optional custom CSS style for list items
            matrix_mode: Force matrix display mode for 2D arrays (default: auto-detect)
            nesting_colors: Optional list of colors to use for different nesting levels
            **inline_styles: Additional CSS styles to apply to list items
            
        Raises:
            ListError: If there's an issue with the list data
            StyleNotFoundError: If specified style is not found
            InvalidParameterError: If invalid parameters are provided
            ColorError: If color validation fails
            DisplayEnvironmentError: If display environment is not available
        """
        try:
            self.list_displayer.display(
                items,
                ordered=ordered,
                style=style,
                item_style=item_style,
                matrix_mode=matrix_mode,
                nesting_colors=nesting_colors,
                **inline_styles
            )
        except (ListError, StyleNotFoundError, InvalidParameterError, ColorError, DisplayEnvironmentError) as e:
            # Pass through known exceptions
            raise
        except Exception as e:
            # Wrap unknown exceptions
            raise ListError(f"Error displaying list: {str(e)}")

    def display_dict(self, data: Dict, *, style: str = 'default',
                     key_style: Optional[str] = None,
                     value_style: Optional[str] = None,
                     **inline_styles) -> None:
        """
        Display a dictionary as an HTML definition list.
        
        Args:
            data: The dictionary to display
            style: Named style for the definition list container
            key_style: Optional custom CSS style for keys (<dt>)
            value_style: Optional custom CSS style for values (<dd>)
            **inline_styles: Additional CSS styles to apply to list items
            
        Raises:
            DictError: If data is not a dictionary or there's an issue with the dictionary
            StyleNotFoundError: If specified style is not found
            DisplayEnvironmentError: If display environment is not available
        """
        try:
            if not isinstance(data, dict):
                raise DictError(f"Input must be a dictionary, got {type(data).__name__}")

            self.dict_displayer.display(
                data,
                style=style,
                key_style=key_style,
                value_style=value_style,
                **inline_styles
            )
        except (DictError, StyleNotFoundError, DisplayEnvironmentError) as e:
            # Pass through known exceptions
            raise
        except Exception as e:
            # Wrap unknown exceptions
            raise DictError(f"Error displaying dictionary: {str(e)}")

    def display_mermaid(self, diagram: str, *, 
                       style: str = 'default', 
                       theme: str = 'default',
                       custom_css: Optional[Dict[str, str]] = None,
                       **inline_styles) -> None:
        """
        Display a Mermaid diagram.
        
        Args:
            diagram: Mermaid diagram definition or file path to a Mermaid diagram file
            style: Named style from available styles for the container
            theme: Mermaid theme ('default', 'forest', 'dark', 'neutral')
            custom_css: Optional dictionary mapping Mermaid CSS selectors to style properties
            **inline_styles: Additional CSS styles to apply to the container
            
        Raises:
            MermaidError: If there's an issue with the diagram or diagram file
            StyleNotFoundError: If specified style is not found
            DisplayEnvironmentError: If display environment is not available
            InvalidParameterError: If theme is not valid
            
        Examples:
            # Display a Mermaid diagram from a string
            printer.display_mermaid('''
            graph TD;
                A-->B;
                A-->C;
                B-->D;
                C-->D;
            ''')
            
            # Display a Mermaid diagram from a file
            printer.display_mermaid('path/to/diagram.mmd', theme='dark')
            
            # Apply custom CSS styles to Mermaid elements
            printer.display_mermaid(diagram, custom_css={
                '.node rect': 'fill: #f9f9f9; stroke: #333; stroke-width: 2px;',
                '.edgeLabel': 'background-color: white; padding: 2px;'
            })
        """
        self.mermaid_displayer.display(
            diagram,
            style=style,
            theme=theme,
            custom_css=custom_css,
            **inline_styles
        )

    def add_style(self, name: str, style_definition: str) -> None:
        """
        Add a new style to the available styles.
        
        Args:
            name: Name of the style
            style_definition: CSS style string
            
        Raises:
            InvalidParameterError: If parameters are invalid
            StyleError: If there's an issue with the style definition
        """
        try:
            if not isinstance(name, str):
                raise InvalidParameterError("name", "string", received=type(name).__name__)

            if not isinstance(style_definition, str):
                raise InvalidParameterError("style_definition", "string", received=type(style_definition).__name__)

            if name in self.styles:
                warnings.warn(f"Overwriting existing style: {name}")

            self.styles[name] = style_definition
        except InvalidParameterError:
            raise
        except Exception as e:
            raise StyleError(f"Error adding style: {str(e)}") from e

    def get_available_styles(self) -> List[str]:
        """
        Get a list of available style names.
        
        Returns:
            List of style names
        """
        return list(self.styles.keys())

    def create_styled_display(self, style: str, **default_styles) -> Callable[[str], None]:
        """
        Create a reusable display function with predefined style settings.
        
        This method returns a callable function that applies the specified 
        style and default inline styles to any text passed to it.
        
        Args:
            style: Named style from available styles
            **default_styles: Default inline CSS styles to apply
            
        Returns:
            A callable function that displays text with predefined styling
            
        Raises:
            StyleNotFoundError: If specified style is not found
            StyleError: If there's an issue with the style settings
            
        Example:
            # Create a header display function
            header = printer.create_styled_display('header')
            
            # Use it multiple times
            header("First Section")
            header("Second Section")
            
            # Create with overrides
            alert = printer.create_styled_display('error', font_weight='bold')
            
            # Override inline styles at call time
            header("Custom Header", color="#FF5722")
        """
        if style not in self.styles:
            raise StyleNotFoundError(style_name=style)

        def styled_display(text: str, **override_styles) -> None:
            # Merge default_styles with any override_styles
            combined_styles = default_styles.copy()
            combined_styles.update(override_styles)

            # Call the regular display method with the combined styles
            self.display(text, style=style, **combined_styles)

        return styled_display

    def display_progress(self, total: Optional[int] = None, *,
                         desc: str = "",
                         style: str = "default",
                         color: str = "#3498DB",
                         height: str = "20px",
                         animated: bool = True,
                         **inline_styles) -> str:
        """
        Display a progress bar with either determined or undetermined progress.
        
        Args:
            total: Total number of steps (None for undetermined progress)
            desc: Description text to display with the progress bar
            style: Named style from available styles
            color: Color of the progress bar
            height: Height of the progress bar
            animated: Whether to animate the progress bar
            **inline_styles: Additional CSS styles to apply
            
        Returns:
            Progress bar ID that can be used to update the progress
            
        Raises:
            ProgressError: If there's an issue with the progress bar
            StyleNotFoundError: If specified style is not found
            ColorError: If color validation fails
            DisplayEnvironmentError: If display environment is not available
            InvalidParameterError: If any parameter is invalid
        """
        try:
            # Validate parameters
            if total is not None and not isinstance(total, int):
                raise InvalidParameterError("total", "integer or None", received=type(total).__name__)

            if not isinstance(desc, str):
                raise InvalidParameterError("desc", "string", received=type(desc).__name__)

            if not isinstance(color, str):
                raise InvalidParameterError("color", "string", received=type(color).__name__)

            if not isinstance(height, str):
                raise InvalidParameterError("height", "string", received=type(height).__name__)

            if not isinstance(animated, bool):
                raise InvalidParameterError("animated", "boolean", received=type(animated).__name__)

            # Validate style exists
            if style not in self.styles:
                available_styles = ', '.join(list(self.styles.keys())[:10]) + "..." if len(
                    self.styles) > 10 else ', '.join(self.styles.keys())
                raise StyleNotFoundError(style_name=style,
                                         message=f"Style '{style}' not found. Available styles: {available_styles}")

            # Validate color format (basic check)
            if color.startswith('#') and not (len(color) == 7 or len(color) == 4):
                raise ColorError(color_value=color, message=f"Invalid hex color format: {color}")

            return self.progress_displayer.display(
                total=total,
                desc=desc,
                style=style,
                color=color,
                height=height,
                animated=animated,
                **inline_styles
            )
        except (InvalidParameterError, StyleNotFoundError, ColorError, DisplayEnvironmentError) as e:
            # Pass through known exceptions
            raise
        except Exception as e:
            # Wrap unknown exceptions
            raise ProgressError(f"Error displaying progress bar: {str(e)}") from e

    def update_progress(self, progress_id: str, value: int, total: Optional[int] = None) -> None:
        """
        Update the progress of a displayed progress bar.
        
        Args:
            progress_id: ID of the progress bar to update
            value: Current progress value
            total: Optional new total (if changed)
            
        Raises:
            DisplayUpdateError: If update fails
            InvalidParameterError: If parameters are invalid
            IPythonNotAvailableError: If IPython environment is not detected
        """
        try:
            if not isinstance(progress_id, str):
                raise InvalidParameterError("progress_id", "string", received=type(progress_id).__name__)

            if not isinstance(value, int):
                raise InvalidParameterError("value", "integer", received=type(value).__name__)

            if total is not None and not isinstance(total, int):
                raise InvalidParameterError("total", "integer or None", received=type(total).__name__)

            if value < 0:
                raise InvalidParameterError("value", "positive integer", received=str(value))

            if total is not None and total <= 0:
                raise InvalidParameterError("total", "positive integer", received=str(total))

            self.progress_displayer.update(progress_id, value, total)
        except (InvalidParameterError, DisplayUpdateError, IPythonNotAvailableError):
            raise
        except Exception as e:
            raise DisplayUpdateError(element_id=progress_id, message=f"Failed to update progress bar: {str(e)}") from e

    def display_code(self, code: str, *,
                style: str = 'code_block',
                highlighting_mode: str = 'block',
                background_color: Optional[str] = None,
                prompt_style: Optional[str] = None,
                **inline_styles) -> None:
        """
        Display code with syntax highlighting and prompt formatting.
        
        Args:
            code: Code to display
            style: Named style from available styles
            highlighting_mode: 'block' for indentation-based coloring or 'gradient' for gradient coloring
            background_color: Optional background color override
            prompt_style: Optional style for prompt markers
            **inline_styles: Additional CSS styles to apply
            
        Raises:
            CodeError: If code is not a string or other code display issues occur
            StyleNotFoundError: If specified style is not found
            StyleParsingError: If there's an error parsing inline styles
            CodeParsingError: If there's an error parsing the code
            SyntaxHighlightingError: If there's an error applying syntax highlighting
            HTMLRenderingError: If HTML content cannot be rendered
        """
        try:
            # Validate inputs
            if not isinstance(code, str):
                raise CodeError(f"Code must be a string, received {type(code).__name__}")

            if style not in self.styles:
                available_styles = ', '.join(list(self.styles.keys())[:10]) + "..." if len(
                    self.styles) > 10 else ', '.join(self.styles.keys())
                raise StyleNotFoundError(style_name=style,
                                        message=f"Style '{style}' not found. Available styles: {available_styles}")

            self.code_displayer.display(
                code, 
                style=style, 
                highlighting_mode=highlighting_mode,
                background_color=background_color,
                prompt_style=prompt_style,
                **inline_styles
            )
        except (CodeError, StyleNotFoundError, StyleParsingError, DisplayEnvironmentError) as e:
            # Pass through known exceptions
            raise
        except Exception as e:
            # Wrap unknown exceptions
            raise CodeError(f"Error displaying code: {str(e)}") from e


# Add a function to check if we're in an IPython environment
def is_in_notebook() -> bool:
    """
    Check if code is running inside an IPython/Jupyter notebook.
    
    Returns:
        True if in a notebook, False otherwise
    """
    try:
        from IPython import get_ipython
        if get_ipython() is None:
            return False
        if 'IPKernelApp' not in get_ipython().config:
            return False
        return True
    except ImportError:
        return False


P = Printer()


# Text display shortcuts - primary display styles
def header(text: str, **override_styles) -> None:
    """
    Display text as a prominent header with top/bottom borders.
    
    Args:
        text: Text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='header', **override_styles)


def title(text: str, **override_styles) -> None:
    """
    Display text as a large centered title.
    
    Args:
        text: Text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='title', **override_styles)


def subtitle(text: str, **override_styles) -> None:
    """
    Display text as a medium-sized subtitle with italic styling.
    
    Args:
        text: Text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='subtitle', **override_styles)


def section_divider(text: str, **override_styles) -> None:
    """
    Display text as a section divider with bottom border.
    
    Args:
        text: Text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='section_divider', **override_styles)


def subheader(text: str, **override_styles) -> None:
    """
    Display text as a subheading with left accent border.
    
    Args:
        text: Text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='subheader', **override_styles)


# Content display shortcuts - specialized content formatting
def code(text: str, **override_styles) -> None:
    """
    Display text as a code block with monospaced font, background, and syntax highlighting.
    
    Args:
        text: Code text to display
        **override_styles: Override any CSS style properties or configure highlighting options
    """
    P.display_code(text, style='code_block', **override_styles)


def card(text: str, **override_styles) -> None:
    """
    Display text in a card-like container with shadow and border.
    
    Args:
        text: Text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='card', **override_styles)


def quote(text: str, **override_styles) -> None:
    """
    Display text as a block quote with left border.
    
    Args:
        text: Quote text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='quote', **override_styles)


def badge(text: str, **override_styles) -> None:
    """
    Display text as a small rounded badge/label.
    
    Args:
        text: Short text to display as badge
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='badge', **override_styles)


def data_highlight(text: str, **override_styles) -> None:
    """
    Display text with emphasis suitable for important data points.
    
    Args:
        text: Data or numeric value to highlight
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='data_highlight', **override_styles)


def footer(text: str, **override_styles) -> None:
    """
    Display text as a footer with top border.
    
    Args:
        text: Footer text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='footer', **override_styles)


# Status/context display shortcuts - convey information status
def highlight(text: str, **override_styles) -> None:
    """
    Display text with standout styling to draw attention.
    
    Args:
        text: Text to highlight
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='highlight', **override_styles)


def info(text: str, **override_styles) -> None:
    """
    Display text as informational content with blue styling.
    
    Args:
        text: Informational text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='info', **override_styles)


def success(text: str, **override_styles) -> None:
    """
    Display text as a success message with green styling.
    
    Args:
        text: Success message to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='success', **override_styles)


def warning(text: str, **override_styles) -> None:
    """
    Display text as a warning notification with orange styling.
    
    Args:
        text: Warning message to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='warning', **override_styles)


def error(text: str, **override_styles) -> None:
    """
    Display text as an error message with red styling.
    
    Args:
        text: Error message to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='error', **override_styles)


def muted(text: str, **override_styles) -> None:
    """
    Display text with de-emphasized styling for secondary content.
    
    Args:
        text: Text to display with reduced emphasis
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='muted', **override_styles)


def primary(text: str, **override_styles) -> None:
    """
    Display text with primary styling for important content.
    
    Args:
        text: Primary text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='primary', **override_styles)


def secondary(text: str, **override_styles) -> None:
    """
    Display text with secondary styling for supporting content.
    
    Args:
        text: Secondary text to display
        **override_styles: Override any CSS style properties
    """
    P.display(text, style='secondary', **override_styles)


# Container display shortcuts - for structured data
def dfd(df: pd.DataFrame, **display_options) -> None:
    """
    Display a pandas DataFrame with enhanced styling.
    
    Args:
        df: DataFrame to display
        **display_options: DataFrame display options (max_rows, max_cols, etc.)
    """
    style_options = {'style': 'df'}
    display_options = {**style_options, **display_options}
    P.display_df(df, **display_options)


def table(headers: List[str], rows: List[List[Any]], **table_options) -> None:
    """
    Display data as a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of rows, each row being a list of cell values
        **table_options: Table styling options
    """
    style_options = {'style': 'table'}
    table_options = {**style_options, **table_options}
    P.display_table(headers, rows, **table_options)


def list_(items: Union[List, Tuple], **list_options) -> None:
    """
    Display a list with enhanced styling.
    
    Args:
        items: List or tuple of items to display
        **list_options: List display options (ordered, item_style, etc.)
    """
    style_options = {'style': 'list'}
    list_options = {**style_options, **list_options}
    P.display_list(items, **list_options)


def dict_(data: Dict, **dict_options) -> None:
    """
    Display a dictionary with enhanced styling.
    
    Args:
        data: Dictionary to display
        **dict_options: Dictionary display options (key_style, value_style, etc.)
    """
    style_options = {'style': 'dict'}
    dict_options = {**style_options, **dict_options}
    P.display_dict(data, **dict_options)


def progress(iterable=None, *,
             total: Optional[int] = None,
             desc: str = "",
             style: str = "progress",
             color: str = "#3498DB",
             height: str = "20px",
             animated: bool = True,
             **inline_styles) -> Union[str, Any]:
    """
    Display a progress bar with either determined or undetermined progress.
    
    This function can be used in two ways:
    1. As a direct progress bar creator (returns progress_id)
    2. As an iterable wrapper like tqdm (returns a generator that updates progress)
    
    Args:
        iterable: Optional iterable to track progress over (list, tuple, etc.)
        total: Total number of steps or length of iterable if not provided
        desc: Description text to display with the progress bar
        style: Named style from available styles
        color: Color of the progress bar
        height: Height of the progress bar
        animated: Whether to animate the progress bar
        **inline_styles: Additional CSS styles to apply
        
    Returns:
        If iterable is None: Progress bar ID that can be used with P.update_progress()
        If iterable is provided: Generator that yields items and updates progress automatically
    """
    if iterable is not None:
        # Use as a tqdm-like wrapper
        return _progress_iter(iterable, total=total, desc=desc, style=style,
                             color=color, height=height, animated=animated,
                             **inline_styles)

    # Use as a direct progress bar creator
    return P.display_progress(
        total=total,
        desc=desc,
        style=style,
        color=color,
        height=height,
        animated=animated,
        **inline_styles
    )


def _progress_iter(iterable, *,
                  total: Optional[int] = None,
                  desc: str = "",
                  style: str = "progress",
                  color: str = "#3498DB",
                  height: str = "20px",
                  animated: bool = True,
                  **inline_styles) -> Any:
    # Determine total if not provided
    if total is None:
        try:
            total = len(iterable)
        except (TypeError, AttributeError):
            # If length cannot be determined, use undetermined progress
            progress_id = P.display_progress(
                total=None,
                desc=desc,
                style=style,
                color=color,
                height=height,
                animated=animated,
                **inline_styles
            )

            # Yield items with undetermined progress
            try:
                for i, item in enumerate(iterable):
                    yield item

                # When finished, show as complete
                P.update_progress(progress_id, 100, 100)
            except Exception as e:
                # Ensure progress is finalized even if iteration fails
                P.update_progress(progress_id, 100, 100)
                raise

            return

    # Create progress bar
    progress_id = P.display_progress(
        total=total,
        desc=desc,
        style=style,
        color=color,
        height=height,
        animated=animated,
        **inline_styles
    )

    # Yield items while updating progress
    i = 0
    try:
        for i, item in enumerate(iterable):
            P.update_progress(progress_id, i + 1, total)
            yield item
    except Exception as e:
        # Ensure the progress bar shows the error state
        P.update_progress(progress_id, i + 1, total)  # Show partial completion
        raise


def mermaid(diagram: str, *,
           theme: str = 'default',
           style: str = 'default',
           custom_css: Optional[Dict[str, str]] = None,
           **inline_styles) -> None:
    """
    Display a Mermaid diagram with optional custom styling.
    
    Args:
        diagram: Mermaid diagram definition or file path to a Mermaid diagram file
        theme: Mermaid theme ('default', 'forest', 'dark', 'neutral')
        style: Named style for the container from available styles
        custom_css: Optional dictionary mapping Mermaid CSS selectors to style properties
        **inline_styles: Additional CSS styles to apply to the container
        
    Examples:
        # Display a simple diagram
        mermaid('''
        graph TD;
            A-->B;
            A-->C;
            B-->D;
            C-->D;
        ''')
        
        # Read from a file
        mermaid('diagrams/flow.mmd', theme='dark')
        
        # Apply custom CSS
        mermaid(diagram, custom_css={
            '.node rect': 'fill: #f9f9f9; stroke: #333; stroke-width: 2px;',
            '.edgeLabel': 'background-color: white; padding: 2px;'
        })
    """
    P = Printer()
    P.display_mermaid(diagram, style=style, theme=theme, custom_css=custom_css, **inline_styles)
