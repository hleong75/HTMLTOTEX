#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of the EPUB to LaTeX converter
"""

import os
import sys

def main():
    """Demonstrate converter usage"""
    
    print("=" * 60)
    print("EPUB to LaTeX Converter - Usage Examples")
    print("=" * 60)
    print()
    
    print("1. Basic conversion (auto-generated output filename):")
    print("   python epub2tex.py book.epub")
    print()
    
    print("2. Custom output filename:")
    print("   python epub2tex.py book.epub my_document.tex")
    print()
    
    print("3. After conversion, compile the LaTeX file:")
    print("   pdflatex my_document.tex")
    print("   pdflatex my_document.tex  # Run twice for TOC")
    print()
    
    print("4. Or use XeLaTeX (recommended for UTF-8):")
    print("   xelatex my_document.tex")
    print("   xelatex my_document.tex")
    print()
    
    print("=" * 60)
    print("Features:")
    print("=" * 60)
    print("✓ Preserves document structure (chapters, sections)")
    print("✓ Converts formatting (bold, italic, underline, etc.)")
    print("✓ Handles lists (ordered and unordered)")
    print("✓ Converts tables with proper LaTeX formatting")
    print("✓ Extracts and includes images")
    print("✓ Creates hyperlinks from HTML links")
    print("✓ Escapes special LaTeX characters")
    print("✓ Generates professional LaTeX preamble")
    print("✓ Automatic table of contents")
    print()
    
    print("=" * 60)
    print("Generated LaTeX includes:")
    print("=" * 60)
    print("- UTF-8 encoding support")
    print("- French and English language support")
    print("- Professional typography (microtype)")
    print("- Hyperlinks with colors")
    print("- Image support with graphicx")
    print("- Professional tables with booktabs")
    print("- And more...")
    print()
    
    # Check if we're in the right directory
    if os.path.exists('epub2tex.py'):
        print("=" * 60)
        print("Quick Start:")
        print("=" * 60)
        
        if os.path.exists('sample.epub'):
            print("Sample EPUB file detected!")
            print()
            print("Run this command to test:")
            print("  python epub2tex.py sample.epub")
            print()
        else:
            print("To create a sample EPUB for testing:")
            print("  python create_sample_epub.py")
            print()
            print("Then convert it:")
            print("  python epub2tex.py sample.epub")
            print()
    
    print("For more information, see README.md")
    print()

if __name__ == '__main__':
    main()
