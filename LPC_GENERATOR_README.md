# 🎮 LPC Sprite Sheet to Phaser 3 Texture Atlas Generator

**Conversión profesional de Liberated Pixel Cup Sprite Sheets a Texture Atlas optimizados para Phaser 3**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      LPC ATLAS GENERATOR v1.0.0                             ║
║                   Expert Image Processing & Game Development                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## ✨ Características Principales

### ✓ Análisis Geométrico LPC
- Validación automática de células 64×64
- Soporte para múltiples direcciones (4 u 8 direcciones)
- Cálculo inteligente de dimensiones
- Detección de anomalías

### ✓ Procesamiento Avanzado de Imágenes
- Limpieza profesional de transparencia
- Remoción de fondos negros con tolerancia configurable
- Detección y eliminación de ruido
- Preservación de calidad de píxeles

### ✓ Generación de Texture Atlas Phaser 3
- Formato JSON compatible con Phaser 3
- Nomenclatura automática LPC (walk_up_0, slash_down_1, etc.)
- Metadata completa de frames
- Soporte para múltiples animaciones

### ✓ Pivotes Inteligentes
- Posicionamiento automático en pies del personaje
- Coordenadas: (x: 0.5, y: 0.9)
- Facilita colisiones realistas en RPG
- Permite caminar detrás de objetos

### ✓ Cajas de Colisión Automáticas
- Generación basada en geometría del personaje
- Ocupan 25% inferior del frame
- Formato compatible con physics engines
- Optimizado para juegos isométricos

### ✓ Estadísticas Detalladas
- Análisis de cobertura de atlas
- Estimaciones de memoria
- Conteo de frames por animación
- Exportación en múltiples formatos

### ✓ Integración Automática
- Generación de código Phaser 3
- Clase LPCCharacter funcional
- Ejemplos de Scene
- Configuración TypeScript

---

## 🚀 Inicio Rápido

### 1. Instalación
```bash
pip install -r requirements.txt
```

### 2. Procesar Sprite
```bash
python lpc_process.py
```

### 3. Usar en Phaser
```typescript
scene.load.atlas('lpc_atlas', 'assets/lpc_atlas.png', 'assets/lpc_atlas.json');
```

✅ **¡Listo en 3 pasos!**

---

## 📁 Estructura del Proyecto

```
LPC Sprite Sheet Generator/
│
├── 🎯 SCRIPTS PRINCIPALES
│   ├── lpc_process.py                  ← Script principal (CLI)
│   ├── lpc_integration_manager.py      ← Gestor de integración
│   └── test_lpc_pipeline.py            ← Tests y validación
│
├── 🔧 MÓDULOS CORE
│   ├── lpc_atlas_generator.py          ← Motor de generación
│   ├── lpc_atlas_advanced.py           ← Features avanzadas
│   ├── lpc_config.py                   ← Configuración central
│   └── lpc_utils.py                    ← Utilidades
│
├── 📚 DOCUMENTACIÓN
│   ├── QUICKSTART.md                   ← Inicio en 5 minutos
│   ├── HELP.md                         ← Guía de referencia
│   ├── LPC_ATLAS_README.md             ← Documentación completa
│   └── README.md                       ← Este archivo
│
├── 📋 CONFIGURACIÓN
│   └── requirements.txt                ← Dependencias Python
│
└── 🎨 OUTPUTS (Generados)
    ├── lpc_atlas.png                   ← Sprite procesado
    ├── lpc_atlas.json                  ← Metadata Phaser
    ├── lpc_atlas_stats.json            ← Estadísticas
    ├── lpc-config.ts                   ← Config Phaser (auto)
    └── ExampleScene.ts                 ← Scene ejemplo (auto)
```

---

## 📖 Documentación

| Archivo | Contenido |
|---------|-----------|
| **QUICKSTART.md** | ⚡ Inicio rápido en 5 minutos |
| **HELP.md** | 📚 Guía rápida de referencia |
| **LPC_ATLAS_README.md** | 📖 Documentación técnica completa |
| **lpc_config.py** | ⚙️ Configuración centralizada |

---

## 🎮 Uso Principal

### Modo Interactivo (Recomendado)
```bash
python lpc_process.py
```
✓ Se abre selector gráfico de archivos  
✓ Diálogos para configurar opciones  
✓ Más cómodo y visual

### Modo Línea de Comandos
```bash
python lpc_process.py \
    --sprite "src/assets/hero.png" \
    --output "output/dir" \
    --prefix "hero_atlas" \
    --tolerance 20 \
    --verbose
```

### Ver Ayuda
```bash
python lpc_process.py --help
```

---

## 🔍 Opciones de Línea de Comandos

```
--sprite RUTA              Ruta al sprite PNG
--prefix NOMBRE            Prefijo de salida (default: lpc_atlas)
--tolerance NUM            Umbral 0-255 (default: 20)
--output RUTA              Directorio de salida (default: misma carpeta del sprite)
--validate-only            Solo validar sin generar
--verbose                  Modo debug detallado
--help                     Mostrar ayuda
--version                  Mostrar versión
```

### Ejemplos de Tolerancia

| Tipo de Fondo | Tolerancia | Comando |
|---------------|-----------|---------|
| Negro puro | 10-15 | `--tolerance 12` |
| Negro estándar | 20-25 | `--tolerance 20` |
| Negro oscuro | 25-35 | `--tolerance 30` |
| Fondo complejo | 35-50 | `--tolerance 40` |

---

## 🧪 Testing

### Ejecutar Suite de Tests
```bash
python test_lpc_pipeline.py
```

Verifica:
- ✓ Importaciones de módulos
- ✓ Validación de sprites
- ✓ Generación de mapeos
- ✓ Estadísticas
- ✓ Exportación Phaser

### Analizar Sprites
```bash
python lpc_utils.py analyze "src/assets/sprite.png"
```

---

## 🎨 Integración Phaser 3

### Cargar Atlas
```typescript
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
        
        // Usar sprite
        const player = this.add.sprite(100, 100, 'lpc_atlas');
        player.play('walk_down');
    }
}
```

### Con Clase Generada
```typescript
import { LPCCharacter, preloadLPCAtlas, createLPCAnimations } 
    from './game/lpc-config';

export class GameScene extends Phaser.Scene {
    preload() {
        preloadLPCAtlas(this);
    }
    
    create() {
        createLPCAnimations(this, DEFAULT_LPC_ANIMATIONS);
        
        const player = new LPCCharacter(this, {
            x: 100,
            y: 100,
            texture: 'lpc_atlas',
            scale: 2
        });
    }
}
```

---

## 📊 Archivos Generados

### lpc_atlas.png
- Sprite limpiado con transparencia correcta
- Formato RGBA8888
- Canal alfa procesado profesionalmente

### lpc_atlas.json
- Metadata compatible con Phaser 3
- Frames nombrados automáticamente
- Pivotes y colisiones incluidas

### lpc_atlas_stats.json
- Estadísticas de cobertura
- Conteo de frames
- Estimaciones de memoria

### lpc-config.ts
- Configuración Phaser automatizada
- Clase LPCCharacter
- Helper functions

### ExampleScene.ts
- Escena de ejemplo funcional
- Manejo de controles
- Integración completa

---

## 🎯 Nomenclatura de Frames

Formato automático: `{animación}_{dirección}_{frame}`

### Ejemplos
```
walk_down_0     Primer frame de walk hacia abajo
walk_up_7       Octavo frame de walk hacia arriba
idle_left_2     Tercer frame de idle hacia la izquierda
slash_right_4   Quinto frame de slash hacia la derecha
```

### Animaciones Soportadas
```
idle, walk, run, sprint, attack
slash, shoot, thrust, hurt, death
climb, jump, sit, emote, spellcast, magic
```

### Direcciones
```
down   (sur ↓)      left   (oeste ←)
up     (norte ↑)    right  (este →)
```

---

## ⚙️ Características Técnicas

### Geometría LPC
- Células: 64×64 píxeles
- Validación de múltiplos
- Soporte para n×m frames

### Transparencia
- Detección de fondos negros
- Tolerancia configurable (0-255)
- Umbral inteligente de ruido
- Preservación de bordes

### Pivotes
- Posición automática: (0.5, 0.9)
- Pies del personaje
- Sincronización con colisiones

### Colisiones
- 25% inferior del frame
- 80% del ancho
- Compatible con physics

### Estadísticas
- Cobertura de atlas
- Píxeles utilizados
- Estimación de memoria
- Conteo animaciones

---

## 🔧 Requisitos

### Software
- Python 3.7+
- pip

### Librerías Python
- `opencv-python` (cv2)
- `Pillow` (PIL)

### Instalación
```bash
pip install -r requirements.txt
```

---

## 📚 Documentación Técnica

### API Reference

#### LPCAtlasGenerator
```python
generator = LPCAtlasGenerator(input_path, output_dir)
png_path, json_path = generator.generate_complete_atlas(
    tolerance=20,
    prefix="atlas"
)
```

#### AnimationMapGenerator
```python
animation_map = AnimationMapGenerator.generate_lpc_standard(total_rows)
```

#### SpriteSheetValidator
```python
validation = SpriteSheetValidator.validate_dimensions(width, height)
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: cv2"
```bash
pip install opencv-python
```

### "ModuleNotFoundError: PIL"
```bash
pip install Pillow
```

### "Sprite sheet not found"
- Especifica ruta: `--sprite "ruta/correcta.png"`
- O coloca en: `src/assets/character-spritesheet.png`

### "Atlas tiene fondo negro"
```bash
python lpc_process.py --tolerance 30
```

### "Frame not found en Phaser"
- Verifica nombre exacto en JSON
- Asegúrate que atlas se cargó
- Chequea nomenclatura

---

## 💡 Tips

✅ Valida primero: `--validate-only`  
✅ Aumenta tolerancia si hay fondo: `--tolerance 30`  
✅ Usa verbose para debug: `--verbose`  
✅ Los nombres son case-sensitive  
✅ Pivotes en pies: (0.5, 0.9)  
✅ Colisiones 25% inferior  

---

## 📈 Performance

### Optimización
- Procesamiento vectorizado con OpenCV
- Uso eficiente de memoria
- Exports en múltiples formatos
- Cálculos de collision optimizados

### Para Proyectos Grandes
1. Divide sprites en múltiples atlases
2. Comprime PNG con TinyPNG
3. Usa WebP para menor tamaño

---

## 🔗 Referencias

- **LPC Estándar**: https://liberated-pixel-cup.github.io/
- **Phaser 3**: https://phaser.io/
- **OpenCV**: https://opencv.org/
- **Python**: https://python.org/

---

## 📝 Versión

```
LPC Sprite Sheet to Phaser 3 Atlas Generator
Version: 1.0.0
Python: 3.7+
Dependencies: opencv-python, Pillow
License: MIT
```

---

## 🚀 Próximos Pasos

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Leer guía rápida**
   ```bash
   cat QUICKSTART.md
   ```

3. **Procesar sprite**
   ```bash
   python lpc_process.py
   ```

4. **Usar en Phaser**
   - Importar atlas en tu Scene
   - Crear animaciones
   - Reproducir en sprites

5. **Explorar características**
   - Estadísticas: `lpc_atlas_stats.json`
   - Config Phaser: `lpc-config.ts`
   - Ejemplo: `ExampleScene.ts`

---

## 🎉 ¡Listo!

Ya tienes todo lo necesario para convertir LPC Sprite Sheets a Texture Atlas profesionales para Phaser 3.

**¡A crear increíbles juegos 2D! 🎮✨**

---

### Soporte

Para problemas o preguntas:
1. Revisa `HELP.md` para referencia rápida
2. Consulta `LPC_ATLAS_README.md` para detalles técnicos
3. Ejecuta `python test_lpc_pipeline.py` para diagnosticar
4. Usa `--verbose` para debug detallado

### Made with ❤️ for Game Developers

