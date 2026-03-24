#!/usr/bin/env python3
"""
LPC Atlas Integration Manager
==============================
Gestor de integración del atlas LPC con el proyecto Phaser 3 y React.

Funcionalidades:
  - Generación automática del atlas
  - Integración con assets.json existente
  - Generación de configuración TypeScript
  - Validación completa del pipeline
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import sys

# Importar módulos locales
sys.path.insert(0, str(Path(__file__).parent))

try:
    from lpc_atlas_generator import LPCAtlasGenerator
    from lpc_atlas_advanced import (
        AnimationMapGenerator,
        SpriteSheetValidator,
        AtlasStatisticsGenerator,
        PhaserExporter
    )
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de que lpc_atlas_generator.py y lpc_atlas_advanced.py existan.")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# GESTOR DE INTEGRACIÓN
# ============================================================================
class LPCIntegrationManager:
    """
    Gestor central de integración de LPC sprites con Phaser/React.
    """

    def __init__(self, project_root: str):
        """
        Inicializa el gestor de integración.

        Args:
            project_root: Ruta raíz del proyecto
        """
        self.project_root = Path(project_root)
        self.assets_dir = self.project_root / "src" / "assets"
        self.src_dir = self.project_root / "src"

        # Validar estructura
        if not self.assets_dir.exists():
            raise FileNotFoundError(f"Directorio de assets no encontrado: {self.assets_dir}")

        logger.info(f"Proyecto inicializado: {self.project_root}")

    def find_sprite_sheet(self, filename: str = "character-spritesheet.png") -> Optional[Path]:
        """Busca el sprite sheet en los assets."""
        sprite_path = self.assets_dir / filename
        if sprite_path.exists():
            return sprite_path

        # Buscar cualquier PNG que podría ser el sprite
        png_files = list(self.assets_dir.glob("*.png"))
        for png in png_files:
            if "character" in png.name.lower() or "sprite" in png.name.lower():
                return png

        return None

    def load_assets_json(self) -> Optional[Dict[str, Any]]:
        """Carga el archivo assets.json existente."""
        assets_json = self.assets_dir / "assets.json"

        if not assets_json.exists():
            logger.warning(f"assets.json no encontrado: {assets_json}")
            return None

        try:
            with open(assets_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear assets.json: {e}")
            return None

    def generate_atlas(self,
                      sprite_path: Path,
                      prefix: str = "lpc_atlas",
                      tolerance: int = 20) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Genera el atlas LPC.

        Args:
            sprite_path: Ruta al sprite sheet PNG
            prefix: Prefijo para los archivos generados
            tolerance: Umbral de transparencia

        Returns:
            Tuple[Path, Path]: Rutas del PNG y JSON generados
        """
        logger.info("=" * 70)
        logger.info("GENERANDO ATLAS LPC")
        logger.info("=" * 70)

        try:
            generator = LPCAtlasGenerator(str(sprite_path), str(self.assets_dir))

            png_path, json_path = generator.generate_complete_atlas(
                tolerance=tolerance,
                prefix=prefix
            )

            logger.info(f"✓ Atlas generado exitosamente")
            logger.info(f"  PNG: {png_path}")
            logger.info(f"  JSON: {json_path}")

            return Path(png_path), Path(json_path)

        except Exception as e:
            logger.error(f"Error al generar atlas: {e}", exc_info=True)
            return None, None

    def create_phaser_config(self, atlas_prefix: str = "lpc_atlas") -> str:
        """
        Genera configuración de Phaser 3 optimizada.

        Returns:
            str: Código TypeScript de configuración
        """
        config = f'''// Auto-generated Phaser 3 Configuration
// LPC Atlas Integration

import Phaser from 'phaser';

export const LPC_ATLAS_CONFIG = {{
    key: '{atlas_prefix}',
    texture: '{atlas_prefix}',
    atlasJSON: 'assets/{atlas_prefix}.json',
    atlasPNG: 'assets/{atlas_prefix}.png'
}};

export function preloadLPCAtlas(scene: Phaser.Scene) {{
    scene.load.atlas(
        '{atlas_prefix}',
        LPC_ATLAS_CONFIG.atlasPNG,
        LPC_ATLAS_CONFIG.atlasJSON
    );
}}

export interface LPCAnimationConfig {{
    key: string;
    animation: string;
    direction: string;
    frameRate?: number;
    repeat?: number;
}}

export function createLPCAnimations(
    scene: Phaser.Scene,
    configs: LPCAnimationConfig[]
) {{
    configs.forEach(config => {{
        const framePattern = `${{config.animation}}_${{config.direction}}_`;

        scene.anims.create({{
            key: config.key,
            frames: scene.anims.generateFrameNames('{atlas_pivot}', {{
                prefix: framePattern,
                start: 0,
                end: 13,
                zeroPad: 1
            }}).filter(f => f !== undefined),
            frameRate: config.frameRate || 10,
            repeat: config.repeat !== undefined ? config.repeat : -1
        }});
    }});
}}

// Configuraciones predefinidas de animaciones LPC
export const DEFAULT_LPC_ANIMATIONS: LPCAnimationConfig[] = [
    {{ key: 'walk_down', animation: 'walk', direction: 'down', frameRate: 10 }},
    {{ key: 'walk_up', animation: 'walk', direction: 'up', frameRate: 10 }},
    {{ key: 'walk_left', animation: 'walk', direction: 'left', frameRate: 10 }},
    {{ key: 'walk_right', animation: 'walk', direction: 'right', frameRate: 10 }},

    {{ key: 'idle_down', animation: 'idle', direction: 'down', frameRate: 5, repeat: -1 }},
    {{ key: 'idle_up', animation: 'idle', direction: 'up', frameRate: 5, repeat: -1 }},
    {{ key: 'idle_left', animation: 'idle', direction: 'left', frameRate: 5, repeat: -1 }},
    {{ key: 'idle_right', animation: 'idle', direction: 'right', frameRate: 5, repeat: -1 }},

    {{ key: 'slash_down', animation: 'slash', direction: 'down', frameRate: 15 }},
    {{ key: 'slash_up', animation: 'slash', direction: 'up', frameRate: 15 }},
    {{ key: 'slash_left', animation: 'slash', direction: 'left', frameRate: 15 }},
    {{ key: 'slash_right', animation: 'slash', direction: 'right', frameRate: 15 }},
];

export interface LPCCharacterConfig {{
    x: number;
    y: number;
    texture: string;
    frame?: string;
    scale?: number;
    depth?: number;
}}

export class LPCCharacter extends Phaser.Physics.Arcade.Sprite {{
    private currentDirection: string = 'down';
    private isMoving: boolean = false;

    constructor(scene: Phaser.Scene, config: LPCCharacterConfig) {{
        super(scene, config.x, config.y, config.texture, config.frame || 'idle_down_0');

        scene.add.existing(this);
        scene.physics.add.existing(this);

        if (config.scale) this.setScale(config.scale);
        if (config.depth) this.setDepth(config.depth);

        // Configurar física
        this.setCollideWorldBounds(true);
        this.setBounce(0.1);
    }}

    playAnimation(direction: string) {{
        if (this.currentDirection !== direction) {{
            this.currentDirection = direction;
        }}

        const animKey = `walk_${{direction}}`;
        if (this.scene.anims.exists(animKey)) {{
            this.play(animKey);
        }}
    }}

    stopAnimation() {{
        this.stop();
        this.setFrame(`idle_${{this.currentDirection}}_0`);
    }}

    moveTo(x: number, y: number, speed: number = 100) {{
        this.isMoving = true;

        const angle = Phaser.Math.Angle.Between(this.x, this.y, x, y);
        const distance = Phaser.Math.Distance.Between(this.x, this.y, x, y);

        // Determinar dirección
        let direction = 'down';
        if (angle < -Math.PI * 0.75 || angle > Math.PI * 0.75) {{
            direction = 'left';
        }} else if (angle >= -Math.PI * 0.25 && angle < Math.PI * 0.25) {{
            direction = 'right';
        }} else if (angle >= Math.PI * 0.25 && angle < Math.PI * 0.75) {{
            direction = 'down';
        }} else {{
            direction = 'up';
        }}

        this.playAnimation(direction);
        this.scene.physics.moveToObject(this, {{ x, y }}, speed);

        // Detener cuando se alcanza el destino
        const checkDistance = () => {{
            if (Phaser.Math.Distance.Between(this.x, this.y, x, y) < speed / 60) {{
                this.setVelocity(0, 0);
                this.stopAnimation();
                this.isMoving = false;
            }}
        }};

        this.scene.events.on('update', checkDistance);
    }}
}}
'''

        return config.replace('{atlas_pivot}', 'lpc_atlas')

    def create_scene_example(self) -> str:
        """Genera un ejemplo de Scene con el personaje LPC."""

        scene_code = '''// Example Phaser 3 Scene with LPC Character
// src/game/ExampleScene.ts

import Phaser from 'phaser';
import {
    preloadLPCAtlas,
    createLPCAnimations,
    DEFAULT_LPC_ANIMATIONS,
    LPCCharacter,
    LPCCharacterConfig
} from '../assets/lpc-config';

export class ExampleScene extends Phaser.Scene {
    private player: LPCCharacter | null = null;
    private cursors: Phaser.Types.Input.Keyboard.CursorKeys | null = null;

    constructor() {
        super({ key: 'ExampleScene' });
    }

    preload() {
        preloadLPCAtlas(this);
    }

    create() {
        // Crear animaciones
        createLPCAnimations(this, DEFAULT_LPC_ANIMATIONS);

        // Crear personaje
        const playerConfig: LPCCharacterConfig = {
            x: this.cameras.main.centerX,
            y: this.cameras.main.centerY,
            texture: 'lpc_atlas',
            frame: 'idle_down_0',
            scale: 2
        };

        this.player = new LPCCharacter(this, playerConfig);

        // Configurar controles
        this.cursors = this.input.keyboard?.createCursorKeys();

        // Configurar cámara para seguir al jugador
        this.cameras.main.startFollow(this.player);
    }

    update() {
        if (!this.player || !this.cursors) return;

        let isMoving = false;

        if (this.cursors.left?.isDown) {
            this.player.setVelocityX(-200);
            this.player.playAnimation('left');
            isMoving = true;
        } else if (this.cursors.right?.isDown) {
            this.player.setVelocityX(200);
            this.player.playAnimation('right');
            isMoving = true;
        } else {
            this.player.setVelocityX(0);
        }

        if (this.cursors.up?.isDown) {
            this.player.setVelocityY(-200);
            this.player.playAnimation('up');
            isMoving = true;
        } else if (this.cursors.down?.isDown) {
            this.player.setVelocityY(200);
            this.player.playAnimation('down');
            isMoving = true;
        } else {
            this.player.setVelocityY(0);
        }

        if (!isMoving) {
            this.player.stopAnimation();
        }
    }
}
'''

        return scene_code

    def generate_integration_package(self,
                                    sprite_path: Optional[Path] = None,
                                    prefix: str = "lpc_atlas") -> bool:
        """
        Genera paquete completo de integración.

        Args:
            sprite_path: Ruta al sprite (si None, busca automáticamente)
            prefix: Prefijo para los archivos

        Returns:
            bool: True si la generación fue exitosa
        """
        logger.info("\n" + "=" * 70)
        logger.info("GENERADOR DE PAQUETE DE INTEGRACIÓN LPC")
        logger.info("=" * 70 + "\n")

        # Buscar sprite
        if sprite_path is None:
            sprite_path = self.find_sprite_sheet()
            if sprite_path is None:
                logger.error("✗ No se encontró sprite sheet")
                return False
            logger.info(f"Sprite encontrado: {sprite_path.name}")

        # Validar
        logger.info("\n1. Validando sprite sheet...")
        val = SpriteSheetValidator.validate_dimensions(*self._get_image_dims(sprite_path))
        if val["warnings"]:
            for warning in val["warnings"]:
                logger.warning(f"   ⚠ {warning}")

        # Generar atlas
        logger.info("\n2. Generando atlas...")
        png_path, json_path = self.generate_atlas(sprite_path, prefix)

        if png_path is None or json_path is None:
            logger.error("✗ Error al generar atlas")
            return False

        # Cargar JSON generado
        with open(json_path, 'r', encoding='utf-8') as f:
            atlas_data = json.load(f)

        frames = atlas_data['textures'][0]['frames']

        # Generar estadísticas
        logger.info("\n3. Generando estadísticas...")
        stats = AtlasStatisticsGenerator.generate_stats(
            frames,
            atlas_data['meta']['size']['w'],
            atlas_data['meta']['size']['h']
        )

        stats_path = self.assets_dir / f"{prefix}_stats.json"
        AtlasStatisticsGenerator.export_stats_to_json(stats, str(stats_path))

        # Generar configuración TypeScript
        logger.info("\n4. Generando configuración Phaser...")
        phaser_config = self.create_phaser_config(prefix)
        config_path = self.src_dir / "game" / "lpc-config.ts"

        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(phaser_config)

        logger.info(f"   ✓ Configuración guardada: {config_path}")

        # Generar ejemplo de Scene
        logger.info("\n5. Generando ejemplo de Scene...")
        scene_code = self.create_scene_example()
        example_path = self.src_dir / "game" / "ExampleScene.ts"

        with open(example_path, 'w', encoding='utf-8') as f:
            f.write(scene_code)

        logger.info(f"   ✓ Ejemplo guardado: {example_path}")

        # Resumen
        logger.info("\n" + "=" * 70)
        logger.info("✓✓✓ INTEGRACIÓN COMPLETADA EXITOSAMENTE ✓✓✓")
        logger.info("=" * 70)
        logger.info(f"\nArchivos generados:")
        logger.info(f"  - {png_path}")
        logger.info(f"  - {json_path}")
        logger.info(f"  - {stats_path}")
        logger.info(f"  - {config_path}")
        logger.info(f"  - {example_path}")
        logger.info(f"\nEstadísticas:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")

        return True

    @staticmethod
    def _get_image_dims(image_path: Path) -> Tuple[int, int]:
        """Obtiene dimensiones de una imagen."""
        from PIL import Image
        try:
            img = Image.open(image_path)
            return img.size
        except Exception:
            return (0, 0)


# ============================================================================
# SCRIPT PRINCIPAL
# ============================================================================
def main():
    """Ejecuta el gestor de integración."""

    project_root = Path(__file__).parent

    try:
        manager = LPCIntegrationManager(str(project_root))
        success = manager.generate_integration_package()

        if success:
            logger.info("\n✓ Puedes ahora importar las configuraciones en tu proyecto React:")
            logger.info("  import { preloadLPCAtlas, createLPCAnimations } from './game/lpc-config';")
        else:
            logger.error("\n✗ Hubo un error en la integración")
            return 1

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

