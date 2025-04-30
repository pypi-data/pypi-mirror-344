import subprocess
import pyautogui

def execute_command(command):
    subprocess.run(command, shell=True)

def write_text(text):
    pyautogui.typewrite(text)
