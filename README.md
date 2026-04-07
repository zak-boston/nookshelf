# 🍵 NookShelf
 
A service dashboard for your homelab.
 
---
 
## Folder structure
 
```
nookshelf/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── README.md
└── static/
    └── index.html
```
 
---
 
## Quick start
 
```
docker compose up -d --build
```
 
Then open **http://localhost:5001** in your browser,
or `http://<your-server-ip>:5001` from anywhere on your network.
 
---
 
## Features
 
| Feature | Details |
| --- | --- |
| 🍵 Service tiles | Name, description, URL, emoji icon, colour accent |
| 🟢 Status dots | Live up/down indicator on every tile, rechecks every 30s |
| 🗂️ Shelves | Group tiles into named shelves |
| ↔️ Drag to rearrange | Reorder tiles within a shelf, or drag across shelves |
| ⠿ Shelf reordering | Drag entire shelves to change their order |
| ✏️ Edit tiles | Edit any tile's details after adding it |
| 🔍 Search | Filter tiles instantly by name or description |
| 🎨 Emoji picker | Quick-pick row plus a full categorised emoji browser |
| 💾 Backup | One-click JSON download of your entire shelf layout |
| 📂 Restore | Restore from a backup file directly in the UI |
| 💾 Persistent data | Shelf data saved to `data/nookshelf.json` on the host |
 
---
 
## How status dots work
 
NookShelf checks each service from the **server side** (Flask makes the request,
not your browser). This avoids CORS errors that would block direct browser fetches
to services on your local network.
 
* 🟡 Pulsing amber — check in progress
* 🟢 Green — service responded (tooltip shows response time in ms)
* 🔴 Red — unreachable or timed out after 2 seconds
 
Any HTTP response counts as "up" — including 401 (auth required) and 403 (forbidden),
since those mean the service is running, just protected.
 
---
 
## Adding a service
 
Fill in the form at the bottom of the page:
 
| Field | Required | Notes |
| --- | --- | --- |
| Name | Yes | Display name on the tile |
| Description | No | Small italic subtitle on the tile |
| URL | Yes | Full URL including port |
| Shelf | Yes | Which shelf to place it on |
| Icon | Yes | Quick-pick row or browse the full emoji library |
| Colour | Yes | Accent colour for the tile border |
 
NookShelf accepts the following URL formats and adds `http://` automatically if omitted:
 
* Private IPs — `192.168.x.x`, `10.x.x.x`, `172.16-31.x.x`
* Tailscale — `100.64-127.x.x`
* Localhost — `localhost`
* Local hostnames — `hostname.local`, `hostname.home`
 
---
 
## Rearranging
 
Click **✏️ Edit** in the top bar to enter edit mode. In this mode:
 
* **Drag tiles** left/right to reorder them within a shelf
* **Drag a tile onto a different shelf** to move it there
* **Empty shelves** show a dashed drop zone so you can still drag tiles onto them
* **Drag the ⠿ handle** on a shelf label to reorder the whole shelf
* **✕ button** appears on each tile to remove it
* **✕ remove shelf** appears on each shelf label to delete the shelf and all its tiles
* Click **✅ Done** to exit edit mode
 
---
 
## Backup and restore
 
Click **💾 Backup** to download `nookshelf-backup-YYYY-MM-DD.json`.
 
Click **📂 Restore** to load a backup file directly in the UI — this replaces all
current shelves and services and saves immediately. No server access required.
 
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
 
```
docker compose down
docker compose up -d --build
```
 
Your data in `./data/nookshelf.json` is untouched by rebuilds.
 
---
 
## Configuration
 
The only things you may want to change in `app.py`:
 
```python
PORT           = 5001   # change if 5001 is taken
STATUS_TIMEOUT = 2      # seconds before a service is marked down
```
 
---
 
## Tech stack
 
| Layer | What |
| --- | --- |
| Backend | Python 3.12, Flask, Requests |
| Frontend | Vanilla HTML/CSS/JS — no framework, no build step |
| Storage | JSON file on disk |
| Container | Docker + Compose |

## TODO

⬜ Themes
