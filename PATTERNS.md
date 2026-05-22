# Documentación de los 4 patrones (Código)

Este documento describe exclusivamente el código y **dónde** están implementados los cuatro patrones mencionados en el proyecto.

## 1) Command
- Archivo principal: [app/patterns/command.py](app/patterns/command.py)
- Uso/consumo desde: [app/routes/api.py](app/routes/api.py)
- Persistencia / modelo relacionado: [app/models.py](app/models.py) → `HistoryEntry`.

Qué mirar:
- `Command` (abstracto) — métodos `execute()` y `undo()`.
- Comandos concretos: `AddShapeCommand`, `CloneLayerCommand`, `DeleteLayerCommand`, `UpdateLayerCommand`, `ApplyFilterCommand`.
- `CommandHistory` — invocador que guarda `HistoryEntry` en BD y mantiene undo/redo.
- `COMMAND_REGISTRY` — registry simple que permite reconstruir comandos por nombre.

Por qué está aquí: modela acciones del editor (add, clone, delete, update, apply-filter) y permite undo/redo persistente en SQLite.

---

## 2) Decorator
- Archivo principal: [app/patterns/decorator.py](app/patterns/decorator.py)
- Uso/consumo desde: [app/services/renderer.py](app/services/renderer.py)

Qué mirar:
- `ImageComponent` (interfaz) y `BaseImageComponent`.
- `FilterDecorator` (abstracto) y las implementaciones concretas (`BrightnessFilter`, `ContrastFilter`, `SaturationFilter`, etc.).
- `FILTER_REGISTRY` y `build_pipeline(filters)` construyen la cadena de decoradores a partir del JSON guardado en `Layer.data`.

Por qué está aquí: cada slider crea/actualiza una entrada en `filters` y el renderer aplica la cadena de decoradores al `base` o a la imagen de la forma.

---

## 3) Prototype
- Archivo principal: [app/patterns/prototype.py](app/patterns/prototype.py)
- Uso desde: `CloneLayerCommand` en [app/patterns/command.py](app/patterns/command.py)

Qué mirar:
- `Prototype` (abstracto) y `LayerPrototype` con `clone()`.
- `clone_from_layer(layer)` — adapta un ORM `Layer` a un `LayerPrototype` y devuelve su clon con pequeño offset.

Por qué está aquí: implementa duplicación de capas (copy/paste) sin que los clientes necesiten conocer la estructura interna del `data`.

---

## 4) MVC (MTV) — arquitectura general
- Entrada / factory: [app/__init__.py](app/__init__.py)
- Modelos: [app/models.py](app/models.py)
- Rutas / Controladores HTML: [app/routes/main.py](app/routes/main.py)
- Rutas / API JSON: [app/routes/api.py](app/routes/api.py)
- Templates: [app/templates/index.html](app/templates/index.html), [app/templates/editor.html](app/templates/editor.html), [app/templates/base.html](app/templates/base.html)

Qué mirar:
- `create_app()` en `app/__init__.py` — registra blueprints y configura la app (Application Factory).
- Blueprints: `main` (HTML) y `api` (JSON) separan responsabilidades.
- `models.py` define `Project`, `Layer`, `HistoryEntry`.

Por qué está aquí: la separación Model–Template–View (MTV) facilita que la lógica de negocio (patrones) esté aislada del enrutamiento y del renderizado HTML.

---

## Apoyos / patrones auxiliares (relevantes)
- **Service layer**: [app/services/renderer.py](app/services/renderer.py) — composición/renderer centraliza la lógica de render de imagen.
- **Registry / factory**: `COMMAND_REGISTRY` y `FILTER_REGISTRY` permiten instanciar clases por nombre.
- **Mixin**: `TimestampMixin` en [app/models.py](app/models.py) reutiliza campos de fecha.

---

## Cómo usar este archivo
- Si quieres subir el repo a GitHub (por ejemplo `https://github.com/pitonC/Patrones4`), sigue las instrucciones en el archivo `PUSH_INSTRUCTIONS.md` que te puedo generar, o ejecuta los comandos que te dejo abajo.

---

Archivo creado por la revisión automática — solo documenta código (no incluye diseño ni instrucciones de uso). Si quieres, puedo:
- Generar un `PUSH_INSTRUCTIONS.md` con comandos `git` exactos para subir al repo `pitonC/Patrones4`.
- Crear un pequeño `docs/` con extractos de código y enlaces a líneas concretas.
- Hacer el push automáticamente si me das el acceso adecuado.

Dime qué prefieres.
