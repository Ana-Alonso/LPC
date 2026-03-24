LPC Sprite Sheet to Phaser 3 Atlas - Complete Documentation
============================================================

Este conjunto de scripts Python proporciona una solución profesional y completa 
para convertir Liberated Pixel Cup (LPC) Sprite Sheets a Texture Atlas compatible 
con Phaser 3, con características avanzadas de procesamiento de imágenes.

TABLE OF CONTENTS
=================
1. Instalación
2. Uso Rápido
3. Módulos Disponibles
4. Características Técnicas
5. Ejemplos de Uso
6. Integración con Phaser 3
7. Troubleshooting


INSTALACIÓN
===========

1. Prerequisitos:
   - Python 3.7+
   - pip (gestor de paquetes de Python)

2. Instalar dependencias:

   pip install -r requirements.txt

   O instalar manualmente:
   
   pip install opencv-python pillow

   OpenCV (cv2):    Procesamiento avanzado de imágenes
   Pillow (PIL):    Lectura/escritura de imágenes


USO RÁPIDO
==========

Modo Interactivo (Recomendado):
   
   python lpc_process.py

Este comando abrirá:
   ✓ Selector gráfico para elegir el sprite PNG
   ✓ Diálogo para seleccionar carpeta de salida
   ✓ Diálogo para configurar prefijo del atlas
   ✓ Diálogo para ajustar tolerancia de transparencia
   ✓ Genera atlas.png y atlas.json
   ✓ Crea configuración Phaser 3


Modo Línea de Comandos (sin diálogos):

   # Especificar todos los parámetros
   python lpc_process.py --sprite src/assets/my-sprite.png --output output/ --prefix hero_atlas --tolerance 20

   # Especificar sprite
   python lpc_process.py --sprite src/assets/my-sprite.png

   # Cambiar prefijo del atlas
   python lpc_process.py --prefix hero_atlas

   # Ajustar tolerancia (0-255)
   python lpc_process.py --tolerance 25

   # Solo validar sin generar
   python lpc_process.py --validate-only

   # Modo verbose (más detalles)
   python lpc_process.py --verbose

   # Combinado
   python lpc_process.py --sprite char.png --prefix game_atlas --tolerance 20 --verbose --output output/


MÓDULOS DISPONIBLES
====================

1. lpc_atlas_generator.py
   ━━━━━━━━━━━━━━━━━━━━━
   Módulo principal de generación de atlas.
   
   Clases:
   - LPCAtlasGenerator: Núcleo del procesamiento
     * validate_geometry()        → Valida geometría LPC (64x64)
     * clean_transparency()       → Remueve fondos negros
     * extract_frames()           → Extrae frames con nomenclatura LPC
     * generate_atlas_json()      → Genera JSON para Phaser 3
     * save_atlas()              → Guarda PNG y JSON
     * generate_complete_atlas() → Pipeline completo
   
   - PhaserAtlasLoader: Utilidades de integración Phaser


2. lpc_atlas_advanced.py
   ━━━━━━━━━━━━━━━━━━━━━
   Configuraciones avanzadas y validaciones.
   
   Clases:
   - AnimationMapGenerator: Genera mapeos de animaciones
   - SpriteSheetValidator: Valida contra estándares LPC
   - AtlasStatisticsGenerator: Genera estadísticas detalladas
   - PhaserExporter: Exporta a TypeScript/JavaScript


3. lpc_integration_manager.py
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Gestor de integración con React/Phaser.
   
   Clases:
   - LPCIntegrationManager: Orquesta todo el pipeline


4. lpc_process.py
   ━━━━━━━━━━━━━
   Script ejecutable principal con CLI.


CARACTERÍSTICAS TÉCNICAS
========================

✓ Análisis de Geometría LPC:
  - Valida células de 64×64 píxeles
  - Soporta múltiples direcciones (4 u 8 direcciones)
  - Calcula dimensiones automáticamente

✓ Limpieza Avanzada de Transparencia:
  - Detección de fondos negros con tolerancia configurable
  - Procesamiento de píxeles con remoción de ruido
  - Preserva canales alfa de forma inteligente

✓ Generación de Texture Atlas:
  - Compatible con formato Phaser 3 JSON
  - Nombres de frames automáticos (walk_up_0, slash_down_1, etc.)
  - Soporte para 4 y 8 direcciones

✓ Pivotes Inteligentes:
  - Pivote configurado en pies del personaje (x:0.5, y:0.9)
  - Facilita colisiones realistas en RPG
  - Permite caminar detrás de objetos

✓ Cajas de Colisión:
  - Generación automática basada en 25% inferior
  - Formato compatible con physics engines
  - Optimizado para juegos 2D isométricos

✓ Estadísticas Detalladas:
  - Análisis de cobertura de atlas
  - Estimaciones de memoria
  - Conteo de frames por animación


EJEMPLOS DE USO
===============

Ejemplo 1: Uso básico
─────────────────────

from lpc_atlas_generator import LPCAtlasGenerator

generator = LPCAtlasGenerator("src/assets/character.png")
png_path, json_path = generator.generate_complete_atlas(
    tolerance=20,
    prefix="my_atlas"
)

print(f"Atlas generado: {png_path}, {json_path}")


Ejemplo 2: Con validación previa
─────────────────────────────────

from lpc_atlas_advanced import SpriteSheetValidator

validator = SpriteSheetValidator()
validation = validator.validate_dimensions(832, 832)

if validation['valid']:
    print("✓ Dimensiones válidas")
    print(f"Frames: {validation['analysis']['totalFrames']}")


Ejemplo 3: Uso completo con integración
────────────────────────────────────────

from lpc_integration_manager import LPCIntegrationManager

manager = LPCIntegrationManager(".")
success = manager.generate_integration_package(
    sprite_path="src/assets/hero.png",
    prefix="hero_atlas"
)

# Genera:
# - hero_atlas.png (limpiado)
# - hero_atlas.json (atlas metadata)
# - hero_atlas_stats.json (estadísticas)
# - src/game/lpc-config.ts (configuración Phaser)
# - src/game/ExampleScene.ts (escena de ejemplo)


INTEGRACIÓN CON PHASER 3
========================

1. Cargar el atlas en tu Scene:

   export class GameScene extends Phaser.Scene {
       preload() {
           this.load.atlas(
               'lpc_atlas',
               'assets/lpc_atlas.png',
               'assets/lpc_atlas.json'
           );
       }
       
       create() {
           // Crear animación
           this.anims.create({
               key: 'walk_down',
               frames: this.anims.generateFrameNames('lpc_atlas', {
                   prefix: 'walk_down_',
                   start: 0,
                   end: 8
               }),
               frameRate: 10,
               repeat: -1
           });
           
           // Crear sprite
           const player = this.add.sprite(100, 100, 'lpc_atlas', 'idle_down_0');
           
           // Reproducir animación
           player.play('walk_down');
       }
   }


2. Con la clase LPCCharacter (generada):

   import { preloadLPCAtlas, createLPCAnimations, LPCCharacter } 
       from './game/lpc-config';
   
   export class GameScene extends Phaser.Scene {
       private player: LPCCharacter;
       
       preload() {
           preloadLPCAtlas(this);
       }
       
       create() {
           createLPCAnimations(this, DEFAULT_LPC_ANIMATIONS);
           
           this.player = new LPCCharacter(this, {
               x: 100,
               y: 100,
               texture: 'lpc_atlas',
               scale: 2
           });
       }
       
       update() {
           if (this.cursors.left.isDown) {
               this.player.playAnimation('left');
               this.player.setVelocityX(-200);
           }
       }
   }


3. Acceder a frames individuales:

   const frame = 'walk_down_0';
   sprite.setFrame(frame);
   
   // Con pivot automático
   const frameData = atlas.frames[frame];
   console.log(frameData.anchor); // { x: 0.5, y: 0.9 }


NOMENCLATURA DE FRAMES
======================

El script genera frames con nomenclatura estándar LPC:

Formato: {animation}_{direction}_{frame_number}

Ejemplos:
   - walk_down_0    → Primer frame de walk hacia abajo
   - walk_up_7      → Octavo frame de walk hacia arriba
   - idle_left_2    → Tercer frame de idle hacia la izquierda
   - slash_right_5  → Sexto frame de slash hacia la derecha

Direcciones soportadas:
   - down   (sur)
   - up     (norte)
   - left   (oeste)
   - right  (este)
   - (opcional: downleft, upleft, upright, downright para 8 direcciones)

Animaciones estándar LPC:
   - idle, walk, run, sprint
   - attack, slash, shoot, thrust
   - hurt, death, climb, jump
   - sit, emote, spellcast, magic
   - (más configurables)


ARCHIVOS GENERADOS
==================

Después de ejecutar lpc_process.py, se generan:

1. lpc_atlas.png
   - Versión limpiada del sprite sheet
   - Canal alfa procesado
   - Formato RGBA8888

2. lpc_atlas.json
   - Metadata de frames
   - Pivotes y colisiones
   - Compatible con Phaser 3

3. lpc_atlas_stats.json (opcional)
   - Estadísticas de cobertura
   - Conteo de frames
   - Estimaciones de memoria

4. src/game/lpc-config.ts
   - Configuración automatizada
   - Clases y funciones helper
   - Lista de animaciones

5. src/game/ExampleScene.ts
   - Ejemplo funcional
   - Implementación LPCCharacter
   - Manejo de controles


TROUBLESHOOTING
===============

Problema: "ModuleNotFoundError: No module named 'cv2'"
Solución: pip install opencv-python

Problema: "ModuleNotFoundError: No module named 'PIL'"
Solución: pip install Pillow

Problema: "FileNotFoundError: sprite sheet no encontrado"
Solución: Especifica la ruta correcta con --sprite
         o coloca el sprite en src/assets/character-spritesheet.png

Problema: "Atlas se ve con fondo negro en lugar de transparencia"
Solución: Aumenta --tolerance (ej: --tolerance 30)

Problema: "Frames tienen nombres extraños"
Solución: Verifica que el JSON tenga estructura correcta
         Usa --verbose para más detalles

Problema: "Error al cargar en Phaser: Frame no existe"
Solución: Verifica nombres exactos en el JSON
         Los nombres diferencia entre mayúsculas
         Usa scene.textures.getPixels() para debug


OPTIMIZACIÓN
============

Para proyectos grandes:

1. Divide sprites en múltiples atlases:
   python lpc_process.py --sprite animations_set1.png --prefix atlas_1
   python lpc_process.py --sprite animations_set2.png --prefix atlas_2

2. Ajusta tolerancia según fondo:
   - Fondo negro puro: tolerance = 10-15
   - Fondo negro oscuro: tolerance = 20-25
   - Fondos complejos: tolerance = 30-40

3. Comprime PNG con:
   - TinyPNG.com
   - ImageOptim
   - pngquant

4. Usa WebP para menor tamaño:
   - ffmpeg -i atlas.png atlas.webp
   - Soportado en navegadores modernos


API REFERENCE
=============

LPCAtlasGenerator
─────────────────

__init__(input_path: str, output_dir: str = None)
    Inicializa el generador

validate_geometry() -> bool
    Valida geometría LPC (múltiplos de 64)

clean_transparency(tolerance: int = 20, target_color: Tuple = (0, 0, 0))
    Limpia transparencia de fondos

extract_frames(animation_map: Dict = None) -> List[FrameData]
    Extrae frames del sprite sheet

generate_atlas_json() -> Dict
    Genera JSON del atlas para Phaser 3

save_atlas(prefix: str = "atlas") -> Tuple[str, str]
    Guarda PNG y JSON

generate_complete_atlas(tolerance: int = 20, animation_map: Dict = None,
                       prefix: str = "atlas") -> Tuple[str, str]
    Ejecuta pipeline completo


SOPORTE Y DOCUMENTACIÓN
=======================

Para problemas o sugerencias:
1. Revisa los logs con --verbose
2. Consulta los ejemplos en lpc_process.py
3. Inspecciona el JSON generado en un formateador JSON

Estándares y referencias:
- LPC Estándar: https://liberated-pixel-cup.github.io/
- Phaser 3: https://phaser.io/
- OpenCV: https://opencv.org/


VERSION
=======

LPC Sprite Sheet to Phaser 3 Atlas Generator
Version: 1.0.0
Python: 3.7+
Dependencies: opencv-python, Pillow
License: MIT

Created with ❤️ for game developers

