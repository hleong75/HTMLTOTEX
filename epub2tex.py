#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB to LaTeX Converter
Ultra-puissant et robuste convertisseur EPUB vers LaTeX avec préservation du style

This script converts EPUB files to LaTeX format while preserving:
- Document structure (chapters, sections, subsections)
- Text formatting (bold, italic, underline, etc.)
- Lists (ordered and unordered)
- Tables
- Images
- Links and references
- Special characters

Usage:
    python epub2tex.py input.epub [output.tex]
"""

import os
import sys
import re
import zipfile
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil

try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    print("Error: Required libraries not installed.")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


class EPUBToLaTeXConverter:
    """
    Ultra-robust EPUB to LaTeX converter with style preservation.
    """
    
    def __init__(self, epub_path: str, output_path: Optional[str] = None):
        """
        Initialize the converter.
        
        Args:
            epub_path: Path to the input EPUB file
            output_path: Path to the output LaTeX file (optional)
        """
        self.epub_path = epub_path
        self.output_path = output_path or self._default_output_path()
        self.book = None
        self.images = {}
        self.image_counter = 0
        self.output_dir = Path(self.output_path).parent
        self.images_dir = self.output_dir / "images"
        
        # LaTeX special characters mapping
        self.latex_special_chars = {
            '\\': r'\textbackslash{}',
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }
        
        # HTML to LaTeX formatting mapping
        self.format_mapping = {
            'b': ('\\textbf{', '}'),
            'strong': ('\\textbf{', '}'),
            'i': ('\\textit{', '}'),
            'em': ('\\emph{', '}'),
            'u': ('\\underline{', '}'),
            'code': ('\\texttt{', '}'),
            'tt': ('\\texttt{', '}'),
            'small': ('{\\small ', '}'),
            'sub': ('$_{\\text{', '}}$'),
            'sup': ('$^{\\text{', '}}$'),
            'del': ('\\sout{', '}'),
            'strike': ('\\sout{', '}'),
        }
    
    def _default_output_path(self) -> str:
        """Generate default output path based on input filename."""
        base = os.path.splitext(self.epub_path)[0]
        return f"{base}.tex"
    
    def _escape_latex(self, text: str) -> str:
        """
        Escape special LaTeX characters in text.
        
        Args:
            text: Input text string
            
        Returns:
            Escaped LaTeX-safe string
        """
        for char, replacement in self.latex_special_chars.items():
            text = text.replace(char, replacement)
        return text
    
    def _extract_images(self):
        """Extract and save images from EPUB file."""
        if not self.images_dir.exists():
            self.images_dir.mkdir(parents=True, exist_ok=True)
        
        for item in self.book.get_items_of_type(ebooklib.ITEM_IMAGE):
            img_name = item.get_name()
            # Create a clean filename
            img_filename = f"image_{self.image_counter}_{Path(img_name).name}"
            self.image_counter += 1
            
            # Save image
            img_path = self.images_dir / img_filename
            with open(img_path, 'wb') as f:
                f.write(item.get_content())
            
            # Store mapping
            self.images[img_name] = img_filename
    
    def _convert_heading(self, tag: Tag) -> str:
        """
        Convert HTML heading tags to LaTeX sections.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX section command
        """
        level_map = {
            'h1': 'chapter',
            'h2': 'section',
            'h3': 'subsection',
            'h4': 'subsubsection',
            'h5': 'paragraph',
            'h6': 'subparagraph',
        }
        
        level = tag.name.lower()
        latex_cmd = level_map.get(level, 'section')
        # Process only the children, not the tag itself to avoid recursion
        content = ''.join(self._convert_element(child, inline=True) for child in tag.children)
        
        return f"\\{latex_cmd}{{{content}}}\n\n"
    
    def _convert_paragraph(self, tag: Tag) -> str:
        """
        Convert HTML paragraph to LaTeX.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX paragraph
        """
        # Process only the children, not the tag itself
        content = ''.join(self._convert_element(child, inline=True) for child in tag.children)
        if not content.strip():
            return ""
        return f"{content}\n\n"
    
    def _convert_list(self, tag: Tag) -> str:
        """
        Convert HTML list (ul/ol) to LaTeX itemize/enumerate.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX list environment
        """
        list_type = 'enumerate' if tag.name == 'ol' else 'itemize'
        result = f"\\begin{{{list_type}}}\n"
        
        for item in tag.find_all('li', recursive=False):
            # Process only the children of each list item
            content = ''.join(self._convert_element(child, inline=True) for child in item.children)
            result += f"    \\item {content}\n"
        
        result += f"\\end{{{list_type}}}\n\n"
        return result
    
    def _convert_table(self, tag: Tag) -> str:
        """
        Convert HTML table to LaTeX tabular.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX table environment
        """
        # Find all rows
        rows = tag.find_all('tr')
        if not rows:
            return ""
        
        # Determine number of columns
        first_row = rows[0]
        cols = len(first_row.find_all(['td', 'th']))
        
        if cols == 0:
            return ""
        
        # Create table
        col_format = '|' + 'l|' * cols
        result = "\\begin{table}[h]\n\\centering\n"
        result += f"\\begin{{tabular}}{{{col_format}}}\n"
        result += "\\hline\n"
        
        for i, row in enumerate(rows):
            cells = row.find_all(['td', 'th'])
            cell_contents = []
            for cell in cells:
                # Process children of each cell
                content = ''.join(self._convert_element(child, inline=True) for child in cell.children).strip()
                cell_contents.append(content)
            
            result += " & ".join(cell_contents) + " \\\\\n"
            result += "\\hline\n"
        
        result += "\\end{tabular}\n\\end{table}\n\n"
        return result
    
    def _convert_image(self, tag: Tag) -> str:
        """
        Convert HTML image to LaTeX figure.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX figure environment
        """
        src = tag.get('src', '')
        alt = tag.get('alt', '')
        
        # Clean up image path
        src = src.split('/')[-1] if '/' in src else src
        
        # Find image in our mapping
        img_filename = None
        for orig_name, mapped_name in self.images.items():
            if src in orig_name or orig_name.endswith(src):
                img_filename = mapped_name
                break
        
        if not img_filename:
            return f"% Image not found: {src}\n"
        
        result = "\\begin{figure}[h]\n"
        result += "\\centering\n"
        result += f"\\includegraphics[max width=\\textwidth]{{images/{img_filename}}}\n"
        if alt:
            escaped_alt = self._escape_latex(alt)
            result += f"\\caption{{{escaped_alt}}}\n"
        result += "\\end{figure}\n\n"
        
        return result
    
    def _convert_link(self, tag: Tag) -> str:
        """
        Convert HTML link to LaTeX hyperlink.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX hyperlink
        """
        href = tag.get('href', '')
        # Process children of link
        text = ''.join(self._convert_element(child, inline=True) for child in tag.children)
        
        if not href:
            return text
        
        # External links
        if href.startswith('http://') or href.startswith('https://'):
            return f"\\href{{{href}}}{{{text}}}"
        # Internal references
        else:
            return text  # Simplified for internal links
    
    def _convert_blockquote(self, tag: Tag) -> str:
        """
        Convert HTML blockquote to LaTeX quote environment.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX quote environment
        """
        # Process children of blockquote
        content = ''.join(self._convert_element(child, inline=False) for child in tag.children)
        return f"\\begin{{quote}}\n{content}\\end{{quote}}\n\n"
    
    def _convert_pre_code(self, tag: Tag) -> str:
        """
        Convert HTML pre/code blocks to LaTeX verbatim.
        
        Args:
            tag: BeautifulSoup tag object
            
        Returns:
            LaTeX verbatim environment
        """
        content = tag.get_text()
        return f"\\begin{{verbatim}}\n{content}\\end{{verbatim}}\n\n"
    
    def _convert_div_span(self, tag: Tag, inline: bool = False) -> str:
        """
        Convert HTML div/span containers.
        
        Args:
            tag: BeautifulSoup tag object
            inline: Whether to process as inline content
            
        Returns:
            Converted LaTeX content
        """
        # Process children only
        return ''.join(self._convert_element(child, inline=inline) for child in tag.children)
    
    def _convert_element(self, element, inline: bool = False) -> str:
        """
        Recursively convert HTML element to LaTeX.
        
        Args:
            element: BeautifulSoup element (Tag or NavigableString)
            inline: Whether to process as inline content
            
        Returns:
            Converted LaTeX string
        """
        # Handle text nodes
        if isinstance(element, NavigableString):
            text = str(element)
            # Clean up whitespace
            if inline:
                text = re.sub(r'\s+', ' ', text)
            return self._escape_latex(text)
        
        # Handle tag elements
        if not isinstance(element, Tag):
            return ""
        
        tag_name = element.name.lower()
        
        # Handle different tag types
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            return self._convert_heading(element)
        
        elif tag_name == 'p':
            return self._convert_paragraph(element)
        
        elif tag_name in ['ul', 'ol']:
            return self._convert_list(element)
        
        elif tag_name == 'table':
            return self._convert_table(element)
        
        elif tag_name == 'img':
            return self._convert_image(element)
        
        elif tag_name == 'a':
            return self._convert_link(element)
        
        elif tag_name == 'blockquote':
            return self._convert_blockquote(element)
        
        elif tag_name in ['pre', 'code'] and tag_name == 'pre':
            return self._convert_pre_code(element)
        
        elif tag_name == 'br':
            return "\\\\\n" if inline else "\n"
        
        elif tag_name == 'hr':
            return "\\noindent\\rule{\\textwidth}{0.4pt}\n\n"
        
        elif tag_name in ['div', 'span', 'section', 'article']:
            return self._convert_div_span(element, inline=inline)
        
        # Handle inline formatting
        elif tag_name in self.format_mapping:
            start, end = self.format_mapping[tag_name]
            content = ''.join(self._convert_element(child, inline=True) 
                            for child in element.children)
            return f"{start}{content}{end}"
        
        # Default: process children
        else:
            result = ""
            for child in element.children:
                result += self._convert_element(child, inline=inline)
            return result
    
    def _convert_html_to_latex(self, html_content: str) -> str:
        """
        Convert HTML content to LaTeX.
        
        Args:
            html_content: HTML string
            
        Returns:
            LaTeX string
        """
        # Suppress XML/HTML parser warning
        import warnings
        from bs4 import XMLParsedAsHTMLWarning
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Find body content
        body = soup.find('body')
        if not body:
            body = soup
        
        return self._convert_element(body, inline=False)
    
    def _get_metadata(self) -> Dict[str, str]:
        """
        Extract metadata from EPUB file.
        
        Returns:
            Dictionary with title, author, etc.
        """
        metadata = {
            'title': 'Untitled',
            'author': 'Unknown',
            'date': '',
        }
        
        # Get title
        title = self.book.get_metadata('DC', 'title')
        if title:
            metadata['title'] = self._escape_latex(title[0][0])
        
        # Get author
        creators = self.book.get_metadata('DC', 'creator')
        if creators:
            authors = [self._escape_latex(c[0]) for c in creators]
            metadata['author'] = ', '.join(authors)
        
        # Get date
        date = self.book.get_metadata('DC', 'date')
        if date:
            metadata['date'] = self._escape_latex(date[0][0])
        
        return metadata
    
    def _generate_preamble(self, metadata: Dict[str, str]) -> str:
        """
        Generate LaTeX preamble with packages and settings.
        
        Args:
            metadata: Document metadata
            
        Returns:
            LaTeX preamble string
        """
        preamble = r"""\documentclass[12pt,a4paper]{book}

% Encoding and fonts
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}

% Language support
\usepackage[french,english]{babel}

% Graphics and images
\usepackage{graphicx}
\usepackage{float}

% Page layout
\usepackage[margin=2.5cm]{geometry}

% Colors and hyperlinks
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    pdfauthor={""" + metadata['author'] + r"""},
    pdftitle={""" + metadata['title'] + r"""}
}

% Tables
\usepackage{booktabs}
\usepackage{tabularx}

% Lists
\usepackage{enumitem}

% Typography
\usepackage{microtype}
\usepackage{setspace}
\setstretch{1.2}

% Strikethrough
\usepackage[normalem]{ulem}

% Title information
\title{""" + metadata['title'] + r"""}
\author{""" + metadata['author'] + r"""}
"""
        
        if metadata['date']:
            preamble += r"\date{" + metadata['date'] + "}\n"
        else:
            preamble += r"\date{\today}" + "\n"
        
        preamble += r"""
\begin{document}

\maketitle
\tableofcontents
\clearpage

"""
        return preamble
    
    def _generate_epilogue(self) -> str:
        """
        Generate LaTeX epilogue.
        
        Returns:
            LaTeX epilogue string
        """
        return "\n\\end{document}\n"
    
    def convert(self) -> bool:
        """
        Perform the EPUB to LaTeX conversion.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Reading EPUB file: {self.epub_path}")
            self.book = epub.read_epub(self.epub_path)
            
            print("Extracting images...")
            self._extract_images()
            
            print("Extracting metadata...")
            metadata = self._get_metadata()
            
            print("Converting content to LaTeX...")
            latex_content = self._generate_preamble(metadata)
            
            # Process all document items
            for item in self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                html_content = item.get_content().decode('utf-8', errors='ignore')
                
                # Convert HTML to LaTeX
                latex_text = self._convert_html_to_latex(html_content)
                latex_content += latex_text
            
            latex_content += self._generate_epilogue()
            
            print(f"Writing LaTeX file: {self.output_path}")
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            print(f"\n✓ Conversion successful!")
            print(f"  Output: {self.output_path}")
            if self.images:
                print(f"  Images: {len(self.images)} images extracted to {self.images_dir}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error during conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point for the converter."""
    parser = argparse.ArgumentParser(
        description='Convert EPUB files to LaTeX format with style preservation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python epub2tex.py book.epub
  python epub2tex.py book.epub output.tex
  python epub2tex.py --help

The converter will:
  - Preserve document structure (chapters, sections)
  - Convert formatting (bold, italic, underline)
  - Handle lists, tables, images, and links
  - Extract images to an 'images' subdirectory
  - Generate clean, readable LaTeX code
        """
    )
    
    parser.add_argument(
        'epub_file',
        help='Path to the input EPUB file'
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Path to the output LaTeX file (optional, defaults to input filename with .tex extension)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='EPUB to LaTeX Converter v1.0'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.isfile(args.epub_file):
        print(f"Error: File not found: {args.epub_file}")
        sys.exit(1)
    
    # Create converter and run
    converter = EPUBToLaTeXConverter(args.epub_file, args.output_file)
    success = converter.convert()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
