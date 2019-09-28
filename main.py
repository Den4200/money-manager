import os
import sys
import time

class Manager:
    
    def __init__(self):
        self.file = os.path.join(sys.path[0], "money.csv")

    def _store(self, op, amount, total):

        if op == 'deposit':
            sym = '+'
        elif op == 'withdraw':
            sym = '-'

        with open(self.file, 'a') as f:
            f.write(f'{time.ctime()},{op},{sym}{amount},{total}\n')

    def _read(self):
        with open(self.file, 'r') as f:
            line = f.readlines()[-1].split(',')
        
        date = line[0]
        op = line[1]
        money = line[3][:-1]

        return date, op, money

    def deposit(self, amount):
        try:
            float(amount)
        except Exception:
            amount = 0
            return 'not_number'

        try:
            total = float(self._read()[2]) + float(amount)
        except:
            total = float(amount)
        finally:
            self._store('deposit', amount, total)
            return total

    def withdraw(self, amount):
        try:
            float(amount)
        except Exception:
            amount = 0
            return 'not_number'

        total = float(self._read()[2]) - float(amount)

        if total < 0:
            total = float(self._read()[2]) + float(amount)
            return 'not_enough_money'
        
        else:
            self._store('withdraw', amount, total)
            return total

    def listTransactions(self):
        transactions = []

        with open(self.file, 'r') as f:
            lines = f.readlines()

            for line in lines:
                
                t_inst = []
                line = line.split(',')

                date = line[0]
                op = line[1]
                amount = line[2]
                money = line[3][:-1]

                t_inst.append(date)
                t_inst.append(op)
                t_inst.append(amount)
                t_inst.append(money)

                transactions.append(t_inst)
        
        return transactions

def mainLoop():

    while True:
        option = input("""
        --------------------------
        | 1. Deposit             |
        | 2. Withdraw            |
        | 3. List transactions   |
        | 4. Exit                |
        --------------------------

        Option: """)

        if option == '1':
            a = input('\nAmount to deposit: ')

            if Manager().deposit(a) == 'not_number':
                print('\nDeposit failed.. Value entered was not a number.')

        elif option == '2':
            a = input('\nAmount to withdraw: ')
            mw = Manager().withdraw(a)

            if mw == 'not_enough_money':
                print('\nWithdraw failed.. There is not enough money in your account.')
            elif mw == 'not_number':
                print('\nWithdraw failed.. Value entered was not a number.')

        elif option == '3':
            for transaction in Manager().listTransactions():
                print(f'\nDate: {transaction[0]}\n{transaction[1].capitalize()}: ${transaction[2][1:]}\nTotal: ${transaction[3]}\n')

        elif option == '4':
            break

        else:
            print('\nOption is not valid!')


if __name__ == "__main__":
    mainLoop()


