#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example demonstrating CSS class attribute support in EPUB to LaTeX conversion
"""

from epub2tex import EPUBToLaTeXConverter
import os

def main():
    """Demonstrate class attribute conversion"""
    
    print("=" * 60)
    print("CSS Class Attribute Support - Example")
    print("=" * 60)
    print()
    
    # Check if test EPUB exists
    if not os.path.exists('class_test.epub'):
        print("Creating test EPUB with class attributes...")
        import create_class_test_epub
        create_class_test_epub.create_class_test_epub()
        print()
    
    # Convert EPUB to LaTeX
    input_file = 'class_test.epub'
    output_file = 'class_test_example.tex'
    
    print(f"Converting {input_file} to {output_file}...")
    print()
    
    converter = EPUBToLaTeXConverter(input_file, output_file)
    
    if converter.convert():
        print()
        print("✓ Conversion successful!")
        print()
        print("The following CSS classes were converted:")
        print()
        
        # Read output and show examples
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        examples = [
            ("important", "\\textbf{\\large", "Important text (bold, large)"),
            ("note", "\\textcolor{blue}", "Note text (blue, italic)"),
            ("warning", "\\textcolor{red}", "Warning text (red, bold)"),
            ("code-inline", "\\texttt{", "Inline code (monospace)"),
            ("author-note", "{\\small\\itshape", "Author note (small, italic)"),
            ("done", "\\textcolor{green}", "Done item (green)"),
            ("pending", "\\textcolor{orange}", "Pending item (orange)"),
            ("todo", "\\textcolor{gray}", "Todo item (gray)"),
            ("highlight", "\\begin{shadedquotation}", "Highlight block (shaded box)"),
            ("info", "\\begin{mdframed}", "Info box (framed)"),
            ("highlight-row", "\\rowcolor{highlightyellow}", "Table row highlight"),
            ("epigraph", "{\\itshape", "Epigraph quote (italic)"),
        ]
        
        found = []
        not_found = []
        
        for class_name, latex_marker, description in examples:
            if latex_marker in content:
                found.append(f"  ✓ {class_name:15} → {description}")
            else:
                not_found.append(f"  ✗ {class_name:15} → {description}")
        
        if found:
            print("Classes found and converted:")
            for item in found:
                print(item)
        
        if not_found:
            print()
            print("Classes not found in output:")
            for item in not_found:
                print(item)
        
        print()
        print(f"View the output file: {output_file}")
        print()
        print("You can compile it with:")
        print(f"  pdflatex {output_file}")
        print()
    else:
        print("✗ Conversion failed")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
