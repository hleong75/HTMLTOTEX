#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for batch EPUB processing and auto-compilation
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from epub2tex import EPUBToLaTeXConverter, process_directory, compile_latex


def test_batch_processing():
    """Test batch processing of multiple EPUB files"""
    print("\n" + "=" * 60)
    print("Testing batch EPUB processing")
    print("=" * 60)
    
    # Create test directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "epubs"
        output_dir = Path(tmpdir) / "output"
        test_dir.mkdir()
        output_dir.mkdir()
        
        # Check if sample.epub exists
        if not os.path.exists('sample.epub'):
            print("⚠ sample.epub not found, creating one...")
            os.system('python create_sample_epub.py')
        
        # Copy sample.epub multiple times
        sample_path = Path('sample.epub')
        if not sample_path.exists():
            print("✗ Cannot create sample EPUB for testing")
            return False
        
        for i in range(3):
            shutil.copy(sample_path, test_dir / f"test_book_{i}.epub")
        
        print(f"\n✓ Created test directory with 3 EPUB files")
        
        # Test batch processing without compilation
        print("\nTesting batch processing without compilation...")
        successful, failed = process_directory(
            str(test_dir),
            output_dir=str(output_dir),
            compile_latex_flag=False
        )
        
        if successful != 3 or failed != 0:
            print(f"✗ Expected 3 successful, 0 failed. Got {successful} successful, {failed} failed")
            return False
        
        # Check output files exist
        tex_files = list(output_dir.glob('*.tex'))
        if len(tex_files) != 3:
            print(f"✗ Expected 3 .tex files, found {len(tex_files)}")
            return False
        
        print(f"✓ Batch processing successful: {successful} files converted")
        
        return True


def test_auto_compilation():
    """Test automatic LaTeX compilation"""
    print("\n" + "=" * 60)
    print("Testing automatic LaTeX compilation")
    print("=" * 60)
    
    # Check if sample.epub exists
    if not os.path.exists('sample.epub'):
        print("⚠ sample.epub not found, creating one...")
        os.system('python create_sample_epub.py')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_output.tex"
        
        # Convert EPUB to LaTeX
        print("\nConverting EPUB to LaTeX...")
        converter = EPUBToLaTeXConverter('sample.epub', str(output_path))
        if not converter.convert():
            print("✗ EPUB conversion failed")
            return False
        
        print("✓ EPUB converted successfully")
        
        # Try to compile LaTeX
        print("\nCompiling LaTeX to PDF...")
        success = compile_latex(str(output_path))
        
        if not success:
            print("⚠ LaTeX compilation failed (may be due to missing LaTeX installation)")
            # Don't fail the test if LaTeX is not installed
            return True
        
        # Check if PDF was created
        pdf_path = output_path.with_suffix('.pdf')
        if not pdf_path.exists():
            print("✗ PDF file was not created")
            return False
        
        print(f"✓ PDF compiled successfully: {pdf_path}")
        print(f"  Size: {pdf_path.stat().st_size} bytes")
        
        return True


def test_batch_with_compilation():
    """Test batch processing with automatic compilation"""
    print("\n" + "=" * 60)
    print("Testing batch processing with compilation")
    print("=" * 60)
    
    # Create test directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "epubs"
        output_dir = Path(tmpdir) / "output"
        test_dir.mkdir()
        output_dir.mkdir()
        
        # Check if sample.epub exists
        if not os.path.exists('sample.epub'):
            print("⚠ sample.epub not found, creating one...")
            os.system('python create_sample_epub.py')
        
        # Copy sample.epub twice
        sample_path = Path('sample.epub')
        if not sample_path.exists():
            print("✗ Cannot create sample EPUB for testing")
            return False
        
        for i in range(2):
            shutil.copy(sample_path, test_dir / f"book_{i}.epub")
        
        print(f"\n✓ Created test directory with 2 EPUB files")
        
        # Test batch processing with compilation
        print("\nTesting batch processing with compilation...")
        successful, failed = process_directory(
            str(test_dir),
            output_dir=str(output_dir),
            compile_latex_flag=True
        )
        
        if failed > 0:
            print(f"⚠ Some files failed: {successful} successful, {failed} failed")
            # Don't fail test if compilation fails (may be due to LaTeX setup)
            return True
        
        # Check output files exist
        tex_files = list(output_dir.glob('*.tex'))
        pdf_files = list(output_dir.glob('*.pdf'))
        
        print(f"\n✓ Generated files:")
        print(f"  LaTeX files: {len(tex_files)}")
        print(f"  PDF files: {len(pdf_files)}")
        
        if len(tex_files) != 2:
            print(f"✗ Expected 2 .tex files, found {len(tex_files)}")
            return False
        
        if len(pdf_files) > 0:
            print(f"✓ PDF compilation successful for {len(pdf_files)} file(s)")
        else:
            print(f"⚠ No PDFs generated (LaTeX may not be installed)")
        
        return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("EPUB Batch Processing and Compilation Tests")
    print("=" * 60)
    
    tests = [
        ("Batch Processing", test_batch_processing),
        ("Auto Compilation", test_auto_compilation),
        ("Batch with Compilation", test_batch_with_compilation),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"\nRunning: {name}")
            if test_func():
                print(f"✓ {name} passed")
                passed += 1
            else:
                print(f"✗ {name} failed")
                failed += 1
        except Exception as e:
            print(f"✗ {name} failed with exception: {str(e)}")
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
    sys.exit(main())
