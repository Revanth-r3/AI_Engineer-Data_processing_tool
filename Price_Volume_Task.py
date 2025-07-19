import pandas as pd

# ---- Step 1: USER INPUT ---- #
input_path = r"E:\Praveen\Task_JMN\NSE_TANLA.csv"       # <-- Your input CSV file
output_path = r"E:\Praveen\Task_JMN\result.xlsx"        # <-- Your output Excel file

x = int(input("Enter number of previous days for volume average (x): "))
y = int(input("Enter number of forward days for price return (y): "))
i = int(input("Enter bin interval size for volume % difference (i): "))
j = int(input("Enter bin interval size for price forward return % (j): "))

# ---- Step 2: LOAD DATA ---- #
df = pd.read_csv(input_path)

# ---- Step 3: REMOVE ROWS WHERE VOLUME IS ZERO ---- #
df = df[df['Volume'] != 0]
df.reset_index(drop=True, inplace=True)

# ---- Step 4: Convert 'time' to datetime and sort ---- #
df['time'] = pd.to_datetime(df['time'], dayfirst=True)
df.sort_values(by='time', inplace=True)
df.reset_index(drop=True, inplace=True)

# ---- Step 5: CALCULATE VOLUME METRICS ---- #
volume_avg_col = f'Volume_{x}_day_avg'
volume_pct_diff_col = f'Volume_vs_{x}_day_avg_%'
df[volume_avg_col] = df['Volume'].rolling(window=x).mean().shift(1)
df[volume_pct_diff_col] = ((df['Volume'] - df[volume_avg_col]) / df[volume_avg_col]) * 100 

# ---- Step 6: CALCULATE PRICE FORWARD RETURN ---- #
price_return_col = f'Price_{y}_day_forward_return_%'
df[price_return_col] = ((df['Price'].shift(-y) - df['Price']) / df['Price']) * 100

# ---- Step 7: BINNING FUNCTION ---- #
def get_range_label(val, interval):
    if pd.isna(val):
        return None
    lower = (val // interval) * interval
    upper = lower + interval
    return f"{int(lower)} to {int(upper)}"

# ---- Step 8: CREATE BINNED RANGE COLUMNS ---- #
volume_range_col = f'{volume_pct_diff_col}_Range_{i}'
price_range_col = f'{price_return_col}_Range_{j}'

df[volume_range_col] = df[volume_pct_diff_col].apply(lambda v: get_range_label(v, i))
df[price_range_col] = df[price_return_col].apply(lambda v: get_range_label(v, j))

# ---- Step 9: REORDER COLUMNS ---- #
df = df[['time', 
         'Volume', volume_avg_col, volume_pct_diff_col, volume_range_col,
         'Price', price_return_col, price_range_col]]

# ---- Step 10: BUILD SORTED FREQUENCY TABLE ---- #
freq_table = pd.crosstab(df[volume_range_col], df[price_range_col])

def extract_lower_bound(label):
    try:
        return int(str(label).split(" to ")[0])
    except:
        return float('inf')  # fallback for malformed values

# Properly sorted by numeric ranges
freq_table = freq_table.reindex(sorted(freq_table.index, key=extract_lower_bound))
freq_table = freq_table[sorted(freq_table.columns, key=extract_lower_bound)]

# ---- Step 11: SAVE TO EXCEL WITH TWO SHEETS ---- #
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    freq_table.to_excel(writer, sheet_name='Frequency_Table')

print(f"\n✅ Process complete. Excel file saved to: {output_path}")
