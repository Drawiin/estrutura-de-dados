
class BigDigit():
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return str(self.value)


class BigNum():
    def __init__(self):
        self.head = None

    def __str__(self):
        if self.head is None:
            return '0'
        string = ''
        current = self.head
        while current is not None:
            string = str(current) + string
            current = current.next
        return string

    def insert(self, value):
        if self.head is None:
            self.head = BigDigit(value)
        else:
            oldHead = self.head
            self.head = BigDigit(value)
            self.head.next = oldHead

    def append(self, value):
        if self.head is None:
            self.head = BigDigit(value)
        else:
            current = self.head
            while current.next is not None:
                current = current.next

            current.next = BigDigit(value)

    def readNumber(self, number):
        if not number.isnumeric():
            print('Somente numeros são permitidos')
            exit(0)
        for digit in number:
            self.insert(int(digit))


class BigNumCalculator():
    def __init__(self):
        self.base = 10

    def sumCarry(self, result):
        return result // self.base

    def sumFinalResult(self, result):
        return result % self.base

    def bigSum(self, number1, number2):
        result = BigNum()
        current1 = number1.head
        current2 = number2.head
        carry = 0
        while current1 is not None and current2 is not None:
            parcialResult = current1.value + current2.value + carry
            carry = self.sumCarry(parcialResult)
            finalResult = self.sumFinalResult(parcialResult)

            result.append(finalResult)
            current1 = current1.next
            current2 = current2.next

        while current1 is not None:
            parcialResult = current1.value + carry
            carry = self.sumCarry(parcialResult)
            finalResult = self.sumFinalResult(parcialResult)

            result.append(finalResult)

            current1 = current1.next

        while current2 is not None:
            parcialResult = current2.value + carry
            carry = self.sumCarry(parcialResult)
            finalResult = self.sumFinalResult(parcialResult)

            result.append(finalResult)

            current2 = current2.next

        if carry > 0:
            result.append(carry)

        return result

    def bigSubtraction(self, number1, number2):
        result = BigNum()
        current1 = number1.head
        current2 = number2.head
        carry = 0
        while current1 is not None and current2 is not None:
            parcialResult = current1.value - current2.value - carry
            if parcialResult < 0:
                finalResult = parcialResult + self.base
                carry = 1
            else:
                finalResult = parcialResult
                carry = 0

            result.append(finalResult)
            current1 = current1.next
            current2 = current2.next

        while current1 is not None:
            parcialResult = current1.value - carry
            if parcialResult < 0:
                finalResult = parcialResult + self.base
                carry = 1
            else:
                finalResult = parcialResult
                carry = 0

            result.append(finalResult)
            current1 = current1.next

        if current2 is not None or carry > 0:
            return -1

        return result

    def bigProduct(self, number1, number2):
        one = BigNum()
        one.insert(1)
        result = BigNum()

        while self.bigSubtraction(number2, one) != -1:
            result = self.bigSum(result, number1)
            number2 = self.bigSubtraction(number2, one)

        return result

    def bigDivision(self, number1, number2):
        one = BigNum()
        one.insert(1)

        result = BigNum()
        result.insert(0)

        if number2.head.next is None and number2.head.value == 0:
            return -1

        while self.bigSubtraction(number1, number2) != -1:
            result = self.bigSum(result, one)
            number1 = self.bigSubtraction(number1, number2)

        return result


if __name__ == "__main__":
    entry = ""
    calculator = BigNumCalculator()
    while True:
        number1 = BigNum()
        number2 = BigNum()
        entry = input('> ').strip()
        if entry == "q":
            break
        entry = entry.split(' ')
        if len(entry) != 3:
            print('> [Entrada incorreta]')
        else:
            number1.readNumber(entry[0])
            op = entry[1]
            number2.readNumber(entry[2])

            if op == '+':
                print('>', calculator.bigSum(number1, number2))

            elif op == '-':
                print('>', calculator.bigSubtraction(number1, number2))

            elif op == '*':
                print('>', calculator.bigProduct(number1, number2))

            elif op == '/':
                print('>', calculator.bigDivision(number1, number2))

            else:
                print('> [Operação Inválida]')
