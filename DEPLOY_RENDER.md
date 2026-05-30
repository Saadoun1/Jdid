# Deploy on Render

Use these settings when creating the Render web service:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

Environment variables:

- `ADMIN_PASSWORD`: the password for `/admin`
- `SECRET_KEY`: any long random text
- `DATABASE_PATH`: `database.db` locally, or `/opt/render/project/src/storage/database.db` if you attach a Render disk

Important: SQLite stores data in a file. On Render, use a persistent disk if you want submitted names to survive deploys/restarts.

