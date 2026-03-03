from pathlib import Path
import pandas as pd

# -----------------------------
# 1. Set project paths
# -----------------------------

ROOT = Path.cwd()
DATA_DIR = ROOT / "data"

books_csv = DATA_DIR / "03_Library Systembook.csv"
customers_csv = DATA_DIR / "03_Library SystemCustomers.csv"

# -----------------------------
# 2. Load data
# -----------------------------

books_df = pd.read_csv(books_csv)
cust_df  = pd.read_csv(customers_csv)

# -----------------------------
# 3. Remove missing values
# -----------------------------

books_df_v01 = books_df.dropna()
cust_df_v01 = cust_df.dropna()

# -----------------------------
# 4. Clean 'Book checkout'
# -----------------------------

books_df_v01["Book checkout"] = (
    books_df_v01["Book checkout"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.strip()
    .pipe(pd.to_datetime, errors="coerce", dayfirst=True)
)

# -----------------------------
# 5. Clean 'Book Returned'
# -----------------------------

books_df_v01["Book Returned"] = (
    books_df_v01["Book Returned"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.strip()
    .pipe(pd.to_datetime, errors="coerce", dayfirst=True)
)

# -----------------------------
# 6. Convert "X weeks" → X*7 days
# -----------------------------

books_df_v01["Days allowed to borrow"] = (
    books_df_v01["Days allowed to borrow"]
        .astype(str)
        .str.split()
        .str[0]
        .astype(int)
        .mul(7)
)

# -----------------------------
# 7. Print confirmation
# -----------------------------

output_path_books = DATA_DIR / "cleaned_books.csv"
books_df_v01.to_csv(output_path_books, index=False)

output_path_cust = DATA_DIR / "cleaned_cust.csv"
cust_df_v01.to_csv(output_path_cust, index=False)

print("Python is running from:", Path.cwd())
print(f"Books file saved to: {output_path_books}")
print(f"Customers file saved to: {output_path_cust}")