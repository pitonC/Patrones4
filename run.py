"""Punto de entrada para correr la aplicación Flask en local.

Se envuelve la creación de la app en un try/except para que, si hay
errores en tiempo de inicialización (ej. dependencias faltantes, DB),
la traza se imprima en stdout y quede visible en los logs de Vercel.
"""
from app import create_app
import traceback
import sys

try:
    app = create_app()
except Exception:
    traceback.print_exc()
    # Re-raise para que la plataforma registre el fallo, pero imprimimos
    # la traza arriba para facilitar debugging en logs.
    raise


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
