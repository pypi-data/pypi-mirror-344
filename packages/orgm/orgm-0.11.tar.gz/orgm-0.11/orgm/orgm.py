# -*- coding: utf-8 -*-
# Main ORGM CLI application
import os
import sys
import typer
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from typing import Callable

from orgm.apps.clientes import clientes as clientes_app
from orgm.apps.proyectos import proyecto as proyecto_app
from orgm.apps.cotizaciones import cotizacion as cotizacion_app
from orgm.apps.docker import docker as docker_app
from orgm.apps.rnc_app import rnc_app

from orgm.apps.env_app import env_app 
from orgm.apps.pdf_app import pdf_app 
from orgm.apps.ai_app import ai_app 
from orgm.apps.pago_app import pago_app 

from orgm.commands.base import base_app
from orgm.commands.api_commands import api_app
from orgm.commands.menu import menu_principal


console = Console()

# Clase principal que maneja la aplicación CLI
class OrgmCLI:
    def __init__(self):
        # Crear la aplicación Typer
        self.app = typer.Typer(
            context_settings={"help_option_names": ["-h", "--help"]},
            no_args_is_help=False, # Evita la ayuda predeterminada de Typer sin argumentos
            add_completion=True # Opcional: deshabilitar la autocompletación si no se usa
        )
        # Añadir todos los módulos usando add_typer
        self.app.add_typer(env_app, name="env")
        self.app.add_typer(pdf_app, name="pdf")
        self.app.add_typer(ai_app, name="ai")
        self.app.add_typer(pago_app, name="payment")
        self.app.add_typer(clientes_app, name="client")
        self.app.add_typer(proyecto_app, name="project")
        self.app.add_typer(cotizacion_app, name="quotation")
        self.app.add_typer(docker_app, name="docker")
        self.app.add_typer(base_app, name="base")
        self.app.add_typer(api_app, name="api")
        self.app.add_typer(rnc_app, name="find-company")
        
        # Configurar el callback principal
        self.configurar_callback()
        
        # Cargar variables de entorno
        self.cargar_variables_entorno()

    def configurar_callback(self) -> None:
        """Configura el callback principal para mostrar el menú interactivo."""
        @self.app.callback(invoke_without_command=True)
        def main_callback(ctx: typer.Context):
            """
            Si no se invoca ningún subcomando, muestra el menú interactivo.
            """
            if ctx.invoked_subcommand is None:
                while True:
                    # Mostrar el menú interactivo
                    resultado = menu_principal() # Puede devolver función, str o "exit"

                    if resultado == "exit":
                        break
                    elif resultado is None or resultado == "error":
                        break # Salir en caso de error o Ctrl+C en el menú

                    elif callable(resultado):
                        # Si es una función de menú, ejecutar el submenú
                        self.ejecutar_submenu(resultado)
                        continue # Volver al menú principal después del submenú

                    elif isinstance(resultado, str):
                        # Si es una cadena, ejecutar como comando
                        try:
                            comando_args = resultado.split()
                            args_originales = sys.argv.copy()
                            sys.argv = [sys.argv[0]] + comando_args
                            self.app() # Ejecutar el comando Typer
                            sys.argv = args_originales
                        except Exception as e:
                            console.print(f"[bold red]Error al ejecutar el comando '{resultado}': {e}[/bold red]")
                            input("\nPresione Enter para continuar...")
                        continue # Volver al menú principal después del comando
                    
                    else:
                        # Caso inesperado
                        console.print(f"[bold red]Error inesperado: Tipo de resultado desconocido del menú: {type(resultado)}[/bold red]")
                        break

    def ejecutar_submenu(self, submenu_func: Callable):
        """Ejecuta un submenú (función) y maneja su resultado para la navegación."""
        try:
            resultado_submenu = submenu_func() # Ejecutar la función de menú (e.g., pdf_menu())
            
            # Si el submenú devuelve un comando (string), ejecutarlo
            if isinstance(resultado_submenu, str) and resultado_submenu not in ["exit", "error"]:
                comando_args = resultado_submenu.split()
                args_originales = sys.argv.copy()
                sys.argv = [sys.argv[0]] + comando_args
                self.app() # Ejecutar el comando devuelto por el submenú
                sys.argv = args_originales
            # Si devuelve "exit" o "error", simplemente volvemos al bucle principal (o salimos si es "exit")
            # Si devuelve None (por ejemplo, Ctrl+C dentro del submenú), también volvemos

        except Exception as e:
            console.print(f"[bold red]Error en el submenú {submenu_func.__name__}: {e}[/bold red]")
            input("\nPresione Enter para continuar...")

    def cargar_variables_entorno(self) -> None:
        """Cargar variables de entorno desde un archivo .env"""
        # Find .env file relative to the main script or project root
        # This assumes orgm.py is in the 'orgm' directory
        project_root = Path(__file__).parent.parent
        dotenv_path = project_root / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path, override=True)
        else:
            # Try loading from current working directory as fallback
            load_dotenv(override=True)
            if not Path(".env").exists():
                # No .env found, run env edit command
                console.print("[yellow]No se encontró archivo .env. Ejecutando 'orgm env edit'...[/yellow]")
                args_originales = sys.argv.copy()
                sys.argv = [sys.argv[0], "env", "edit"] 
                self.app()
                sys.argv = args_originales

# Inicializar y ejecutar la CLI 
def main():
    # Crear instancia de la CLI
    cli = OrgmCLI()
    # Ejecutar la aplicación Typer y manejar interrupciones de usuario
    try:
        cli.app()
    except (KeyboardInterrupt, EOFError):
        console.print("[bold yellow]Saliendo...[/bold yellow]")
        sys.exit(0)

if __name__ == "__main__":
    main() 