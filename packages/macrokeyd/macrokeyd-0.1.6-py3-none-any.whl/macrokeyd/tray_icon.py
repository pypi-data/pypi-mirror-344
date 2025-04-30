import pystray
from PIL import Image
import threading
import sys
import os

def create_tray_icon(stop_callback, pause_callback, resume_callback):
    icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon64x64.png')

    if not os.path.exists(icon_path):
        print(f"Error: Icon file not found at {icon_path}.")
        sys.exit(1)

    image = Image.open(icon_path)

    menu = pystray.Menu(
        pystray.MenuItem("Pause", pause_callback),
        pystray.MenuItem("Resume", resume_callback),
        pystray.MenuItem("Exit", stop_callback)
    )

    icon = pystray.Icon("macrokeyd", image, "MacroKeyD", menu)
    return icon

def run_tray_icon(stop_callback, pause_callback, resume_callback):
    icon = create_tray_icon(stop_callback, pause_callback, resume_callback)
    threading.Thread(target=icon.run, daemon=True).start()
    