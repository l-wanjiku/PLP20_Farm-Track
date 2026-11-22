# PLP20_Farm-Track

FarmTrack CLI is a simple Python app that runs in the terminal. Farmers use it to record harvests, sales, expenses and losses, and to see their stock and profit.

## The problem

Many farmers in Rwanda lose crops after harvest, and without simple records they cannot see their stock, sales and losses. FarmTrack CLI keeps these records in one place so a farmer can decide what to sell, store or improve.

## What you can do

Choose a number from the main menu:

| Option | What it does |
|--------|--------------|
| 1 | View recorded harvests |
| 2 | Record a farm input purchase (seeds, fertilizer) |
| 4 | Record a new harvest |
| 5 | Record a produce sale (cannot sell more than the stock) |
| 6 | Record a produce loss |
| 7 | Record a farm expense |
| 8 | View current inventory |
| 9 | View farm summary (revenue, expenses, profit or loss) |
| 10 | View transaction history |
| 0 | Exit |

## What you need

- Python 3
- MySQL
- The MySQL connector for Python:

```
pip install mysql-connector-python
```

## How to run it

1. Create the database in MySQL:

```
CREATE DATABASE farmtrack_db;
```

2. Set your MySQL password (PowerShell example):

```
$env:DB_PASSWORD="your_password"
```

By default the app uses host `localhost`, port `3306`, user `root` and database `farmtrack_db`. You can change them with `DB_HOST`, `DB_PORT`, `DB_USER` and `DB_NAME`.

3. Start the app:

```
python farm_track.py
```

The tables (harvests, sales, expenses, losses) are created automatically the first time you run it.

