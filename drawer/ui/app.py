import os
import subprocess
import webbrowser
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import platform
from PIL import Image
import sys
import os.path

class AppWindow:
    def __init__(self, json_handler, theme_manager):
        self.json_handler = json_handler
        self.theme_manager = theme_manager
        
        # Load settings from JSON
        self.settings = self.json_handler.get_settings()
        self.grid_columns = self.settings.get("grid_columns", 4)
        
        # Apply theme from settings
        self.theme_manager.set_theme(self.settings.get("theme", "light"))
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("WinDrawer")
        self.root.geometry(f"{self.settings.get('window_width', 800)}x{self.settings.get('window_height', 600)}")
        self.root.minsize(600, 400)
        
        # Set up the main frame with scroll capability
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas for scrolling
        self.canvas = ctk.CTkCanvas(self.main_container, bg=self.theme_manager.get_color("bg_color"), highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.main_container, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create frame inside canvas for content
        self.scrollable_frame = ctk.CTkFrame(self.canvas, corner_radius=0)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure scroll region when frame size changes
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Create header frame
        self.header_frame = ctk.CTkFrame(self.scrollable_frame)
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # App title
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="WinDrawer", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            self.header_frame,
            text="Toggle Theme",
            command=self.toggle_theme,
            width=120
        )
        self.theme_button.pack(side=tk.RIGHT, padx=10)
        
        # Add shortcut button
        self.add_button = ctk.CTkButton(
            self.header_frame,
            text="Add Shortcut",
            command=self.toggle_add_shortcut_form,
            width=120
        )
        self.add_button.pack(side=tk.RIGHT, padx=10)
        
        # Create add shortcut form frame (initially hidden)
        self.add_form_visible = False
        self.add_form_frame = ctk.CTkFrame(self.scrollable_frame)
        
        # Form elements
        self.form_title = ctk.CTkLabel(
            self.add_form_frame,
            text="Add New Shortcut",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.form_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 20), sticky="w")
        
        # Label input
        ctk.CTkLabel(self.add_form_frame, text="Label:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.label_entry = ctk.CTkEntry(self.add_form_frame, width=200)
        self.label_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Path input
        ctk.CTkLabel(self.add_form_frame, text="Path:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.path_entry = ctk.CTkEntry(self.add_form_frame, width=200)
        self.path_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.browse_button = ctk.CTkButton(
            self.add_form_frame, 
            text="Browse", 
            command=self.browse_path,
            width=80
        )
        self.browse_button.grid(row=2, column=2, padx=10, pady=5)
        
        # Category input
        ctk.CTkLabel(self.add_form_frame, text="Category:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.category_var = ctk.StringVar(value="Apps")
        self.category_dropdown = ctk.CTkOptionMenu(
            self.add_form_frame,
            values=["Apps", "Folders", "Web"],
            variable=self.category_var,
            width=200
        )
        self.category_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        # Group input
        ctk.CTkLabel(self.add_form_frame, text="Group:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.group_entry = ctk.CTkEntry(self.add_form_frame, width=200)
        self.group_entry.insert(0, "Default")
        self.group_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        # Form buttons
        self.form_buttons_frame = ctk.CTkFrame(self.add_form_frame, fg_color="transparent")
        self.form_buttons_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=(20, 10), sticky="e")
        
        self.cancel_button = ctk.CTkButton(
            self.form_buttons_frame,
            text="Cancel",
            command=self.toggle_add_shortcut_form,
            fg_color=self.theme_manager.get_color("cancel_button"),
            hover_color=self.theme_manager.get_color("cancel_hover"),
            width=100
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        self.save_button = ctk.CTkButton(
            self.form_buttons_frame,
            text="Save",
            command=self.save_shortcut,
            width=100
        )
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        # Create content area for shortcuts
        self.content_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Fill the window with shortcuts
        self.refresh_shortcuts()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_frame_configure(self, event):
        """Update the scrollregion when the frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """Resize the canvas window when the canvas changes size"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def toggle_add_shortcut_form(self):
        """Show or hide the add shortcut form"""
        if self.add_form_visible:
            self.add_form_frame.pack_forget()
            self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.add_form_visible = False
            self.add_button.configure(text="Add Shortcut")
        else:
            self.content_frame.pack_forget()
            self.add_form_frame.pack(fill=tk.X, padx=10, pady=10, after=self.header_frame)
            self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.add_form_visible = True
            self.add_button.configure(text="Close Form")
            
            # Clear form fields
            self.label_entry.delete(0, tk.END)
            self.path_entry.delete(0, tk.END)
            self.category_var.set("Apps")
            self.group_entry.delete(0, tk.END)
            self.group_entry.insert(0, "Default")
    
    def browse_path(self):
        """Open file or folder browser"""
        category = self.category_var.get()
        
        if category == "Apps":
            path = filedialog.askopenfilename(
                title="Select Application",
                filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
            )
        elif category == "Folders":
            path = filedialog.askdirectory(title="Select Folder")
        else:  # Web category doesn't need a file browser
            return
            
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def save_shortcut(self):
        """Save the new shortcut to the JSON file"""
        label = self.label_entry.get().strip()
        path = self.path_entry.get().strip()
        category = self.category_var.get()
        group = self.group_entry.get().strip() or "Default"
        
        # Validation
        if not label:
            messagebox.showerror("Error", "Label cannot be empty")
            return
            
        if not path:
            messagebox.showerror("Error", "Path cannot be empty")
            return
            
        # For web shortcuts, add https:// if no protocol is specified
        if category == "Web" and not (path.startswith("http://") or path.startswith("https://")):
            path = "https://" + path
        
        # Add the shortcut
        self.json_handler.add_shortcut({
            "label": label,
            "path": path,
            "category": category,
            "group": group
        })
        
        # Refresh the shortcuts display
        self.toggle_add_shortcut_form()
        self.refresh_shortcuts()
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current_theme = self.theme_manager.get_current_theme()
        new_theme = "dark" if current_theme == "light" else "light"
        self.theme_manager.set_theme(new_theme)
        
        # Update the JSON with the new theme setting
        self.settings["theme"] = new_theme
        self.json_handler.save_settings(self.settings)
        
        # Update canvas background color
        self.canvas.configure(bg=self.theme_manager.get_color("bg_color"))
        
        # Update cancel button color
        self.cancel_button.configure(
            fg_color=self.theme_manager.get_color("cancel_button"),
            hover_color=self.theme_manager.get_color("cancel_hover")
        )
    
    def open_shortcut(self, path, category):
        """Open the shortcut based on its category"""
        try:
            if category == "Web":
                webbrowser.open(path)
            elif category == "Folders":
                if os.path.exists(path):
                    if platform.system() == "Windows":
                        os.startfile(path)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.call(["open", path])
                    else:  # Linux
                        subprocess.call(["xdg-open", path])
                else:
                    messagebox.showerror("Error", f"Folder not found: {path}")
            else:  # Apps
                if os.path.exists(path):
                    if platform.system() == "Windows":
                        os.startfile(path)
                    else:
                        subprocess.Popen([path])
                else:
                    messagebox.showerror("Error", f"Application not found: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {path}: {str(e)}")
    
    def refresh_shortcuts(self):
        """Refresh the shortcuts display"""
        # Clear existing shortcuts
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get all shortcuts grouped by 'group'
        grouped_shortcuts = self.json_handler.get_shortcuts_by_group()
        
        # No shortcuts message if needed
        if not grouped_shortcuts:
            no_shortcuts_label = ctk.CTkLabel(
                self.content_frame,
                text="No shortcuts found. Click 'Add Shortcut' to create one.",
                font=ctk.CTkFont(size=14)
            )
            no_shortcuts_label.pack(pady=50)
            return
        
        # Create a frame for each group
        row = 0
        for group_name, shortcuts in grouped_shortcuts.items():
            # Create a frame for this group
            group_frame = ctk.CTkFrame(self.content_frame)
            group_frame.pack(fill=tk.X, pady=(15, 5), padx=5)
            
            # Group header
            group_header = ctk.CTkLabel(
                group_frame, 
                text=group_name,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            group_header.pack(fill=tk.X, padx=10, pady=5)
            
            # Create grid frame for shortcuts in this group
            shortcut_grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            shortcut_grid.pack(fill=tk.X, pady=(0, 15), padx=5)
            
            # Add shortcuts to the grid
            for i, shortcut in enumerate(shortcuts):
                col = i % self.grid_columns
                row = i // self.grid_columns
                
                # Create shortcut button
                button_color = self.get_button_color(shortcut["category"])
                hover_color = self.get_hover_color(shortcut["category"])
                
                shortcut_button = ctk.CTkButton(
                    shortcut_grid,
                    text=shortcut["label"],
                    command=lambda p=shortcut["path"], c=shortcut["category"]: self.open_shortcut(p, c),
                    width=150,
                    height=40,
                    fg_color=button_color,
                    hover_color=hover_color
                )
                shortcut_button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Configure grid weights to make columns equal width
            for i in range(self.grid_columns):
                shortcut_grid.grid_columnconfigure(i, weight=1)
    
    def get_button_color(self, category):
        """Get button color based on category"""
        if category == "Apps":
            return self.theme_manager.get_color("app_button")
        elif category == "Folders":
            return self.theme_manager.get_color("folder_button")
        elif category == "Web":
            return self.theme_manager.get_color("web_button")
        return self.theme_manager.get_color("button")
    
    def get_hover_color(self, category):
        """Get button hover color based on category"""
        if category == "Apps":
            return self.theme_manager.get_color("app_hover")
        elif category == "Folders":
            return self.theme_manager.get_color("folder_hover")
        elif category == "Web":
            return self.theme_manager.get_color("web_hover")
        return self.theme_manager.get_color("button_hover")
    
    def on_close(self):
        """Handle window close event"""
        # Save current window size
        self.settings["window_width"] = self.root.winfo_width()
        self.settings["window_height"] = self.root.winfo_height()
        self.json_handler.save_settings(self.settings)
        
        # Close the window
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()