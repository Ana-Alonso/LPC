# LPC Sprite Atlas Generator

Convierte un sprite sheet LPC (PNG) en un atlas compatible con Phaser 3.

## Requisitos

- Python 3.7+
- Dependencias de `requirements.txt`

## Instalacion

```bash
pip install -r requirements.txt
```

## Uso rapido

### Modo interactivo (recomendado)

```bash
python lpc_process.py
```

Si ejecutas sin argumentos, el script abre dialogos graficos para:
1. Seleccionar el sprite PNG.
2. Elegir la carpeta de salida.
3. Definir prefijo del atlas.
4. Ajustar tolerancia (0-255).

### Modo CLI (sin dialogos)

```bash
python lpc_process.py --sprite "ruta/al/sprite.png" --output "ruta/salida" --prefix "hero_atlas" --tolerance 20 --verbose
```

## Opciones principales

- `--sprite`: ruta al sprite PNG.
- `--output`: directorio de salida (por defecto, carpeta del sprite).
- `--prefix`: prefijo de archivos generados (por defecto `lpc_atlas`).
- `--tolerance`: tolerancia de transparencia 0-255 (por defecto `20`).
- `--validate-only`: valida el sprite sin generar atlas.
- `--verbose`: salida detallada para depuracion.
- `--help`: muestra ayuda.
- `--version`: muestra version.

## Archivos generados

El pipeline genera, como minimo:
- `<prefix>.png`
- `<prefix>.json`

Se guardan en la carpeta definida por `--output` o en la carpeta del sprite.

## Validacion y pruebas

```bash
python lpc_process.py --validate-only --sprite "ruta/al/sprite.png"
python test_lpc_pipeline.py
```

## Integracion en Phaser 3

```typescript
this.load.atlas('lpc_atlas', 'assets/lpc_atlas.png', 'assets/lpc_atlas.json');
```

Los frames siguen un patron tipo `walk_down_0`, `idle_up_3`, etc.

## Troubleshooting rapido

- `ModuleNotFoundError: No module named 'cv2'` -> `pip install opencv-python`
- `ModuleNotFoundError: No module named 'PIL'` -> `pip install Pillow`
- Fondo negro en salida -> subir `--tolerance` (por ejemplo `30`).

## Notas

- El script principal es `lpc_process.py`.
- Para detalles tecnicos, usa `python lpc_process.py --help`.

