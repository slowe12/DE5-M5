from pathlib import Path
import pandas as pd
import argparse
import datetime

# Global changes log to track modifications
changes_log = []

# Helper function to log changes
def log_change(action, details, df_name, before_rows=None, after_rows=None, before_cols=None, after_cols=None, dropped_rows=None):

    changes_log.append({
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Action": action,
        "Details": details,
        "DataFrame": df_name,
        "Rows Before": before_rows,
        "Rows After": after_rows,
        "Columns Before": before_cols,
        "Columns After": after_cols,
        "Dropped Rows": dropped_rows,  # New column to track dropped rows
    })


def remove_missing_values(df, df_name):
    original_rows = len(df)
    original_cols = len(df.columns)
    
    df = df.dropna()
    dropped_rows = original_rows - len(df)
    
    if dropped_rows > 0:
        log_change("Remove Missing Values", f"Dropped {dropped_rows} rows", df_name, original_rows, len(df), original_cols, len(df.columns), dropped_rows)
    
    return df


def clean_date_column(df, column_name, df_name):
    if column_name in df.columns:
        original_missing = df[column_name].isna().sum()
        df[column_name] = (
            pd.to_datetime(
                df[column_name].astype(str).str.replace('"', '').str.strip(),
                errors="coerce",
                dayfirst=True
            )
        )
        new_missing = df[column_name].isna().sum()
        
        if new_missing > original_missing:
            log_change("Clean Date Column", f"Converted {new_missing - original_missing} entries to NaT in '{column_name}'", df_name, len(df), len(df), None, None, None)
    
    return df


def drop_invalid_date_rows(df, df_name):
    required_cols = ["Book checkout", "Book Returned"]
    existing = [col for col in required_cols if col in df.columns]
    original_rows = len(df)
    original_cols = len(df.columns)

    df = df.dropna(subset=existing)
    dropped_rows = original_rows - len(df)
    
    if dropped_rows > 0:
        log_change("Drop Invalid Date Rows", f"Dropped {dropped_rows} rows due to missing dates", df_name, original_rows, len(df), original_cols, len(df.columns), dropped_rows)
    
    return df


def convert_weeks_to_days(df, df_name):
    if "Days allowed to borrow" in df.columns:
        original_na = df["Days allowed to borrow"].isna().sum()
        df["Days allowed to borrow"] = (
            pd.to_numeric(
                df["Days allowed to borrow"].astype(str).str.split().str[0],
                errors="coerce"
            )
            .mul(7)
        )
        new_na = df["Days allowed to borrow"].isna().sum()
        
        if new_na > original_na:
            log_change("Convert Weeks to Days", f"Converted {new_na - original_na} entries to NaN", df_name, len(df), len(df), None, None, None)
    
    return df


def enrich_books(df: pd.DataFrame, late_fee: float = 1.0, df_name="Books") -> pd.DataFrame:
    original_rows = len(df)
    original_cols = len(df.columns)
    
    df["Days Borrowed"] = (df["Book Returned"] - df["Book checkout"]).dt.days
    df["Was Late"] = df["Days Borrowed"] > df["Days allowed to borrow"]
    df["Date Miss Match"] = df["Days Borrowed"] < 0
    df["Days Late"] = (df["Days Borrowed"] - df["Days allowed to borrow"]).clip(lower=0)
    df["Returned Early"] = df["Days Borrowed"] < df["Days allowed to borrow"]
    df["Checkout Day Name"] = df["Book checkout"].dt.day_name()
    df["Checkout Month"] = df["Book checkout"].dt.month_name()
    df["Checkout Year"] = df["Book checkout"].dt.year
    df["Late Fee"] = df["Days Late"] * late_fee

    enriched_columns = len(df.columns) - original_cols
    
    if enriched_columns > 0:
        log_change("Enrich Books Data", f"Added {enriched_columns} new columns", df_name, original_rows, len(df), original_cols, len(df.columns), None)
    
    return df


def main():
    # -------------------------
    # Argument Parser Setup
    # -------------------------
    parser = argparse.ArgumentParser(
        description="Clean and enrich library book checkout data."
    )

    ROOT = Path.cwd()
    DATA_DIR = ROOT / "data"

    parser.add_argument("--books", type=str, default=str(DATA_DIR / "03_Library Systembook.csv"))
    parser.add_argument("--customers", type=str, default=str(DATA_DIR / "03_Library SystemCustomers.csv"))
    parser.add_argument("--late-fee", type=float, default=1.0, help="Late fee per day (default = 1.0)")
    parser.add_argument("--output-books", type=str, default="cleaned_books.csv", help="Output filename for cleaned books")
    parser.add_argument("--output-customers", type=str, default="cleaned_cust.csv", help="Output filename for cleaned customers")
    parser.add_argument("--changes-log", type=str, default="changes_log.csv", help="Output filename for change log")

    args = parser.parse_args()

    # -------------------------
    # Load Files
    # -------------------------
    books_df = pd.read_csv(args.books)
    cust_df = pd.read_csv(args.customers)

    # Clean column names
    books_df.columns = books_df.columns.str.strip()
    cust_df.columns = cust_df.columns.str.strip()

    # -------------------------
    # Cleaning
    # -------------------------
    books_df = remove_missing_values(books_df, "Books")
    cust_df = remove_missing_values(cust_df, "Customers")
    books_df = clean_date_column(books_df, "Book checkout", "Books")
    books_df = clean_date_column(books_df, "Book Returned", "Books")
    books_df = drop_invalid_date_rows(books_df, "Books")
    books_df = convert_weeks_to_days(books_df, "Books")

    # -------------------------
    # Enrich Data
    # -------------------------
    books_df = enrich_books(books_df, late_fee=args.late_fee, df_name="Books")

    # -------------------------
    # Save Files
    # -------------------------
    books_df.to_csv(args.output_books, index=False)
    cust_df.to_csv(args.output_customers, index=False)

    # Export Changes Log to CSV
    changes_df = pd.DataFrame(changes_log)
    changes_df.to_csv(args.changes_log, index=False)

    print("Cleaning complete!")


if __name__ == "__main__":
    main()