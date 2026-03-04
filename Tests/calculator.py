class Calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def get_sum(self):
        return self.num1 + self.num2

    def get_difference(self):
        return self.num1 - self.num2
    
    def get_product(self):
        return self.num1 * self.num2
    
    def get_quotient(self):
        return self.num1 / self.num2

if __name__ == "__main__":

    myCalc = Calculator(num1=100, num2=20)

    answer = myCalc.get_sum()
    print("Sum:", answer)
    print("Difference:", myCalc.get_difference())
    print("Product:", myCalc.get_product())
    print("Quotient:", myCalc.get_quotient())
