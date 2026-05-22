# Despliegue en Vercel — notas y pasos

Este repositorio ya contiene la configuración mínima para que Vercel detecte y arranque la aplicación Flask:

- `pyproject.toml` con `tool.vercel.entrypoint = "run:app"` (entrypoint WSGI).
- `vercel.json` con `@vercel/python` como builder y `run.py` como destino.

Pasos recomendados para desplegar en Vercel (UI o CLI):

1. Conectar el repositorio `pitonC/Patrones4` en Vercel (Import Project).
2. En Settings → Environment Variables, añade las variables necesarias:
   - `SECRET_KEY` (secreto Flask)
   - `DATABASE_URL` (recomendado: usar Postgres/managed DB en vez de SQLite)
   - Si migras uploads a S3: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET_NAME`, `S3_REGION`

Limitaciones importantes (leer antes de desplegar):

- Persistencia de disco: Vercel funciona en entornos serverless — el disco local no es persistente entre invocaciones y no está pensado para almacenar archivos subidos ni bases de datos SQLite en producción. En este repositorio la app usa por defecto:
  - `instance/photo_editor.sqlite3` (SQLite) — NO persistirá correctamente en Vercel.
  - `app/static/uploads/` para imágenes subidas — NO persistirá.

Recomendaciones para producción en Vercel:

- Usar una base de datos gestionada (Postgres) y configurar `DATABASE_URL` en Vercel.
- Mover las subidas a un almacenamiento externo (S3, Google Cloud Storage) y configurar el código para usar el bucket. Alternativa: mantener las subidas en un servicio dedicado.
- Si prefieres evitar estos cambios, despliega en un servicio con disco persistente (Render, Railway, DigitalOcean App Platform) donde SQLite y la carpeta `uploads` funcionen "como en local".

Comandos útiles (vercel CLI):

```bash
# inicia sesión si hace falta
vercel login
# desplegar manualmente
vercel --prod
```

Si quieres, puedo:
- Adaptar el proyecto para usar Postgres + S3 (añadir cambios en `app/__init__.py` y el storage service).
- Preparar un `docker-compose` minimal para desplegar en un host con Docker.
- O desplegarte en Render/Railway y ajustar settings.
