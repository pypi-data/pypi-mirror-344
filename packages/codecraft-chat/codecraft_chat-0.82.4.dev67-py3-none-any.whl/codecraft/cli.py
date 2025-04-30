#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entry point script for CodeCraft with proper UTF-8 handling.
This script is referenced in setup.py/pyproject.toml to create the
console script entry point that's callable from anywhere.
"""

import os
import sys
import subprocess


def main():
    """
    Launch CodeCraft with UTF-8 encoding properly set.
    This function serves as the entry point when installed via pip.
    """
    # Set UTF-8 mode
    os.environ["PYTHONUTF8"] = "1"
    os.environ["PYTHONIOENCODING"] = "utf-8"

    # If running on Windows, we might need additional handling
    if sys.platform == "win32":
        try:
            # Try to run with explicit UTF-8 mode
            args = [sys.executable, "-X", "utf8", "-m", "codecraft"] + sys.argv[1:]
            result = subprocess.run(args)
            sys.exit(result.returncode)
        except UnicodeDecodeError:
            print("Error: Unable to handle Unicode properly.")
            print("Please try setting PYTHONUTF8=1 in your environment variables.")
            print("You can do this by running: $env:PYTHONUTF8=\"1\" in PowerShell")
            print("Or SET PYTHONUTF8=1 in Command Prompt before running codecraft.")
            sys.exit(1)
    else:
        # For non-Windows platforms, just import and run the main function
        from codecraft.main import main_with_utf8
        sys.exit(main_with_utf8())


if __name__ == "__main__":
    main() 