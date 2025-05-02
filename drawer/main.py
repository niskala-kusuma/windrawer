"""
WinDrawer - Lightweight Windows app launcher.
Main entry point for the application.
"""
import os
import sys
from pathlib import Path

# Add the project root directory to the path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import application modules
from drawer.logic.json_handler import JSONHandler
from drawer.ui.theme import ThemeManager
from drawer.ui.app import AppWindow


def main():
    """Main entry point for the application."""
    # Initialize data handler
    json_handler = JSONHandler()
    
    # Initialize theme manager
    theme_manager = ThemeManager(json_handler)
    
    # Create and run main application window
    app = AppWindow(json_handler, theme_manager)
    app.mainloop()


if __name__ == "__main__":
    main()