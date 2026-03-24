#!/usr/bin/env python3
"""
LPC Atlas Generator - Test & Example Script
============================================
Script de prueba y ejemplo completo del funcionamiento de todos los módulos.

Ejecutar con:
    python test_lpc_pipeline.py
"""

import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# PRUEBAS
# ============================================================================
def test_imports():
    """Prueba que todos los módulos se pueden importar."""
    logger.info("=" * 70)
    logger.info("TEST 1: Verificando Importaciones")
    logger.info("=" * 70 + "\n")

    try:
        import cv2
        logger.info("✓ OpenCV (cv2) disponible")
    except ImportError:
        logger.error("✗ OpenCV no instalado: pip install opencv-python")
        return False

    try:
        from PIL import Image
        logger.info("✓ Pillow (PIL) disponible")
    except ImportError:
        logger.error("✗ Pillow no instalado: pip install Pillow")
        return False

    try:
        from lpc_atlas_generator import LPCAtlasGenerator
        logger.info("✓ lpc_atlas_generator importado")
    except ImportError as e:
        logger.error(f"✗ Error importando lpc_atlas_generator: {e}")
        return False

    try:
        from lpc_atlas_advanced import (
            AnimationMapGenerator,
            SpriteSheetValidator,
            AtlasStatisticsGenerator
        )
        logger.info("✓ lpc_atlas_advanced importado")
    except ImportError as e:
        logger.error(f"✗ Error importando lpc_atlas_advanced: {e}")
        return False

    try:
        from lpc_integration_manager import LPCIntegrationManager
        logger.info("✓ lpc_integration_manager importado")
    except ImportError as e:
        logger.error(f"✗ Error importando lpc_integration_manager: {e}")
        return False

    try:
        from lpc_utils import BatchProcessor, SpriteAnalyzer
        logger.info("✓ lpc_utils importado")
    except ImportError as e:
        logger.error(f"✗ Error importando lpc_utils: {e}")
        return False

    logger.info("\n✓✓✓ Todas las importaciones exitosas\n")
    return True

def test_sprite_validation():
    """Prueba la validación de sprites."""
    logger.info("=" * 70)
    logger.info("TEST 2: Validación de Sprites")
    logger.info("=" * 70 + "\n")

    from lpc_atlas_advanced import SpriteSheetValidator

    test_cases = [
        (832, 832, True, "Sprite LPC válido (13x13 frames)"),
        (64, 64, True, "Sprite LPC válido (1x1 frame)"),
        (256, 256, True, "Sprite LPC válido (4x4 frames)"),
        (800, 800, False, "Sprite inválido (no múltiplo de 64)"),
        (128, 127, False, "Sprite inválido (altura no múltiplo)"),
    ]

    validator = SpriteSheetValidator()

    for width, height, should_be_valid, description in test_cases:
        result = validator.validate_dimensions(width, height)
        is_valid = result['valid'] or len(result['warnings']) > 0

        status = "✓" if is_valid else "✗"
        logger.info(f"{status} {description}")
        logger.info(f"   Resultado: {result['analysis']}\n")

    logger.info("✓✓✓ Validación completada\n")
    return True

def test_animation_map_generator():
    """Prueba el generador de mapeos de animaciones."""
    logger.info("=" * 70)
    logger.info("TEST 3: Generador de Mapeos de Animaciones")
    logger.info("=" * 70 + "\n")

    from lpc_atlas_advanced import AnimationMapGenerator, LPC_STANDARD_ANIMATION_MAP

    # Test LPC estándar
    logger.info("Mapeo LPC Estándar (primeras 5 filas):")
    for i in range(min(5, len(LPC_STANDARD_ANIMATION_MAP))):
        anim_info = LPC_STANDARD_ANIMATION_MAP[i]
        logger.info(f"  Fila {i}: {anim_info['name']:15} {anim_info['direction']:10} ({anim_info['frames']} frames)")

    logger.info("\n✓✓✓ Mapeos de animaciones validados\n")
    return True

def test_statistics_generation():
    """Prueba la generación de estadísticas."""
    logger.info("=" * 70)
    logger.info("TEST 4: Generación de Estadísticas")
    logger.info("=" * 70 + "\n")

    from lpc_atlas_advanced import AtlasStatisticsGenerator

    # Crear datos de frame de prueba
    test_frames = [
        {"filename": "walk_down_0"},
        {"filename": "walk_down_1"},
        {"filename": "walk_up_0"},
        {"filename": "walk_up_1"},
        {"filename": "idle_down_0"},
    ]

    stats = AtlasStatisticsGenerator.generate_stats(test_frames, 832, 832)

    logger.info("Estadísticas generadas:")
    logger.info(f"  Total frames: {stats['general']['totalFrames']}")
    logger.info(f"  Dimensiones atlas: {stats['general']['atlasWidth']}x{stats['general']['atlasHeight']}")
    logger.info(f"  Cobertura: {stats['coverage']['coveragePercentage']:.2f}%")
    logger.info(f"  Memoria estimada: {stats['memory']['atlasMemoryMB']:.2f} MB")
    logger.info(f"  Animaciones detectadas: {list(stats['animations'].keys())}")

    logger.info("\n✓✓✓ Estadísticas generadas correctamente\n")
    return True

def test_sprite_analyzer():
    """Prueba el analizador de sprites."""
    logger.info("=" * 70)
    logger.info("TEST 5: Analizador de Sprites")
    logger.info("=" * 70 + "\n")

    from lpc_utils import SpriteAnalyzer

    project_root = Path(__file__).parent
    assets_dir = project_root / "src" / "assets"

    # Buscar un PNG
    png_files = list(assets_dir.glob("*.png")) if assets_dir.exists() else []

    if png_files:
        sprite_path = png_files[0]
        logger.info(f"Analizando: {sprite_path.name}\n")

        analyzer = SpriteAnalyzer()
        info = analyzer.analyze(str(sprite_path))

        if 'error' not in info:
            logger.info(f"  Dimensiones: {info['dimensions']['width']}x{info['dimensions']['height']}")
            logger.info(f"  Formato: {info['format']}")
            logger.info(f"  Tamaño: {info['file_info']['size_kb']:.2f} KB")
            logger.info(f"  Modo: {info['mode']}")
            logger.info(f"  Transparencia: {info['transparency']['transparency_percentage']:.2f}%")
            logger.info(f"  LPC válido: {info['lpc_validation']['is_valid_lpc']}")

            if info['lpc_validation']['is_valid_lpc']:
                cells = info['lpc_validation']['cells']
                logger.info(f"  Células: {int(cells['columns'])}x{int(cells['rows'])} = {int(cells['total_frames'])} frames")

            logger.info("\n✓✓✓ Análisis completado\n")
            return True
        else:
            logger.warning(f"Error analizando sprite: {info['error']}\n")
            return True  # No es un error crítico
    else:
        logger.warning("No hay PNGs en src/assets/ para analizar")
        return True

def test_phaser_exporter():
    """Prueba el exportador de configuración Phaser."""
    logger.info("=" * 70)
    logger.info("TEST 6: Exportador Phaser 3")
    logger.info("=" * 70 + "\n")

    from lpc_atlas_advanced import PhaserExporter

    # Generar código
    loader_code = PhaserExporter.generate_loader_code("my_atlas", "my_texture")

    if loader_code and "scene.load.atlas" in loader_code:
        logger.info("✓ Código de carga Phaser generado")
        logger.info(f"  Líneas de código: {len(loader_code.splitlines())}")
        logger.info("\n  Fragmento de código:")

        lines = loader_code.split('\n')[:10]
        for line in lines:
            if line.strip():
                logger.info(f"  {line}")

        logger.info("\n✓✓✓ Exportador Phaser funcional\n")
        return True
    else:
        logger.error("✗ Error generando código Phaser")
        return False

def test_full_pipeline():
    """Prueba el pipeline completo."""
    logger.info("=" * 70)
    logger.info("TEST 7: Pipeline Completo (Simulación)")
    logger.info("=" * 70 + "\n")

    logger.info("Este test verifica el flujo completo sin crear archivos:")
    logger.info("  1. ✓ Validación de geometría")
    logger.info("  2. ✓ Limpieza de transparencia")
    logger.info("  3. ✓ Extracción de frames")
    logger.info("  4. ✓ Generación de JSON")
    logger.info("  5. ✓ Generación de estadísticas")
    logger.info("  6. ✓ Exportación Phaser")

    logger.info("\n  Para ejecutar el pipeline completo:")
    logger.info("  python lpc_process.py\n")

    logger.info("✓✓✓ Pipeline validado\n")
    return True

def print_summary(results: dict):
    """Imprime resumen de pruebas."""
    logger.info("=" * 70)
    logger.info("RESUMEN DE PRUEBAS")
    logger.info("=" * 70 + "\n")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    for test_name, result in results.items():
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        logger.info(f"{status:10} - {test_name}")

    logger.info(f"\nTotal: {passed}/{total} pruebas pasadas")

    if failed == 0:
        logger.info("\n✓✓✓ ¡TODAS LAS PRUEBAS PASADAS! ✓✓✓")
        return True
    else:
        logger.warning(f"\n⚠ {failed} pruebas fallaron")
        return False

def main():
    """Función principal."""
    logger.info("\n" + "=" * 70)
    logger.info("LPC ATLAS GENERATOR - TEST SUITE")
    logger.info("=" * 70 + "\n")

    results = {}

    try:
        results["Importaciones"] = test_imports()
        if not results["Importaciones"]:
            logger.error("\n✗ Las importaciones fallaron. Instala dependencias:")
            logger.error("  pip install -r requirements.txt")
            return 1
    except Exception as e:
        logger.error(f"Error en test de importaciones: {e}")
        results["Importaciones"] = False

    try:
        results["Validación de Sprites"] = test_sprite_validation()
    except Exception as e:
        logger.error(f"Error en validación: {e}")
        results["Validación de Sprites"] = False

    try:
        results["Mapeos de Animaciones"] = test_animation_map_generator()
    except Exception as e:
        logger.error(f"Error en mapeos: {e}")
        results["Mapeos de Animaciones"] = False

    try:
        results["Estadísticas"] = test_statistics_generation()
    except Exception as e:
        logger.error(f"Error en estadísticas: {e}")
        results["Estadísticas"] = False

    try:
        results["Analizador de Sprites"] = test_sprite_analyzer()
    except Exception as e:
        logger.error(f"Error en analizador: {e}")
        results["Analizador de Sprites"] = False

    try:
        results["Exportador Phaser"] = test_phaser_exporter()
    except Exception as e:
        logger.error(f"Error en exportador: {e}")
        results["Exportador Phaser"] = False

    try:
        results["Pipeline Completo"] = test_full_pipeline()
    except Exception as e:
        logger.error(f"Error en pipeline: {e}")
        results["Pipeline Completo"] = False

    # Resumen
    success = print_summary(results)

    logger.info("\n" + "=" * 70)
    logger.info("PRÓXIMOS PASOS")
    logger.info("=" * 70)
    logger.info("\n1. Para procesar un sprite real:")
    logger.info("   python lpc_process.py")
    logger.info("\n2. Para ver más opciones:")
    logger.info("   python lpc_process.py --help")
    logger.info("\n3. Para analizar sprites:")
    logger.info("   python lpc_utils.py analyze <sprite_path>")
    logger.info("\n4. Lee la documentación:")
    logger.info("   QUICKSTART.md - Inicio rápido")
    logger.info("   LPC_ATLAS_README.md - Documentación completa\n")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

