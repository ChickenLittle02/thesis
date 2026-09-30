#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def generar_arbol(ruta, archivo_salida, prefijo="", profundidad=0, max_profundidad=3):
    """
    Recorre recursivamente el directorio y escribe su estructura en un archivo.
    """
    if profundidad > max_profundidad:
        return

    try:
        # Obtener lista de elementos (archivos y carpetas) ordenada
        elementos = sorted(os.listdir(ruta))
    except PermissionError:
        # Si no se puede acceder, escribir un mensaje y continuar
        archivo_salida.write(f"{prefijo}[Permiso denegado]\n")
        return

    for i, elemento in enumerate(elementos):
        # Determinar si es el último elemento para la simbología del árbol
        es_ultimo = (i == len(elementos) - 1)
        conector = "└── " if es_ultimo else "├── "
        ruta_completa = os.path.join(ruta, elemento)

        # Escribir el elemento actual con el prefijo y conector adecuados
        archivo_salida.write(f"{prefijo}{conector}{elemento}\n")

        # Si es un directorio, recursión (aumentar profundidad)
        if os.path.isdir(ruta_completa):
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            generar_arbol(ruta_completa, archivo_salida, nuevo_prefijo, profundidad + 1, max_profundidad)

def main():
    # Directorio raíz: donde se ejecuta el script (puedes cambiarlo)
    directorio_inicial = os.getcwd()
    archivo_salida_nombre = "arbol_depth3.txt"

    try:
        with open(archivo_salida_nombre, "w", encoding="utf-8") as f:
            # Escribir la raíz
            f.write(f"{os.path.basename(directorio_inicial)}/\n")
            generar_arbol(directorio_inicial, f, "", 0, 3)
        print(f"✅ Árbol guardado en '{archivo_salida_nombre}' (profundidad máxima = 3)")
    except Exception as e:
        print(f"❌ Error al generar el árbol: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()