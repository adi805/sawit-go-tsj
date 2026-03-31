"""
Sawit Go - TSJ - Entry Point
Main entry point for the application
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import SawitGoApp

def main():
    """Main entry point"""
    app = SawitGoApp()
    app.run()

if __name__ == "__main__":
    main()
