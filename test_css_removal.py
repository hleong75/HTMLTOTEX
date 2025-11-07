#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify that CSS styles are properly removed from output
"""

import os
import sys
import tempfile
from pathlib import Path
from ebooklib import epub

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub2tex import EPUBToLaTeXConverter


def create_test_epub_with_css():
    """Create a simple EPUB with CSS styles for testing"""
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('test-css-epub-456')
    book.set_title('Test CSS Removal')
    book.set_language('fr')
    book.add_author('Test Author')
    
    # Create chapter with CSS in head and body
    chapter = epub.EpubHtml(
        title='Test Chapter',
        file_name='chap_01.xhtml',
        lang='fr'
    )
    chapter.content = '''
    <html>
    <head>
        <title>Test Chapter</title>
        <style type="text/css">
            body {
                font-family: Arial, sans-serif;
                color: #333;
                background-color: #f0f0f0;
            }
            .highlight {
                background-color: yellow;
                padding: 10px;
            }
        </style>
        <link rel="stylesheet" href="styles.css" />
    </head>
    <body>
        <h1>Chapter Title</h1>
        <p style="color: red; font-size: 18px;">Paragraph with inline style</p>
        <style>
            /* Style block in body - should also be removed */
            .body-style {
                margin: 20px;
            }
        </style>
        <p>Another paragraph</p>
        <div class="highlight">
            <p>Highlighted text</p>
        </div>
    </body>
    </html>
    '''
    book.add_item(chapter)
    
    # Add navigation
    book.toc = (epub.Link('chap_01.xhtml', 'Test Chapter', 'chapter1'),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    book.spine = ['nav', chapter]
    
    # Write EPUB
    epub_path = '/tmp/test_css_removal.epub'
    epub.write_epub(epub_path, book)
    
    return epub_path


def test_css_removal():
    """Test that CSS styles are completely removed from output"""
    print("Creating test EPUB with CSS styles...")
    epub_path = create_test_epub_with_css()
    
    try:
        # Convert to LaTeX
        output_path = '/tmp/test_css_removal_output.tex'
        converter = EPUBToLaTeXConverter(epub_path, output_path)
        success = converter.convert()
        
        if not success:
            print("✗ Conversion failed")
            return False
        
        # Read output file
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # List of CSS-related strings that should NOT appear in output
        css_strings = [
            'font-family',
            'background-color',
            'Arial',
            'sans-serif',
            '.highlight',
            '.body-style',
            'padding:',
            'margin:',
            'color: #333',
            'color: red',
            'font-size: 18px',
        ]
        
        failed_checks = []
        for css_str in css_strings:
            if css_str in content:
                failed_checks.append(css_str)
        
        if failed_checks:
            print("✗ Found CSS content in output:")
            for css_str in failed_checks:
                print(f"  - '{css_str}'")
            return False
        
        # Verify that actual content is still present
        required_content = [
            'Chapter Title',
            'Paragraph with inline style',
            'Another paragraph',
            'Highlighted text',
        ]
        
        missing_content = []
        for content_str in required_content:
            if content_str not in content:
                missing_content.append(content_str)
        
        if missing_content:
            print("✗ Missing required content:")
            for content_str in missing_content:
                print(f"  - '{content_str}'")
            return False
        
        print("✓ CSS styles are properly removed!")
        print("  - No CSS properties in output")
        print("  - Content is preserved")
        
        return True
        
    finally:
        # Clean up
        if os.path.exists(epub_path):
            os.remove(epub_path)
        if os.path.exists(output_path):
            os.remove(output_path)


def main():
    """Run the test"""
    print("=" * 60)
    print("Testing CSS Removal")
    print("=" * 60)
    print()
    
    try:
        if test_css_removal():
            print()
            print("✓ All tests passed!")
            return 0
        else:
            print()
            print("✗ Test failed")
            return 1
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
