#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify that images use proper float positioning [htbp]
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


def create_test_epub_with_images():
    """Create a simple EPUB with images for testing positioning"""
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('test-image-pos-789')
    book.set_title('Test Image Positioning')
    book.set_language('en')
    book.add_author('Test Author')
    
    # Create a test image
    img = Image.new('RGB', (150, 100), color='red')
    img_path = '/tmp/test_pos_image.jpg'
    img.save(img_path, 'JPEG')
    
    # Add image to EPUB
    with open(img_path, 'rb') as f:
        img_content = f.read()
    
    epub_image = epub.EpubImage()
    epub_image.file_name = 'test_pos_image.jpg'
    epub_image.content = img_content
    book.add_item(epub_image)
    
    # Create chapter with images
    chapter = epub.EpubHtml(
        title='Test Chapter',
        file_name='chap_01.xhtml',
        lang='en'
    )
    chapter.content = '''
    <html>
    <head><title>Test Chapter</title></head>
    <body>
        <h1>Test Image Positioning</h1>
        <p>Image using img tag:</p>
        <img src="test_pos_image.jpg" alt="Test with img tag"/>
        
        <p>Image using figure tag:</p>
        <figure>
            <img src="test_pos_image.jpg"/>
            <figcaption>Test with figure tag</figcaption>
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
    epub_path = '/tmp/test_image_positioning.epub'
    epub.write_epub(epub_path, book)
    
    # Clean up temp image
    os.remove(img_path)
    
    return epub_path


def test_image_positioning():
    """Test that images use [htbp] positioning instead of [h]"""
    print("Creating test EPUB with images...")
    epub_path = create_test_epub_with_images()
    
    try:
        # Convert to LaTeX
        output_path = '/tmp/test_image_positioning_output.tex'
        converter = EPUBToLaTeXConverter(epub_path, output_path)
        success = converter.convert()
        
        if not success:
            print("✗ Conversion failed")
            return False
        
        # Read output file
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for incorrect positioning (should not exist)
        if '\\begin{figure}[h]' in content:
            print("✗ Found incorrect '\\begin{figure}[h]' positioning")
            print("  Images should use [htbp] for better float positioning")
            return False
        
        # Check for correct positioning
        if '\\begin{figure}[htbp]' not in content:
            print("✗ Could not find correct '\\begin{figure}[htbp]' positioning")
            print("  Checking what was generated:")
            for line in content.split('\n'):
                if 'begin{figure}' in line:
                    print(f"  Found: {line.strip()}")
            return False
        
        # Count occurrences (should be 2: one for <img> and one for <figure>)
        count = content.count('\\begin{figure}[htbp]')
        if count != 2:
            print(f"✗ Expected 2 occurrences of \\begin{{figure}}[htbp], found {count}")
            return False
        
        print(f"✓ Image positioning is correct!")
        print(f"  Found {count} images with [htbp] float positioning")
        print(f"  This allows LaTeX to place images at: here, top, bottom, or page")
        
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
    print("Testing Image Float Positioning")
    print("=" * 60)
    print()
    
    try:
        if test_image_positioning():
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
