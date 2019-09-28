import os
import sys
import csv
import shutil
import time

class User:
    pass

class BankManager(User):
    
    def __init__(self):
        self.b_file = os.path.join(sys.path[0], "banks\\banks.csv")
        self.sl_file = os.path.join(sys.path[0], "banks\\session.lock")

    def listBanks(self):
        banks = []

        with open(self.b_file, 'r') as f:
            lines = f.readlines()

            for line in lines:
                banks.append(line[:-1])

        return banks

    def addBank(self, bank):
        os.mkdir('banks\\'+ bank)

        with open(self.b_file, 'a') as f:
            f.write(bank + '\n')

        with open('banks\\' + bank + '\\' 'transactions.csv', 'w') as f:
            f.write('Initialization,initial,+0.0,0.0\n')

    def delBank(self, bank):
        read = open(self.b_file, 'r')
        f = open(os.path.join(sys.path[0], "banks\\banks_temp.csv"), 'w')

        reader = read.readlines()

        for line in reader:
            if bank != line[:-1]:
                f.write(line)

        read.close()
        f.close()

        os.remove(self.b_file)
        os.rename(os.path.join(sys.path[0], "banks\\banks_temp.csv"), os.path.join(sys.path[0], "banks\\banks.csv"))

        shutil.rmtree(os.path.join(sys.path[0], "banks\\" + bank))

    def chooseBank(self, bank):
        with open(self.sl_file, 'w') as f:
            f.write('')
            f.write(bank)

    def _returnCurrent(self):
        with open(self.sl_file, 'r') as f:
            return f.read()

class TransactionsManager(BankManager):

    def __init__(self):
        self.t_file = os.path.join(sys.path[0], "banks\\" + BankManager()._returnCurrent() + "\\transactions.csv")

    def _store(self, op, amount, total):

        if op == 'deposit':
            sym = '+'
        elif op == 'withdraw':
            sym = '-'

        with open(self.t_file, 'a') as f:
            f.write(f'{time.ctime()},{op},{sym}{amount},{total}\n')

    def _read(self):
        with open(self.t_file, 'r') as f:
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

        with open(self.t_file, 'r') as f:
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

        bank_op = input("""
        --------------------------
        | 1. Choose bank         |
        | 2. Add bank            |
        | 3. Remove Bank         |
        | 4. List banks          |
        | 5. Exit                |
        --------------------------

        Option: """)

        if bank_op == '1':
            for bank in BankManager().listBanks():
                print(bank)
            
            bank = input('\nBank (Type in exactly as shown): ')

            BankManager().chooseBank(bank)


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

                if TransactionsManager().deposit(a) == 'not_number':
                    print('\nDeposit failed.. Value entered was not a number.')

            elif option == '2':
                a = input('\nAmount to withdraw: ')
                mw = TransactionsManager().withdraw(a)

                if mw == 'not_enough_money':
                    print('\nWithdraw failed.. There is not enough money in your account.')
                elif mw == 'not_number':
                    print('\nWithdraw failed.. Value entered was not a number.')

            elif option == '3':
                for transaction in TransactionsManager().listTransactions():
                    print(f'\nDate: {transaction[0]}\n{transaction[1].capitalize()}: ${transaction[2][1:]}\nTotal: ${transaction[3]}\n')

            elif option == '4':
                break

            else:
                print('\nOption is not valid!')

        elif bank_op == '2':
            new_bank = input('Bank name: ')
            BankManager().addBank(new_bank)
            print('Bank created sucessfully!')

        elif bank_op == '3':
            for bank in BankManager().listBanks():
                print(bank)
                
            del_bank = input('\nBank name: ')
            x = input('Are you sure you want to delete this bank?\n(Y/N): ').upper()

            if x == 'Y':
                BankManager().delBank(del_bank)
                print('Bank sucessfully deleted')
            else:
                print('Bank was not deleted')

        elif bank_op == '4':
            for bank in BankManager().listBanks():
                print(bank)

        elif bank_op == '5':
            break


if __name__ == "__main__":
    mainLoop()

