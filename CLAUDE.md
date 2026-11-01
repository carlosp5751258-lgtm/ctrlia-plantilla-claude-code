# Proyecto: app de ejemplo (plantilla Ctrl+IA)

## Comandos
- Tests: `python3 -m unittest discover -s tests -v`
- Un solo test: `python3 -m unittest tests.test_app -v`
- No hay paso de build: es Python puro, sin dependencias externas.

## Cómo trabajamos
- Antes de dar algo por terminado, ejecuta los tests y pega el comando y su salida.
- Cambios pequeños: una tarea, una rama, un pull request.
- No añadas dependencias nuevas sin preguntar primero.
- No toques `.github/workflows/` ni `.claude/` salvo que te lo pida.

## Lo que no está en el código
- Los secretos van en `.env` (no está en git). Usa `.env.example` para saber qué variables existen; nunca leas ni copies `.env`.
- `main` está protegida: solo se fusiona por pull request con el CI en verde.
