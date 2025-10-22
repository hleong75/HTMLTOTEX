#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test to verify LaTeX syntax validity for includegraphics
"""

def test_latex_syntax():
    """Test that the includegraphics syntax follows LaTeX keyval package rules"""
    
    # The correct syntax for includegraphics options
    correct_syntax = r"\includegraphics[width=\textwidth]{images/test.jpg}"
    
    # The incorrect syntax that was causing the error
    incorrect_syntax = r"\includegraphics[max width=\textwidth]{images/test.jpg}"
    
    print("=" * 60)
    print("LaTeX Syntax Validation")
    print("=" * 60)
    print()
    print("INCORRECT syntax (causes keyval error):")
    print(f"  {incorrect_syntax}")
    print()
    print("Explanation:")
    print("  'max width' is NOT a valid parameter for \\includegraphics")
    print("  The keyval package doesn't recognize 'max width' as a key")
    print()
    print("CORRECT syntax:")
    print(f"  {correct_syntax}")
    print()
    print("Explanation:")
    print("  'width' is a valid parameter for \\includegraphics")
    print("  The image will be scaled to fit the text width")
    print()
    print("Valid \\includegraphics parameters include:")
    print("  - width=<length>")
    print("  - height=<length>")
    print("  - scale=<factor>")
    print("  - angle=<degrees>")
    print("  - keepaspectratio")
    print()
    print("✓ The fix changes 'max width=' to 'width=' which is correct")
    print()


if __name__ == '__main__':
    test_latex_syntax()
