# LPC Sprite Atlas Generator - QUICK START GUIDE
# ===============================================

## 🚀 Inicio Rápido en 5 Minutos

### Paso 1: Instalación
```bash
cd C:\Users\Ana\Desktop\prueba\my-portfolio
pip install -r requirements.txt
```

### Paso 2: Verificar sprite
Asegúrate de que tienes `character-spritesheet.png` en:
```
src/assets/character-spritesheet.png
```

### Paso 3: Ejecutar
```bash
python lpc_process.py
```

¡Listo! El script abrirá:
1. **Selector de Sprite** - Elige tu PNG
2. **Selector de Carpeta de Salida** - Elige dónde guardar
3. **Diálogos de Configuración** - Prefijo y tolerancia

Genera:
- `lpc_atlas.png` (sprite limpiado)
- `lpc_atlas.json` (metadata para Phaser)

---

## 📚 Casos de Uso

### Caso 1: Modo Interactivo (Recomendado)
```bash
python lpc_process.py
```
✅ Abre diálogos gráficos para seleccionar archivos y configurar opciones

### Caso 2: Línea de Comandos (Automático)
```bash
python lpc_process.py --sprite "src/assets/my-hero.png" --prefix hero --output "output/dir"
```
✅ Sin diálogos gráficos, configurable vía argumentos

### Caso 3: Ajustar Tolerancia
```bash
python lpc_process.py --tolerance 30
```
✅ Aumenta la tolerancia para fondos oscuros

### Caso 4: Solo Validar
```bash
python lpc_process.py --validate-only
```
✅ Valida el sprite sin generar atlas

### Caso 5: Debug Completo
```bash
python lpc_process.py --verbose
```
✅ Muestra detalles completos del proceso

---

## 🎮 Usar en Phaser 3

### En tu Scene TypeScript:

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

        // Crear sprite
        const player = this.add.sprite(100, 100, 'lpc_atlas');
        player.play('walk_down');
    }
}
```

---

## 📊 Analizar Sprites

```bash
# Información detallada de un sprite
python lpc_utils.py analyze "src/assets/character-spritesheet.png"

# Comparar todos los sprites en un directorio
python lpc_utils.py compare "src/assets"
```

---

## ⚙️ Opciones Avanzadas

```bash
# Ver todas las opciones
python lpc_process.py --help

# Especificar sprite y directorio de salida
python lpc_process.py \
    --sprite "src/assets/hero.png" \
    --output "output/sprites" \
    --prefix "hero_atlas" \
    --tolerance 20 \
    --verbose
```

### Parámetros disponibles:
- `--sprite RUTA` - Ruta al sprite PNG
- `--prefix NOMBRE` - Prefijo del atlas (default: lpc_atlas)
- `--tolerance NUM` - Umbral 0-255 (default: 20)
- `--output RUTA` - Directorio de salida (default: misma carpeta del sprite)
- `--validate-only` - Solo validar
- `--verbose` - Mostrar detalles
- `--help` - Ver ayuda
- `--version` - Ver versión

---

## 🛠️ Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: cv2` | `pip install opencv-python` |
| `ModuleNotFoundError: PIL` | `pip install Pillow` |
| Sprite no encontrado | Coloca en `src/assets/character-spritesheet.png` |
| Fondo negro en atlas | Aumenta `--tolerance` (ej: 30) |
| Error de Python | Usa `python lpc_process.py --verbose` |

---

## 📁 Archivos Generados

```
src/assets/
├── lpc_atlas.png           ← Sprite limpiado
├── lpc_atlas.json          ← Metadata para Phaser
└── lpc_atlas_stats.json    ← Estadísticas (opcional)
```

---

## 🎨 Nomenclatura de Frames

Los frames generados siguen este patrón:
```
{animación}_{dirección}_{frame}

Ejemplos:
- walk_down_0   (primer frame de walk hacia abajo)
- idle_up_3     (cuarto frame de idle hacia arriba)
- slash_left_2  (tercer frame de slash hacia la izquierda)
```

---

## 📝 Configuración Típica

### Para juegos RPG
```bash
python lpc_process.py --tolerance 20
```

### Para juegos Pixel Art
```bash
python lpc_process.py --tolerance 10
```

### Para fondos complejos
```bash
python lpc_process.py --tolerance 30
```

---

## 🔗 Integración Automática

El script puede generar automáticamente:
1. `lpc-config.ts` - Configuración Phaser
2. `ExampleScene.ts` - Escena de ejemplo
3. Clase `LPCCharacter` - Personaje funcional

Usar con:
```bash
python lpc_integration_manager.py
```

---

## 📖 Documentación Completa

Para detalles técnicos, ver: `LPC_ATLAS_README.md`

---

## 💡 Tips

✅ Siempre valida primero con `--validate-only`
✅ Usa `--verbose` para debugging
✅ Ajusta tolerance según el fondo del sprite
✅ Los pivotes automáticos van en los pies (x:0.5, y:0.9)
✅ Las cajas de colisión ocupan el 25% inferior

---

## 🎯 Próximos Pasos

1. ✅ Generar atlas: `python lpc_process.py`
2. ✅ Verificar archivos en `src/assets/`
3. ✅ Usar en tu Scene de Phaser
4. ✅ Reproducir animaciones con `sprite.play('walk_down')`

---

¡Listo! Ya tienes tu atlas LPC para Phaser 3 🎉

