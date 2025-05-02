# WinDrawer

A lightweight, offline Windows app launcher written in Python with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

---

## 🚀 Overview

**WinDrawer** helps users organize shortcuts to applications, folders, and web URLs in a sleek, minimal interface. Designed to be lightweight and fast, it aims to provide a modern, persistent launcher that stays out of the way—perfect for productivity-focused users.

---

## ✨ Features

- 🎨 **Light/Dark Mode** – Seamlessly toggle between modern light and dark themes
- 🧩 **Grid Layout** – Organize shortcuts in a responsive and customizable grid
- 🔗 **Multiple Shortcut Types** – Supports EXE files, folders, and website links
- 💾 **Persistent Settings** – Remembers user preferences and shortcuts
- 🧱 **Modular Design** – Cleanly separated UI, logic, and data layers
- 🔌 **Pluggable Architecture** *(future-ready)* – Designed with plugin support in mind

---

## 🧰 Installation

1. **Clone this repository**
```bash
git clone https://github.com/your-username/windrawer.git
cd windrawer
```
2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the app**

```bash
python run_windrawer.py
```


---


## 🗂 Project Structure
```bash
WinDrawer/
├── assets/                  # Static assets (icons, images, etc.)
├── backups/                 # Backup files (user shortcut data, settings)
├── drawer/                 
│   ├── __init__.py
│   ├── ui/                  # UI Layer
│   │   ├── __init__.py
│   │   ├── app.py           # Main window setup
│   │   ├── theme.py         # Theme switching logic
│   ├── logic/               # Core application logic
│   │   ├── __init__.py
│   │   ├── shortcuts.py     # Shortcut management
│   │   ├── backup_restore.py# Backup/restore logic
│   │   ├── json_handler.py  # JSON handling logic
│   ├── tray/
│   │   ├── __init__.py
│   │   ├── tray_icon.py     # System tray functionality
│   └── main.py              # Internal entry point
├── data/                    # JSON config and shortcut data
│   └── dummy_data.json      # Dummy shortcut entries
├── requirements.txt         # Python dependency list
├── run_windrawer.py         # Main script to run the app
└── README.md                # You're reading it
```

---

## 📦 Dependencies

CustomTkinter – Modern UI components for Tkinter
Pillow – Image handling
pystray – System tray integration
PyInstaller – Create distributable EXE files
Install them all with:

```bash
pip install -r requirements.txt
```

## 🏗 Building Executable
To package the app into a single EXE:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico run_windrawer.py
```
This will create a dist/ folder with your executable.

## 🛠 Development Roadmap
✅ Light/Dark theme support

✅ Grid-based shortcut layout

✅ Persistent local storage for shortcuts and settings

🔜 Backup and Restore user data

🔜 Add/Edit/Delete shortcut dialog

🔜 Minimize to system tray

🔜 Plugin architecture for community-contributed extensions

🔜 Settings: persistent across sessions

## 🤝 Contribution
We're planning to open plugin support so contributors can expand WinDrawer's functionality. Stay tuned for guidelines and plugin API!

## 📄 License
This project is licensed under the MIT License.







