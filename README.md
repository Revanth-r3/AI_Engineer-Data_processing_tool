This project is a Streamlit-based web application that allows users to upload Excel or CSV files, automatically formats and cleans the data (removing dangerous characters, fixing column types, etc.), and exports a sanitized version for download.

✅ Technologies Used
Python – Backend logic

Streamlit – Web app interface

Pandas – Data manipulation

XlsxWriter – Export to Excel

Docker – Containerization

Git/GitHub – Version control & deployment

Streamlit Community Cloud – Hosting

🔐 Vulnerabilities Identified & Fixes
#	Vulnerability	Fix
1	CSV/Excel Injection (e.g. =2+3)	Escaped values by prefixing dangerous entries with '
2	Missing Required Columns	Added validation function with Streamlit error messaging
3	Bad Encoding in CSVs	Implemented utf-8 with fallback to ISO-8859-1
4	Uncaught Exceptions	Added try-except blocks and logging support
5	Excel Output Corruption	Sanitized DataFrame before writing using XlsxWriter
6	Deprecated Pandas Calls	Replaced applymap with safer column-wise .apply()
7	Invalid Dates	Used errors='coerce' for date parsing
