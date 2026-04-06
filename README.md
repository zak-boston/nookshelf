# 🍵 NookShelf

A cosy service dashboard for your homelab.
Add tiles for all your self-hosted services, drag to rearrange, and see at a glance
which ones are up.

![NookShelf screenshot — warm dark room with stone fireplace, wooden shelves, and service tiles]

---

## Folder structure

```
nookshelf/
├── app.py              ← Python/Flask backend
├── Dockerfile
├── docker-compose.yml
├── README.md
└── static/
    └── index.html      ← The UI (single file, no build step)
```

---

## Quick start

```bash
docker compose up -d --build
```

Then open **http://localhost:5001** in your browser,
or `http://<your-server-ip>:5001` from anywhere on your network.

---

## Features

| Feature | Details |
|---------|---------|
| 🍵 Service tiles | Name, description, URL, emoji icon, colour accent |
| 🟢 Status dots | Live up/down indicator on every tile, rechecks every 30s |
| 🗂️ Shelves | Group tiles into named shelves (Media, Tools, Diagnostics by default) |
| ↔️ Drag to rearrange | Reorder tiles within a shelf, or drag across shelves |
| ⠿ Shelf reordering | Drag entire shelves to change their order |
| 💾 Backup | One-click JSON download of your entire shelf layout |
| 💾 Persistent data | Shelf data saved to `data/nookshelf.json` on the host |

---

## How status dots work

NookShelf checks each service from the **server side** (Flask makes the request,
not your browser). This avoids CORS errors that would block direct browser fetches
to services on your local network.

- 🟡 Pulsing amber — check in progress
- 🟢 Green — service responded (tooltip shows response time in ms)
- 🔴 Red — unreachable or timed out after 2 seconds

Any HTTP response counts as "up" — including 401 (auth required) and 403 (forbidden),
since those mean the service is running, just protected.

---

## Adding a service

Fill in the form at the bottom of the page:

| Field | Required | Notes |
|-------|----------|-------|
| Name | Yes | Display name on the tile |
| Description | No | Small italic subtitle on the tile |
| URL | Yes | Full URL including port, e.g. `http://192.168.1.x:8096` |
| Shelf | Yes | Which shelf to place it on |
| Icon | Yes | Pick from the emoji grid |
| Colour | Yes | Accent colour for the tile border |

If you omit `http://`, NookShelf adds it automatically.

---

## Rearranging

Click **✏️ Rearrange** in the top bar to enter edit mode. In this mode:

- **Drag tiles** left/right to reorder them within a shelf
- **Drag a tile onto a different shelf** to move it there
- **Empty shelves** show a dashed drop zone so you can still drag tiles onto them
- **Drag the ⠿ handle** on a shelf label to reorder the whole shelf
- **✕ button** appears on each tile to remove it
- **✕ remove shelf** appears on each shelf label to delete the shelf and all its tiles
- Click **✅ Done** to exit edit mode

---

## Backup and restore

Click **💾 Backup** to download `nookshelf-backup-YYYY-MM-DD.json`.

To restore, replace `data/nookshelf.json` on your server with the backup file
and restart the container:

```bash
cp nookshelf-backup-2026-03-18.json ~/nookshelf/data/nookshelf.json
docker compose restart
```

---

## Data storage

Shelf data is saved to `./data/nookshelf.json` on the host machine via the
Docker volume mount in `docker-compose.yml`:

```yaml
volumes:
  - ./data:/data
```

This means your shelves survive container rebuilds, restarts, and updates.
The `data/` folder is created automatically on first save.

---

## Updating

```bash
# Pull your updated files into the project folder, then:
docker compose down
docker compose up -d --build
```

Your data in `./data/nookshelf.json` is untouched by rebuilds.

---

## Configuration

The only thing you may want to change in `app.py`:

```python
PORT           = 5001          # change if 5001 is taken
STATUS_TIMEOUT = 2             # seconds before a service is marked down
```


---

## Tech stack

| Layer | What |
|-------|------|
| Backend | Python 3.12, Flask, Requests |
| Frontend | Vanilla HTML/CSS/JS — no framework, no build step |
| Storage | JSON file on disk |
| Container | Docker + Compose |
