# -*- coding: utf-8 -*-
import questionary
from rich.console import Console
import typer
import os
import subprocess
from pathlib import Path

# Importar funciones de menú de las apps
from orgm.apps.env_app import env_menu
from orgm.apps.pdf_app import pdf_menu
from orgm.apps.ai_app import ai_menu
from orgm.apps.pago_app import pago_menu
# Importar el módulo de búsqueda de RNC (si es necesario, aunque find-company es ahora directo)
# from orgm.apps.rnc_app import rnc_menu # Ya no se necesita rnc_menu aquí

# Crear consola para salida con Rich
console = Console()

def menu_principal():
    """Muestra un menú interactivo para los comandos principales de orgm."""
    console.print("[bold blue]===== ORGM CLI - Menú Principal =====[/bold blue]")
    
    # Definimos las categorías de comandos disponibles
    main_opciones = [
        {"name": "🧩 Administración", "value": "adm"},
        {"name": "🧮 Cálculos", "value": "calc"},
        {"name": "🔑 Configuracion", "value": "cfg"},
        {"name": "🔍 Utilidades", "value": "util"},
        {"name": "❓ Ayuda", "value": "help"},
        {"name": "❌ Salir", "value": "exit"}
    ]

    administracion = [
        {"name": "🧩 Clientes", "value": "client"},
        {"name": "📋 Proyectos", "value": "project"},
        {"name": "💰 Cotizaciones", "value": "quotation"},
        {"name": "💰 Presupuestos", "value": "presupuesto"},
        {"name": "💵 Pagos", "value": pago_menu}, # Devolver la función pago_menu
        {"name": "💰 Facturas de Venta", "value": "factura_venta"},
        {"name": "💰 Facturas de Compra", "value": "factura_compra"},
        {"name": "💰 Facturas de Compras a Personas", "value": "cfactura_compra_persona"},
        {"name": "💰 Facturas de Compras Menores", "value": "cfactura_compra_menor"},
        {"name": "🧾 Comprobantes", "value": "comprobante"},
        {"name": "👤 Personas Fisicas", "value": "persona_fisica"},
        {"name": "🏢 Proveedores", "value": "proveedor"},
        {"name": "🏢 Empleados", "value": "empleado"},
        {"name": "🔄 Volver al menú principal", "value": "main-menu"},
    ]

    calculos = [
        {"name": "🧮 Calculo de Breaker", "value": "breaker"},
        {"name": "🧮 Calculo de Cable", "value": "cable"},
        {"name": "🧮 Calculo de Sistema de Puesta a Tierra", "value": "spt"},
        {"name": "🔄 Volver al menú principal", "value": "main-menu"},
    ]

    configuracion = [
        {"name": "🔑 Variables de entorno", "value": env_menu}, # Devolver la función env_menu
        {"name": "🔄 Volver al menú principal", "value": "main-menu"},
    ]
    
    utilidades = [
        {"name": "🐳 Docker", "value": "docker"},
        {"name": "📄 Operaciones PDF", "value": pdf_menu}, # Devolver la función pdf_menu
        {"name": "🔍 Buscar empresa (RNC)", "value": "find-company"}, # Comando directo
        {"name": "💱 Tasa de divisa", "value": "currency-rate"}, # Comando directo
        {"name": "🔄 Actualizar", "value": "update"}, # Comando directo
        {"name": "⚙️ Verificar URLs", "value": "check"}, # Comando directo
        {"name": "🤖 Inteligencia Artificial", "value": ai_menu}, # Devolver la función ai_menu
        {"name": "🔄 Volver al menú principal", "value": "main-menu"},
    ]

    # --- Lógica principal del menú --- 
    while True:
        seleccion_categoria = questionary.select(
            "Seleccione una categoría:",
            choices=[opcion["name"] for opcion in main_opciones],
            use_indicator=True,
            use_shortcuts=True
        ).ask()
        
        if seleccion_categoria is None: return "exit" # Ctrl+C
        
        categoria_value = next(opcion["value"] for opcion in main_opciones if opcion["name"] == seleccion_categoria)

        if categoria_value == "exit": return "exit"
        if categoria_value == "help":
            mostrar_ayuda()
            continue # Volver a mostrar el menú principal

        # Seleccionar la lista de opciones de la categoría
        opciones_categoria = []
        if categoria_value == "adm": opciones_categoria = administracion
        elif categoria_value == "calc": opciones_categoria = calculos
        elif categoria_value == "cfg": opciones_categoria = configuracion
        elif categoria_value == "util": opciones_categoria = utilidades
        else: continue # Categoría no válida, volver a mostrar

        # Mostrar submenú de la categoría
        seleccion_opcion = questionary.select(
            f"Seleccione una opción de '{seleccion_categoria}':",
            choices=[opcion["name"] for opcion in opciones_categoria],
            use_indicator=True,
            use_shortcuts=True
        ).ask()

        if seleccion_opcion is None: return "exit" # Ctrl+C

        # Obtener el valor (puede ser string o función)
        valor_seleccionado = next(opcion["value"] for opcion in opciones_categoria if opcion["name"] == seleccion_opcion)

        if valor_seleccionado == "main-menu":
            continue # Volver a mostrar el menú principal
        else:
            # Devolver la cadena del comando o la función del submenú
            return valor_seleccionado 

# --- Fin Lógica principal del menú --- 

def mostrar_ayuda():
    """Muestra el contenido del archivo comandos.md"""
    try:
        # Obtener la ruta del script actual
        script_dir = Path(__file__).parent
        # Construir la ruta al archivo comandos.md (está en el directorio principal de orgm)
        orgm_dir = script_dir.parent # Subir un nivel desde 'commands' a 'orgm'
        comandos_path = orgm_dir / "comandos.md"
        
        # Leer y mostrar el archivo
        with open(comandos_path, "r", encoding="utf-8") as f:
            contenido = f.read()
        console.print(contenido)
    except Exception as e:
        console.print(f"[bold red]Error al mostrar la ayuda: {e}[/bold red]")

if __name__ == "__main__":
    # Para pruebas
    resultado = menu_principal()
    console.print(f"Resultado: {resultado}") 