"""
generate_dataset.py
Generates a synthetic Superstore-style sales CSV and loads it into SQLite.
Run this first before opening the notebook.
"""

import sqlite3
import pandas as pd
import numpy as np
import os

np.random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
N_ROWS   = 10_000
DB_PATH  = "sales.db"
CSV_PATH = "data/superstore_sales.csv"
os.makedirs("data", exist_ok=True)

# ── Reference data ────────────────────────────────────────────────────────────
regions    = ["West", "East", "Central", "South"]
categories = {
    "Technology":       ["Phones", "Accessories", "Machines", "Copiers"],
    "Furniture":        ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies":  ["Binders", "Paper", "Storage", "Art", "Labels"],
}
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

first_names = ["James","Mary","John","Patricia","Robert","Jennifer","Michael",
               "Linda","William","Barbara","David","Susan","Richard","Jessica",
               "Joseph","Sarah","Thomas","Karen","Charles","Lisa"]
last_names  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller",
               "Davis","Wilson","Taylor","Anderson","Thomas","Jackson","White",
               "Harris","Martin","Thompson","Young","Robinson","Lewis"]

cities_by_region = {
    "West":    ["Los Angeles","San Francisco","Seattle","Portland","Las Vegas"],
    "East":    ["New York","Philadelphia","Boston","Atlanta","Miami"],
    "Central": ["Chicago","Dallas","Houston","Minneapolis","Kansas City"],
    "South":   ["New Orleans","Memphis","Nashville","Charlotte","Louisville"],
}

states_by_region = {
    "West":    ["California","California","Washington","Oregon","Nevada"],
    "East":    ["New York","Pennsylvania","Massachusetts","Georgia","Florida"],
    "Central": ["Illinois","Texas","Texas","Minnesota","Missouri"],
    "South":   ["Louisiana","Tennessee","Tennessee","North Carolina","Kentucky"],
}

product_names = {
    "Phones":       ["Samsung Galaxy","Apple iPhone","Motorola Edge","Nokia 5310","OnePlus Nord"],
    "Accessories":  ["Logitech Mouse","HP Keyboard","Belkin Hub","Anker Cable","Samsung Charger"],
    "Machines":     ["HP LaserJet","Canon Printer","Brother MFC","Epson WorkForce","Xerox Phaser"],
    "Copiers":      ["Ricoh MP","Sharp MX","Konica Minolta","Canon imageRUNNER","Toshiba e-Studio"],
    "Chairs":       ["HON Ignition","Serta Executive","Flash Furniture","OFM Essentials","Boss Task"],
    "Tables":       ["Safco Workspace","Flash Folding","Lorell Rect","Bestar Office","Realspace Magellan"],
    "Bookcases":    ["Sauder Bookcase","Bush Bookcase","Prepac Tall","Ameriwood 5-Shelf","South Shore"],
    "Furnishings":  ["Eldon Organizer","Rubbermaid Caddy","Deflecto Shelf","Artistic Wire","Fiskars Lamp"],
    "Binders":      ["Avery Binder","Cardinal Binder","Wilson Jones","Staples Economy","Fellowes Binder"],
    "Paper":        ["Hammermill Copy","HP Office Paper","Georgia-Pacific","Boise X-9","Domtar Copy"],
    "Storage":      ["Sterilite Box","Bankers Box","Fellowes Case","Avery Sorter","Iris Stack"],
    "Art":          ["Sanford Pencil","Crayola Markers","Pilot Pens","Dixon Ticonderoga","BIC Pens"],
    "Labels":       ["Avery Labels","Maco Labels","Dymo Label","Pendaflex Labels","Smead Labels"],
}

# ── Generate rows ─────────────────────────────────────────────────────────────
rows = []
order_counter = 1

for _ in range(N_ROWS):
    region   = np.random.choice(regions)
    idx      = np.random.randint(0, 5)
    city     = cities_by_region[region][idx]
    state    = states_by_region[region][idx]
    category = np.random.choice(list(categories.keys()))
    sub_cat  = np.random.choice(categories[category])
    product  = np.random.choice(product_names[sub_cat])

    base_price = {
        "Technology": np.random.uniform(50, 1500),
        "Furniture":  np.random.uniform(80, 900),
        "Office Supplies": np.random.uniform(5, 200),
    }[category]

    qty      = np.random.randint(1, 10)
    discount = np.random.choice([0, 0, 0, 0.1, 0.2, 0.3, 0.4], p=[0.5,0.1,0.1,0.1,0.1,0.05,0.05])
    sales    = round(base_price * qty * (1 - discount), 2)
    profit   = round(sales * np.random.uniform(0.05, 0.35), 2)

    order_date = pd.Timestamp("2021-01-01") + pd.Timedelta(days=int(np.random.randint(0, 365*3)))
    ship_date  = order_date + pd.Timedelta(days=int(np.random.randint(1, 7)))

    fn = np.random.choice(first_names)
    ln = np.random.choice(last_names)

    rows.append({
        "order_id":      f"CA-{2021 + order_date.year % 3}-{order_counter:05d}",
        "order_date":    order_date.strftime("%Y-%m-%d"),
        "ship_date":     ship_date.strftime("%Y-%m-%d"),
        "ship_mode":     np.random.choice(ship_modes),
        "customer_name": f"{fn} {ln}",
        "region":        region,
        "city":          city,
        "state":         state,
        "category":      category,
        "sub_category":  sub_cat,
        "product_name":  product,
        "quantity":      qty,
        "discount":      discount,
        "sales":         sales,
        "profit":        profit,
    })
    order_counter += 1

df = pd.DataFrame(rows)
df.to_csv(CSV_PATH, index=False)
print(f"✅  CSV saved → {CSV_PATH}  ({len(df):,} rows)")

# ── Load into SQLite ──────────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
df.to_sql("sales", conn, if_exists="replace", index=False)

# Create helpful indexes
conn.execute("CREATE INDEX IF NOT EXISTS idx_region   ON sales(region)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON sales(category)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_date     ON sales(order_date)")
conn.commit()
conn.close()
print(f"✅  SQLite DB saved → {DB_PATH}")
print("\nDone! Open retail_sales_analysis.ipynb to start the analysis.")
