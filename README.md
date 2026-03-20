# RouteCluster

A web-based tool to cluster geographic locations and generate optimized travel routes using real road data (Travelling Salesman Problem).

**Illustration:** https://youtu.be/giG7-zn7DPs?si=mjvFTqZkbYPYb0xG

---

## Overview

RouteCluster allows users to upload a list of Google Maps location links and:

* Automatically group nearby locations (distance-based clustering)
* Optimize the visit order within each group
* Visualize real road routes on an interactive map
* Download processed results as an Excel file

---

## Core Features

* Excel upload (`.xlsx`)
* Google Maps link parsing (`?q=lat,lng`)
* Distance-based clustering (DBSCAN)
* Route optimization (Nearest Neighbor + OSRM)
* Interactive map visualization (Leaflet.js)
* Export clustered results

---

## Architecture

Frontend → Backend → Processing → Visualization

```
Frontend (HTML + JS + Leaflet)
        ↓
FastAPI Backend
        ↓
Clustering (DBSCAN)
        ↓
Route Optimization (OSRM + TSP)
        ↓
Response → Map Rendering
```

---

## Input Format

Excel file must contain:

| excel_id | map_link                                     |
| -------- | -------------------------------------------- |
| 1        | https://www.google.com/maps?q=8.5464,76.9045 |

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* MySQL
* Pandas
* Scikit-learn (DBSCAN)

### Routing

* OSRM (public API)

### Frontend

* Vanilla JS
* Leaflet.js

---

## Setup (VPS / Local Machine)

### 1. Install dependencies

```bash
sudo apt update
git clone https://github.com/S-kailas/RouteCluster.git
```

### 2. Backend setup

```bash
cd backend
uv venv
uv pip install -r requirements.txt
source .venv/bin/activate
```

### 3. Run servers

```bash
~/backend uvicorn main:app --host 0.0.0.0 --port 8000
~/frontend python3 -m http.server 3000
```

---

## Access

* Frontend → `http://<VPS-IP>:3000`
* Backend → `http://<VPS-IP>:8000`

---

## How It Works

1. Upload Excel file
2. System extracts coordinates
3. Locations are clustered by distance (km radius)
4. Each cluster is optimized into a route
5. Routes are generated using real road geometry
6. Results are displayed and available for download

---

## Limitations

* Uses public OSRM
* No traffic-aware routing
* No multi-vehicle optimization
* Strict input format

---

## Future Improvements

* Dynamic radius slider (live clustering)
* Self-hosted OSRM for better performance
