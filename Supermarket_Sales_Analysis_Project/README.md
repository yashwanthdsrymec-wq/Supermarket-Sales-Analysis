# Supermarket Sales Analysis

A ready-to-run Data Analytics project based on the supplied `SUPER MARKET DATA.pdf`.

## Included
- `app.py` — interactive Streamlit dashboard
- `analysis.py` — command-line analysis
- `data/supermarket_sales.csv` — 500 transactions extracted from the supplied PDF
- `data/SOURCE_SUPER_MARKET_DATA.pdf` — original source document
- `requirements.txt` — Python packages
- `run_app.bat` — Windows one-click launcher
- `README.md` — setup instructions

## Run in VS Code / terminal

### 1. Open this folder
Open `Supermarket_Sales_Analysis_Project` in VS Code.

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate it on Windows PowerShell
```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
```

### 4. Install packages
```bash
pip install -r requirements.txt
```

### 5. Start the dashboard
```bash
streamlit run app.py
```

The browser will open the local Streamlit dashboard.

## Windows shortcut
Double-click `run_app.bat`.

## Expected source insights
Using the 500 transactions in the supplied PDF:
- Highest-sales product: Cheese — ₹27,906.30
- Highest-sales branch: Branch C (Mumbai) — ₹72,469.45
- Highest-sales category: Beverages — ₹56,108.24
- Most-used payment method: UPI — 127 transactions
- Average Member transaction: ₹483.14
- Average Normal-customer transaction: ₹497.07
- Average customer rating: 3.99/5

The dashboard calculates these dynamically, so filters can change the live results.
