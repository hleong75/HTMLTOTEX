#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for class attribute support in EPUB to LaTeX converter
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub2tex import EPUBToLaTeXConverter


def test_class_detection():
    """Test that CSS classes are correctly detected"""
    from bs4 import BeautifulSoup, Tag
    
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    # Test single class
    html = '<p class="important">Test</p>'
    soup = BeautifulSoup(html, 'lxml')
    tag = soup.find('p')
    classes = converter._get_element_classes(tag)
    assert 'important' in classes, f"Expected 'important' in {classes}"
    
    # Test multiple classes
    html = '<div class="box info highlight">Test</div>'
    soup = BeautifulSoup(html, 'lxml')
    tag = soup.find('div')
    classes = converter._get_element_classes(tag)
    assert 'box' in classes, f"Expected 'box' in {classes}"
    assert 'info' in classes, f"Expected 'info' in {classes}"
    assert 'highlight' in classes, f"Expected 'highlight' in {classes}"
    
    # Test no class
    html = '<p>Test</p>'
    soup = BeautifulSoup(html, 'lxml')
    tag = soup.find('p')
    classes = converter._get_element_classes(tag)
    assert len(classes) == 0, f"Expected no classes, got {classes}"
    
    print("✓ Class detection works correctly")
    return True


def test_class_formatting():
    """Test that class-based formatting is applied"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    # Test important class
    content = "Important text"
    classes = ['important']
    result = converter._apply_class_formatting(content, classes, inline=True)
    assert '\\textbf{\\large' in result, f"Expected bold large formatting in {result}"
    
    # Test note class
    content = "Note text"
    classes = ['note']
    result = converter._apply_class_formatting(content, classes, inline=True)
    assert '\\textcolor{blue}' in result, f"Expected blue color in {result}"
    
    # Test code-inline class
    content = "code"
    classes = ['code-inline']
    result = converter._apply_class_formatting(content, classes, inline=True)
    assert '\\texttt{' in result, f"Expected texttt formatting in {result}"
    
    # Test multiple classes
    content = "Text"
    classes = ['important', 'highlight']
    result = converter._apply_class_formatting(content, classes, inline=True)
    # Should have both formatings applied
    assert '\\textbf' in result or '\\hl{' in result, f"Expected formatting in {result}"
    
    print("✓ Class formatting works correctly")
    return True


def test_class_conversion():
    """Test conversion of EPUB with classes"""
    if not os.path.exists('class_test.epub'):
        print("⚠ class_test.epub not found, skipping class conversion test")
        print("  Run: python create_class_test_epub.py")
        return True
    
    # Test with temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as tmp:
        output_path = tmp.name
    
    try:
        converter = EPUBToLaTeXConverter('class_test.epub', output_path)
        success = converter.convert()
        
        if not success:
            print("✗ Conversion failed")
            return False
        
        if not os.path.exists(output_path):
            print("✗ Output file was not created")
            return False
        
        # Check file is not empty
        file_size = os.path.getsize(output_path)
        if file_size == 0:
            print("✗ Output file is empty")
            return False
        
        # Check for class-based formatting in output
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for specific class-based conversions
        expected_markers = [
            r'\textbf{\large',  # important class
            r'\textcolor{blue}',  # note class
            r'\textcolor{red}',  # warning class
            r'\textcolor{green}',  # done class (list item)
            r'\textcolor{orange}',  # pending class (list item)
            r'\textcolor{gray}',  # todo class (list item)
            r'\texttt{',  # code-inline class
            r'{\small\itshape',  # author-note class
            r'{\itshape',  # epigraph class
            r'\begin{shadedquotation}',  # highlight block class
            r'\begin{mdframed}',  # box/info block class
            r'\rowcolor{highlightyellow}',  # highlight-row class
        ]
        
        missing_markers = []
        for marker in expected_markers:
            if marker not in content:
                missing_markers.append(marker)
        
        if missing_markers:
            print(f"✗ Some class-based formatting not found:")
            for marker in missing_markers:
                print(f"  - {marker}")
            return False
        
        print(f"✓ Class test EPUB converted successfully ({file_size} bytes)")
        print(f"✓ All class-based formatting markers found")
        return True
        
    finally:
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)


def test_backward_compatibility():
    """Test that conversion without classes still works"""
    if not os.path.exists('sample.epub'):
        print("⚠ sample.epub not found, skipping backward compatibility test")
        return True
    
    # Test with temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as tmp:
        output_path = tmp.name
    
    try:
        converter = EPUBToLaTeXConverter('sample.epub', output_path)
        success = converter.convert()
        
        if not success:
            print("✗ Backward compatibility test failed")
            return False
        
        # Check file was created and is not empty
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            print("✗ Backward compatibility test failed - no output")
            return False
        
        print("✓ Backward compatibility maintained")
        return True
        
    finally:
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)


def run_all_tests():
    """Run all class support tests"""
    print("=" * 60)
    print("Testing Class Attribute Support")
    print("=" * 60)
    
    tests = [
        ("Class Detection", test_class_detection),
        ("Class Formatting", test_class_formatting),
        ("Class Conversion", test_class_conversion),
        ("Backward Compatibility", test_backward_compatibility),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
