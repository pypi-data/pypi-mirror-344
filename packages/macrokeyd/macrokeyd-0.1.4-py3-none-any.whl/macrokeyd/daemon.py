import sys
import click
from macrokeyd import __version__
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select
from macrokeyd.config_loader import load_config
from macrokeyd import actions
import os

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
            print(f"[+] Se copió configuración por defecto en {config_path}")
        else:
            print(f"[!] No se encontró archivo de configuración por defecto en {default_path}")

CONFIG_PATH = get_config_path()
ensure_config_exists(CONFIG_PATH)

def detectar_teclados(target_device_name):
    teclados = []
    for path in list_devices():
        device = InputDevice(path)
        capabilities = device.capabilities()

        if ecodes.EV_KEY in capabilities and ecodes.EV_REL not in capabilities:
            if device.name == target_device_name:
                try:
                    device.grab()
                    print(f"[+] Grab exclusivo: {device.name} ({device.path})")
                    teclados.append(device)
                except OSError as e:
                    print(f"[!] No se pudo hacer grab a {device.name}: {e}")
    return teclados

def ejecutar_macro(keycode, macros):
    macro = macros.get(keycode)
    if not macro:
        print(f"[!] Tecla {keycode} no asignada.")
        return

    action_type = macro.get('action')
    value = macro.get('value')

    print(f"[MACRO] Ejecutando {action_type}: {value}")

    if action_type == 'command':
        actions.execute_command(value)
    elif action_type == 'text':
        actions.write_text(value)
    else:
        print(f"[!] Tipo de acción desconocido: {action_type}")

@click.command()
@click.option('--version', is_flag=True, help='Mostrar la versión y salir.')
@click.option('--run', is_flag=True, help='Ejecutar el macro daemon.')
def cli(version, run):
    if version:
        print(f"macrokeyd {__version__}")
        return

    if not run:
        print("Usa --run para iniciar el daemon, o --help para más opciones.")
        return

    meta, macros = load_config(CONFIG_PATH)
    target_device_name = meta.get('target_device_name')

    if not target_device_name:
        print("[!] No se especificó 'target_device_name' en la configuración.")
        return

    teclados = detectar_teclados(target_device_name)
    if not teclados:
        print("No se detectaron teclados compatibles.")
        return

    print(f"\nMacro Pad activo para {target_device_name}... (Ctrl+C para salir)\n")
    while True:
        r, _, _ = select(teclados, [], [])
        for dev in r:
            for event in dev.read():
                if event.type == ecodes.EV_KEY:
                    keyevent = categorize(event)
                    if keyevent.keystate == 1:  # Key down
                        ejecutar_macro(keyevent.keycode, macros)

if __name__ == "__main__":
    cli()
