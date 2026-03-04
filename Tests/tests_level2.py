import unittest
from calculator import Calculator
## This shows me how to take out the calculation at each stage
## Added def setUp

class TestOperations(unittest.TestCase):

    def setUp(self):
        self.myCalc = (Calculator(8,2))

    def test_sum(self):
        self.assertEqual(self.myCalc.get_sum(),10, "The get sum is not 10!")

    def test_difference(self):
        self.assertEqual(self.myCalc.get_difference(),6, "The get difference is not 6!")
        
    def test_product(self):
        self.assertEqual(self.myCalc.get_product(),16, "The get product is not 16!")


    def test_quotient(self):
        self.assertEqual(self.myCalc.get_quotient(),4, "The get quotient is not 4!")


if __name__ == "__main__":
    unittest.main()