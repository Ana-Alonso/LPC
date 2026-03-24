#!/usr/bin/env python3
"""
LPC Sprite Sheet to Phaser 3 Atlas - Complete Pipeline
========================================================

Script principal que ejecuta el pipeline completo de conversión
de LPC Sprite Sheets a Texture Atlas para Phaser 3.

Uso:
    python lpc_process.py [--sprite RUTA] [--prefix NOMBRE] [--tolerance NUM]

Ejemplos:
    python lpc_process.py
    python lpc_process.py --sprite src/assets/character-spritesheet.png --prefix my_atlas
    python lpc_process.py --tolerance 15
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================================================
# IMPORTACIONES
# ============================================================================
try:
    from lpc_atlas_generator import LPCAtlasGenerator
    from lpc_atlas_advanced import SpriteSheetValidator, AtlasStatisticsGenerator
    from lpc_integration_manager import LPCIntegrationManager
except ImportError as e:
    logger.error(f"Error de importación: {e}")
    logger.error("Asegúrate de tener todos los módulos Python necesarios:")
    logger.error("  - opencv-python (cv2)")
    logger.error("  - Pillow (PIL)")
    print("\nInstala con:")
    print("  pip install opencv-python Pillow")
    sys.exit(1)

# ============================================================================
# FUNCIONES DE DIÁLOGOS GRÁFICOS
# ============================================================================
def select_sprite_file(initial_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Abre un explorador de archivos para seleccionar el sprite sheet PNG.

    Args:
        initial_dir: Directorio inicial del explorador

    Returns:
        Path al archivo seleccionado o None si se cancela
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    root.attributes('-topmost', True)  # Poner ventana al frente

    try:
        if initial_dir is None:
            initial_dir = Path.cwd()

        file_path = filedialog.askopenfilename(
            title="Selecciona el Sprite Sheet PNG",
            initialdir=str(initial_dir),
            filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")],
            defaultextension=".png"
        )

        if file_path:
            return Path(file_path)
        return None

    finally:
        root.destroy()

def select_output_directory(initial_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Abre un explorador de carpetas para seleccionar el directorio de salida.

    Args:
        initial_dir: Directorio inicial del explorador

    Returns:
        Path al directorio seleccionado o None si se cancela
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    root.attributes('-topmost', True)  # Poner ventana al frente

    try:
        if initial_dir is None:
            initial_dir = Path.cwd()

        dir_path = filedialog.askdirectory(
            title="Selecciona la carpeta para guardar el atlas",
            initialdir=str(initial_dir)
        )

        if dir_path:
            return Path(dir_path)
        return None

    finally:
        root.destroy()

def get_atlas_prefix(default: str = "lpc_atlas") -> Optional[str]:
    """
    Abre un diálogo para ingresar el prefijo del atlas.

    Args:
        default: Valor por defecto

    Returns:
        Prefijo ingresado o None si se cancela
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    try:
        result = simpledialog.askstring(
            "Prefijo del Atlas",
            f"Ingresa el prefijo para los archivos generados:\n(Default: {default})",
            initialvalue=default
        )
        return result
    finally:
        root.destroy()

def get_tolerance_value(default: int = 20) -> Optional[int]:
    """
    Abre un diálogo para ingresar el valor de tolerancia.

    Args:
        default: Valor por defecto (0-255)

    Returns:
        Valor de tolerancia o None si se cancela
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    try:
        while True:
            result = simpledialog.askinteger(
                "Tolerancia",
                f"Tolerancia para conversión a transparencia (0-255):\n(Default: {default})",
                initialvalue=default,
                minvalue=0,
                maxvalue=255
            )
            if result is None:
                return None
            if 0 <= result <= 255:
                return result
            else:
                messagebox.showerror("Error", "La tolerancia debe estar entre 0 y 255")
    finally:
        root.destroy()

def show_info_message(title: str, message: str):
    """Muestra un mensaje de información."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    try:
        messagebox.showinfo(title, message)
    finally:
        root.destroy()

def show_error_message(title: str, message: str):
    """Muestra un mensaje de error."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    try:
        messagebox.showerror(title, message)
    finally:
        root.destroy()

# ============================================================================
# PARSER DE ARGUMENTOS
# ============================================================================
def create_argument_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos de línea de comandos."""

    parser = argparse.ArgumentParser(
        description='LPC Sprite Sheet to Phaser 3 Texture Atlas Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos de uso:

  # Usar sprite sheet por defecto
  python lpc_process.py

  # Especificar ruta del sprite
  python lpc_process.py --sprite src/assets/my-sprite.png

  # Personalizar prefijo del atlas
  python lpc_process.py --prefix character_atlas

  # Ajustar tolerancia de transparencia
  python lpc_process.py --tolerance 25

  # Combinado
  python lpc_process.py --sprite src/assets/hero.png --prefix hero_atlas --tolerance 20

Para más información, ver README.md
        '''
    )

    parser.add_argument(
        '--sprite',
        type=str,
        default=None,
        help='Ruta al sprite sheet PNG (default: busca automáticamente)'
    )

    parser.add_argument(
        '--prefix',
        type=str,
        default='lpc_atlas',
        help='Prefijo para los archivos generados (default: lpc_atlas)'
    )

    parser.add_argument(
        '--tolerance',
        type=int,
        default=20,
        help='Umbral de tolerancia para conversión a transparencia (0-255, default: 20)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Directorio de salida (default: mismo directorio del sprite)'
    )

    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Solo validar sin generar atlas'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Modo verbose (más detalles)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='LPC Atlas Generator v1.0.0'
    )

    return parser

# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================
def print_header():
    """Imprime encabezado del programa."""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    LPC SPRITE SHEET TO PHASER 3 ATLAS                      ║
║                            Generator v1.0.0                                ║
║                                                                            ║
║  Conversión profesional de Liberated Pixel Cup Sprite Sheets a Texture     ║
║  Atlas compatible con Phaser 3, con pivotes inteligentes y colisiones      ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)

def find_project_root() -> Path:
    """Encuentra la raíz del proyecto."""
    current = Path.cwd()

    # Buscar indicadores de proyecto (package.json, tsconfig.json, etc.)
    while current != current.parent:
        if (current / 'package.json').exists():
            return current
        if (current / 'src').exists() and (current / 'tsconfig.json').exists():
            return current
        current = current.parent

    return Path.cwd()

def validate_sprite_file(sprite_path: Path) -> bool:
    """Valida que el sprite sea una imagen PNG válida."""

    if not sprite_path.exists():
        logger.error(f"✗ Archivo no encontrado: {sprite_path}")
        return False

    if sprite_path.suffix.lower() != '.png':
        logger.error(f"✗ El archivo debe ser PNG: {sprite_path}")
        return False

    try:
        from PIL import Image
        img = Image.open(sprite_path)
        width, height = img.size

        if width < 64 or height < 64:
            logger.error(f"✗ El sprite es muy pequeño ({width}x{height}). Mínimo 64x64")
            return False

        logger.info(f"✓ Sprite válido: {sprite_path.name} ({width}x{height})")
        return True

    except Exception as e:
        logger.error(f"✗ Error al validar sprite: {e}")
        return False

def run_validation_only(sprite_path: Path) -> bool:
    """Ejecuta solo la validación del sprite."""

    logger.info("=" * 70)
    logger.info("MODO VALIDACIÓN - Sin generar atlas")
    logger.info("=" * 70 + "\n")

    if not validate_sprite_file(sprite_path):
        return False

    try:
        from PIL import Image
        img = Image.open(sprite_path)
        width, height = img.size

        validator = SpriteSheetValidator()
        validation = validator.validate_dimensions(width, height)

        logger.info("\nResultado de validación:")
        logger.info(f"  Dimensiones originales: {width}x{height}")

        for warning in validation['warnings']:
            logger.warning(f"  ⚠ {warning}")

        analysis = validation['analysis']
        logger.info(f"\n  Análisis:")
        logger.info(f"    - Células: {analysis['columns']}x{analysis['rows']}")
        logger.info(f"    - Total frames: {analysis['totalFrames']}")
        logger.info(f"    - Tamaño célula: {analysis['cellSize']}x{analysis['cellSize']}")

        if validation['valid']:
            logger.info("\n  ✓ Validación EXITOSA")
            return True
        else:
            logger.warning("\n  ⚠ Validación completada con advertencias")
            return True

    except Exception as e:
        logger.error(f"Error durante validación: {e}")
        return False

def run_full_pipeline(sprite_path: Path,
                     output_dir: Optional[Path] = None,
                     prefix: str = 'lpc_atlas',
                     tolerance: int = 20,
                     verbose: bool = False) -> bool:
    """Ejecuta el pipeline completo."""

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("=" * 70)
    logger.info("INICIANDO PIPELINE COMPLETO")
    logger.info("=" * 70 + "\n")

    if not validate_sprite_file(sprite_path):
        return False

    # Validar tolerancia
    if not (0 <= tolerance <= 255):
        logger.error(f"✗ Tolerancia debe estar entre 0 y 255 (ingresado: {tolerance})")
        return False

    try:
        # Crear generador
        output_dir = output_dir or sprite_path.parent
        generator = LPCAtlasGenerator(str(sprite_path), str(output_dir))

        # Generar atlas
        png_path, json_path = generator.generate_complete_atlas(
            tolerance=tolerance,
            prefix=prefix
        )

        if png_path is None or json_path is None:
            logger.error("✗ Error al generar atlas")
            return False

        # Generar estadísticas
        logger.info("\n" + "=" * 70)
        logger.info("GENERANDO ESTADÍSTICAS")
        logger.info("=" * 70 + "\n")

        import json as json_module
        with open(json_path, 'r', encoding='utf-8') as f:
            atlas_data = json_module.load(f)

        frames = atlas_data['textures'][0]['frames']
        stats = AtlasStatisticsGenerator.generate_stats(
            frames,
            atlas_data['meta']['size']['w'],
            atlas_data['meta']['size']['h']
        )

        logger.info("Estadísticas del Atlas:")
        logger.info(f"  Frames totales: {stats['general']['totalFrames']}")
        logger.info(f"  Dimensiones: {stats['general']['atlasWidth']}x{stats['general']['atlasHeight']}")
        logger.info(f"  Cobertura: {stats['coverage']['coveragePercentage']:.1f}%")
        logger.info(f"  Memoria estimada: {stats['memory']['atlasMemoryMB']:.2f} MB")
        logger.info(f"\n  Animaciones detectadas:")
        for anim_name, count in stats['animations'].items():
            logger.info(f"    - {anim_name}: {count} frames")

        # Éxito
        logger.info("\n" + "=" * 70)
        logger.info("✓✓✓ PIPELINE COMPLETADO EXITOSAMENTE ✓✓✓")
        logger.info("=" * 70)
        logger.info(f"\nArchivos generados:")
        logger.info(f"  PNG:  {png_path}")
        logger.info(f"  JSON: {json_path}")

        logger.info(f"\nPróximos pasos:")
        logger.info(f"  1. Importa el atlas en tu Scene de Phaser:")
        logger.info(f"     scene.load.atlas('{prefix}', '{Path(png_path).name}', '{Path(json_path).name}');")
        logger.info(f"  2. Crea animaciones con los nombres generados (walk_down_0, etc.)")
        logger.info(f"  3. Usa los pivotes (x:0.5, y:0.9) para posicionar en pies")

        return True

    except Exception as e:
        logger.error(f"✗ Error durante el pipeline: {e}", exc_info=verbose)
        return False

# ============================================================================
# ENTRADA PRINCIPAL
# ============================================================================
def main():
    """Función principal."""

    print_header()

    # Parser de argumentos
    parser = create_argument_parser()
    args = parser.parse_args()

    # Encontrar proyecto
    project_root = find_project_root()
    logger.info(f"Proyecto encontrado en: {project_root}\n")

    # Determinar ruta del sprite - usar argumento si se proporciona, si no usar diálogo
    if args.sprite:
        sprite_path = Path(args.sprite)
        if not sprite_path.is_absolute():
            sprite_path = project_root / sprite_path
    else:
        # Intentar encontrar carpeta de assets
        assets_dir = project_root / "src" / "assets"
        initial_dir = assets_dir if assets_dir.exists() else project_root

        # Abrir diálogo gráfico para seleccionar sprite
        logger.info("\n📁 Abriendo selector de archivo...\n")
        sprite_path = select_sprite_file(initial_dir)

        if sprite_path is None:
            logger.error("✗ No se seleccionó ningún archivo. Cancelando...")
            return 1

    # Seleccionar directorio de salida usando diálogo
    output_dir = None
    if args.output:
        output_dir = Path(args.output)
    else:
        logger.info("\n📁 Abriendo selector de carpeta de salida...\n")
        output_dir = select_output_directory(sprite_path.parent)

        if output_dir is None:
            logger.warning("⚠ No se seleccionó carpeta. Se usará: " + str(sprite_path.parent))
            output_dir = sprite_path.parent

    # Solicitar prefijo del atlas
    if args.prefix == 'lpc_atlas':  # Si es el valor por defecto, preguntar
        logger.info("\n📝 Configurando prefijo del atlas...\n")
        prefix = get_atlas_prefix('lpc_atlas')
        if prefix is None:
            logger.info("Usando prefijo por defecto: lpc_atlas")
            prefix = 'lpc_atlas'
    else:
        prefix = args.prefix

    # Solicitar tolerancia
    if args.tolerance == 20:  # Si es el valor por defecto, preguntar
        logger.info("\n⚙️  Configurando tolerancia...\n")
        tolerance = get_tolerance_value(20)
        if tolerance is None:
            logger.info("Usando tolerancia por defecto: 20")
            tolerance = 20
    else:
        tolerance = args.tolerance

    # Validar tolerancia
    if not (0 <= tolerance <= 255):
        logger.error(f"✗ Tolerancia inválida: {tolerance} (debe estar entre 0 y 255)")
        return 1

    # Ejecutar
    try:
        if args.validate_only:
            success = run_validation_only(sprite_path)
        else:
            success = run_full_pipeline(
                sprite_path,
                output_dir,
                prefix,
                tolerance,
                args.verbose
            )

        if success:
            show_info_message(
                "✓ Éxito",
                f"Atlas generado exitosamente en:\n{output_dir}"
            )

        return 0 if success else 1

    except KeyboardInterrupt:
        logger.info("\n\n✗ Proceso cancelado por el usuario")
        return 1
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        logger.error(f"\n✗ {error_msg}", exc_info=args.verbose)
        show_error_message("Error", error_msg)
        return 1

if __name__ == "__main__":
    sys.exit(main())

