#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test script for EPUB to LaTeX converter with all new features.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub2tex import EPUBToLaTeXConverter


def test_new_formatting_tags():
    """Test that new formatting tags are properly handled"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    test_cases = [
        # mark tag
        ('<mark>highlighted</mark>', r'\sethlcolor{highlightyellow}\hl{highlighted}'),
        # s tag
        ('<s>strikethrough</s>', r'\sout{strikethrough}'),
        # ins tag
        ('<ins>inserted</ins>', r'\underline{inserted}'),
        # kbd tag
        ('<kbd>Ctrl+C</kbd>', r'\texttt{Ctrl+C}'),
        # samp tag
        ('<samp>output</samp>', r'\texttt{output}'),
        # var tag
        ('<var>x</var>', r'\textit{x}'),
        # abbr tag
        ('<abbr>HTML</abbr>', r'\textsc{HTML}'),
        # q tag
        ('<q>quote</q>', r'``quote'''),
        # dfn tag
        ('<dfn>term</dfn>', r'\emph{term}'),
    ]
    
    for html_input, expected_latex in test_cases:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_input, 'html.parser')
        tag = soup.find()
        result = converter._convert_element(tag, inline=True)
        
        if expected_latex not in result:
            print(f"✗ Formatting tag test failed:")
            print(f"  Input:    {html_input}")
            print(f"  Expected: {expected_latex}")
            print(f"  Got:      {result}")
            return False
    
    print("✓ All new formatting tags work correctly")
    return True


def test_definition_lists():
    """Test that definition lists are properly converted"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    html_input = '''
    <dl>
        <dt>Term 1</dt>
        <dd>Definition 1</dd>
        <dt>Term 2</dt>
        <dd>Definition 2</dd>
    </dl>
    '''
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_input, 'html.parser')
    dl = soup.find('dl')
    result = converter._convert_definition_list(dl)
    
    required_elements = [
        r'\begin{description}',
        r'\item[Term 1] Definition 1',
        r'\item[Term 2] Definition 2',
        r'\end{description}',
    ]
    
    for element in required_elements:
        if element not in result:
            print(f"✗ Definition list test failed - missing: {element}")
            return False
    
    print("✓ Definition lists work correctly")
    return True


def test_nested_lists():
    """Test that nested lists are properly converted"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    html_input = '''
    <ul>
        <li>Item 1
            <ul>
                <li>Nested item 1</li>
                <li>Nested item 2</li>
            </ul>
        </li>
        <li>Item 2</li>
    </ul>
    '''
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_input, 'html.parser')
    ul = soup.find('ul')
    result = converter._convert_list(ul)
    
    # Check for nested itemize
    if result.count(r'\begin{itemize}') < 2:
        print("✗ Nested list test failed - missing nested itemize")
        return False
    
    if result.count(r'\end{itemize}') < 2:
        print("✗ Nested list test failed - missing nested itemize end")
        return False
    
    print("✓ Nested lists work correctly")
    return True


def test_semantic_html5_tags():
    """Test that HTML5 semantic tags are handled"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    html_inputs = [
        '<header><p>Header content</p></header>',
        '<footer><p>Footer content</p></footer>',
        '<aside><p>Aside content</p></aside>',
        '<article><p>Article content</p></article>',
        '<section><p>Section content</p></section>',
        '<main><p>Main content</p></main>',
        '<nav><p>Nav content</p></nav>',
    ]
    
    from bs4 import BeautifulSoup
    for html_input in html_inputs:
        soup = BeautifulSoup(html_input, 'html.parser')
        tag = soup.find()
        result = converter._convert_element(tag, inline=False)
        
        # nav should be empty (ignored)
        if tag.name == 'nav':
            if result.strip() != '':
                print(f"✗ Semantic tag test failed - nav should be empty")
                return False
        else:
            # Other tags should preserve content
            if 'content' not in result:
                print(f"✗ Semantic tag test failed for {tag.name}")
                return False
    
    print("✓ HTML5 semantic tags work correctly")
    return True


def test_table_with_caption():
    """Test that tables with captions are properly converted"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    html_input = '''
    <table>
        <caption>Test Caption</caption>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
        </tr>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </table>
    '''
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_input, 'html.parser')
    table = soup.find('table')
    result = converter._convert_table(table)
    
    if r'\caption{Test Caption}' not in result:
        print("✗ Table caption test failed")
        return False
    
    print("✓ Tables with captions work correctly")
    return True


def test_page_breaks():
    """Test that page breaks are added for chapters and sections"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    from bs4 import BeautifulSoup
    
    # Test h1 - should have \clearpage
    h1 = BeautifulSoup('<h1>Chapter</h1>', 'html.parser').find('h1')
    result = converter._convert_element(h1, inline=False)
    if r'\clearpage' not in result:
        print("✗ Page break test failed - h1 should have clearpage")
        return False
    
    # Test h2 - should have \newpage
    h2 = BeautifulSoup('<h2>Section</h2>', 'html.parser').find('h2')
    result = converter._convert_element(h2, inline=False)
    if r'\newpage' not in result:
        print("✗ Page break test failed - h2 should have newpage")
        return False
    
    print("✓ Page breaks work correctly")
    return True


def test_comprehensive_epub_conversion():
    """Test conversion of comprehensive EPUB"""
    if not os.path.exists('comprehensive_test.epub'):
        print("⚠ comprehensive_test.epub not found, skipping test")
        print("  Run: python create_comprehensive_test_epub.py")
        return True
    
    # Test with temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as tmp:
        output_path = tmp.name
    
    try:
        converter = EPUBToLaTeXConverter('comprehensive_test.epub', output_path)
        success = converter.convert()
        
        if not success:
            print("✗ Comprehensive EPUB conversion failed")
            return False
        
        if not os.path.exists(output_path):
            print("✗ Output file was not created")
            return False
        
        # Check file is not empty
        file_size = os.path.getsize(output_path)
        if file_size == 0:
            print("✗ Output file is empty")
            return False
        
        # Check for required LaTeX elements
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            r'\documentclass',
            r'\begin{document}',
            r'\end{document}',
            r'\usepackage{soul}',  # For highlighting
            r'\usepackage{titlesec}',  # For better sections
            r'\begin{description}',  # Definition lists
            r'\sethlcolor',  # Highlight color
        ]
        
        for element in required_elements:
            if element not in content:
                print(f"✗ Comprehensive test missing element: {element}")
                return False
        
        print(f"✓ Comprehensive EPUB converted successfully ({file_size} bytes)")
        return True
        
    finally:
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)


def test_error_handling():
    """Test that error handling works for invalid files"""
    converter = EPUBToLaTeXConverter('nonexistent.epub', '/tmp/output.tex')
    success = converter.convert()
    
    if success:
        print("✗ Error handling test failed - should have failed for nonexistent file")
        return False
    
    print("✓ Error handling works correctly")
    return True


def main():
    """Run all comprehensive tests"""
    print("=" * 60)
    print("Comprehensive EPUB to LaTeX Converter Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("New Formatting Tags", test_new_formatting_tags),
        ("Definition Lists", test_definition_lists),
        ("Nested Lists", test_nested_lists),
        ("HTML5 Semantic Tags", test_semantic_html5_tags),
        ("Tables with Captions", test_table_with_caption),
        ("Page Breaks", test_page_breaks),
        ("Error Handling", test_error_handling),
        ("Comprehensive EPUB Conversion", test_comprehensive_epub_conversion),
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
