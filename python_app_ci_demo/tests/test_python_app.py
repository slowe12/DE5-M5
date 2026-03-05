import unittest
from python_app_CI_Demo.app_refactored_solution import enrich_dateDuration
import pandas as pd
import numpy as np


class TestOperations(unittest.TestCase):

    def setUp(self):
        # Creating a test dataframe
        self.test_df = pd.DataFrame({
            'start_date': ['1/01/2025', '2/01/2025', '3/01/2025'],
            'end_date': ['1/02/2025', '2/02/2025', '3/02/2025']
        })

        # Convert the columns to datetime
        self.test_df['start_date'] = pd.to_datetime(self.test_df['start_date'], format='%d/%m/%Y')
        self.test_df['end_date'] = pd.to_datetime(self.test_df['end_date'], format='%d/%m/%Y')

        # Apply the enrichment function
        self.enriched_df = enrich_dateDuration(
            df=self.test_df,
            colA="start_date",
            colB="end_date"
        )

    def test_duration_as_int(self):
        self.assertTrue(
            pd.api.types.is_integer_dtype(self.enriched_df['date_delta']),
            "The delta column is not an integer type"
        )

    def test_duration_above_zero(self):
        self.assertTrue(
            (self.enriched_df['date_delta'] >= 0).all(),
            "Some durations are less than 0"
        )


if __name__ == "__main__":
    unittest.main()