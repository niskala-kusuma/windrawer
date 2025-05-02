import os
import sys
from drawer.logic.json_handler import JSONHandler
from drawer.ui.theme import ThemeManager
from drawer.ui.app import AppWindow

def main():
    """Main entry point for the application."""
    # Get the base directory of the application
    if getattr(sys, 'frozen', False):
        # If running as a bundled executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # If running as a script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Set up data directory
    data_dir = os.path.join(base_dir, "data")
    
    # Initialize components
    json_handler = JSONHandler(data_dir)
    theme_manager = ThemeManager()
    
    # Create and run the main window
    app = AppWindow(json_handler, theme_manager)
    app.run()

if __name__ == "__main__":
    main()