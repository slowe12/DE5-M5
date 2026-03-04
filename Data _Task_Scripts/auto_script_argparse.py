from pathlib import Path
import pandas as pd
import argparse


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


def enrich_books(df: pd.DataFrame, late_fee: float = 1.0) -> pd.DataFrame:
    """Add calculated columns to the books DataFrame."""
    df["Days Borrowed"] = (df["Book Returned"] - df["Book checkout"]).dt.days
    df["Was Late"] = df["Days Borrowed"] > df["Days allowed to borrow"]
    df["Date Miss Match"] = df["Days Borrowed"] < 0
    df["Days Late"] = (df["Days Borrowed"] - df["Days allowed to borrow"]).clip(lower=0)
    df["Returned Early"] = df["Days Borrowed"] < df["Days allowed to borrow"]
    df["Checkout Day Name"] = df["Book checkout"].dt.day_name()
    df["Checkout Month"] = df["Book checkout"].dt.month_name()
    df["Checkout Year"] = df["Book checkout"].dt.year
    df["Late Fee"] = df["Days Late"] * late_fee
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
    books_df = remove_missing_values(books_df)
    cust_df = remove_missing_values(cust_df)
    books_df = clean_date_column(books_df, "Book checkout")
    books_df = clean_date_column(books_df, "Book Returned")
    books_df = drop_invalid_date_rows(books_df)
    books_df = convert_weeks_to_days(books_df)

    # -------------------------
    # Enrich Data
    # -------------------------
    books_df = enrich_books(books_df, late_fee=args.late_fee)

    # -------------------------
    # Save Files
    # -------------------------
    books_df.to_csv(args.output_books, index=False)
    cust_df.to_csv(args.output_customers, index=False)

    print("Cleaning complete!")


if __name__ == "__main__":
    main()