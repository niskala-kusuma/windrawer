"""
Theme management for WinDrawer application.
Handles light and dark mode themes using CustomTkinter.
"""
import customtkinter as ctk


class ThemeManager:
    """Manages application theme (light/dark mode)."""
    
    # Theme constants
    LIGHT = "light"
    DARK = "dark"
    
    # Theme color mappings
    THEME_COLORS = {
        LIGHT: {
            "bg_color": "#f0f0f0",
            "fg_color": "#333333",
            "button_color": "#e0e0e0",
            "button_hover_color": "#d1d1d1",
            "button_text_color": "#333333",
            "accent_color": "#3a7ebf"
        },
        DARK: {
            "bg_color": "#242424",
            "fg_color": "#e0e0e0",
            "button_color": "#3a3a3a",
            "button_hover_color": "#4a4a4a",
            "button_text_color": "#e0e0e0",
            "accent_color": "#4f9ee8"
        }
    }
    
    def __init__(self, json_handler):
        """
        Initialize the theme manager.
        
        Args:
            json_handler (JSONHandler): Instance of JSONHandler to save/load theme settings.
        """
        self.json_handler = json_handler
        self.current_theme = self.json_handler.get_settings().get("theme", self.LIGHT)
        
        # Set the initial theme for CustomTkinter
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply the current theme to CustomTkinter."""
        if self.current_theme == self.DARK:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        
        # Set the default color theme
        ctk.set_default_color_theme("blue")
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.current_theme = self.DARK if self.current_theme == self.LIGHT else self.LIGHT
        self.json_handler.update_setting("theme", self.current_theme)
        self._apply_theme()
        return self.current_theme
    
    def get_current_theme(self):
        """
        Get the current theme name.
        
        Returns:
            str: Current theme name (LIGHT or DARK).
        """
        return self.current_theme
    
    def get_color(self, color_key):
        """
        Get a specific color value for the current theme.
        
        Args:
            color_key (str): Key for the color.
        
        Returns:
            str: Color hex value.
        """
        return self.THEME_COLORS[self.current_theme].get(color_key)