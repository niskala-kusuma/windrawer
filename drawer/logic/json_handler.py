"""
JSON handler for WinDrawer application.
Handles loading and saving shortcut data and settings.
"""
import json
import os
from pathlib import Path


class JSONHandler:
    """Handles loading and saving JSON data for shortcuts and settings."""
    
    def __init__(self, data_file_path=None):
        """
        Initialize the JSON handler.
        
        Args:
            data_file_path (str, optional): Path to the JSON data file.
                Defaults to the dummy data file.
        """
        # Use the provided path or default to the dummy data file
        if data_file_path is None:
            # Get the root directory of the application
            root_dir = Path(__file__).parent.parent.parent
            data_file_path = os.path.join(root_dir, "data", "dummy_data.json")
        
        self.data_file_path = data_file_path
        self.data = self._load_data()
    
    def _load_data(self):
        """
        Load data from the JSON file.
        
        Returns:
            dict: The loaded data.
        """
        try:
            with open(self.data_file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")
            # Return a default structure if the file doesn't exist or is invalid
            return {
                "shortcuts": [],
                "settings": {
                    "theme": "light",
                    "grid_size": [3, 2],
                    "window_size": [800, 600],
                    "startup_minimize": False
                }
            }
    
    def save_data(self):
        """Save the current data to the JSON file."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
            
            with open(self.data_file_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def get_shortcuts(self):
        """
        Get all shortcuts.
        
        Returns:
            list: List of shortcuts.
        """
        return self.data.get("shortcuts", [])
    
    def get_settings(self):
        """
        Get application settings.
        
        Returns:
            dict: Application settings.
        """
        return self.data.get("settings", {
            "theme": "light",
            "grid_size": [3, 2],
            "window_size": [800, 600],
            "startup_minimize": False
        })
    
    def update_setting(self, key, value):
        """
        Update a specific setting.
        
        Args:
            key (str): Setting key.
            value: Setting value.
        """
        if "settings" not in self.data:
            self.data["settings"] = {}
        
        self.data["settings"][key] = value
        self.save_data()
    
    def add_shortcut(self, label, path, category):
        """
        Add a new shortcut.
        
        Args:
            label (str): Shortcut label.
            path (str): Path to the file, folder, or URL.
            category (str): Shortcut category.
        """
        if "shortcuts" not in self.data:
            self.data["shortcuts"] = []
        
        self.data["shortcuts"].append({
            "label": label,
            "path": path,
            "category": category
        })
        self.save_data()
    
    def remove_shortcut(self, index):
        """
        Remove a shortcut by index.
        
        Args:
            index (int): Index of the shortcut to remove.
        """
        if "shortcuts" in self.data and 0 <= index < len(self.data["shortcuts"]):
            self.data["shortcuts"].pop(index)
            self.save_data()