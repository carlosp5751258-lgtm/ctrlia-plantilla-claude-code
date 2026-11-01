---
name: probar
description: Ejecuta los tests del proyecto y resume el resultado con la evidencia. Úsala después de cambiar código o cuando el usuario pregunte si algo funciona.
allowed-tools: Bash(python3 -m unittest *)
---
1. Ejecuta `python3 -m unittest discover -s tests -v`.
2. Si todo pasa, responde con el número de tests y la última línea de la salida (por ejemplo `OK`).
3. Si algo falla, copia el nombre del test, el error y el archivo y la línea donde ocurre.
   Propón la causa más probable, pero no cambies código si el usuario solo pidió probar.
4. Nunca digas «todo funciona» sin pegar la salida real.
