import customtkinter as ctk

class ThemeManager:
    """Manage application themes."""
    
    # Theme colors
    THEMES = {
        "light": {
            "bg_color": "#F5F5F5",
            "fg_color": "#333333",
            "button": "#4A6572",
            "button_hover": "#344955",
            "app_button": "#4CAF50",
            "app_hover": "#388E3C",
            "folder_button": "#FFC107",
            "folder_hover": "#FFA000",
            "web_button": "#2196F3",
            "web_hover": "#1976D2",
            "cancel_button": "#F44336",
            "cancel_hover": "#D32F2F"
        },
        "dark": {
            "bg_color": "#202020",
            "fg_color": "#FFFFFF",
            "button": "#4A6572",
            "button_hover": "#344955",
            "app_button": "#388E3C",
            "app_hover": "#2E7D32",
            "folder_button": "#FFA000",
            "folder_hover": "#FF8F00",
            "web_button": "#1976D2",
            "web_hover": "#1565C0",
            "cancel_button": "#D32F2F",
            "cancel_hover": "#C62828"
        }
    }
    
    def __init__(self):
        """Initialize the theme manager with the default theme."""
        self.current_theme = "light"
    
    def set_theme(self, theme_name):
        """Set the application theme."""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            # Apply theme to CustomTkinter
            ctk.set_appearance_mode("light" if theme_name == "light" else "dark")
            ctk.set_default_color_theme("blue")
    
    def get_color(self, color_name):
        """Get a color from the current theme."""
        return self.THEMES[self.current_theme].get(color_name, "#000000")
    
    def get_current_theme(self):
        """Get the current theme name."""
        return self.current_theme