#!/usr/bin/env python3
"""
LPC Batch Processor & Utility Tools
====================================
Herramientas adicionales para procesamiento batch y utilidades.

Características:
  - Procesamiento de múltiples sprites en lotes
  - Información detallada de sprites
  - Comparación entre sprites
  - Generación de reportes
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# BATCH PROCESSOR
# ============================================================================
class BatchProcessor:
    """Procesa múltiples sprites de una vez."""

    def __init__(self, input_directory: str, output_directory: str = None):
        """
        Inicializa el procesador batch.

        Args:
            input_directory: Directorio con sprites
            output_directory: Directorio de salida (default: input_directory/output)
        """
        self.input_dir = Path(input_directory)
        self.output_dir = Path(output_directory) if output_directory else self.input_dir / "output"

        if not self.input_dir.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {input_directory}")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Procesador batch inicializado: {self.input_dir}")

    def find_sprites(self, pattern: str = "*.png") -> List[Path]:
        """
        Encuentra todos los PNG en el directorio.

        Args:
            pattern: Patrón de búsqueda (default: *.png)

        Returns:
            List[Path]: Lista de sprites encontrados
        """
        sprites = list(self.input_dir.glob(pattern))
        logger.info(f"Encontrados {len(sprites)} sprites")
        return sprites

    def process_batch(self, sprites: List[Path], prefix_template: str = None) -> List[Dict]:
        """
        Procesa un lote de sprites.

        Args:
            sprites: Lista de rutas a sprites
            prefix_template: Template para prefijo (e.g., "{stem}_atlas")

        Returns:
            List[Dict]: Resultados del procesamiento
        """
        from lpc_atlas_generator import LPCAtlasGenerator

        results = []

        for i, sprite_path in enumerate(sprites, 1):
            try:
                logger.info(f"\n[{i}/{len(sprites)}] Procesando: {sprite_path.name}")

                # Generar prefijo
                prefix = prefix_template or f"{sprite_path.stem}_atlas"

                # Generar atlas
                generator = LPCAtlasGenerator(str(sprite_path), str(self.output_dir))
                png_path, json_path = generator.generate_complete_atlas(prefix=prefix)

                if png_path and json_path:
                    results.append({
                        'source': sprite_path.name,
                        'status': 'success',
                        'prefix': prefix,
                        'png': Path(png_path).name,
                        'json': Path(json_path).name,
                        'output_dir': str(self.output_dir)
                    })
                    logger.info(f"✓ {sprite_path.name} procesado exitosamente")
                else:
                    results.append({
                        'source': sprite_path.name,
                        'status': 'error',
                        'error': 'Atlas generation failed'
                    })
                    logger.error(f"✗ Error procesando {sprite_path.name}")

            except Exception as e:
                results.append({
                    'source': sprite_path.name,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"✗ Excepción en {sprite_path.name}: {e}")

        return results

    def export_batch_report(self, results: List[Dict], output_file: str = None) -> str:
        """
        Exporta reporte de procesamiento batch.

        Args:
            results: Resultados del batch
            output_file: Archivo de salida (default: batch_report.json)

        Returns:
            str: Ruta del archivo generado
        """
        if output_file is None:
            output_file = str(self.output_dir / "batch_report.json")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': str(Path.cwd()),
                'total_processed': len(results),
                'successful': sum(1 for r in results if r['status'] == 'success'),
                'failed': sum(1 for r in results if r['status'] == 'error'),
                'results': results
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"Reporte guardado: {output_file}")
        return output_file


# ============================================================================
# SPRITE INFORMATION ANALYZER
# ============================================================================
class SpriteAnalyzer:
    """Analiza información detallada de sprites."""

    @staticmethod
    def analyze(sprite_path: str) -> Dict[str, Any]:
        """
        Analiza un sprite completo.

        Returns:
            Dict: Información detallada
        """
        from PIL import Image
        import numpy as np

        path = Path(sprite_path)

        try:
            img = Image.open(path)
            width, height = img.size

            # Estadísticas de color
            if img.mode == 'RGBA':
                data = np.array(img)
                alpha_channel = data[:, :, 3]
                transparent_pixels = np.sum(alpha_channel == 0)
            else:
                transparent_pixels = 0

            # Tamaño de archivo
            file_size = path.stat().st_size

            return {
                'filename': path.name,
                'path': str(path),
                'format': img.format,
                'mode': img.mode,
                'dimensions': {
                    'width': width,
                    'height': height,
                    'total_pixels': width * height
                },
                'file_info': {
                    'size_bytes': file_size,
                    'size_kb': file_size / 1024,
                    'size_mb': file_size / (1024 * 1024)
                },
                'transparency': {
                    'transparent_pixels': int(transparent_pixels),
                    'transparency_percentage': (transparent_pixels / (width * height) * 100) if (width * height) > 0 else 0
                },
                'lpc_validation': SpriteAnalyzer._validate_lpc_format(width, height)
            }

        except Exception as e:
            return {'error': str(e), 'filename': path.name}

    @staticmethod
    def _validate_lpc_format(width: int, height: int) -> Dict[str, Any]:
        """Valida contra formato LPC."""
        cell_size = 64

        is_valid_width = width % cell_size == 0
        is_valid_height = height % cell_size == 0

        return {
            'valid_width': is_valid_width,
            'valid_height': is_valid_height,
            'is_valid_lpc': is_valid_width and is_valid_height,
            'cells': {
                'columns': width // cell_size if is_valid_width else width / cell_size,
                'rows': height // cell_size if is_valid_height else height / cell_size,
                'total_frames': (width // cell_size) * (height // cell_size) if (is_valid_width and is_valid_height) else None
            }
        }


# ============================================================================
# SPRITE COMPARATOR
# ============================================================================
class SpriteComparator:
    """Compara múltiples sprites."""

    @staticmethod
    def compare_sprites(sprite_paths: List[str]) -> Dict[str, Any]:
        """
        Compara características de múltiples sprites.

        Returns:
            Dict: Comparación detallada
        """
        analyzer = SpriteAnalyzer()
        sprites_info = []

        for sprite_path in sprite_paths:
            info = analyzer.analyze(sprite_path)
            sprites_info.append(info)

        return {
            'count': len(sprites_info),
            'sprites': sprites_info,
            'summary': SpriteComparator._generate_summary(sprites_info)
        }

    @staticmethod
    def _generate_summary(sprites_info: List[Dict]) -> Dict[str, Any]:
        """Genera resumen de comparación."""
        if not sprites_info:
            return {}

        widths = [s['dimensions']['width'] for s in sprites_info if 'dimensions' in s]
        heights = [s['dimensions']['height'] for s in sprites_info if 'dimensions' in s]
        sizes = [s['file_info']['size_bytes'] for s in sprites_info if 'file_info' in s]

        return {
            'dimensions': {
                'widths': widths,
                'heights': heights,
                'all_same_size': len(set(zip(widths, heights))) == 1 if widths and heights else False
            },
            'file_sizes': {
                'sizes_bytes': sizes,
                'total_bytes': sum(sizes) if sizes else 0,
                'total_mb': sum(sizes) / (1024 * 1024) if sizes else 0,
                'average_bytes': sum(sizes) / len(sizes) if sizes else 0
            }
        }


# ============================================================================
# REPORT GENERATOR
# ============================================================================
class ReportGenerator:
    """Genera reportes en diferentes formatos."""

    @staticmethod
    def generate_csv_report(sprites_info: List[Dict], output_file: str) -> str:
        """
        Genera reporte en CSV.

        Args:
            sprites_info: Información de sprites
            output_file: Archivo de salida

        Returns:
            str: Ruta del archivo generado
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Filename', 'Width', 'Height', 'Format', 'Size (KB)',
                'Transparent Pixels', 'Transparency %', 'Valid LPC'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for sprite in sprites_info:
                if 'error' not in sprite:
                    writer.writerow({
                        'Filename': sprite['filename'],
                        'Width': sprite['dimensions']['width'],
                        'Height': sprite['dimensions']['height'],
                        'Format': sprite['format'],
                        'Size (KB)': f"{sprite['file_info']['size_kb']:.2f}",
                        'Transparent Pixels': sprite['transparency']['transparent_pixels'],
                        'Transparency %': f"{sprite['transparency']['transparency_percentage']:.2f}",
                        'Valid LPC': 'Yes' if sprite['lpc_validation']['is_valid_lpc'] else 'No'
                    })

        logger.info(f"Reporte CSV guardado: {output_file}")
        return output_file

    @staticmethod
    def generate_html_report(sprites_info: List[Dict], output_file: str) -> str:
        """
        Genera reporte en HTML.

        Args:
            sprites_info: Información de sprites
            output_file: Archivo de salida

        Returns:
            str: Ruta del archivo generado
        """
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>LPC Sprite Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .valid { color: green; font-weight: bold; }
        .invalid { color: red; font-weight: bold; }
        h1 { color: #333; }
        .summary { background-color: #f0f0f0; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>LPC Sprite Sheet Analysis Report</h1>
'''

        # Tabla de sprites
        html += '<h2>Sprite Details</h2>'
        html += '<table>'
        html += '<tr><th>Filename</th><th>Dimensions</th><th>Format</th><th>Size</th><th>Transparency</th><th>Valid LPC</th></tr>'

        for sprite in sprites_info:
            if 'error' not in sprite:
                valid_class = 'valid' if sprite['lpc_validation']['is_valid_lpc'] else 'invalid'
                valid_text = 'Yes' if sprite['lpc_validation']['is_valid_lpc'] else 'No'

                html += f'''
    <tr>
        <td>{sprite['filename']}</td>
        <td>{sprite['dimensions']['width']}x{sprite['dimensions']['height']}</td>
        <td>{sprite['format']}</td>
        <td>{sprite['file_info']['size_kb']:.2f} KB</td>
        <td>{sprite['transparency']['transparency_percentage']:.2f}%</td>
        <td class="{valid_class}">{valid_text}</td>
    </tr>
'''

        html += '</table>'
        html += '</body></html>'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"Reporte HTML guardado: {output_file}")
        return output_file


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def analyze_sprite(sprite_path: str) -> None:
    """Analiza un sprite individual."""
    analyzer = SpriteAnalyzer()
    info = analyzer.analyze(sprite_path)

    print("\n" + "=" * 70)
    print(f"ANÁLISIS DE SPRITE: {info.get('filename', 'Unknown')}")
    print("=" * 70)

    for key, value in info.items():
        if key != 'path':
            print(f"\n{key.upper()}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {value}")

def compare_batch(directory: str) -> None:
    """Compara todos los sprites en un directorio."""
    batch = BatchProcessor(directory)
    sprites = batch.find_sprites()

    comparator = SpriteComparator()
    comparison = comparator.compare_sprites([str(s) for s in sprites])

    print("\n" + "=" * 70)
    print("COMPARACIÓN DE SPRITES")
    print("=" * 70)
    print(f"\nTotal de sprites: {comparison['count']}")
    print(f"\nResumen:")

    summary = comparison['summary']
    if 'dimensions' in summary:
        print(f"  Tamaños únicos: {len(set(zip(summary['dimensions']['widths'], summary['dimensions']['heights'])))}")
        print(f"  Todos del mismo tamaño: {'Sí' if summary['dimensions']['all_same_size'] else 'No'}")

    if 'file_sizes' in summary:
        print(f"  Tamaño total: {summary['file_sizes']['total_mb']:.2f} MB")
        print(f"  Promedio por sprite: {summary['file_sizes']['average_bytes'] / 1024:.2f} KB")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'analyze' and len(sys.argv) > 2:
            analyze_sprite(sys.argv[2])
        elif command == 'compare' and len(sys.argv) > 2:
            compare_batch(sys.argv[2])
        else:
            print("Uso:")
            print("  python lpc_utils.py analyze <sprite_path>")
            print("  python lpc_utils.py compare <directory>")
    else:
        print("Uso:")
        print("  python lpc_utils.py analyze <sprite_path>")
        print("  python lpc_utils.py compare <directory>")

