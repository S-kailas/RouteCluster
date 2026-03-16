# Proximate Location Locator (PLL)

## Project Overview

**Proximate Location Locator (PLL)** is a web-based tool that groups nearby geographic locations automatically using a **distance-based clustering algorithm**.

Users upload an Excel file containing **Google Maps location links**, and the system:

1. Extracts latitude and longitude coordinates.
2. Applies a **distance clustering algorithm (DBSCAN)**.
3. Groups nearby locations within a defined radius (3 km).
4. Displays clustered locations on an interactive map.
5. Allows downloading the clustered results as a new Excel file.

This tool is designed for scenarios such as:

* Field service planning
* Delivery route grouping
* Sales territory organization
* Regional customer segmentation

The goal is to quickly identify **locations that can be visited within the same geographic area**.

---

# Core Features

* Excel file upload
* Automatic coordinate extraction from Google Maps links
* Distance-based clustering
* Interactive map visualization
* Download clustered results as Excel
* Persistent database storage

---

# System Architecture

```
User (Browser)
      │
      ▼
Frontend (HTML + JavaScript + Leaflet.js)
      │
      ▼
FastAPI Backend
      │
      ├── Excel Parser
      ├── Google Maps Link Parser
      ├── Clustering Engine (DBSCAN)
      │
      ▼
MySQL Database
```

---

# Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pandas
* Scikit-learn
* PyMySQL

### Frontend

* HTML
* JavaScript
* Leaflet.js (OpenStreetMap)

### Database

* MySQL

### Server

* Linux VPS
* Uvicorn ASGI server

---

# Project Structure

```
PLL/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── clustering.py
│   ├── excel_parser.py
│   ├── map_parser.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
└── uploads/
```

---

# Excel Input Format

The uploaded Excel file must contain two columns:

| excel_id | map_link                                            |
| -------- | --------------------------------------------------- |
| 1        | https://www.google.com/maps?q=8.5464093,76.90457449 |
| 2        | https://www.google.com/maps?q=8.5470000,76.9052000  |

Rules:

* File format: `.xlsx`
* Maximum recommended rows: **50**
* Map links must follow this format:

```
https://www.google.com/maps?q=LATITUDE,LONGITUDE
```

Example:

```
https://www.google.com/maps?q=8.5464093,76.90457449
```

---

# Clustering Algorithm

The system uses **DBSCAN (Density-Based Spatial Clustering)**.

Configuration:

* Distance radius: **3 km**
* Minimum samples: **1**

Steps:

1. Convert latitude and longitude into radians
2. Apply Haversine distance calculation
3. Run DBSCAN clustering
4. Assign cluster IDs to each location

Result example:

```
Cluster 0
  - Location 1
  - Location 2
  - Location 3

Cluster 1
  - Location 4
  - Location 5
```

---

# Setup Guide

## 1. Clone Repository

```
git clone https://github.com/your-repo/pll.git
cd pll/backend
```

---

## 2. Create Python Virtual Environment

```
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

Main dependencies:

```
fastapi
uvicorn
pandas
scikit-learn
sqlalchemy
pymysql
cryptography
python-multipart
openpyxl
```

---

## 4. Configure MySQL Database

Create database:

```
CREATE DATABASE location_cluster;
```

Update `database.py`:

```
DATABASE_URL = "mysql+pymysql://username:password@localhost/location_cluster"
```

---

## 5. Create Upload Directory

```
mkdir uploads
```

---

## 6. Run Backend Server

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API documentation:

```
http://SERVER_IP:8000/docs
```

---

## 7. Run Frontend

From the frontend folder:

```
python -m http.server 3000
```

Open in browser:

```
http://SERVER_IP:3000
```

---

# Usage

1. Open the web interface
2. Upload the Excel file
3. Click **Analyze**
4. View clusters on the map
5. Click **Download Result** to export clustered data

---

# Output Example

Downloaded Excel:

| excel_id | map_link              | latitude | longitude | cluster |
| -------- | --------------------- | -------- | --------- | ------- |
| 1        | maps?q=8.5464,76.9045 | 8.5464   | 76.9045   | 0       |
| 2        | maps?q=8.5468,76.9049 | 8.5468   | 76.9049   | 0       |
| 3        | maps?q=8.5600,76.9100 | 8.5600   | 76.9100   | 1       |

---

# Future Improvements

Potential enhancements:

* Route optimization within clusters
* Cluster statistics panel
* Batch upload support
* Authentication system
* Cluster boundary visualization
* API-based integration

---

# License

This project is intended for internal or client usage and can be extended for commercial or operational deployment.
