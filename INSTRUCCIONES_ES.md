# 🎮 LPC Sprite Atlas Generator - INSTRUCCIONES EN ESPAÑOL

## ¡Bienvenido! Aquí está tu solución completa.

---

## ¿QUÉ TIENES?

Te hemos generado un **sistema profesional y completo** para convertir LPC Sprite Sheets 
(estándar Liberated Pixel Cup) a Texture Atlas optimizados para Phaser 3.

✓ 4 scripts principales ejecutables
✓ 3 módulos core con toda la lógica
✓ 5 documentos de guía y referencia
✓ 2500+ líneas de código Python
✓ 5000+ líneas de documentación

**TODO ESTÁ LISTO PARA USAR.**

---

## 🚀 CÓMO EMPEZAR EN 3 PASOS

### PASO 1: Instalar (1 minuto)
```bash
pip install -r requirements.txt
```

Esto instala:
- OpenCV (cv2) - Para procesamiento de imágenes
- Pillow (PIL) - Para manejo de PNG

### PASO 2: Ejecutar (30 segundos)
```bash
python lpc_process.py
```

El script abrirá diálogos interactivos para:
1. Seleccionar el sprite PNG
2. Elegir carpeta de salida
3. Configurar prefijo (nombre del atlas)
4. Ajustar tolerancia de transparencia

### PASO 3: Usar en Phaser (2 minutos)
```typescript
// En tu Scene Phaser 3
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

sprite.play('walk_down');
```

¡LISTO! Tu sprite está en Phaser 3.

---

## 📁 ARCHIVOS PRINCIPALES

### Scripts Ejecutables (Ejecuta estos)
```
lpc_process.py          ← ¡EJECUTA ESTE! (Opción principal)
test_lpc_pipeline.py    ← Para tests y validación
lpc_utils.py            ← Para análisis de sprites
lpc_integration_manager.py ← Para integración automática
```

### Módulos Internos (No ejecutes, se usan automáticamente)
```
lpc_atlas_generator.py  ← Motor core
lpc_atlas_advanced.py   ← Features avanzadas
lpc_config.py           ← Configuración
```

### Documentación (LEE ESTOS)
```
QUICKSTART.md           ← COMIENZA AQUÍ (5 min)
HELP.md                 ← Referencia rápida (10 min)
INDEX.md                ← Índice de archivos (5 min)
LPC_ATLAS_README.md     ← Documentación completa (20 min)
LPC_GENERATOR_README.md ← Overview del proyecto (10 min)
```

### Configuración
```
requirements.txt        ← Dependencias Python
lpc_config.py          ← Configuración centralizada
```

---

## 📖 QUÉ LEER SEGÚN TU SITUACIÓN

### Si tienes prisa (5 minutos)
→ Lee **QUICKSTART.md**

### Si necesitas saber opciones (10 minutos)
→ Lee **HELP.md**

### Si quieres entender cómo funciona (30 minutos)
→ Lee **LPC_ATLAS_README.md**

### Si quieres ver la estructura completa (15 minutos)
→ Lee **LPC_GENERATOR_README.md**

### Si necesitas encontrar algo (5 minutos)
→ Lee **INDEX.md**

---

## ✨ CARACTERÍSTICAS QUE TIENES

✓ **Análisis Geométrico**: Valida que tu sprite sea un verdadero LPC (64×64)
✓ **Limpieza de Transparencia**: Elimina fondos negros automáticamente
✓ **Generación de Atlas**: Crea JSON y PNG para Phaser 3
✓ **Pivotes Inteligentes**: Los personajes se posicionan en los pies (0.5, 0.9)
✓ **Cajas de Colisión**: Generadas automáticamente en el 25% inferior
✓ **Nomenclatura LPC**: Nombres automáticos (walk_down_0, idle_up_2, etc.)
✓ **Estadísticas**: Reportes de cobertura, memoria y animaciones
✓ **Integración Phaser**: Código TypeScript generado automáticamente

---

## 🎯 COMANDOS MÁS COMUNES

### Comando Básico (recomendado - Interactivo)
```bash
python lpc_process.py
```
✓ Se abre selector gráfico de archivos
✓ Diálogos para configurar opciones
✓ Más cómodo y visual

### Especificar Sprite (Línea de Comandos)
```bash
python lpc_process.py --sprite "src/assets/mi-sprite.png"
```

### Especificar Salida
```bash
python lpc_process.py --sprite "hero.png" --output "output/sprites"
```

### Cambiar Nombre del Atlas
```bash
python lpc_process.py --prefix "hero_atlas"
```
Genera: `hero_atlas.png` y `hero_atlas.json`

### Ajustar Transparencia (si tiene fondo oscuro)
```bash
python lpc_process.py --tolerance 30
```
Valores:
- 10-15: Fondo negro puro
- 20-25: Fondo negro normal (por defecto)
- 30-40: Fondo negro oscuro/gris

### Ver Ayuda Completa
```bash
python lpc_process.py --help
```

### Solo Validar (sin generar)
```bash
python lpc_process.py --validate-only
```

### Debug Detallado
```bash
python lpc_process.py --verbose
```

---

## 🧪 PROBAR QUE TODO FUNCIONA

```bash
python test_lpc_pipeline.py
```

Esto ejecuta 7 tests que validan:
1. Que los módulos se importan correctamente
2. Que la validación de sprites funciona
3. Que se generan mapeos de animaciones
4. Que se calculan estadísticas
5. Que funciona el analizador
6. Que funciona el exportador Phaser
7. Que el pipeline completo está OK

Si todo dice "✓", ¡tu sistema está listo!

---

## 📊 ANALIZAR UN SPRITE

Para ver información detallada de tu sprite:

```bash
python lpc_utils.py analyze "src/assets/character-spritesheet.png"
```

Te muestra:
- Dimensiones exactas
- Formato y modo de color
- Tamaño del archivo
- Porcentaje de transparencia
- Si es un sprite LPC válido
- Cuántos frames contiene

---

## ❌ SI ALGO SALE MAL

### Error: "ModuleNotFoundError: cv2"
**Solución:**
```bash
pip install opencv-python
```

### Error: "ModuleNotFoundError: PIL"
**Solución:**
```bash
pip install Pillow
```

### Error: "Sprite sheet not found"
**Solución:**
Coloca tu sprite en: `src/assets/character-spritesheet.png`

O especifica la ruta:
```bash
python lpc_process.py --sprite "ruta/correcta.png"
```

### "El atlas tiene fondo negro en lugar de transparencia"
**Solución:**
Aumenta la tolerancia:
```bash
python lpc_process.py --tolerance 30
```

### "Phaser dice 'Frame not found' al cargar"
**Solución:**
1. Verifica el nombre del frame en `lpc_atlas.json`
2. Asegúrate que el atlas se cargó correctamente
3. Los nombres son sensibles a mayúsculas/minúsculas

**Para debug:**
```bash
python lpc_process.py --verbose
```

Más ayuda en **HELP.md** (sección Troubleshooting)

---

## 🎨 NOMENCLATURA DE FRAMES

El sistema genera nombres automáticos así:

```
{animación}_{dirección}_{número}

Ejemplos:
walk_down_0     ← Primer frame de "walk" hacia abajo
walk_up_7       ← Octavo frame de "walk" hacia arriba
idle_left_2     ← Tercer frame de "idle" hacia la izquierda
slash_right_4   ← Quinto frame de "slash" hacia la derecha
```

Las **direcciones** soportadas son:
- `down`  (sur ↓)
- `up`    (norte ↑)
- `left`  (oeste ←)
- `right` (este →)

Las **animaciones** estándar LPC son:
`idle`, `walk`, `run`, `attack`, `slash`, `shoot`, `hurt`, etc.

---

## 📁 ARCHIVOS GENERADOS

Después de ejecutar `python lpc_process.py`, se crean:

```
src/assets/
├── lpc_atlas.png          ← Tu sprite limpiado con transparencia
├── lpc_atlas.json         ← Metadata para Phaser 3
└── lpc_atlas_stats.json   ← Estadísticas del procesamiento

src/game/
├── lpc-config.ts          ← Configuración Phaser (auto-gen)
└── ExampleScene.ts        ← Escena de ejemplo (auto-gen)
```

### Qué es cada uno

**lpc_atlas.png**: Tu sprite original pero procesado
- Fondo limpiado (transparente)
- Mismo tamaño
- Listo para usar en Phaser

**lpc_atlas.json**: Metadata que Phaser necesita
- Posición de cada frame
- Pivotes (puntos de anclaje)
- Cajas de colisión
- Nombres de frames

**lpc_atlas_stats.json**: Información de debug
- Cuántos frames hay
- Cobertura del atlas
- Memoria aproximada
- Animaciones detectadas

**lpc-config.ts**: Código Phaser automático
- Funciones para cargar el atlas
- Funciones para crear animaciones
- Clase LPCCharacter ready-to-use

**ExampleScene.ts**: Ejemplo funcional
- Scene de demostración
- Manejo de controles
- Todo listo para adaptarlo

---

## 🔧 CONFIGURACIÓN AVANZADA

Si necesitas personalizar el comportamiento, edita `lpc_config.py`:

```python
# Cambiar tamaño de célula (si tu sprite no es 64×64)
LPC_CONFIG['CELL_SIZE'] = 64

# Cambiar pivote del personaje
LPC_CONFIG['PIVOT'] = {'x': 0.5, 'y': 0.9}

# Cambiar altura de caja de colisión
LPC_CONFIG['COLLISION']['height_ratio'] = 0.25  # 25% inferior
```

---

## 💻 REQUISITOS TÉCNICOS

### Sistema
- Windows / macOS / Linux
- Python 3.7 o superior
- ~100MB de espacio disco

### Dependencias Python
- opencv-python (procesamiento imágenes)
- Pillow (manejo PNG)
- numpy (usado por OpenCV)

### Navegador (para Phaser)
- Cualquier navegador moderno con WebGL

---

## 🎯 FLUJO TÍPICO DE TRABAJO

```
1. Tengo un sprite LPC
         ↓
2. Ejecuto: python lpc_process.py
         ↓
3. Se genera lpc_atlas.png y lpc_atlas.json
         ↓
4. Los importo en mi Scene Phaser
         ↓
5. Creo animaciones con los nombres generados
         ↓
6. Reproduzco animaciones en mi sprite
         ↓
7. ¡Juego con sprites LPC en Phaser! 🎮
```

---

## 📞 AYUDA RÁPIDA

| Necesito | Hago |
|----------|------|
| Empezar rápido | Lee QUICKSTART.md |
| Ver opciones | Ejecuta `--help` |
| Referencia rápida | Lee HELP.md |
| Debug | Ejecuta `--verbose` |
| Validar | Ejecuta `--validate-only` |
| Analizar sprite | `python lpc_utils.py analyze` |
| Entender todo | Lee LPC_ATLAS_README.md |

---

## ✅ CHECKLIST FINAL

- [ ] He instalado requirements.txt
- [ ] He leído QUICKSTART.md
- [ ] Tengo un sprite PNG en src/assets/
- [ ] Ejecuté python lpc_process.py
- [ ] Se crearon lpc_atlas.png y lpc_atlas.json
- [ ] Importé el atlas en mi Scene Phaser
- [ ] Creé una animación
- [ ] Reproducí la animación en un sprite
- [ ] ¡Mi sprite se ve en Phaser! 🎉

---

## 🚀 ¡LISTO PARA EMPEZAR!

**3 pasos simples:**

1. **Instala:**
```bash
pip install -r requirements.txt
```

2. **Ejecuta:**
```bash
python lpc_process.py
```

3. **Usa en Phaser:**
```typescript
scene.load.atlas('lpc_atlas', 'assets/lpc_atlas.png', 'assets/lpc_atlas.json');
```

**¡Eso es todo!** Tu sprite LPC está listo para Phaser 3.

---

## 📚 MÁS INFORMACIÓN

- **Inicio rápido:** QUICKSTART.md
- **Referencia:** HELP.md
- **Documentación:** LPC_ATLAS_README.md
- **Índice:** INDEX.md

---

## 💡 TIPS

✅ Siempre valida primero: `--validate-only`
✅ Si el atlas tiene fondo negro, aumenta `--tolerance`
✅ Los nombres de frames son case-sensitive
✅ El pivote automático va en los pies (0.5, 0.9)
✅ Las colisiones ocupan el 25% inferior
✅ Usa `--verbose` si algo falla

---

**¡Ahora sí! A crear increíbles juegos 2D con LPC y Phaser 3! 🎮✨**

Made with ❤️ for Game Developers

