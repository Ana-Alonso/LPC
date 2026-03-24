#!/usr/bin/env python3
"""
LPC Atlas Advanced Configuration & Utilities
==============================================
Módulo de configuración avanzada y utilidades para el procesamiento de LPC.

Características adicionales:
  - Mapeos de animaciones personalizados
  - Procesamiento batch de múltiples sprites
  - Validación contra estándares LPC
  - Exportación de estadísticas
  - Integración con assets.json existente
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURACIONES AVANZADAS DE ANIMACIONES LPC
# ============================================================================
ANIMATION_CONFIGS = {
    "standard_4dir": {
        "description": "4 direcciones (arriba, abajo, izquierda, derecha)",
        "rows_per_animation": 4,
        "directions": ["down", "left", "right", "up"],
        "frames_per_direction": 8
    },

    "standard_8dir": {
        "description": "8 direcciones (con diagonales)",
        "rows_per_animation": 8,
        "directions": ["down", "downleft", "left", "upleft",
                      "up", "upright", "right", "downright"],
        "frames_per_direction": 4
    },

    "single_row": {
        "description": "Una única fila de animación",
        "rows_per_animation": 1,
        "directions": ["default"],
        "frames_per_direction": 13
    },

    "combat_idle": {
        "description": "Idle en combate (típicamente 4 direcciones)",
        "rows_per_animation": 4,
        "directions": ["down", "left", "right", "up"],
        "frames_per_direction": 4
    }
}

# ============================================================================
# MAPEO ESTÁNDAR LPC (LIBERATED PIXEL CUP)
# ============================================================================
LPC_STANDARD_ANIMATION_MAP = {
    0: {"name": "spellcast", "direction": "down", "frames": 7},
    1: {"name": "spellcast", "direction": "left", "frames": 7},
    2: {"name": "spellcast", "direction": "right", "frames": 7},
    3: {"name": "spellcast", "direction": "up", "frames": 7},

    4: {"name": "thrust", "direction": "down", "frames": 8},
    5: {"name": "thrust", "direction": "left", "frames": 8},
    6: {"name": "thrust", "direction": "right", "frames": 8},
    7: {"name": "thrust", "direction": "up", "frames": 8},

    8: {"name": "walk", "direction": "down", "frames": 9},
    9: {"name": "walk", "direction": "left", "frames": 9},
    10: {"name": "walk", "direction": "right", "frames": 9},
    11: {"name": "walk", "direction": "up", "frames": 9},

    12: {"name": "slash", "direction": "down", "frames": 6},
    13: {"name": "slash", "direction": "left", "frames": 6},
    14: {"name": "slash", "direction": "right", "frames": 6},
    15: {"name": "slash", "direction": "up", "frames": 6},

    16: {"name": "shoot", "direction": "down", "frames": 13},
    17: {"name": "shoot", "direction": "left", "frames": 13},
    18: {"name": "shoot", "direction": "right", "frames": 13},
    19: {"name": "shoot", "direction": "up", "frames": 13},

    20: {"name": "hurt", "direction": "down", "frames": 6},
    21: {"name": "hurt", "direction": "left", "frames": 6},
    22: {"name": "hurt", "direction": "right", "frames": 6},
    23: {"name": "hurt", "direction": "up", "frames": 6},

    24: {"name": "climb", "direction": "down", "frames": 4},
    25: {"name": "climb", "direction": "left", "frames": 4},
    26: {"name": "climb", "direction": "right", "frames": 4},
    27: {"name": "climb", "direction": "up", "frames": 4},

    28: {"name": "idle", "direction": "down", "frames": 4},
    29: {"name": "idle", "direction": "left", "frames": 4},
    30: {"name": "idle", "direction": "right", "frames": 4},
    31: {"name": "idle", "direction": "up", "frames": 4},

    32: {"name": "jump", "direction": "down", "frames": 4},
    33: {"name": "jump", "direction": "left", "frames": 4},
    34: {"name": "jump", "direction": "right", "frames": 4},
    35: {"name": "jump", "direction": "up", "frames": 4},
}

# ============================================================================
# GENERADOR DE MAPEOS DE ANIMACIONES
# ============================================================================
class AnimationMapGenerator:
    """
    Generador de mapeos de animaciones personalizados.
    """

    @staticmethod
    def generate_from_config(config_type: str,
                            total_rows: int) -> Dict[int, Dict[str, Any]]:
        """
        Genera mapeo de animaciones basado en configuración predefinida.

        Args:
            config_type: Tipo de configuración (e.g., 'standard_4dir')
            total_rows: Número total de filas en el sprite sheet

        Returns:
            Dict: Mapeo de animaciones
        """
        if config_type not in ANIMATION_CONFIGS:
            raise ValueError(f"Configuración desconocida: {config_type}")

        config = ANIMATION_CONFIGS[config_type]
        animation_map = {}
        row_idx = 0

        directions = config['directions']
        frames_per_dir = config['frames_per_direction']

        # Usar animaciones estándar LPC
        animations = [
            "idle", "walk", "run", "sprint",
            "attack", "hurt", "death", "magic"
        ]

        for animation in animations:
            for direction in directions:
                if row_idx >= total_rows:
                    break

                animation_map[row_idx] = {
                    "name": animation,
                    "direction": direction,
                    "frames": frames_per_dir
                }
                row_idx += 1

            if row_idx >= total_rows:
                break

        return animation_map

    @staticmethod
    def generate_lpc_standard(total_rows: int) -> Dict[int, Dict[str, Any]]:
        """
        Genera mapeo estándar LPC (Liberated Pixel Cup).

        Args:
            total_rows: Número total de filas disponibles

        Returns:
            Dict: Mapeo LPC estándar
        """
        result = {}
        for row_idx in range(min(total_rows, len(LPC_STANDARD_ANIMATION_MAP))):
            result[row_idx] = LPC_STANDARD_ANIMATION_MAP.get(row_idx, {})

        return result


# ============================================================================
# VALIDADOR DE SPRITE SHEETS
# ============================================================================
class SpriteSheetValidator:
    """
    Valida sprite sheets contra estándares LPC.
    """

    @staticmethod
    def validate_dimensions(width: int, height: int,
                           cell_size: int = 64) -> Dict[str, Any]:
        """
        Valida que las dimensiones sean múltiplos de cell_size.

        Returns:
            Dict: Resultado de validación
        """
        result = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "analysis": {}
        }

        # Validar ancho
        if width % cell_size != 0:
            result["warnings"].append(
                f"Ancho ({width}px) no es múltiplo de {cell_size}. "
                f"Será ajustado a {(width // cell_size) * cell_size}px"
            )

        # Validar alto
        if height % cell_size != 0:
            result["warnings"].append(
                f"Alto ({height}px) no es múltiplo de {cell_size}. "
                f"Será ajustado a {(height // cell_size) * cell_size}px"
            )

        # Análisis
        adjusted_width = (width // cell_size) * cell_size
        adjusted_height = (height // cell_size) * cell_size
        cols = adjusted_width // cell_size
        rows = adjusted_height // cell_size

        result["analysis"] = {
            "originalDimensions": (width, height),
            "adjustedDimensions": (adjusted_width, adjusted_height),
            "cellSize": cell_size,
            "columns": cols,
            "rows": rows,
            "totalFrames": cols * rows
        }

        return result

    @staticmethod
    def validate_against_assets_json(assets_json_path: str,
                                    expected_animations: List[str]) -> Dict:
        """
        Valida que el sprite sheet cumpla con las animaciones
        definidas en assets.json.

        Args:
            assets_json_path: Ruta al assets.json
            expected_animations: Animaciones esperadas

        Returns:
            Dict: Resultado de validación
        """
        result = {
            "valid": True,
            "missingAnimations": [],
            "enabledAnimations": [],
            "unsupportedAnimations": []
        }

        try:
            with open(assets_json_path, 'r', encoding='utf-8') as f:
                assets_data = json.load(f)

            enabled_anims = assets_data.get('enabledAnimations', {})

            for anim_name in expected_animations:
                if anim_name not in enabled_anims:
                    result["missingAnimations"].append(anim_name)
                elif enabled_anims[anim_name]:
                    result["enabledAnimations"].append(anim_name)
                else:
                    result["unsupportedAnimations"].append(anim_name)

            if result["missingAnimations"]:
                result["valid"] = False

        except FileNotFoundError:
            result["valid"] = False
            result["error"] = f"assets.json no encontrado: {assets_json_path}"
        except json.JSONDecodeError as e:
            result["valid"] = False
            result["error"] = f"Error al parsear assets.json: {str(e)}"

        return result


# ============================================================================
# GENERADOR DE ESTADÍSTICAS
# ============================================================================
class AtlasStatisticsGenerator:
    """
    Genera estadísticas detalladas del atlas procesado.
    """

    @staticmethod
    def generate_stats(frames_data: List[Dict],
                      image_width: int,
                      image_height: int) -> Dict[str, Any]:
        """
        Genera estadísticas completas del atlas.
        """
        stats = {
            "general": {
                "totalFrames": len(frames_data),
                "atlasWidth": image_width,
                "atlasHeight": image_height,
                "atlasPixels": image_width * image_height,
                "pixelsPerFrame": 64 * 64  # Asumiendo 64x64 estándar
            },
            "animations": {},
            "coverage": {},
            "memory": {}
        }

        # Agrupar por animación
        animation_groups = {}
        for frame in frames_data:
            filename = frame.get('filename', '')
            anim_name = filename.split('_')[0] if '_' in filename else 'unknown'

            if anim_name not in animation_groups:
                animation_groups[anim_name] = []

            animation_groups[anim_name].append(frame)

        stats["animations"] = {
            anim: len(frames)
            for anim, frames in animation_groups.items()
        }

        # Cobertura
        total_frame_pixels = stats["general"]["totalFrames"] * stats["general"]["pixelsPerFrame"]
        stats["coverage"]["framePixels"] = total_frame_pixels
        stats["coverage"]["coveragePercentage"] = (
            (total_frame_pixels / stats["general"]["atlasPixels"]) * 100
        )

        # Estimaciones de memoria
        stats["memory"]["atlasMemoryMB"] = (stats["general"]["atlasPixels"] * 4) / (1024 * 1024)
        stats["memory"]["estimatedJSONKB"] = len(str(frames_data)) / 1024

        return stats

    @staticmethod
    def export_stats_to_json(stats: Dict, output_path: str) -> None:
        """
        Exporta estadísticas a archivo JSON.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        logger.info(f"Estadísticas exportadas a: {output_path}")


# ============================================================================
# EXPORTADOR A FORMATO PHASER 3
# ============================================================================
class PhaserExporter:
    """
    Exporta atlas en diferentes formatos compatibles con Phaser 3.
    """

    @staticmethod
    def export_to_typescript_config(frames_data: List[Dict],
                                    texture_name: str,
                                    output_path: str) -> None:
        """
        Exporta configuración de animaciones como TypeScript.
        """
        ts_code = f'''// Generated Atlas Configuration - Phaser 3
// Auto-generated by LPC Atlas Generator

export const {texture_name.upper()}_ANIMATIONS = {{
'''

        animations = {}
        for frame in frames_data:
            filename = frame.get('filename', '')
            parts = filename.rsplit('_', 1)

            if len(parts) == 2:
                anim_key = parts[0]
                frame_num = parts[1]

                if anim_key not in animations:
                    animations[anim_key] = []

                animations[anim_key].append(frame_num)

        for anim_name, frame_indices in animations.items():
            ts_code += f'''    {anim_name}: {{
        key: '{anim_name}',
        frames: [
'''
            for idx in frame_indices:
                ts_code += f"            '{anim_name}_{idx}',\n"

            ts_code += f'''        ],
        frameRate: 10,
        repeat: -1
    }},
'''

        ts_code += "};"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ts_code)

        logger.info(f"Configuración TypeScript exportada a: {output_path}")

    @staticmethod
    def generate_loader_code(atlas_prefix: str,
                           texture_name: str = None) -> str:
        """
        Genera código de carga para Phaser 3.
        """
        if texture_name is None:
            texture_name = atlas_prefix

        code = f'''
// ============================================================
// LPC Sprite Sheet Loader - Phaser 3
// ============================================================

export function preloadAtlas(scene: Phaser.Scene) {{
    // Cargar Texture Atlas
    scene.load.atlas(
        '{texture_name}',
        'assets/{atlas_prefix}.png',
        'assets/{atlas_prefix}.json'
    );
}}

export function createAnimations(scene: Phaser.Scene, textureName: string = '{texture_name}') {{
    const animsConfig = [
        {{
            key: 'walk_down',
            frames: scene.anims.generateFrameNames(textureName, {{
                prefix: 'walk_down_',
                start: 0,
                end: 8,
                zeroPad: 1
            }}),
            frameRate: 10,
            repeat: -1
        }},
        {{
            key: 'walk_up',
            frames: scene.anims.generateFrameNames(textureName, {{
                prefix: 'walk_up_',
                start: 0,
                end: 8,
                zeroPad: 1
            }}),
            frameRate: 10,
            repeat: -1
        }},
        {{
            key: 'walk_left',
            frames: scene.anims.generateFrameNames(textureName, {{
                prefix: 'walk_left_',
                start: 0,
                end: 8,
                zeroPad: 1
            }}),
            frameRate: 10,
            repeat: -1
        }},
        {{
            key: 'walk_right',
            frames: scene.anims.generateFrameNames(textureName, {{
                prefix: 'walk_right_',
                start: 0,
                end: 8,
                zeroPad: 1
            }}),
            frameRate: 10,
            repeat: -1
        }},
        {{
            key: 'idle_down',
            frames: scene.anims.generateFrameNames(textureName, {{
                prefix: 'idle_down_',
                start: 0,
                end: 3,
                zeroPad: 1
            }}),
            frameRate: 5,
            repeat: -1
        }},
    ];

    animsConfig.forEach(config => {{
        if (!scene.anims.exists(config.key)) {{
            scene.anims.create(config);
        }}
    }});
}}

// Uso en Scene:
// preloadAtlas(this);
// createAnimations(this);
// sprite.play('walk_down');
'''
        return code


# ============================================================================
# SCRIPT DE VALIDACIÓN Y PRUEBA
# ============================================================================
def validate_sprite_sheet(sprite_path: str, assets_json_path: str = None) -> None:
    """
    Realiza validación completa de un sprite sheet.
    """
    from PIL import Image

    print("\n" + "=" * 70)
    print("VALIDADOR DE SPRITE SHEETS LPC")
    print("=" * 70 + "\n")

    sprite_path = Path(sprite_path)

    if not sprite_path.exists():
        print(f"✗ Sprite sheet no encontrado: {sprite_path}")
        return

    # Validar dimensiones
    try:
        img = Image.open(sprite_path)
        width, height = img.size

        print(f"Sprite Sheet: {sprite_path.name}")
        print(f"Dimensiones: {width}x{height}")
        print()

        val = SpriteSheetValidator.validate_dimensions(width, height)

        print("Validación de Geometría:")
        for warning in val["warnings"]:
            print(f"  ⚠ {warning}")

        print(f"\nAnálisis:")
        for key, value in val["analysis"].items():
            print(f"  {key}: {value}")

        # Validar contra assets.json si existe
        if assets_json_path and Path(assets_json_path).exists():
            print(f"\nValidando contra: {assets_json_path}")

            expected_anims = [
                "idle", "walk", "run", "attack", "hurt", "death"
            ]
            val_assets = SpriteSheetValidator.validate_against_assets_json(
                assets_json_path,
                expected_anims
            )

            print(f"  Animaciones habilitadas: {len(val_assets['enabledAnimations'])}")
            print(f"  Animaciones faltantes: {len(val_assets['missingAnimations'])}")

        print()

    except Exception as e:
        print(f"✗ Error al validar: {str(e)}")


if __name__ == "__main__":
    # Ejemplo de uso
    import sys

    if len(sys.argv) > 1:
        sprite_file = sys.argv[1]
        validate_sprite_sheet(sprite_file)
    else:
        print("Uso: python lpc_atlas_advanced.py <ruta_sprite_sheet>")

