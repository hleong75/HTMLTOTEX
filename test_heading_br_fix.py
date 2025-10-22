#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for the fix of "Paragraph ended before \ttl@straight@i was complete" error.

This test ensures that headings with <br> tags don't cause LaTeX compilation errors
by converting <br> to spaces instead of \\ in section titles.
"""

import os
import sys
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub2tex import EPUBToLaTeXConverter
from bs4 import BeautifulSoup


def test_heading_with_br_tag():
    """Test that headings with <br> tags convert to spaces, not line breaks"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    test_cases = [
        ('<h1>Chapter Title<br/>With Line Break</h1>', 'Chapter Title With Line Break', '\\chapter'),
        ('<h2>Section<br/>Title</h2>', 'Section Title', '\\section'),
        ('<h3>Subsection<br/>With<br/>Multiple<br/>Breaks</h3>', 'Subsection With Multiple Breaks', '\\subsection'),
    ]
    
    for html_input, expected_text, expected_cmd in test_cases:
        soup = BeautifulSoup(html_input, 'html.parser')
        tag = soup.find()
        result = converter._convert_element(tag, inline=False)
        
        # Should NOT contain \\ (line break)
        if '\\\\' in result:
            print(f"✗ Test FAILED: {tag.name} with <br> still contains line break \\\\")
            print(f"  Input:  {html_input}")
            print(f"  Output: {repr(result)}")
            return False
        
        # Should contain the expected LaTeX command
        if expected_cmd not in result:
            print(f"✗ Test FAILED: {tag.name} missing expected command {expected_cmd}")
            return False
        
        # Should contain the text (with spaces instead of breaks)
        words = expected_text.split()
        for word in words:
            if word not in result:
                print(f"✗ Test FAILED: {tag.name} missing word '{word}'")
                return False
    
    print("✓ Headings with <br> tags convert to spaces correctly")
    return True


def test_heading_with_inline_formatting():
    """Test that headings with inline formatting still work"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    test_cases = [
        ('<h1>Title with <b>bold</b></h1>', r'\textbf{bold}'),
        ('<h2>Title with <i>italic</i></h2>', r'\textit{italic}'),
        ('<h3>Title with <code>code</code></h3>', r'\texttt{code}'),
    ]
    
    for html_input, expected_latex in test_cases:
        soup = BeautifulSoup(html_input, 'html.parser')
        tag = soup.find()
        result = converter._convert_element(tag, inline=False)
        
        if expected_latex not in result:
            print(f"✗ Inline formatting test failed:")
            print(f"  Input:    {html_input}")
            print(f"  Expected: {expected_latex}")
            print(f"  Got:      {result}")
            return False
    
    print("✓ Headings with inline formatting work correctly")
    return True


def test_br_tag_outside_headings():
    """Test that <br> tags still work as line breaks outside headings"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    # In paragraph, br should create line break
    html = '<p>Line 1<br/>Line 2</p>'
    soup = BeautifulSoup(html, 'html.parser')
    p = soup.find('p')
    result = converter._convert_element(p, inline=False)
    
    if '\\\\' not in result:
        print("✗ Test FAILED: <br> in paragraph should create line break")
        return False
    
    print("✓ <br> tags work correctly outside headings")
    return True


def test_comprehensive_epub_with_br_in_headings():
    """Test full conversion of EPUB with <br> in headings"""
    try:
        from ebooklib import epub
    except ImportError:
        print("⚠ ebooklib not available, skipping EPUB creation test")
        return True
    
    # Create a test EPUB
    book = epub.EpubBook()
    book.set_identifier('test_br_001')
    book.set_title('Test BR in Headings')
    book.set_language('en')
    book.add_author('Test')
    
    c1 = epub.EpubHtml(title='Chapter 1',
                       file_name='chap_01.xhtml',
                       lang='en')
    
    c1.content = '''<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Test</title></head>
<body>
<h1>Chapter<br/>Title</h1>
<p>Content</p>
</body>
</html>'''
    
    book.add_item(c1)
    book.toc = (epub.Link('chap_01.xhtml', 'Chapter 1', 'chap_01'),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav', c1]
    
    # Write temporary EPUB
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.epub', delete=False) as tmp_epub:
        epub_path = tmp_epub.name
        epub.write_epub(epub_path, book)
    
    # Convert to LaTeX
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as tmp_tex:
        tex_path = tmp_tex.name
    
    try:
        converter = EPUBToLaTeXConverter(epub_path, tex_path)
        success = converter.convert()
        
        if not success:
            print("✗ Comprehensive test failed: conversion unsuccessful")
            return False
        
        # Read generated LaTeX
        with open(tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should NOT contain \\ in chapter command
        if '\\chapter{Chapter\\\\' in content:
            print("✗ Comprehensive test failed: chapter still has line break")
            return False
        
        # Should contain chapter with space
        if '\\chapter{Chapter Title}' not in content:
            print("✗ Comprehensive test failed: chapter not formatted correctly")
            return False
        
        print("✓ Full EPUB conversion with <br> in headings works correctly")
        return True
        
    finally:
        # Clean up
        if os.path.exists(epub_path):
            os.remove(epub_path)
        if os.path.exists(tex_path):
            os.remove(tex_path)
        # Clean up images directory if created
        img_dir = os.path.join(os.path.dirname(tex_path), 'images')
        if os.path.exists(img_dir):
            import shutil
            shutil.rmtree(img_dir)


def main():
    """Run all tests for the br tag fix"""
    print("=" * 60)
    print("Tests for 'Paragraph ended before \\ttl@straight@i' Fix")
    print("=" * 60)
    print()
    
    tests = [
        ("Heading with <br> tag", test_heading_with_br_tag),
        ("Heading with inline formatting", test_heading_with_inline_formatting),
        ("<br> outside headings", test_br_tag_outside_headings),
        ("Comprehensive EPUB with <br>", test_comprehensive_epub_with_br_in_headings),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    if failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
