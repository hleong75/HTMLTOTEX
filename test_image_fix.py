#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify that includegraphics syntax is correct
"""

import os
import sys
import tempfile
from pathlib import Path
from PIL import Image
from ebooklib import epub

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub2tex import EPUBToLaTeXConverter


def create_test_epub_with_image():
    """Create a simple EPUB with an image for testing"""
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('test-image-epub-123')
    book.set_title('Test Image EPUB')
    book.set_language('en')
    book.add_author('Test Author')
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_path = '/tmp/test_image.jpg'
    img.save(img_path, 'JPEG')
    
    # Add image to EPUB
    with open(img_path, 'rb') as f:
        img_content = f.read()
    
    epub_image = epub.EpubImage()
    epub_image.file_name = 'test_image.jpg'
    epub_image.content = img_content
    book.add_item(epub_image)
    
    # Create chapter with image
    chapter = epub.EpubHtml(
        title='Test Chapter',
        file_name='chap_01.xhtml',
        lang='en'
    )
    chapter.content = '''
    <html>
    <head><title>Test Chapter</title></head>
    <body>
        <h1>Test Image</h1>
        <p>This chapter contains an image:</p>
        <img src="test_image.jpg" alt="Test Image"/>
        
        <h2>Test Figure</h2>
        <figure>
            <img src="test_image.jpg"/>
            <figcaption>This is a test figure caption</figcaption>
        </figure>
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
    epub_path = '/tmp/test_image.epub'
    epub.write_epub(epub_path, book)
    
    # Clean up temp image
    os.remove(img_path)
    
    return epub_path


def test_image_syntax():
    """Test that image conversion uses correct LaTeX syntax"""
    print("Creating test EPUB with image...")
    epub_path = create_test_epub_with_image()
    
    try:
        # Convert to LaTeX
        output_path = '/tmp/test_image_output.tex'
        converter = EPUBToLaTeXConverter(epub_path, output_path)
        success = converter.convert()
        
        if not success:
            print("✗ Conversion failed")
            return False
        
        # Read output file
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for incorrect syntax (should not exist)
        if 'max width=' in content:
            print("✗ Found incorrect 'max width=' syntax in output")
            print("  This should have been 'width='")
            return False
        
        # Check for correct syntax
        if '\\includegraphics[width=\\textwidth]' not in content:
            print("✗ Could not find correct '\\includegraphics[width=\\textwidth]' syntax")
            print("  Checking what was generated:")
            for line in content.split('\n'):
                if 'includegraphics' in line:
                    print(f"  Found: {line.strip()}")
            return False
        
        # Count occurrences (should be 2: one for <img> and one for <figure>)
        count = content.count('\\includegraphics[width=\\textwidth]')
        if count != 2:
            print(f"✗ Expected 2 occurrences of includegraphics, found {count}")
            return False
        
        print(f"✓ Image syntax is correct!")
        print(f"  Found {count} correct \\includegraphics[width=\\textwidth] commands")
        
        return True
        
    finally:
        # Clean up
        if os.path.exists(epub_path):
            os.remove(epub_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        # Clean up images directory
        import shutil
        images_dir = '/tmp/images'
        if os.path.exists(images_dir):
            shutil.rmtree(images_dir)


def main():
    """Run the test"""
    print("=" * 60)
    print("Testing Image LaTeX Syntax Fix")
    print("=" * 60)
    print()
    
    try:
        if test_image_syntax():
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
