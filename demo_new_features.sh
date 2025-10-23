#!/bin/bash

# Demo script for new batch processing and auto-compilation features

echo "========================================"
echo "EPUB to LaTeX Converter v2.0 - Demo"
echo "========================================"
echo ""

# Create demo directory
mkdir -p /tmp/demo_library
cp sample.epub /tmp/demo_library/book1.epub
cp sample.epub /tmp/demo_library/book2.epub
cp sample.epub /tmp/demo_library/book3.epub

echo "1. Single file conversion (traditional mode)"
echo "--------------------------------------------"
python epub2tex.py sample.epub /tmp/single_output.tex
echo ""

echo "2. Single file with auto-compilation"
echo "--------------------------------------------"
python epub2tex.py sample.epub /tmp/single_compiled.tex --compile
echo ""

echo "3. Batch processing of directory"
echo "--------------------------------------------"
python epub2tex.py --directory /tmp/demo_library --output-dir /tmp/batch_output
echo ""

echo "4. Batch processing with auto-compilation"
echo "--------------------------------------------"
python epub2tex.py --directory /tmp/demo_library --output-dir /tmp/batch_compiled --compile
echo ""

echo "========================================"
echo "Demo completed! Check:"
echo "  - /tmp/single_output.tex (LaTeX only)"
echo "  - /tmp/single_compiled.pdf (compiled PDF)"
echo "  - /tmp/batch_output/ (3 LaTeX files)"
echo "  - /tmp/batch_compiled/ (3 PDFs + LaTeX)"
echo "========================================"

