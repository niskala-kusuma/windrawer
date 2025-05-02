"""
Main application window for WinDrawer.
Handles the UI layout and shortcut display.
"""
import os
import subprocess
import webbrowser
import customtkinter as ctk
from PIL import Image


class AppWindow(ctk.CTk):
    """Main application window class."""
    
    def __init__(self, json_handler, theme_manager):
        """
        Initialize the main application window.
        
        Args:
            json_handler: Instance of JSONHandler to load shortcuts.
            theme_manager: Instance of ThemeManager for theme handling.
        """
        super().__init__()
        
        self.json_handler = json_handler
        self.theme_manager = theme_manager
        self.shortcuts = self.json_handler.get_shortcuts()
        self.settings = self.json_handler.get_settings()
        
        # Configure window
        self.title("WinDrawer")
        self.geometry(f"{self.settings['window_size'][0]}x{self.settings['window_size'][1]}")
        self.minsize(400, 300)
        
        # Bind window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Track icon references to prevent garbage collection
        self.icon_references = []
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create menu frame (top)
        self.create_menu_frame()
        
        # Create shortcuts grid (center)
        self.create_shortcuts_grid()
    
    def create_menu_frame(self):
        """Create the menu frame with theme toggle and other options."""
        menu_frame = ctk.CTkFrame(self.main_frame)
        menu_frame.pack(fill="x", padx=5, pady=5)
        
        # App title
        title_label = ctk.CTkLabel(
            menu_frame, 
            text="WinDrawer", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Theme toggle button
        theme_text = "🌙 Dark" if self.theme_manager.get_current_theme() == "light" else "☀️ Light"
        self.theme_button = ctk.CTkButton(
            menu_frame,
            text=theme_text,
            width=100,
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=10)
    
    def create_shortcuts_grid(self):
        """Create the grid of shortcut buttons."""
        self.grid_frame = ctk.CTkFrame(self.main_frame)
        self.grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Calculate grid dimensions
        grid_size = self.settings.get("grid_size", [3, 2])
        cols, rows = grid_size
        
        # Configure grid
        for i in range(rows):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        for i in range(cols):
            self.grid_frame.grid_columnconfigure(i, weight=1)
        
        # Add shortcuts to grid
        for i, shortcut in enumerate(self.shortcuts):
            # Calculate row and column
            row = i // cols
            col = i % cols
            
            # Create shortcut button
            shortcut_button = self.create_shortcut_button(shortcut)
            shortcut_button.grid(
                row=row, 
                column=col, 
                padx=10, 
                pady=10, 
                sticky="nsew"
            )
    
    def create_shortcut_button(self, shortcut):
        """
        Create a button for a shortcut.
        
        Args:
            shortcut (dict): Shortcut data with label, path, and category.
        
        Returns:
            CTkButton: Button widget for the shortcut.
        """
        # Determine button color based on category
        category_colors = {
            "Apps": "#3a7ebf",
            "Folders": "#388e3c",
            "Web": "#d32f2f",
            "Tools": "#7b1fa2"
        }
        
        # Get default color for the category or use a fallback
        category = shortcut.get("category", "Others")
        color = category_colors.get(category, "#616161")
        
        # Add an icon based on type
        icon_text = ""
        path = shortcut.get("path", "")
        if path.startswith(("http://", "https://")):
            icon_text = "🌐 "
        elif os.path.exists(path) and os.path.isdir(path):
            icon_text = "📁 "
        else:
            icon_text = "📌 "
        
        button = ctk.CTkButton(
            self.grid_frame,
            text=f"{icon_text}{shortcut['label']}",
            height=80,
            corner_radius=8,
            fg_color=color,
            hover_color=self.darken_color(color),
            command=lambda: self.open_shortcut(shortcut)
        )
        
        return button
    
    def open_shortcut(self, shortcut):
        """
        Open the shortcut (app, folder, or URL).
        
        Args:
            shortcut (dict): Shortcut data with path.
        """
        path = shortcut.get("path", "")
        if not path:
            print("Error: Shortcut has no path")
            return
            
        try:
            # Handle URLs
            if path.startswith(("http://", "https://")):
                webbrowser.open(path)
            # Handle files and folders
            elif os.path.exists(path):
                if os.path.isdir(path):
                    # Open folder
                    os.startfile(path)
                else:
                    # Open file
                    os.startfile(path)
            else:
                print(f"Path does not exist: {path}")
        except Exception as e:
            print(f"Error opening shortcut: {e}")
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = self.theme_manager.toggle_theme()
        
        # Update theme button text
        theme_text = "🌙 Dark" if new_theme == "light" else "☀️ Light"
        self.theme_button.configure(text=theme_text)
        
        # Refresh UI elements
        self.update_idletasks()
    
    def on_close(self):
        """Handle window close event."""
        # Save window size
        self.json_handler.update_setting("window_size", [self.winfo_width(), self.winfo_height()])
        
        # Close the window
        self.destroy()
    
    @staticmethod
    def darken_color(hex_color, factor=0.8):
        """
        Darken a hex color by a factor.
        
        Args:
            hex_color (str): Hex color code (e.g., "#3a7ebf").
            factor (float): Factor to darken by (0-1).
        
        Returns:
            str: Darkened hex color.
        """
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Darken
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"