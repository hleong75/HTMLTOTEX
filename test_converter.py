#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for EPUB to LaTeX converter
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub2tex import EPUBToLaTeXConverter


def test_converter_exists():
    """Test that the converter can be imported"""
    print("✓ Converter module imported successfully")
    return True


def test_sample_conversion():
    """Test conversion of sample EPUB"""
    if not os.path.exists('sample.epub'):
        print("⚠ sample.epub not found, skipping conversion test")
        print("  Run: python create_sample_epub.py")
        return True
    
    # Test with temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as tmp:
        output_path = tmp.name
    
    try:
        converter = EPUBToLaTeXConverter('sample.epub', output_path)
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
        
        # Check for LaTeX markers
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_markers = [
            r'\documentclass',
            r'\begin{document}',
            r'\end{document}',
            r'\maketitle',
            r'\tableofcontents',
        ]
        
        for marker in required_markers:
            if marker not in content:
                print(f"✗ Required LaTeX marker not found: {marker}")
                return False
        
        print(f"✓ Sample EPUB converted successfully ({file_size} bytes)")
        return True
        
    finally:
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)


def test_special_characters():
    """Test that special characters are properly escaped"""
    converter = EPUBToLaTeXConverter('dummy.epub')
    
    test_cases = [
        ('Hello & World', r'Hello \& World'),
        ('50% complete', r'50\% complete'),
        ('Cost: $100', r'Cost: \$100'),
        ('Section #1', r'Section \#1'),
        ('file_name', r'file\_name'),
        ('Use {braces}', r'Use \{braces\}'),
    ]
    
    for input_text, expected in test_cases:
        result = converter._escape_latex(input_text)
        if result != expected:
            print(f"✗ Special character escaping failed:")
            print(f"  Input:    {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
            return False
    
    print("✓ Special characters escaped correctly")
    return True


def test_help_command():
    """Test that help command works"""
    import subprocess
    result = subprocess.run(
        [sys.executable, 'epub2tex.py', '--help'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("✗ Help command failed")
        return False
    
    if 'Convert EPUB files to LaTeX' not in result.stdout:
        print("✗ Help text missing expected content")
        return False
    
    print("✓ Help command works")
    return True


def test_version_command():
    """Test that version command works"""
    import subprocess
    result = subprocess.run(
        [sys.executable, 'epub2tex.py', '--version'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("✗ Version command failed")
        return False
    
    if 'EPUB to LaTeX Converter' not in result.stdout:
        print("✗ Version text missing")
        return False
    
    print("✓ Version command works")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing EPUB to LaTeX Converter")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Import", test_converter_exists),
        ("Special Characters", test_special_characters),
        ("Help Command", test_help_command),
        ("Version Command", test_version_command),
        ("Sample Conversion", test_sample_conversion),
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
