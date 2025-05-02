import json
import os
from collections import defaultdict

class JSONHandler:
    def __init__(self, data_path):
        """Initialize the JSON handler with the data file path."""
        self.data_path = data_path
        self.shortcuts_file = os.path.join(data_path, "shortcuts.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_path, exist_ok=True)
        
        # Create or load shortcuts file
        if not os.path.exists(self.shortcuts_file):
            self.create_dummy_data()
        
        self.load_data()
    
    def create_dummy_data(self):
        """Create a dummy data file if it doesn't exist."""
        dummy_data = {
            "shortcuts": [
                {
                    "label": "Notepad",
                    "path": "C:/Windows/System32/notepad.exe",
                    "category": "Apps",
                    "group": "Editors"
                },
                {
                    "label": "Calculator",
                    "path": "C:/Windows/System32/calc.exe",
                    "category": "Apps",
                    "group": "Utilities"
                },
                {
                    "label": "Documents",
                    "path": os.path.expanduser("~/Documents"),
                    "category": "Folders",
                    "group": "System Folders"
                },
                {
                    "label": "Downloads",
                    "path": os.path.expanduser("~/Downloads"),
                    "category": "Folders",
                    "group": "System Folders"
                },
                {
                    "label": "Google",
                    "path": "https://www.google.com",
                    "category": "Web",
                    "group": "Search"
                },
                {
                    "label": "GitHub",
                    "path": "https://github.com",
                    "category": "Web",
                    "group": "Development"
                }
            ],
            "settings": {
                "theme": "light",
                "grid_columns": 4,
                "window_width": 800,
                "window_height": 600
            }
        }
        
        with open(self.shortcuts_file, 'w') as f:
            json.dump(dummy_data, f, indent=2)
    
    def load_data(self):
        """Load data from the JSON file."""
        try:
            with open(self.shortcuts_file, 'r') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file doesn't exist or is invalid, create a new one
            self.data = {"shortcuts": [], "settings": {"theme": "light"}}
            self.save_data()
    
    def save_data(self):
        """Save data to the JSON file."""
        with open(self.shortcuts_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_shortcuts(self):
        """Get all shortcuts."""
        return self.data.get("shortcuts", [])
    
    def get_shortcuts_by_group(self):
        """Get shortcuts organized by group."""
        groups = defaultdict(list)
        
        for shortcut in self.get_shortcuts():
            group = shortcut.get("group", "Default")
            groups[group].append(shortcut)
        
        # Sort groups alphabetically but keep "Default" first if it exists
        sorted_groups = {}
        if "Default" in groups:
            sorted_groups["Default"] = groups.pop("Default")
        
        # Add other groups in alphabetical order
        for group in sorted(groups.keys()):
            sorted_groups[group] = groups[group]
            
        return sorted_groups
    
    def get_unique_groups(self):
        """Get a list of all unique groups."""
        groups = set()
        for shortcut in self.get_shortcuts():
            groups.add(shortcut.get("group", "Default"))
        
        # Sort groups alphabetically but keep "Default" first
        sorted_groups = []
        if "Default" in groups:
            sorted_groups.append("Default")
            groups.remove("Default")
        
        sorted_groups.extend(sorted(groups))
        return sorted_groups
    
    def add_shortcut(self, shortcut):
        """Add a new shortcut."""
        # Make sure the shortcut has all required fields
        if not all(key in shortcut for key in ["label", "path", "category"]):
            raise ValueError("Shortcut must have label, path, and category fields")
        
        # Add default group if not specified
        if "group" not in shortcut:
            shortcut["group"] = "Default"
        
        # Add the shortcut to the data
        self.data["shortcuts"].append(shortcut)
        self.save_data()
    
    def remove_shortcut(self, index):
        """Remove a shortcut by index."""
        if 0 <= index < len(self.data["shortcuts"]):
            del self.data["shortcuts"][index]
            self.save_data()
    
    def update_shortcut(self, index, shortcut):
        """Update a shortcut by index."""
        if 0 <= index < len(self.data["shortcuts"]):
            self.data["shortcuts"][index] = shortcut
            self.save_data()
    
    def get_settings(self):
        """Get application settings."""
        return self.data.get("settings", {})
    
    def save_settings(self, settings):
        """Save application settings."""
        self.data["settings"] = settings
        self.save_data()