"""
Sawit Go - TSJ - Entry Point
Main entry point for the application
"""

import sys
import os

sys.setrecursionlimit(10000)

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from src.app import SawitGoApp

def main():
    """Main entry point"""
    app = SawitGoApp()
    return app.exec()

if __name__ == "__main__":
    main()
