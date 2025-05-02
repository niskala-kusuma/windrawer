WinDrawer
A lightweight, offline Windows app launcher written in Python with CustomTkinter.

Overview
WinDrawer allows users to organize shortcuts (apps, folders, and URLs) in a grid-based layout. The application is designed to be minimal and fast while maintaining a modern look.

Features
Light/Dark Mode: Toggle between light and dark themes
Grid Layout: Display shortcuts in a customizable grid
Multiple Shortcut Types: Support for applications, folders, and web URLs
Persistent Settings: Save user preferences and shortcut data
Installation
Clone this repository
Install dependencies:
pip install -r requirements.txt
Run the application:
python run_windrawer.py
Project Structure
WinDrawer/
├── assets/                  # All static files (icons, images, etc.)
├── backups/                 # Backup files (for storing user data like shortcuts)
├── drawer/                  # Core logic of the application
│   ├── __init__.py          # Initialization file for the main drawer logic
│   ├── ui/                  # All UI-related files
│   │   ├── __init__.py      # UI logic initialization
│   │   ├── app.py           # Main application window setup
│   │   ├── theme.py         # Theme management (light/dark mode)
│   ├── logic/               # Core application logic
│   │   ├── __init__.py      # Logic initialization
│   │   ├── shortcuts.py     # Logic to manage shortcut data
│   │   ├── backup_restore.py# Backup and restore logic
│   │   ├── json_handler.py  # Handling JSON data
│   ├── tray/                # Logic for system tray
│   │   ├── __init__.py      # Tray icon setup
│   │   ├── tray_icon.py     # Code for tray icon functionality
│   └── main.py              # Entry point of the application
├── data/                    # Stores JSON files for shortcuts & settings
│   └── dummy_data.json      # Placeholder file for shortcuts
├── requirements.txt         # List of dependencies
├── run_windrawer.py         # Entry point script
└── README.md                # Project overview and instructions
Dependencies
CustomTkinter: Modern UI widgets for tkinter
Pillow: Image processing
pystray: System tray functionality
PyInstaller: Creates standalone executables
Building Executable
To create a standalone executable:

pyinstaller --onefile --windowed --icon=assets/icon.ico run_windrawer.py
Development
Next Steps
Implement system tray functionality
Add ability to add, edit, and delete shortcuts
Implement backup and restore functionality
Create a proper executable with PyInstaller
