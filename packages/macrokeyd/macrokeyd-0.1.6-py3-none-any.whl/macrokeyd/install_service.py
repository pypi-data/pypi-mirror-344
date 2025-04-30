import subprocess
import os
import sys
import platform
import click

@click.command()
def cli():
    """Instala el servicio macrokeyd en systemd (Linux)."""
    if platform.system() != "Linux":
        click.echo("Error: macrokeyd solo puede instalarse como servicio en sistemas Linux.")
        sys.exit(1)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, '..', 'scripts', 'install_service.sh')
    script_path = os.path.normpath(script_path)

    if not os.path.exists(script_path):
        click.echo(f"Error: no se encuentra el script {script_path}")
        sys.exit(2)

    click.echo("Instalando servicio macrokeyd...")
    subprocess.run(['sudo', 'bash', script_path])

if __name__ == "__main__":
    cli()