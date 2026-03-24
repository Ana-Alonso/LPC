#!/usr/bin/env python3
"""
LPC Atlas Configuration File
=============================
Archivo centralizado de configuración para todo el sistema LPC.

Puedes personalizar todas las opciones aquí.
"""

# ============================================================================
# CONFIGURACIÓN LPC ESTÁNDAR
# ============================================================================

LPC_CONFIG = {
    # Geometría
    'CELL_SIZE': 64,                    # Tamaño estándar de célula LPC
    'STANDARD_WIDTH': 832,              # 13 celdas × 64px

    # Transparencia
    'TRANSPARENCY': {
        'default_tolerance': 20,        # Umbral por defecto (0-255)
        'target_color': (0, 0, 0),     # Color negro en BGR
        'min_tolerance': 0,
        'max_tolerance': 255,
    },

    # Pivotes
    'PIVOT': {
        'x': 0.5,                       # Centro horizontal
        'y': 0.9,                       # En los pies
    },

    # Colisiones
    'COLLISION': {
        'height_ratio': 0.25,           # 25% del frame
        'width_ratio': 0.8,             # 80% del ancho
    },

    # Animaciones estándar
    'ANIMATIONS': [
        'spellcast',    # Lanzar hechizo
        'thrust',       # Empuje/Estocada
        'walk',         # Caminar
        'slash',        # Corte
        'shoot',        # Disparar
        'hurt',         # Recibir daño
        'climb',        # Escalar
        'idle',         # Inactivo
        'jump',         # Saltar
        'sit',          # Sentarse
        'emote',        # Emote/Expresión
        'run',          # Correr
        'combat_idle',  # Inactivo en combate
        'backslash',    # Corte inverso
        'halfslash',    # Medio corte
    ],

    # Direcciones
    'DIRECTIONS': {
        'down': 0,      # Sur ↓
        'left': 1,      # Oeste ←
        'right': 2,     # Este →
        'up': 3,        # Norte ↑
    },
}

# ============================================================================
# CONFIGURACIÓN DE SALIDA
# ============================================================================

OUTPUT_CONFIG = {
    # Prefijo por defecto
    'default_prefix': 'lpc_atlas',

    # Formatos soportados
    'formats': {
        'PNG': {
            'extension': '.png',
            'mode': 'RGBA8888',
            'quality': 95,
        },
        'JSON': {
            'extension': '.json',
            'indent': 2,
            'ensure_ascii': False,
        },
    },

    # Generación automática
    'auto_generate': {
        'stats': True,
        'phaser_config': True,
        'example_scene': True,
    },
}

# ============================================================================
# CONFIGURACIÓN PHASER 3
# ============================================================================

PHASER_CONFIG = {
    # Nombre de texture por defecto
    'default_texture_name': 'lpc_atlas',

    # Configuración de animaciones
    'animation_defaults': {
        'frameRate': 10,
        'repeat': -1,
        'delay': 0,
        'yoyo': False,
    },

    # Physics (física)
    'physics': {
        'enabled': True,
        'type': 'arcade',
        'bounce': 0.1,
        'collideWorldBounds': True,
    },
}

# ============================================================================
# CONFIGURACIÓN DE VALIDACIÓN
# ============================================================================

VALIDATION_CONFIG = {
    # Validaciones estrictas
    'strict_mode': False,

    # Advertencias
    'warnings': {
        'non_standard_size': True,
        'high_memory_usage': True,
        'transparency_issues': True,
    },

    # Límites
    'limits': {
        'max_image_size': (4096, 4096),
        'min_image_size': (64, 64),
        'max_file_size_mb': 50,
    },
}

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'format': '%(asctime)s - [%(levelname)s] %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'file': None,                       # Ruta para guardar logs (None = solo consola)
}

# ============================================================================
# CONFIGURACIÓN DE BATCH PROCESSING
# ============================================================================

BATCH_CONFIG = {
    'max_workers': 4,                   # Threads paralelos
    'skip_errors': False,               # Continuar en caso de error
    'verbose_progress': True,           # Mostrar progreso detallado
    'generate_summary': True,           # Generar reporte final
}

# ============================================================================
# CONFIGURACIÓN DE ESTADÍSTICAS
# ============================================================================

STATS_CONFIG = {
    'calculate_coverage': True,
    'estimate_memory': True,
    'count_animations': True,
    'export_formats': ['json', 'csv', 'html'],
}

# ============================================================================
# PRESETS PREDEFINIDOS
# ============================================================================

PRESETS = {
    'aggressive': {
        'tolerance': 15,
        'description': 'Tolerancia baja, fondos muy limpios',
        'use_case': 'Sprites con fondos negros puros',
    },
    'normal': {
        'tolerance': 20,
        'description': 'Tolerancia normal, balanceado',
        'use_case': 'Sprites LPC estándar',
    },
    'lenient': {
        'tolerance': 30,
        'description': 'Tolerancia alta, permite más ruido',
        'use_case': 'Sprites con fondos oscuros',
    },
    'ultra_lenient': {
        'tolerance': 40,
        'description': 'Tolerancia muy alta',
        'use_case': 'Sprites con fondos complejos',
    },
}

# ============================================================================
# FUNCIONES HELPER
# ============================================================================

def get_preset(preset_name: str = 'normal'):
    """Obtiene configuración de un preset."""
    if preset_name not in PRESETS:
        raise ValueError(f"Preset desconocido: {preset_name}")
    return PRESETS[preset_name]

def get_tolerance_for_preset(preset_name: str) -> int:
    """Obtiene tolerancia para un preset."""
    return get_preset(preset_name)['tolerance']

def validate_tolerance(tolerance: int) -> bool:
    """Valida que la tolerancia esté en rango."""
    min_tol = LPC_CONFIG['TRANSPARENCY']['min_tolerance']
    max_tol = LPC_CONFIG['TRANSPARENCY']['max_tolerance']
    return min_tol <= tolerance <= max_tol

def get_default_tolerance() -> int:
    """Obtiene tolerancia por defecto."""
    return LPC_CONFIG['TRANSPARENCY']['default_tolerance']

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("Configuración LPC Atlas")
    print("=" * 50)
    print(f"\nTamaño de célula: {LPC_CONFIG['CELL_SIZE']}x{LPC_CONFIG['CELL_SIZE']}")
    print(f"Pivote: ({LPC_CONFIG['PIVOT']['x']}, {LPC_CONFIG['PIVOT']['y']})")
    print(f"Tolerancia por defecto: {get_default_tolerance()}")

    print(f"\nAnimaciones soportadas ({len(LPC_CONFIG['ANIMATIONS'])}):")
    for i, anim in enumerate(LPC_CONFIG['ANIMATIONS'], 1):
        print(f"  {i:2}. {anim}")

    print(f"\nPresets disponibles ({len(PRESETS)}):")
    for preset_name, preset_config in PRESETS.items():
        print(f"  - {preset_name:15} | Tolerancia: {preset_config['tolerance']:2} | {preset_config['use_case']}")

    print("\nUso en código:")
    print("  from lpc_config import LPC_CONFIG, get_tolerance_for_preset")
    print("  tolerance = get_tolerance_for_preset('aggressive')")
    print("  cell_size = LPC_CONFIG['CELL_SIZE']")

