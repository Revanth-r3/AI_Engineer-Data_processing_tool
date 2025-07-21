import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import logging

st.set_page_config(page_title="Price-Volume Analyzer", layout="wide")
st.title("📈 Price-Volume Analyzer")

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Helper: Prevent CSV/Excel Injection ---
def sanitize_for_excel(df):
    def sanitize(val):
        if isinstance(val, str) and val.startswith(('=', '+', '-', '@')):
            return "'" + val
        return val
    return df.copy().apply(lambda col: col.map(sanitize) if col.dtype == 'object' else col)

# --- Helper: Column Check ---
def check_required_columns(df, required_cols):
    return [col for col in required_cols if col not in df.columns]

# File Upload
uploaded_file = st.file_uploader("Upload NSE Stock CSV File", type=["csv"])

# Inputs
x = st.number_input("Enter number of previous days for volume average (x):", min_value=1, step=1)
y = st.number_input("Enter number of forward days for price return (y):", min_value=1, step=1)
i = st.number_input("Enter bin interval size for volume % difference (i):", min_value=1, step=1)
j = st.number_input("Enter bin interval size for price forward return % (j):", min_value=1, step=1)

# Generate Output
if uploaded_file and x and y and i and j:
    if st.button("🚀 Generate Output"):
        try:
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                st.warning("⚠️ File wasn't UTF-8. Loaded using fallback encoding ISO-8859-1.")

            required_cols = ['time', 'Price', 'Volume']
            missing = check_required_columns(df, required_cols)
            if missing:
                st.error(f"❌ Missing required column(s): {', '.join(missing)}")
                st.stop()

            # Clean & sort
            df = df[df['Volume'] != 0].copy()
            df['time'] = pd.to_datetime(df['time'], dayfirst=True, errors='coerce')
            df.dropna(subset=['time'], inplace=True)
            df.sort_values(by='time', inplace=True)
            df.reset_index(drop=True, inplace=True)

            # Calculations
            volume_avg_col = f'Volume_{x}_day_avg'
            volume_pct_diff_col = f'Volume_vs_{x}_day_avg_%'
            df[volume_avg_col] = df['Volume'].rolling(window=x).mean().shift(1)
            df[volume_pct_diff_col] = ((df['Volume'] - df[volume_avg_col]) / df[volume_avg_col]) * 100

            price_return_col = f'Price_{y}_day_forward_return_%'
            df[price_return_col] = ((df['Price'].shift(-y) - df['Price']) / df['Price']) * 100

            # Binning
            def get_range_label(val, interval):
                if pd.isna(val):
                    return None
                lower = (val // interval) * interval
                upper = lower + interval
                return f"{int(lower)} to {int(upper)}"

            def extract_lower_bound(label):
                try:
                    return int(str(label).split(" to ")[0])
                except:
                    return float('inf')

            volume_range_col = f'{volume_pct_diff_col}_Range_{i}'
            price_range_col = f'{price_return_col}_Range_{j}'
            df[volume_range_col] = df[volume_pct_diff_col].apply(lambda v: get_range_label(v, i))
            df[price_range_col] = df[price_return_col].apply(lambda v: get_range_label(v, j))

            # Reorder columns
            df = df[['time',
                     'Volume', volume_avg_col, volume_pct_diff_col, volume_range_col,
                     'Price', price_return_col, price_range_col]]

            # Crosstab
            freq_table = pd.crosstab(df[volume_range_col], df[price_range_col])
            freq_table = freq_table.reindex(sorted(freq_table.index, key=extract_lower_bound))
            freq_table = freq_table[sorted(freq_table.columns, key=extract_lower_bound)]

            # Sanitize for Excel
            df_sanitized = sanitize_for_excel(df)
            freq_sanitized = sanitize_for_excel(freq_table)

            # Export to Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_sanitized.to_excel(writer, index=False, sheet_name='Data')
                freq_sanitized.to_excel(writer, sheet_name='Frequency_Table')
            processed_data = output.getvalue()

            # Download link
            st.success("✅ Processing completed. Download your Excel file below:")
            b64 = base64.b64encode(processed_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.xlsx">📥 Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)

            # Previews
            with st.expander("📄 Preview Transformed Data"):
                st.dataframe(df.head())

            with st.expander("📊 Preview Frequency Table"):
                st.dataframe(freq_table)

        except Exception as e:
            logging.error("Unhandled exception: %s", str(e))
            st.error("❌ An unexpected error occurred.")
            st.exception(e)

else:
    st.info("📌 Upload CSV and enter all values to generate output")