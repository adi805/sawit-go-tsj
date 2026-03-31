"""
Sawit Go - TSJ - Entry Point
Main entry point for the application
"""

import sys
from pathlib import Path

def setup_environment():
    """Setup application environment"""
    app_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(app_dir))

def main():
    """Main entry point"""
    setup_environment()
    
    from src.app import SawitGoApp
    
    app = SawitGoApp()
    app.run()

if __name__ == "__main__":
    main()
