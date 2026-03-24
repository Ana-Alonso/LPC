# 📑 ÍNDICE DE ARCHIVOS - LPC ATLAS GENERATOR
## Guía de Navegación Completa

---

## 🚀 COMIENZA AQUÍ

### Para empezar en 5 minutos
→ **QUICKSTART.md**
- Instalación paso a paso
- Primer comando
- Uso básico
- Troubleshooting rápido

### Para ver opciones disponibles
→ **HELP.md**
- Tabla de comandos
- Ejemplos comunes
- Tips útiles
- Referencia rápida

---

## 📚 DOCUMENTACIÓN

### Documentación General del Proyecto
→ **LPC_GENERATOR_README.md**
- Visión general
- Características principales
- Estructura del proyecto
- Integración Phaser 3
- Referencias

### Documentación Técnica Completa
→ **LPC_ATLAS_README.md**
- Análisis geométrico
- Limpieza y transparencia
- Generación de atlas
- Pivotes y colisiones
- API completa
- Troubleshooting avanzado

### Resumen de Archivos Generados
→ **RESUMEN_ARCHIVOS_GENERADOS.md**
- Qué se generó
- Estadísticas del proyecto
- Flujo de trabajo
- Sistema modular
- Validaciones

---

## 💻 SCRIPTS PRINCIPALES

### Script Ejecutable Principal
→ **lpc_process.py** (490 líneas)
```bash
python lpc_process.py [opciones]
```

**Funciones:**
- Interfaz CLI completa
- Procesamiento de sprites
- Validación automática
- Generación de atlas
- Manejo de errores

**Opciones:**
- `--sprite RUTA` - Ruta al sprite
- `--prefix NOMBRE` - Prefijo de salida
- `--tolerance NUM` - Umbral (0-255)
- `--validate-only` - Solo validar
- `--verbose` - Debug detallado
- `--help` - Ver ayuda

### Gestor de Integración
→ **lpc_integration_manager.py** (530 líneas)
```python
from lpc_integration_manager import LPCIntegrationManager
manager = LPCIntegrationManager(".")
manager.generate_integration_package()
```

**Funciones:**
- Buscar sprites automáticamente
- Generar configuración Phaser
- Crear escenas de ejemplo
- Integración con React

### Suite de Tests
→ **test_lpc_pipeline.py** (400 líneas)
```bash
python test_lpc_pipeline.py
```

**Validaciones:**
- Importaciones
- Validación de sprites
- Generación de mapeos
- Estadísticas
- Analizador
- Exportador Phaser
- Pipeline completo

---

## 🔧 MÓDULOS CORE

### Motor Principal de Generación
→ **lpc_atlas_generator.py** (700+ líneas)

**Clases:**
- `LPCAtlasGenerator` - Motor principal
- `FrameData` - Dataclass de frames
- `CollisionBox` - Dataclass de colisiones
- `PhaserAtlasLoader` - Utilidades Phaser

**Métodos principales:**
- `validate_geometry()` - Valida 64×64
- `clean_transparency()` - Limpia fondos
- `extract_frames()` - Extrae frames
- `generate_atlas_json()` - Crea JSON
- `save_atlas()` - Guarda archivos
- `generate_complete_atlas()` - Pipeline completo

### Features Avanzadas
→ **lpc_atlas_advanced.py** (450+ líneas)

**Clases:**
- `AnimationMapGenerator` - Mapeos de anim.
- `SpriteSheetValidator` - Validaciones
- `AtlasStatisticsGenerator` - Estadísticas
- `PhaserExporter` - Exportación

**Constantes:**
- `ANIMATION_CONFIGS` - Presets
- `LPC_STANDARD_ANIMATION_MAP` - Mapa LPC
- `LPC_STANDARD_ANIMATION_MAP` - Animaciones

### Utilidades y Herramientas
→ **lpc_utils.py** (400+ líneas)

**Clases:**
- `BatchProcessor` - Procesa lotes
- `SpriteAnalyzer` - Analiza sprites
- `SpriteComparator` - Compara múltiples
- `ReportGenerator` - Genera reportes

**Usos:**
```bash
python lpc_utils.py analyze "sprite.png"
python lpc_utils.py compare "src/assets"
```

### Configuración Centralizada
→ **lpc_config.py** (300+ líneas)

**Contenido:**
- `LPC_CONFIG` - Configuración LPC
- `OUTPUT_CONFIG` - Config de salida
- `PHASER_CONFIG` - Config Phaser
- `VALIDATION_CONFIG` - Validaciones
- `LOGGING_CONFIG` - Logging
- `BATCH_CONFIG` - Batch processing
- `PRESETS` - Presets predefinidos

**Usos:**
```python
from lpc_config import LPC_CONFIG, get_tolerance_for_preset
cell_size = LPC_CONFIG['CELL_SIZE']
tol = get_tolerance_for_preset('aggressive')
```

---

## 📋 CONFIGURACIÓN Y REQUISITOS

### Dependencias Python
→ **requirements.txt**

```
opencv-python>=4.5.0
Pillow>=9.0.0
numpy>=1.21.0
```

**Instalación:**
```bash
pip install -r requirements.txt
```

---

## 📂 DIRECTORIOS DE ENTRADA/SALIDA

### Entrada
```
src/assets/
└── character-spritesheet.png  ← Tu sprite aquí
```

### Salida Generada
```
src/assets/
├── lpc_atlas.png              ← Sprite procesado
├── lpc_atlas.json             ← Metadata Phaser
└── lpc_atlas_stats.json       ← Estadísticas

src/game/
├── lpc-config.ts              ← Config Phaser
└── ExampleScene.ts            ← Escena ejemplo
```

---

## 🎯 FLUJOS DE TRABAJO

### Flujo 1: Procesamiento Simple
```
1. Ejecuta:        python lpc_process.py
2. Revisa output:  src/assets/lpc_atlas.*
3. Usa en Phaser:  load.atlas(...)
```

### Flujo 2: Procesamiento Personalizado
```
1. Ejecuta:        python lpc_process.py --sprite "hero.png" --prefix "hero"
2. Revisa output:  src/assets/hero.*
3. Usa en Phaser:  load.atlas('hero', ...)
```

### Flujo 3: Debug y Análisis
```
1. Valida:         python lpc_process.py --validate-only
2. Analiza:        python lpc_utils.py analyze "sprite.png"
3. Procesa:        python lpc_process.py --verbose
4. Inspecciona:    cat src/assets/lpc_atlas_stats.json
```

### Flujo 4: Integración Completa
```
1. Importa:        from lpc_integration_manager import LPCIntegrationManager
2. Crea manager:   manager = LPCIntegrationManager(".")
3. Genera:         manager.generate_integration_package()
4. Usa output:     src/game/lpc-config.ts
```

---

## 🧪 TESTING Y VALIDACIÓN

### Validar Instalación
```bash
python test_lpc_pipeline.py
```

Se ejecutan 7 tests:
1. Importaciones
2. Validación de sprites
3. Mapeos de animaciones
4. Estadísticas
5. Analizador de sprites
6. Exportador Phaser
7. Pipeline completo

---

## 📖 GUÍA DE LECTURA RECOMENDADA

### Ruta para Principiantes
1. **QUICKSTART.md** (5 min)
   - Entender los pasos básicos
   
2. **HELP.md** (10 min)
   - Ver opciones disponibles
   
3. **Ejecutar ejemplo:**
   ```bash
   python lpc_process.py
   ```

### Ruta para Usuarios Avanzados
1. **LPC_ATLAS_README.md** (20 min)
   - Entender arquitectura
   
2. **lpc_config.py**
   - Personalizar configuración
   
3. **lpc_integration_manager.py**
   - Integración automática

### Ruta Técnica Completa
1. **lpc_atlas_generator.py**
   - Entender algoritmos
   
2. **lpc_atlas_advanced.py**
   - Features avanzadas
   
3. **lpc_utils.py**
   - Utilidades
   
4. **test_lpc_pipeline.py**
   - Validar funcionamiento

---

## 🔗 CONEXIONES ENTRE ARCHIVOS

```
lpc_process.py
├─ importa lpc_atlas_generator.py
│  └─ usa LPCAtlasGenerator
│
├─ importa lpc_atlas_advanced.py
│  └─ usa SpriteSheetValidator, AtlasStatisticsGenerator
│
├─ importa lpc_integration_manager.py
│  └─ usa LPCIntegrationManager
│
└─ importa lpc_config.py
   └─ usa LPC_CONFIG, get_tolerance_for_preset

test_lpc_pipeline.py
├─ importa todos los módulos
└─ valida que todo funcione

lpc_utils.py
├─ independiente pero usable con otros
└─ proporciona análisis adicionales
```

---

## 💡 CASOS DE USO

### Caso 1: "Quiero procesar mi sprite rápido"
→ Lee: **QUICKSTART.md**
→ Ejecuta: `python lpc_process.py`

### Caso 2: "Necesito ajustar la tolerancia"
→ Lee: **HELP.md** (sección Tolerancia)
→ Ejecuta: `python lpc_process.py --tolerance 30`

### Caso 3: "Quiero entender cómo funciona"
→ Lee: **LPC_ATLAS_README.md**
→ Inspecciona: **lpc_atlas_generator.py**

### Caso 4: "Tengo múltiples sprites"
→ Lee: **LPC_ATLAS_README.md** (sección Batch)
→ Usa: **lpc_utils.py** (BatchProcessor)

### Caso 5: "Quiero integración automática con Phaser"
→ Lee: **LPC_GENERATOR_README.md** (Integración)
→ Usa: **lpc_integration_manager.py**

### Caso 6: "Mi sprite tiene problemas"
→ Lee: **HELP.md** (Troubleshooting)
→ Ejecuta: `python lpc_process.py --verbose`

---

## 🎓 REFERENCIAS RÁPIDAS

### Comandos Frecuentes
```bash
# Procesar con default
python lpc_process.py

# Especificar archivo
python lpc_process.py --sprite "hero.png"

# Cambiar nombre
python lpc_process.py --prefix "hero_atlas"

# Aumentar tolerancia
python lpc_process.py --tolerance 30

# Debug
python lpc_process.py --verbose

# Tests
python test_lpc_pipeline.py

# Analizar
python lpc_utils.py analyze "sprite.png"
```

### Variables Importantes
```python
# Tamaño de célula LPC
CELL_SIZE = 64

# Pivote del personaje
PIVOT = (0.5, 0.9)  # Centro, pies

# Caja de colisión
COLLISION_HEIGHT_RATIO = 0.25  # 25% inferior
COLLISION_WIDTH_RATIO = 0.8    # 80% ancho

# Tolerancia default
DEFAULT_TOLERANCE = 20
```

### Nomenclatura de Frames
```
Formato: {animación}_{dirección}_{frame}

Ejemplo: walk_down_0
         ↓     ↓    ↓
    animación dirección frame_number

Direcciones: down, up, left, right
```

---

## ✅ CHECKLIST DE USO

- [ ] He leído QUICKSTART.md
- [ ] Tengo Python 3.7+
- [ ] Instalé requirements.txt
- [ ] Tengo sprite en src/assets/
- [ ] Ejecuté python lpc_process.py
- [ ] Verifiqué que se creó lpc_atlas.png
- [ ] Importé atlas en mi Scene Phaser
- [ ] Creé animaciones
- [ ] Reproducí sprite

---

## 📞 SOPORTE RÁPIDO

**Problema → Solución:**

| Problema | Solución |
|----------|----------|
| Módulo no encontrado | `pip install -r requirements.txt` |
| Sprite no existe | `--sprite "ruta/correcta.png"` |
| Fondo negro | `--tolerance 30` |
| Frame no existe | Chequea nombres en JSON |
| Error Python | `--verbose` y revisa HELP.md |

---

## 🎉 ¡LISTO PARA EMPEZAR!

### Sigue estos 3 pasos:

1. **Lee QUICKSTART.md** (5 min)
2. **Instala:** `pip install -r requirements.txt`
3. **Ejecuta:** `python lpc_process.py`

---

**Última actualización:** 2024
**Versión:** 1.0.0
**Licencia:** MIT

