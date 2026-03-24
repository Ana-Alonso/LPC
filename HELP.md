# 🎮 LPC Sprite Atlas Generator - Help & Reference
## Guía Rápida de Referencia

---

## 📋 Tabla de Contenidos
- [Instalación](#instalación)
- [Comandos Principales](#comandos-principales)
- [Ejemplos Comunes](#ejemplos-comunes)
- [Opciones Detalladas](#opciones-detalladas)
- [Troubleshooting](#troubleshooting)
- [Archivos del Proyecto](#archivos-del-proyecto)

---

## 📦 Instalación

### Requisitos
- Python 3.7+
- pip (gestor de paquetes)

### Pasos
```bash
# 1. Ir al directorio del proyecto
cd C:\Users\Ana\Desktop\prueba\my-portfolio

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Verificar instalación
python test_lpc_pipeline.py
```

---

## 🚀 Comandos Principales

### Generar Atlas (Modo Interactivo)
```bash
python lpc_process.py
```
✅ Abre diálogos gráficos interactivos  
✅ Selecciona sprite, carpeta de salida, prefijo y tolerancia  
✅ Genera `lpc_atlas.png` y `lpc_atlas.json`

### Especificar Sprite (Línea de Comandos)
```bash
python lpc_process.py --sprite "src/assets/hero.png"
```

### Especificar Salida
```bash
python lpc_process.py --sprite "hero.png" --output "output/sprites"
```

### Cambiar Nombre del Atlas
```bash
python lpc_process.py --prefix "my_custom_atlas"
```

### Ajustar Tolerancia de Transparencia
```bash
python lpc_process.py --tolerance 25
```

### Solo Validar (Sin Generar)
```bash
python lpc_process.py --validate-only
```

### Modo Debug
```bash
python lpc_process.py --verbose
```

### Ver Ayuda
```bash
python lpc_process.py --help
```

---

## 💡 Ejemplos Comunes

### Ejemplo 1: Modo Interactivo (Recomendado)
```bash
python lpc_process.py
```
Se abrirán diálogos para seleccionar archivos y opciones

### Ejemplo 2: Sprite y Prefijo Custom
```bash
python lpc_process.py --sprite "my-sprite.png" --prefix "character"
```

### Ejemplo 3: Fondo Oscuro (Mayor Tolerancia)
```bash
python lpc_process.py --tolerance 30
```

### Ejemplo 4: Fondo Limpio (Menor Tolerancia)
```bash
python lpc_process.py --tolerance 15
```

### Ejemplo 5: Especificar Directorio de Salida
```bash
python lpc_process.py --sprite "hero.png" --output "output/sprites" --prefix "hero_atlas"
```

### Ejemplo 6: Debug Completo
```bash
python lpc_process.py --sprite "hero.png" --prefix "hero_atlas" --tolerance 20 --verbose
```

### Ejemplo 7: Solo Verificar Validez
```bash
python lpc_process.py --validate-only
```

---

## 🔧 Opciones Detalladas

| Opción | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `--sprite RUTA` | str | auto | Ruta al sprite PNG |
| `--prefix NOMBRE` | str | `lpc_atlas` | Prefijo de salida |
| `--tolerance NUM` | int | 20 | Umbral de transparencia (0-255) |
| `--output RUTA` | str | mismo dir | Directorio de salida |
| `--validate-only` | flag | - | Solo validar, no generar |
| `--verbose` | flag | - | Mostrar detalles |
| `--help` | flag | - | Mostrar ayuda |
| `--version` | flag | - | Mostrar versión |

### Tolerancia Recomendada

| Tipo de Fondo | Tolerancia | Comando |
|---------------|-----------|---------|
| Negro puro | 10-15 | `--tolerance 12` |
| Negro estándar | 20-25 | `--tolerance 20` (default) |
| Negro oscuro | 25-35 | `--tolerance 30` |
| Fondo complejo | 35-50 | `--tolerance 40` |

---

## 📊 Analizar Sprites

### Ver Información de un Sprite
```bash
python lpc_utils.py analyze "src/assets/sprite.png"
```

Muestra:
- Dimensiones
- Formato y modo
- Tamaño de archivo
- Porcentaje de transparencia
- Validación LPC

### Comparar Múltiples Sprites
```bash
python lpc_utils.py compare "src/assets"
```

Compara todos los PNGs en el directorio y genera estadísticas.

---

## 🎯 Flujo Completo

### Paso 1: Validar
```bash
python lpc_process.py --validate-only
```
✓ Verifica que el sprite sea válido  
✓ Identifica potenciales problemas

### Paso 2: Procesar
```bash
python lpc_process.py
```
✓ Limpia transparencia  
✓ Genera atlas PNG  
✓ Crea JSON metadata  
✓ Genera estadísticas

### Paso 3: Integrar en Phaser
```typescript
// En tu Scene
scene.load.atlas('lpc_atlas', 'assets/lpc_atlas.png', 'assets/lpc_atlas.json');

scene.anims.create({
    key: 'walk_down',
    frames: scene.anims.generateFrameNames('lpc_atlas', {
        prefix: 'walk_down_',
        start: 0,
        end: 8
    }),
    frameRate: 10,
    repeat: -1
});
```

---

## ❌ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### Error: "ModuleNotFoundError: No module named 'PIL'"
```bash
pip install Pillow
```

### Error: "Sprite sheet not found"
**Soluciones:**
1. Especifica ruta correcta: `--sprite "ruta/correcta.png"`
2. O coloca en: `src/assets/character-spritesheet.png`

### Atlas tiene fondo negro en lugar de transparencia
**Soluciones:**
1. Aumenta tolerancia: `--tolerance 30`
2. Verifica formato PNG: debe ser RGBA, no RGB
3. Comprueba que el fondo sea realmente negro: `python lpc_utils.py analyze "sprite.png"`

### Frames tienen nombres extraños/incorrectos
1. Verifica JSON: `cat lpc_atlas.json | python -m json.tool`
2. Usa `--verbose` para ver más detalles
3. Comprueba estructura del sprite

### Phaser dice "Frame not found"
1. Verifica nombre exacto en JSON (case-sensitive)
2. Asegúrate que el atlas se cargó: `this.load.atlas(...)`
3. Comprueba nomenclatura: `animation_direction_framenum`

---

## 📁 Estructura de Archivos Generados

```
my-portfolio/
├── src/
│   ├── assets/
│   │   ├── character-spritesheet.png   ← Input original
│   │   ├── lpc_atlas.png               ← Sprite procesado ✨
│   │   ├── lpc_atlas.json              ← Metadata Phaser ✨
│   │   └── lpc_atlas_stats.json        ← Estadísticas
│   └── game/
│       ├── lpc-config.ts               ← Config Phaser (auto-gen)
│       └── ExampleScene.ts             ← Scene ejemplo (auto-gen)
├── requirements.txt                    ← Dependencias Python
├── lpc_process.py                      ← Script principal
├── lpc_atlas_generator.py              ← Core
├── lpc_atlas_advanced.py               ← Features avanzadas
├── lpc_integration_manager.py          ← Integración
├── lpc_config.py                       ← Configuración central
├── lpc_utils.py                        ← Utilidades
├── test_lpc_pipeline.py                ← Tests
└── README.md                           ← Esta guía
```

---

## 🎨 Nomenclatura de Frames

El script genera nombres automáticos:

### Formato
```
{animación}_{dirección}_{número}
```

### Ejemplos
```
walk_down_0     ← Primer frame de walk hacia abajo
walk_up_7       ← Octavo frame de walk hacia arriba
idle_left_2     ← Tercer frame de idle hacia la izquierda
slash_right_4   ← Quinto frame de slash hacia la derecha
```

### Direcciones Soportadas
```
down    (sur ↓)
up      (norte ↑)
left    (oeste ←)
right   (este →)
```

### Animaciones LPC Estándar
```
- idle, walk, run, sprint
- attack, slash, shoot, thrust
- hurt, death, climb, jump
- sit, emote, spellcast, magic
```

---

## 📊 JSON Output Format

El `lpc_atlas.json` generado sigue formato Phaser 3:

```json
{
  "textures": [{
    "image": "lpc_atlas",
    "frames": [{
      "filename": "walk_down_0",
      "frame": {"x": 0, "y": 0, "w": 64, "h": 64},
      "anchor": {"x": 0.5, "y": 0.9},
      "collisionBox": {...}
    }]
  }],
  "meta": {
    "size": {"w": 832, "h": 832},
    "frameCount": 13
  }
}
```

---

## 🔌 Integración Phaser

### Cargar Atlas
```typescript
scene.load.atlas('lpc_atlas', 'assets/lpc_atlas.png', 'assets/lpc_atlas.json');
```

### Crear Animación
```typescript
scene.anims.create({
    key: 'walk_down',
    frames: scene.anims.generateFrameNames('lpc_atlas', {
        prefix: 'walk_down_',
        start: 0,
        end: 8
    }),
    frameRate: 10,
    repeat: -1
});
```

### Reproducir
```typescript
sprite.play('walk_down');
```

### Cambiar Frame
```typescript
sprite.setFrame('idle_down_0');
```

---

## ⚙️ Configuración Avanzada

Ver `lpc_config.py` para opciones avanzadas:

```python
from lpc_config import LPC_CONFIG, get_tolerance_for_preset

# Usar preset
tolerance = get_tolerance_for_preset('aggressive')  # 15

# Acceder configuración
cell_size = LPC_CONFIG['CELL_SIZE']                  # 64
pivot_x, pivot_y = LPC_CONFIG['PIVOT']['x'], LPC_CONFIG['PIVOT']['y']
```

---

## 📈 Performance Tips

### Para Sprites Grandes
1. Divide en múltiples atlas
2. Comprime PNG con TinyPNG
3. Usa WebP en lugar de PNG

### Optimización General
```bash
# Tolerancia baja = más rápido
python lpc_process.py --tolerance 15

# Para batch processing
python lpc_utils.py batch "src/assets"
```

---

## 🆘 Contacto & Ayuda

1. **Verificar logs**: Usa `--verbose`
2. **Leer documentación**: Ver `LPC_ATLAS_README.md`
3. **Ejecutar tests**: `python test_lpc_pipeline.py`
4. **Inspeccionar output**: Abre `lpc_atlas.json` en editor

---

## 📚 Referencias

- **LPC Estándar**: https://liberated-pixel-cup.github.io/
- **Phaser 3 Docs**: https://phaser.io/
- **OpenCV Docs**: https://docs.opencv.org/

---

## ✨ Tips & Tricks

✅ Valida primero: `--validate-only`  
✅ Aumenta tolerancia si hay fondo: `--tolerance 30`  
✅ Usa verbose para debug: `--verbose`  
✅ Nombres exactos (case-sensitive)  
✅ Pivotes en pies (0.5, 0.9)  
✅ Colisiones 25% inferior  

---

**¡Listo para crear juegos increíbles con LPC y Phaser! 🚀**

