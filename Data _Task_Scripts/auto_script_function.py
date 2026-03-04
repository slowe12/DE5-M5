from pathlib import Path
import pandas as pd

ROOT = Path.cwd()
DATA_DIR = ROOT / "data"

books_csv = DATA_DIR / "03_Library Systembook.csv"
customers_csv = DATA_DIR / "03_Library SystemCustomers.csv"

books_df = pd.read_csv(books_csv)
cust_df = pd.read_csv(customers_csv)

# Clean column names
books_df.columns = books_df.columns.str.strip()
cust_df.columns = cust_df.columns.str.strip()

def remove_missing_values(df):
    return df.dropna()

def clean_date_column(df, column_name):
    if column_name in df.columns:
        df[column_name] = (
            pd.to_datetime(
                df[column_name].astype(str).str.replace('"', '').str.strip(),
                errors="coerce",
                dayfirst=True
            )
        )
    return df

def drop_invalid_date_rows(df):
    required_cols = ["Book checkout", "Book Returned"]
    existing = [col for col in required_cols if col in df.columns]
    return df.dropna(subset=existing)

def convert_weeks_to_days(df):
    if "Days allowed to borrow" in df.columns:
        df["Days allowed to borrow"] = (
            pd.to_numeric(
                df["Days allowed to borrow"].astype(str).str.split().str[0],
                errors="coerce"
            )
            .mul(7)
        )
    return df

# Apply cleaning
books_df = remove_missing_values(books_df)
cust_df = remove_missing_values(cust_df)

books_df = clean_date_column(books_df, "Book checkout")
books_df = clean_date_column(books_df, "Book Returned")

books_df = drop_invalid_date_rows(books_df)
books_df = convert_weeks_to_days(books_df)


# Save
books_df.to_csv(DATA_DIR / "cleaned_books.csv", index=False)
cust_df.to_csv(DATA_DIR / "cleaned_cust.csv", index=False)