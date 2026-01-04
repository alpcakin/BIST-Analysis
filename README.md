# BIST 100: USD and Inflation-Adjusted Analysis

![BIST Comparison](outputs/bist_normalized_comparison.png)

Analyzing 15 years of Turkish stock market performance through three lenses: nominal TRY returns, USD-adjusted performance, and real purchasing power.

## Key Findings

The BIST 100 index tells dramatically different stories depending on how you measure it:

- **TRY Terms**: +2,100% (220x growth from 2010-2025)
- **USD Terms**: -42% (currency depreciation overwhelmed gains)
- **Real USD Terms**: -53% (accounting for both currency and inflation)

Despite spectacular nominal gains, Turkish equity investors experienced significant purchasing power losses over the 15-year period.

## Motivation

When evaluating investment performance in emerging markets with volatile currencies, nominal returns can be misleading. This project demonstrates the importance of adjusting for currency depreciation and inflation to understand actual wealth creation.

## Project Structure
```
BIST-Analysis/
├── data/                          # Downloaded financial data (CSV)
├── notebooks/
│   └── analysis.ipynb            # Main analysis notebook
├── outputs/                       # Generated charts
│   ├── bist_try_terms.png
│   ├── bist_usd_terms.png
│   ├── bist_real_usd_terms.png
│   └── bist_normalized_comparison.png
├── src/
│   └── data_fetcher.py           # Data collection module
├── requirements.txt               # Python dependencies
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alpcakin/BIST-Analysis.git
cd BIST-Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get a free FRED API key:
   - Sign up at https://fred.stlouisfed.org/
   - Get your API key from https://fredaccount.stlouisfed.org/apikeys
   - Create a `.env` file in the project root:
```
   FRED_API_KEY=your_api_key_here
```

## Usage

### Option 1: Run the Jupyter Notebook
```bash
jupyter notebook notebooks/analysis.ipynb
```

The notebook will:
1. Fetch BIST 100, USD/TRY, and US CPI data
2. Calculate currency and inflation adjustments
3. Generate all visualizations
4. Save charts to `outputs/` folder

### Option 2: Use the Data Fetcher Module
```python
from src.data_fetcher import DataFetcher

# Fetch and process data
fetcher = DataFetcher(start_date='2010-01-01')
df = fetcher.fetch_all_data()

# Save to CSV
fetcher.save_data(df)

# View the data
print(df.head())
```

## Data Sources

- **BIST 100**: Yahoo Finance ticker `XU100.IS`
- **USD/TRY Exchange Rate**: Yahoo Finance ticker `USDTRY=X`
- **US CPI**: FRED API series `CPIAUCSL`

## Methodology

### 1. Data Collection
- Historical daily data from 2010-01-01 to present
- Resampling monthly CPI data to daily frequency using forward fill

### 2. Calculations

**USD-Adjusted Returns:**
```python
BIST_USD = BIST_TRY / USDTRY
```

**Real Returns (Inflation-Adjusted):**
```python
BIST_USD_Real = BIST_USD / (CPI_current / CPI_base)
```

**Normalized Performance (Base = 100):**
```python
Normalized = (Current_Value / Initial_Value) * 100
```

### 3. Limitations

- **Starting point sensitivity**: Results vary significantly based on start date
- **Dividends excluded**: Analysis uses price index, not total return index
- **Only US inflation**: Turkish domestic inflation not included
- **No transaction costs**: Real returns would be lower after taxes and fees

## Results

See the full analysis and discussion: [BIST 100: When Numbers Tell Different Stories](https://open.substack.com/pub/alpcakin/p/did-bist-100-really-grow-a-currency)

Key visualizations:

| Perspective | Chart |
|------------|-------|
| TRY Terms | ![TRY](outputs/bist_try_terms.png) |
| USD Terms | ![USD](outputs/bist_usd_terms.png) |
| Real USD | ![Real](outputs/bist_real_usd_terms.png) |

## Technologies Used

- **Python 3.8+**
- **pandas**: Data manipulation and analysis
- **yfinance**: Financial data fetching
- **fredapi**: US economic data from FRED
- **matplotlib & seaborn**: Data visualization
- **jupyter**: Interactive analysis

## Contributing

Found an issue or have suggestions? Feel free to open an issue or submit a pull request.

## License

MIT License - feel free to use this code for your own analysis.

## Author

**Alp Çakın**
- Substack: (https://alpcakin.substack.com)
- Analysis Article: [BIST 100 Deep Dive](https://open.substack.com/pub/alpcakin/p/did-bist-100-really-grow-a-currency)

## Acknowledgments

- Data provided by Yahoo Finance and Federal Reserve Economic Data (FRED)
- Inspired by the need for realistic performance metrics in emerging markets

---

*This is analytical commentary, not investment advice. Past performance does not guarantee future results.*