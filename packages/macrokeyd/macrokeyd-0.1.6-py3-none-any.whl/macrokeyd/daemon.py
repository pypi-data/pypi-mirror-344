import sys
import click
from macrokeyd import __version__
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select
from macrokeyd.config_loader import load_config
from macrokeyd import actions
import os
from macrokeyd.tray_icon import run_tray_icon

def get_config_path():
    xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    config_path = os.path.join(xdg_data_home, "macrokeyd", "default.json")
    return config_path

def ensure_config_exists(config_path):
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        default_path = os.path.join(os.path.dirname(__file__), 'macros', 'default.json')
        if os.path.exists(default_path):
            with open(default_path, 'r') as src, open(config_path, 'w') as dst:
                dst.write(src.read())
            print(f"[+] Default configuration copied to {config_path}")
        else:
            print(f"[!] Default configuration file not found at {default_path}")

CONFIG_PATH = get_config_path()
ensure_config_exists(CONFIG_PATH)

def detect_keyboards(target_device_name):
    keyboards = []
    available_devices = []
    for path in list_devices():
        device = InputDevice(path)
        capabilities = device.capabilities()

        available_devices.append(device.name)

        if ecodes.EV_KEY in capabilities and ecodes.EV_REL not in capabilities:
            if device.name == target_device_name:
                try:
                    device.grab()
                    print(f"[+] Exclusive grab: {device.name} ({device.path})")
                    keyboards.append(device)
                except OSError as e:
                    print(f"[!] Could not grab {device.name}: {e}")

    if not keyboards:
        print(f"[!] No compatible keyboards found. Available devices: {available_devices}")

    return keyboards

def execute_macro(keycode, macros):
    macro = macros.get(keycode)
    if not macro:
        print(f"[!] Key {keycode} not assigned.")
        return

    action_type = macro.get('action')
    value = macro.get('value')

    print(f"[MACRO] Executing {action_type}: {value}")

    if action_type == 'command':
        actions.execute_command(value)
    elif action_type == 'text':
        actions.write_text(value)
    else:
        print(f"[!] Unknown action type: {action_type}")

@click.command()
@click.option('--version', is_flag=True, help='Show version and exit.')
@click.option('--run', is_flag=True, help='Run the macro daemon.')
def cli(version, run):
    if version:
        print(f"macrokeyd {__version__}")
        return

    if not run:
        print("Use --run to start the daemon, or --help for more options.")
        return

    meta, macros = load_config(CONFIG_PATH)
    target_device_name = meta.get('target_device_name')

    if not target_device_name:
        print("[!] 'target_device_name' not specified in configuration.")
        return

    keyboards = detect_keyboards(target_device_name)
    if not keyboards:
        return

    is_paused = False
    is_running = True

    def stop_service(icon, item):
        nonlocal is_running
        print("Stopping the service...")
        is_running = False
        icon.stop()

    def pause_service(icon, item):
        nonlocal is_paused
        print("Pausing the service...")
        is_paused = True

    def resume_service(icon, item):
        nonlocal is_paused
        print("Resuming the service...")
        is_paused = False

    run_tray_icon(stop_service, pause_service, resume_service)

    print(f"\nMacro Pad active for {target_device_name}... (Ctrl+C to exit)\n")
    while is_running:
        if is_paused:
            continue

        r, _, _ = select(keyboards, [], [])
        for dev in r:
            for event in dev.read():
                if event.type == ecodes.EV_KEY:
                    keyevent = categorize(event)
                    if keyevent.keystate == 1:  # Key down
                        execute_macro(keyevent.keycode, macros)

if __name__ == "__main__":
    cli()
