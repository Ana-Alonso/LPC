#!/usr/bin/env python3
"""
LPC Sprite Sheet to Phaser 3 Texture Atlas Generator
======================================================
Proceso avanzado de conversión de LPC Sprite Sheets (Liberated Pixel Cup)
a formato Texture Atlas compatible con Phaser 3.

Autor: AI Expert - Game Development
Version: 1.0.0

FEATURES:
  1. Validación de geometría LPC (64x64 cell standard)
  2. Limpieza de transparencia (remoción de fondos negros)
  3. Generación de Texture Atlas (JSON + PNG)
  4. Nomenclatura estándar LPC (walk_up_0, slash_down_0, etc.)
  5. Pivotes en pies del personaje (x=0.5, y=0.9)
  6. Cálculo de cajas de colisión (25% inferior)
"""

import cv2
import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import logging

# ============================================================================
# CONFIGURACIÓN LOGGING
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURACIÓN LPC ESTÁNDAR
# ============================================================================
LPC_CONFIG = {
    'CELL_SIZE': 64,
    'STANDARD_WIDTH': 832,  # 13 celdas × 64px (13 direcciones/variaciones)
    'ANIMATIONS': [
        'spellcast',
        'thrust',
        'walk',
        'slash',
        'shoot',
        'hurt',
        'climb',
        'idle',
        'jump',
        'sit',
        'emote',
        'run',
        'combat_idle',
        'backslash',
        'halfslash'
    ],
    'DIRECTIONS': {
        'down': 0,
        'left': 1,
        'right': 2,
        'up': 3
    },
    'PIVOT_FEET': (0.5, 0.9),  # x=0.5 (centro), y=0.9 (pies)
    'COLLISION_BOX_HEIGHT_RATIO': 0.25  # 25% inferior
}

# ============================================================================
# DATA CLASSES
# ============================================================================
@dataclass
class FrameData:
    """Metadata de un frame individual"""
    name: str
    x: int
    y: int
    w: int
    h: int
    pivotX: float
    pivotY: float
    collisionBox: Optional[Dict] = None
    sourceSize: Optional[Dict] = None
    spriteSourceSize: Optional[Dict] = None


@dataclass
class CollisionBox:
    """Caja de colisión simplificada"""
    x: float
    y: float
    w: float
    h: float


# ============================================================================
# CLASE PRINCIPAL: LPC ATLAS GENERATOR
# ============================================================================
class LPCAtlasGenerator:
    """
    Generador profesional de Texture Atlas para Phaser 3
    desde LPC Sprite Sheets.
    """

    def __init__(self, input_path: str, output_dir: str = None):
        """
        Inicializa el generador.

        Args:
            input_path: Ruta al PNG del sprite sheet
            output_dir: Directorio de salida (default: directorio del input)
        """
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir) if output_dir else self.input_path.parent

        if not self.input_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {input_path}")

        logger.info(f"Cargando sprite sheet: {self.input_path}")

        # Cargar imagen
        self.image = cv2.imread(str(self.input_path), cv2.IMREAD_UNCHANGED)
        if self.image is None:
            raise ValueError(f"No se puede leer la imagen: {input_path}")

        # Convertir BGR a RGBA si es necesario
        if len(self.image.shape) == 2:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGRA)
        elif self.image.shape[2] == 3:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2BGRA)

        self.height, self.width = self.image.shape[:2]
        self.frames: List[FrameData] = []
        self.metadata = {}

        logger.info(f"Dimensiones sprite sheet: {self.width}x{self.height}")

    # ========================================================================
    # PASO 1: VALIDACIÓN DE GEOMETRÍA
    # ========================================================================
    def validate_geometry(self) -> bool:
        """
        Valida que la imagen cumpla el estándar LPC (múltiplos de 64).

        Returns:
            bool: True si es válida
        """
        logger.info("=" * 70)
        logger.info("PASO 1: VALIDACIÓN DE GEOMETRÍA LPC")
        logger.info("=" * 70)

        cell_size = LPC_CONFIG['CELL_SIZE']

        # Validar ancho
        if self.width % cell_size != 0:
            logger.warning(f"⚠ Ancho {self.width}px no es múltiplo de {cell_size}")
            logger.warning(f"  Ancho ajustado a: {(self.width // cell_size) * cell_size}")
            self.width = (self.width // cell_size) * cell_size

        # Validar alto
        if self.height % cell_size != 0:
            logger.warning(f"⚠ Alto {self.height}px no es múltiplo de {cell_size}")
            logger.warning(f"  Alto ajustado a: {(self.height // cell_size) * cell_size}")
            self.height = (self.height // cell_size) * cell_size

        cols = self.width // cell_size
        rows = self.height // cell_size
        total_frames = cols * rows

        logger.info(f"✓ Geometría válida: {cols}x{rows} = {total_frames} frames")
        logger.info(f"  Dimensiones: {self.width}x{self.height} píxeles")

        self.metadata['geometry'] = {
            'cellSize': cell_size,
            'columns': cols,
            'rows': rows,
            'totalFrames': total_frames,
            'imageWidth': self.width,
            'imageHeight': self.height
        }

        return True

    # ========================================================================
    # PASO 2: LIMPIEZA Y TRANSPARENCIA
    # ========================================================================
    def clean_transparency(self, tolerance: int = 20,
                          target_color: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
        """
        Remueve fondos negros y establece transparencia correcta.

        Args:
            tolerance: Umbral de tolerancia para consideracódigos negros (0-255)
            target_color: Color BGR a convertir en transparente (predeterminado: negro)

        Returns:
            np.ndarray: Imagen limpiada con canal alfa correcto
        """
        logger.info("=" * 70)
        logger.info("PASO 2: LIMPIEZA Y TRANSPARENCIA")
        logger.info("=" * 70)

        cleaned = self.image.copy()

        # Separar canales BGR y alfa
        if cleaned.shape[2] < 4:
            cleaned = cv2.cvtColor(cleaned, cv2.COLOR_BGR2BGRA)

        b, g, r, a = cv2.split(cleaned)

        # Crear máscara para píxeles cercanos al color negro
        lower = np.array([
            max(0, target_color[0] - tolerance),
            max(0, target_color[1] - tolerance),
            max(0, target_color[2] - tolerance)
        ], dtype=np.uint8)

        upper = np.array([
            min(255, target_color[0] + tolerance),
            min(255, target_color[1] + tolerance),
            min(255, target_color[2] + tolerance)
        ], dtype=np.uint8)

        # Crear máscara (1 si está en rango, 0 si no)
        mask = cv2.inRange(cleaned[:, :, :3], lower, upper)

        # Convertir píxeles negros a transparentes
        a[mask > 0] = 0

        # Recombinar canales
        cleaned = cv2.merge([b, g, r, a])

        # Contar píxeles procesados
        transparent_pixels = np.count_nonzero(mask)
        total_pixels = self.width * self.height
        pct = (transparent_pixels / total_pixels * 100) if total_pixels > 0 else 0

        logger.info(f"✓ Transparencia procesada")
        logger.info(f"  Píxeles convertidos a transparentes: {transparent_pixels:,}")
        logger.info(f"  Porcentaje: {pct:.2f}%")

        self.image = cleaned
        self.metadata['transparency'] = {
            'processedPixels': int(transparent_pixels),
            'toleranceThreshold': tolerance,
            'targetColor': target_color
        }

        return cleaned

    # ========================================================================
    # PASO 3: EXTRACCIÓN DE FRAMES
    # ========================================================================
    def extract_frames(self, animation_map: Optional[Dict] = None) -> List[FrameData]:
        """
        Extrae frames de la imagen y genera nomenclatura LPC.

        Args:
            animation_map: Mapeo personalizado de animaciones (opcional)

        Returns:
            List[FrameData]: Lista de frames con metadata
        """
        logger.info("=" * 70)
        logger.info("PASO 3: EXTRACCIÓN DE FRAMES")
        logger.info("=" * 70)

        cell_size = LPC_CONFIG['CELL_SIZE']
        cols = self.width // cell_size
        rows = self.height // cell_size

        self.frames = []
        frame_index = 0

        # Mapeo de animaciones por defecto (order LPC estándar)
        if animation_map is None:
            animation_map = self._generate_default_animation_map(rows)

        for row_idx in range(rows):
            for col_idx in range(cols):
                x = col_idx * cell_size
                y = row_idx * cell_size

                # Generar nombre del frame
                animation_info = animation_map.get(row_idx, {})
                animation = animation_info.get('name', f'frame_{frame_index}')
                direction = animation_info.get('direction', 'default')
                variant = animation_info.get('variant', col_idx)

                # Nomenclatura: animation_direction_variant
                frame_name = f"{animation}_{direction}_{variant}"

                # Calcular pivote (pies del personaje)
                pivot_x, pivot_y = LPC_CONFIG['PIVOT_FEET']

                # Caja de colisión (25% inferior del frame)
                collision_box = self._calculate_collision_box(
                    cell_size,
                    LPC_CONFIG['COLLISION_BOX_HEIGHT_RATIO']
                )

                frame = FrameData(
                    name=frame_name,
                    x=x,
                    y=y,
                    w=cell_size,
                    h=cell_size,
                    pivotX=pivot_x,
                    pivotY=pivot_y,
                    collisionBox=asdict(collision_box),
                    sourceSize={'w': cell_size, 'h': cell_size},
                    spriteSourceSize={'x': 0, 'y': 0, 'w': cell_size, 'h': cell_size}
                )

                self.frames.append(frame)
                frame_index += 1

        logger.info(f"✓ Frames extraídos exitosamente")
        logger.info(f"  Total de frames: {len(self.frames)}")
        logger.info(f"  Primeros frames de muestra:")
        for i in range(min(5, len(self.frames))):
            f = self.frames[i]
            logger.info(f"    - {f.name} @ ({f.x}, {f.y})")

        return self.frames

    def _generate_default_animation_map(self, rows: int) -> Dict:
        """
        Genera mapeo de animaciones por defecto (estándar LPC).
        """
        animations = LPC_CONFIG['ANIMATIONS']
        directions = list(LPC_CONFIG['DIRECTIONS'].keys())

        animation_map = {}
        row_idx = 0

        for animation in animations:
            for direction in directions:
                if row_idx < rows:
                    animation_map[row_idx] = {
                        'name': animation,
                        'direction': direction,
                        'variant': None
                    }
                    row_idx += 1

        return animation_map

    def _calculate_collision_box(self, cell_size: int, height_ratio: float) -> CollisionBox:
        """
        Calcula caja de colisión simplificada.

        La caja ocupa el porcentaje especificado (altura) en la parte inferior
        del frame, centrada horizontalmente.
        """
        box_height = cell_size * height_ratio
        box_width = cell_size * 0.8  # 80% del ancho para margen

        return CollisionBox(
            x=(cell_size - box_width) / 2,
            y=cell_size - box_height,
            w=box_width,
            h=box_height
        )

    # ========================================================================
    # PASO 4: GENERACIÓN DEL ATLAS JSON
    # ========================================================================
    def generate_atlas_json(self) -> Dict:
        """
        Genera JSON del Texture Atlas compatible con Phaser 3.

        Formato Phaser 3:
        {
          "textures": [{
            "image": "atlas_name",
            "format": "RGBA8888",
            "frames": [...]
          }],
          "meta": {...}
        }
        """
        logger.info("=" * 70)
        logger.info("PASO 4: GENERACIÓN DEL ATLAS JSON")
        logger.info("=" * 70)

        atlas_data = {
            "textures": [
                {
                    "image": self.input_path.stem,
                    "format": "RGBA8888",
                    "frames": [
                        {
                            "filename": frame.name,
                            "rotated": False,
                            "trimmed": False,
                            "sourceSize": frame.sourceSize,
                            "spriteSourceSize": frame.spriteSourceSize,
                            "frame": {
                                "x": frame.x,
                                "y": frame.y,
                                "w": frame.w,
                                "h": frame.h
                            },
                            "anchor": {
                                "x": frame.pivotX,
                                "y": frame.pivotY
                            },
                            "collisionBox": frame.collisionBox
                        }
                        for frame in self.frames
                    ]
                }
            ],
            "meta": {
                "app": "LPC Atlas Generator v1.0",
                "version": "1.0",
                "image": f"{self.input_path.stem}.png",
                "format": "RGBA8888",
                "size": {
                    "w": self.width,
                    "h": self.height
                },
                "scale": 1,
                "smartUpdate": False,
                "frameCount": len(self.frames),
                "lpcConfig": LPC_CONFIG,
                "processingMetadata": self.metadata
            }
        }

        logger.info(f"✓ Atlas JSON generado")
        logger.info(f"  Frames totales: {len(self.frames)}")
        logger.info(f"  Dimensiones: {self.width}x{self.height}")

        self.atlas_json = atlas_data
        return atlas_data

    # ========================================================================
    # PASO 5: GUARDADO DE ARCHIVOS
    # ========================================================================
    def save_atlas(self, prefix: str = "atlas") -> Tuple[str, str]:
        """
        Guarda el atlas PNG y JSON en el directorio de salida.

        Args:
            prefix: Prefijo para los archivos de salida

        Returns:
            Tuple[str, str]: Rutas del PNG y JSON generados
        """
        logger.info("=" * 70)
        logger.info("PASO 5: GUARDADO DE ARCHIVOS")
        logger.info("=" * 70)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Guardar PNG
        png_path = self.output_dir / f"{prefix}.png"
        json_path = self.output_dir / f"{prefix}.json"

        # Convertir BGRA a RGBA para cv2
        image_rgba = cv2.cvtColor(self.image, cv2.COLOR_BGRA2RGBA)

        success = cv2.imwrite(str(png_path), image_rgba)
        if not success:
            raise IOError(f"Error al guardar PNG: {png_path}")

        logger.info(f"✓ PNG guardado: {png_path}")
        logger.info(f"  Tamaño: {os.path.getsize(png_path):,} bytes")

        # Guardar JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.atlas_json, f, indent=2, ensure_ascii=False)

        logger.info(f"✓ JSON guardado: {json_path}")
        logger.info(f"  Tamaño: {os.path.getsize(json_path):,} bytes")

        logger.info("=" * 70)
        logger.info("✓✓✓ ATLAS GENERADO EXITOSAMENTE ✓✓✓")
        logger.info("=" * 70)

        return str(png_path), str(json_path)

    # ========================================================================
    # EJECUCIÓN COMPLETA
    # ========================================================================
    def generate_complete_atlas(self,
                               tolerance: int = 20,
                               animation_map: Optional[Dict] = None,
                               prefix: str = "atlas") -> Tuple[str, str]:
        """
        Ejecuta el pipeline completo de generación del atlas.

        Args:
            tolerance: Umbral de transparencia
            animation_map: Mapeo de animaciones personalizado
            prefix: Prefijo para los archivos de salida

        Returns:
            Tuple[str, str]: Rutas del PNG y JSON generados
        """
        logger.info("\n" + "=" * 70)
        logger.info("LPC SPRITE SHEET ATLAS GENERATOR - INICIO COMPLETO")
        logger.info("=" * 70 + "\n")

        try:
            self.validate_geometry()
            self.clean_transparency(tolerance=tolerance)
            self.extract_frames(animation_map=animation_map)
            self.generate_atlas_json()
            png_path, json_path = self.save_atlas(prefix=prefix)

            return png_path, json_path

        except Exception as e:
            logger.error(f"✗ Error crítico durante la generación: {str(e)}")
            raise


# ============================================================================
# UTILIDADES DE INTEGRACIÓN
# ============================================================================
class PhaserAtlasLoader:
    """
    Utilidades para cargar el atlas en Phaser 3.
    """

    @staticmethod
    def generate_phaser_load_code(atlas_prefix: str,
                                  texture_name: str = None) -> str:
        """
        Genera código TypeScript para cargar el atlas en Phaser.
        """
        if texture_name is None:
            texture_name = atlas_prefix

        code = f'''// Cargar Texture Atlas en Phaser 3
scene.load.atlas(
    '{texture_name}',
    'assets/{atlas_prefix}.png',
    'assets/{atlas_prefix}.json'
);

// Usar en una animación:
scene.anims.create({{
    key: 'walk_down',
    frames: scene.anims.generateFrameNames('{texture_name}', {{
        prefix: 'walk_down_',
        start: 0,
        end: 7
    }}),
    frameRate: 10,
    repeat: -1
}});

// Reproducir animación:
sprite.play('walk_down');

// Acceder al frame individual:
sprite.setFrame('walk_down_0');
'''
        return code


# ============================================================================
# MAIN - SCRIPT DE PRUEBA
# ============================================================================
def main():
    """
    Script principal de ejecución.
    """
    # Rutas de archivo
    PROJECT_ROOT = Path(__file__).parent
    INPUT_SPRITE = PROJECT_ROOT / "src" / "assets" / "character-spritesheet.png"
    OUTPUT_DIR = PROJECT_ROOT / "src" / "assets"

    # Validar que exista el sprite
    if not INPUT_SPRITE.exists():
        logger.error(f"Sprite sheet no encontrado: {INPUT_SPRITE}")
        logger.info("Asegúrate de que 'character-spritesheet.png' exista en src/assets/")
        return

    try:
        # Crear generador
        generator = LPCAtlasGenerator(str(INPUT_SPRITE), str(OUTPUT_DIR))

        # Generar atlas completo
        png_path, json_path = generator.generate_complete_atlas(
            tolerance=20,
            prefix="lpc_atlas"
        )

        # Generar código de ejemplo
        phaser_code = PhaserAtlasLoader.generate_phaser_load_code("lpc_atlas")

        logger.info("\n" + "=" * 70)
        logger.info("CÓDIGO DE INTEGRACIÓN PHASER 3")
        logger.info("=" * 70)
        logger.info(phaser_code)

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()

