import unittest
import pandas as pd
from auto_script_argparse import remove_missing_values, enrich_books

class TestData(unittest.TestCase):

    def test_remove_missing_values_drops_rows(self):
        # Simulate a DataFrame with missing values
        df = pd.DataFrame({
            "A": [1, 2, None],
            "B": [4, None, 6]
        })

        # Act: remove rows with missing values
        result = remove_missing_values(df)

        # Expected output: only one row should remain
        answer = pd.DataFrame({
            "A": [1],
            "B": [4]
        })

        # Assert: compare entire DataFrames
        pd.testing.assert_frame_equal(result, answer)

    def test_days_late_negative_becomes_zero(self):
        # Arrange: create a test DataFrame
        df = pd.DataFrame({
            "Book checkout": [pd.Timestamp("2024-01-01")],
            "Book Returned": [pd.Timestamp("2024-01-05")],
            "Days allowed to borrow": [7]
        })

        # Expected output DataFrame after enriching the data
        answer = pd.DataFrame({
            "Book checkout": [pd.Timestamp("2024-01-01")],
            "Book Returned": [pd.Timestamp("2024-01-05")],
            "Days allowed to borrow": [7],
            "Days Late": [0],
            "Late Fee": [0.0],  # Assuming no late fee for early returns
            "Date Miss Match": [False]  # Assuming a flag for any date mismatch
        })

        # Act: enrich the DataFrame
        result = enrich_books(df, late_fee=1.0)

        # Assert: compare entire DataFrames
        pd.testing.assert_frame_equal(result, answer)

    def test_remove_missing_values_handles_missing_rows(self):
        # Simulate a DataFrame with missing rows (NaN values in critical columns)
        df = pd.DataFrame({
            "Book checkout": [pd.Timestamp("2024-01-01"), None, pd.Timestamp("2024-01-03")],
            "Book Returned": [pd.Timestamp("2024-01-05"), pd.Timestamp("2024-01-07"), None],
            "Days allowed to borrow": [7, 7, None]
        })

        # Act: remove rows with missing values
        result = remove_missing_values(df)

        # Expected output: only one valid row should remain after removing rows with missing values
        answer = pd.DataFrame({
            "Book checkout": [pd.Timestamp("2024-01-01")],
            "Book Returned": [pd.Timestamp("2024-01-05")],
            "Days allowed to borrow": [7]
        })

        # Assert: compare entire DataFrames
        pd.testing.assert_frame_equal(result, answer)

    def test_missing_dates_and_values_are_handled_correctly(self):
        # Simulating a more complex case with missing dates and values
        df = pd.DataFrame({
            "Book checkout": [pd.Timestamp("2024-01-01"), None, pd.Timestamp("2024-01-04")],
            "Book Returned": [pd.Timestamp("2024-01-05"), pd.Timestamp("2024-01-08"), None],
            "Days allowed to borrow": [7, 7, None]
        })

        # Expected output DataFrame after missing values are removed and enriched
        answer = pd.DataFrame({
            "Book checkout": [pd.Timestamp("2024-01-01")],
            "Book Returned": [pd.Timestamp("2024-01-05")],
            "Days allowed to borrow": [7],
            "Days Late": [0],
            "Late Fee": [0.0],  # Assuming no late fee for early return
            "Date Miss Match": [False]
        })

        # Act: remove missing values and enrich the DataFrame
        result = enrich_books(remove_missing_values(df), late_fee=1.0)

        # Assert: compare entire DataFrames
        pd.testing.assert_frame_equal(result, answer)

if __name__ == "__main__":
    unittest.main()