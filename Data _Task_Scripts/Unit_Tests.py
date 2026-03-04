import unittest
import pandas as pd
from auto_script_argparse import remove_missing_values, enrich_books  


class TestData(unittest.TestCase):

    def test_remove_missing_values_drops_rows(self):
        df = pd.DataFrame({
            "A": [1, 2, None],
            "B": [4, None, 6]
        })

        result = remove_missing_values(df)

        self.assertEqual(len(result), 1, "The rows deleted is incorrect this should be one remaining")

    def test_days_late_negative_becomes_zero(self):
        # Arrange: create a test DataFrame
        df = pd.DataFrame({
            "Book checkout": [pd.Timestamp("2024-01-01")],
            "Book Returned": [pd.Timestamp("2024-01-05")],  
            "Days allowed to borrow": [7]  
        })
        answer = pd.DataFrame({
            
        })
        # Act: enrich the DataFrame
        result = enrich_books(df, late_fee=1.0)

        # iloc takes the first row
        self.assertEqual(result, answer, "Days Late should be 0 for early returns")
        self.assertEqual(result["Days Late"].iloc[0], 0, "Days Late should be 0 for early returns")
        self.assertEqual(result["Date Miss Match"].iloc[0], False, "The date miss match test is incorrect")


if __name__ == "__main__":
    unittest.main()