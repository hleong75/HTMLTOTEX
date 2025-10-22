#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for \paragraph and \subparagraph command formatting fix.

This test verifies that h5 and h6 headings are properly converted to LaTeX
\paragraph and \subparagraph commands with correct newline formatting to avoid
the "Paragraph ended before \ttl@straight@i was complete" error with titlesec.
"""

import sys
import tempfile
import os
from epub2tex import EPUBToLaTeXConverter
from bs4 import BeautifulSoup

def test_h5_paragraph_formatting():
    """Test that h5 tags convert to \paragraph with single newline."""
    print("Running: H5 paragraph formatting")
    
    html = '<h5>Test H5 Heading</h5><p>Content after heading</p>'
    soup = BeautifulSoup(html, 'html.parser')
    converter = EPUBToLaTeXConverter('test.epub')
    
    result = ''
    for elem in soup.children:
        if elem.name:
            result += converter._convert_element(elem, inline=False, in_heading=False)
    
    # Check that \paragraph is followed by single newline, not double
    assert '\\paragraph{Test H5 Heading}\n' in result, "\\paragraph should have single newline"
    assert '\\paragraph{Test H5 Heading}\n\n' not in result, "\\paragraph should NOT have double newline"
    
    # Verify content follows immediately after
    lines = result.split('\n')
    para_idx = None
    for i, line in enumerate(lines):
        if '\\paragraph{Test H5 Heading}' in line:
            para_idx = i
            break
    
    assert para_idx is not None, "Could not find \\paragraph command"
    assert para_idx + 1 < len(lines), "No content after \\paragraph"
    assert 'Content after heading' in lines[para_idx + 1], "Content should be on next line"
    
    print("✓ H5 paragraph formatting is correct")
    return True

def test_h6_subparagraph_formatting():
    """Test that h6 tags convert to \subparagraph with single newline."""
    print("Running: H6 subparagraph formatting")
    
    html = '<h6>Test H6 Heading</h6><p>Content after heading</p>'
    soup = BeautifulSoup(html, 'html.parser')
    converter = EPUBToLaTeXConverter('test.epub')
    
    result = ''
    for elem in soup.children:
        if elem.name:
            result += converter._convert_element(elem, inline=False, in_heading=False)
    
    # Check that \subparagraph is followed by single newline, not double
    assert '\\subparagraph{Test H6 Heading}\n' in result, "\\subparagraph should have single newline"
    assert '\\subparagraph{Test H6 Heading}\n\n' not in result, "\\subparagraph should NOT have double newline"
    
    # Verify content follows immediately after
    lines = result.split('\n')
    subpara_idx = None
    for i, line in enumerate(lines):
        if '\\subparagraph{Test H6 Heading}' in line:
            subpara_idx = i
            break
    
    assert subpara_idx is not None, "Could not find \\subparagraph command"
    assert subpara_idx + 1 < len(lines), "No content after \\subparagraph"
    assert 'Content after heading' in lines[subpara_idx + 1], "Content should be on next line"
    
    print("✓ H6 subparagraph formatting is correct")
    return True

def test_other_headings_unchanged():
    """Test that h1-h4 headings still have double newlines."""
    print("Running: Other headings unchanged")
    
    test_cases = [
        ('<h1>Chapter</h1>', '\\chapter{Chapter}\n\n', 'chapter'),
        ('<h2>Section</h2>', '\\section{Section}\n\n', 'section'),
        ('<h3>Subsection</h3>', '\\subsection{Subsection}\n\n', 'subsection'),
        ('<h4>Subsubsection</h4>', '\\subsubsection{Subsubsection}\n\n', 'subsubsection'),
    ]
    
    converter = EPUBToLaTeXConverter('test.epub')
    
    for html, expected_pattern, name in test_cases:
        soup = BeautifulSoup(html, 'html.parser')
        result = converter._convert_element(soup.find(), inline=False, in_heading=False)
        
        # Remove page break prefix for h1 and h2
        if '\\clearpage' in result:
            result = result.replace('\\clearpage\n', '')
        if '\\newpage' in result:
            result = result.replace('\\newpage\n', '')
        
        assert expected_pattern in result, f"\\{name} should still have double newline"
    
    print("✓ Other headings (h1-h4) still have correct formatting")
    return True

def test_mixed_headings():
    """Test document with all heading levels."""
    print("Running: Mixed headings test")
    
    html = '''
    <h1>Chapter Title</h1>
    <p>Chapter content</p>
    <h2>Section Title</h2>
    <p>Section content</p>
    <h3>Subsection Title</h3>
    <p>Subsection content</p>
    <h4>Subsubsection Title</h4>
    <p>Subsubsection content</p>
    <h5>Paragraph Title</h5>
    <p>Paragraph content</p>
    <h6>Subparagraph Title</h6>
    <p>Subparagraph content</p>
    '''
    
    soup = BeautifulSoup(html, 'html.parser')
    converter = EPUBToLaTeXConverter('test.epub')
    
    result = ''
    for elem in soup.children:
        if elem.name:
            result += converter._convert_element(elem, inline=False, in_heading=False)
    
    # Verify paragraph and subparagraph have single newlines
    assert '\\paragraph{Paragraph Title}\n' in result
    assert '\\paragraph{Paragraph Title}\n\n' not in result
    assert '\\subparagraph{Subparagraph Title}\n' in result
    assert '\\subparagraph{Subparagraph Title}\n\n' not in result
    
    # Verify other commands still have double newlines
    assert '\\chapter{Chapter Title}\n\n' in result or '\\clearpage' in result
    assert '\\section{Section Title}\n\n' in result or '\\newpage' in result
    assert '\\subsection{Subsection Title}\n\n' in result
    assert '\\subsubsection{Subsubsection Title}\n\n' in result
    
    print("✓ Mixed headings work correctly")
    return True

def test_h5_h6_with_br_tags():
    """Test that h5/h6 with br tags also work correctly."""
    print("Running: H5/H6 with br tags")
    
    html = '''
    <h5>Title<br/>With Break</h5>
    <p>Content</p>
    <h6>Another<br/>Title</h6>
    <p>More content</p>
    '''
    
    soup = BeautifulSoup(html, 'html.parser')
    converter = EPUBToLaTeXConverter('test.epub')
    
    result = ''
    for elem in soup.children:
        if elem.name:
            result += converter._convert_element(elem, inline=False, in_heading=False)
    
    # Verify br converted to space in headings
    assert 'Title With Break' in result, "br should convert to space in h5"
    assert 'Another Title' in result, "br should convert to space in h6"
    
    # Verify no line breaks in paragraph/subparagraph commands
    assert '\\\\' not in result.split('\\paragraph')[1].split('}')[0], "No \\\\ in \\paragraph argument"
    assert '\\\\' not in result.split('\\subparagraph')[1].split('}')[0], "No \\\\ in \\subparagraph argument"
    
    # Verify single newlines after commands
    assert '\\paragraph{Title With Break}\n' in result
    assert '\\subparagraph{Another Title}\n' in result
    
    print("✓ H5/H6 with br tags work correctly")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Tests for \\paragraph and \\subparagraph Formatting Fix")
    print("=" * 60)
    print()
    
    tests = [
        test_h5_paragraph_formatting,
        test_h6_subparagraph_formatting,
        test_other_headings_unchanged,
        test_mixed_headings,
        test_h5_h6_with_br_tags,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
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
        print("✗ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
