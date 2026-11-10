"""Find the great circle around the Earth that crosses the least land.

Run:  uv run --with numpy --with pillow route.py
Data: Natural Earth 1:10m countries and Antarctic ice shelves (public domain),
      downloaded on first run. Ice shelves count as land: a tube cannot float under them.
"""
import base64, json, os, urllib.request
import numpy as np
from PIL import Image, ImageDraw

BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
FILES = ["ne_10m_admin_0_countries.geojson", "ne_10m_antarctic_ice_shelves_polys.geojson"]
C = 2 * np.pi * 6371.0088  # km, circumference of the mean Earth
S = 20                     # raster cells per degree (~5.6 km at the equator)
W, H = 360 * S, 180 * S

features = []
for name in FILES:
    if not os.path.exists(name):
        urllib.request.urlretrieve(BASE + name, name)
    features += json.load(open(name))["features"]
names = ["ocean"] + [f["properties"].get("ADMIN", "Antarctic ice shelf") for f in features]

# Rasterize the countries: pixel value = country index, 0 = ocean.
img = Image.new("I", (W, H))
draw = ImageDraw.Draw(img)
for i, f in enumerate(features, 1):
    g = f["geometry"]
    for poly in g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]:
        draw.polygon([((x + 180) * S, (90 - y) * S) for x, y in poly[0]], fill=i)
ids = np.array(img)
land = ids > 0


def circle(pole_lat, n):
    """Lat/lon (deg) of n points on the great circle whose pole sits at (pole_lat, 0).
    A pole at another longitude just shifts every lon by that amount."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    p = np.radians(pole_lat)
    lat = np.degrees(np.arcsin(np.cos(p) * np.sin(t)))
    lon = np.degrees(np.arctan2(np.cos(t), -np.sin(p) * np.sin(t)))
    return lat, lon


def pixels(pole_lat, pole_lons, n):
    lat, lon = circle(pole_lat, n)
    row = np.minimum(((90 - lat) * S).astype(int), H - 1)
    col = np.floor((lon + np.atleast_1d(pole_lons)[:, None] + 180) * S).astype(int) % W
    return row, col


def land_share(pole_lats, pole_lons, n):
    """Fraction of land along every great circle on a grid of poles."""
    return np.array([land[pixels(pl, pole_lons, n)].mean(axis=1) for pl in pole_lats])


# 1) Coarse search: every pole on a 0.25 degree grid (one hemisphere covers all circles).
lats, lons = np.arange(0, 90.01, 0.25), np.arange(0, 360, 0.25)
coarse = land_share(lats, lons, 3600)

# 2) Refine the 20 best candidates on a 0.01 degree grid, sampling every 2 km.
fine = np.arange(-0.25, 0.2501, 0.01)
best = (1, 0, 0)
for k in np.argsort(coarse, axis=None)[:20]:
    i, j = np.unravel_index(k, coarse.shape)
    share = land_share(lats[i] + fine, lons[j] + fine, 20000)
    a, b = np.unravel_index(share.argmin(), share.shape)
    best = min(best, (share[a, b], lats[i] + fine[a], lons[j] + fine[b]))
_, pole_lat, pole_lon = best

# 3) Walk the winner in 1 km steps and list every land crossing.
n = round(C)
row, col = pixels(pole_lat, pole_lon, n)
route = ids[row, col[0]]
edges = np.flatnonzero(np.diff(route)) + 1
crossings = []
for a, b in zip(edges, np.append(edges[1:], edges[0] + n)):
    if route[a]:
        crossings.append([round(a * 360 / n, 2), round(b * 360 / n, 2), names[route[a]], int(b - a)])

equator = land_share([90], [0], n)[0, 0]
print(f"pole: {pole_lat:.2f}, {pole_lon:.2f}")
print(f"land: {sum(c[3] for c in crossings)} km of {C:.0f} km ({(route > 0).mean():.2%})")
print(f"equator for comparison: {equator * C:.0f} km ({equator:.2%})")
print("crossings [start deg, end deg, name, km]:", json.dumps(crossings))

# 4) 1 degree land mask for drawing the globe in index.html (180 rows x 360 bits).
mask = land.reshape(180, S, 360, S).mean(axis=(1, 3)) > 0.5
print("mask:", base64.b64encode(np.packbits(mask).tobytes()).decode())
