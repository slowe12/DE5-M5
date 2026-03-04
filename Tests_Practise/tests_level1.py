import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calculation = Calculator(2,2)
        self.assertEqual(calculation.get_sum(),4, "The get sum is not 4!")

    def test_difference(self):
        calculation = Calculator(2,3)
        self.assertEqual(calculation.get_difference(),-1, "The get difference is not -1!")
        
    def test_product(self):
        calculation = Calculator(2,3)
        self.assertEqual(calculation.get_product(),6, "The get product is not 6!")


    def test_quotient(self):
        calculation = Calculator(10,2)
        self.assertEqual(calculation.get_quotient(),5, "The get quotient is not 5!")


class Scientific_Calculator(Calculator):
    def __init__(self, num1, num2):
        super().__init__(num1, num2)

    def science_stuff(self):
        answer = self.get_sum(self.num1, self.num2)
        answer = answer ** self.num1


if __name__ == "__main__":
    unittest.main()

    answer = myCalc.get_sum()
    print(answer)