# Hamrowoda

A GeoDjango web application for visualizing Nepal's administrative ward boundaries using PostGIS, Django REST Framework, and Leaflet.js.

---

## Tech Stack

- **Backend:** Django 6, GeoDjango, Django REST Framework
- **Database:** PostgreSQL + PostGIS
- **GeoJSON API:** djangorestframework-gis
- **Frontend:** Leaflet.js
- **Data:** Nepal ward boundaries (6803 records)

---

## Prerequisites

- Python 3.11+
- PostgreSQL (latest)
- PostGIS
- GDAL

### Install system dependencies (macOS)

```bash
brew install postgresql postgis gdal
brew services start postgresql
```

### Install system dependencies (Ubuntu/Debian)

```bash
sudo apt install postgresql postgis gdal-bin libgdal-dev python3-gdal
sudo systemctl start postgresql
```

---

## 1. Clone the repo

```bash
git clone https://github.com/akashadhikari/hamrowoda.git
cd hamrowoda
```

---

## 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Python dependencies

```bash
pip install django djangorestframework djangorestframework-gis psycopg2-binary GDAL==$(gdal-config --version)
```

---

## 4. Set up PostgreSQL database

```bash
psql postgres
```

Run these SQL commands one at a time:

```sql
CREATE USER mapuser WITH PASSWORD 'mappassword';
```

```sql
CREATE DATABASE mapdb OWNER mapuser;
```

```sql
\c mapdb
```

```sql
CREATE EXTENSION postgis;
```

```sql
GRANT ALL PRIVILEGES ON DATABASE mapdb TO mapuser;
```

```sql
\q
```

Verify PostGIS is working:

```bash
psql -U mapuser -d mapdb -c "SELECT PostGIS_version();"
```

You should see something like:

```
            postgis_version
---------------------------------------
 3.6 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
(1 row)
```

---

## 5. Configure GDAL path in settings.py

Find your GDAL library path:

```bash
# macOS
find /opt/homebrew -name "libgdal*" 2>/dev/null

# Linux
find /usr -name "libgdal*" 2>/dev/null
```

Add the result to `nepal_map/settings.py`:

```python
# macOS (Apple Silicon)
GDAL_LIBRARY_PATH = '/opt/homebrew/lib/libgdal.dylib'
GEOS_LIBRARY_PATH = '/opt/homebrew/lib/libgeos_c.dylib'

# Linux example
# GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'
```

---

## 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 7. Load ward data

The GeoJSON file is not included in the repo due to its size. Obtain `Ward_plus_Limpiyadhura.geojson` separately, then load it into the database:

```bash
python manage.py load_wards /full/path/to/Ward_plus_Limpiyadhura.geojson
```

You should see:

```
Loading /full/path/to/Ward_plus_Limpiyadhura.geojson...
Done. Created: 6803, Skipped: 0
```

---

## 8. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## Navigating the map

| URL | Shows |
|-----|-------|
| `http://127.0.0.1:8000/` | All wards (Nepal) |
| `http://127.0.0.1:8000/5/` | Province 5 |
| `http://127.0.0.1:8000/5/ARGHAKHANCHI/` | Arghakhanchi district |
| `http://127.0.0.1:8000/5/ARGHAKHANCHI/Sandhikharka/` | Sandhikharka GaPa |
| `http://127.0.0.1:8000/5/ARGHAKHANCHI/Sandhikharka/9/` | Ward 9 |

---

## GeoJSON API

| Endpoint | Description |
|----------|-------------|
| `/api/wards/` | All wards |
| `/api/wards/?state=5` | Filter by state code |
| `/api/wards/?state=5&district=ARGHAKHANCHI` | Filter by district |
| `/api/wards/?gapa=Sandhikharka` | Filter by GaPa/NaPa |
| `/api/wards/?gapa=Sandhikharka&ward=9` | Filter by specific ward |

---

## Data Notes

- Source file: `Ward_plus_Limpiyadhura.geojson` (includes Limpiyadhura boundary)
- Total features: 6803 wards
- Geometry types: Polygon and MultiPolygon (SRID 4326)
- Key fields: `STATE_CODE`, `DISTRICT`, `GaPa_NaPa`, `NEW_WARD_N`
- The GeoJSON was also converted to TopoJSON (`wards.topojson`) for optimized frontend rendering
- Neither geodata file is tracked in git — data lives in the PostGIS database and is loaded via the management command