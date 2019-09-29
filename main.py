import os
import sys
import csv
import shutil
import time

class User:
    pass

class BankManager:
    
    def __init__(self):
        self.b_file = os.path.join(sys.path[0], "banks", "banks.csv")
        self.bsl_file = os.path.join(sys.path[0], "banks", "session.lock")

    def listBanks(self):
        banks = []

        with open(self.b_file, 'r') as f:
            lines = f.readlines()

            for line in lines:
                banks.append(line[:-1])

        return banks

    def addBank(self, bank):
        os.mkdir(os.path.join(sys.path[0], 'banks', bank))

        with open(self.b_file, 'a') as f:
            f.write(bank + '\n')

        self.chooseBank(bank)

        AccountsManager()._initAccounts()
        TransactionsManager()._initTransactions()

    def delBank(self, bank):
        read = open(self.b_file, 'r')
        f = open(os.path.join(sys.path[0], "banks", "banks_temp.csv"), 'w')

        reader = read.readlines()

        for line in reader:
            if bank != line[:-1]:
                f.write(line)

        read.close()
        f.close()

        os.remove(self.b_file)
        os.rename(os.path.join(sys.path[0], "banks", "banks_temp.csv"), self.b_file)

        shutil.rmtree(os.path.join(sys.path[0], "banks", bank))

    def chooseBank(self, bank):
        with open(self.bsl_file, 'w') as f:
            f.write(bank)

    def _returnCurrent(self):
        with open(self.bsl_file, 'r') as f:
            return f.read()

class AccountsManager:
    
    def __init__(self):
        self.a_file = os.path.join(sys.path[0], "banks", BankManager()._returnCurrent(), "accounts.csv")
        self.asl_file = os.path.join(sys.path[0], "banks", BankManager()._returnCurrent(), "session.lock")
        self.b_folder = os.path.join(sys.path[0], 'banks', BankManager()._returnCurrent())

    def _initAccounts(self):
        os.mkdir(os.path.join(self.b_folder, 'Checking Account'))
        os.mkdir(os.path.join(self.b_folder, 'Savings Account'))

        with open(self.a_file, 'w') as f:
            f.write('Checking Account\nSavings Account\n')

        with open(self.asl_file, 'w') as f:
            f.write('')

    def listAccounts(self):
        accounts = []

        with open(self.a_file, 'r') as f:
            lines = f.readlines()

            for line in lines:
                accounts.append(line[:-1])

        return accounts

    def addAccount(self, account):
        os.mkdir(os.path.join(self.b_folder, account))

        self.chooseAccount(account)

        TransactionsManager()._newTransactionsFile(account)

        with open(self.a_file, 'a') as f:
            f.write(account + '\n')

    def delAccount(self, account):
        read = open(self.a_file, 'r')
        f = open(os.path.join(sys.path[0], "banks", BankManager()._returnCurrent(), "accounts_temp.csv"), 'w')

        reader = read.readlines()

        for line in reader:
            if account != line[:-1]:
                f.write(line)

        read.close()
        f.close()

        os.remove(self.a_file)
        os.rename(os.path.join(sys.path[0], "banks", BankManager()._returnCurrent(), "accounts_temp.csv"), self.a_file)

        shutil.rmtree(os.path.join(sys.path[0], "banks", BankManager()._returnCurrent(), account))

    def chooseAccount(self, account):
        with open(self.asl_file, 'w') as f:
            f.write(account)

    def _returnCurrent(self):
        with open(self.asl_file, 'r') as f:
            return f.read()

class TransactionsManager:

    def __init__(self):
        self.t_file = os.path.join(sys.path[0], "banks", BankManager()._returnCurrent(), AccountsManager()._returnCurrent(), "transactions.csv")

    def _initTransactions(self):
        with open(os.path.join(sys.path[0], 'banks', BankManager()._returnCurrent(), 'Checking Account', 'transactions.csv'), 'w') as f:
            f.write('Initialization,initial,+0.0,0.0\n')

        with open(os.path.join(sys.path[0], 'banks', BankManager()._returnCurrent(), 'Savings Account', 'transactions.csv'), 'w') as f:
            f.write('Initialization,initial,+0.0,0.0\n')

    def _newTransactionsFile(self, account):
        with open(self.t_file, 'w') as f:
            f.write('Initialization,initial,+0.0,0.0\n')

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

    run1 = True
    while run1:

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

            run2 = True
            while run2:
                acc_op = input("""
                --------------------------
                | 1. Choose account      |
                | 2. Add account         |
                | 3. Remove account      |
                | 4. List accounts       |
                | 5. Back                |
                | 6. Exit                |
                --------------------------

                Option: """)

                if acc_op == '1':
                    for account in AccountsManager().listAccounts():
                        print(account)
                    
                    account = input('\nAccount (Type in exactly as shown): ')

                    AccountsManager().chooseAccount(account)

                    run3 = True
                    while run3:
                        option = input("""
                        --------------------------
                        | 1. Deposit             |
                        | 2. Withdraw            |
                        | 3. List transactions   |
                        | 4. Back                |
                        | 5. Exit                |
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
                            run3 = False

                        elif option == '5':
                            run1 = False
                            run2 = False
                            run3 = False

                        else:
                            print('\nOption is not valid!')

                elif acc_op == '2':
                    new_acc = input('Account name: ')
                    AccountsManager().addAccount(new_acc)
                    print('Account created sucessfully')

                elif acc_op == '3':
                    for account in AccountsManager().listAccounts():
                        print(account)
                        
                    del_acc = input('\nAccount name (Type in exactly as shown): ')
                    x = input('Are you sure you want to delete this account?\n(Y/N): ').upper()

                    if x == 'Y':
                        AccountsManager().delAccount(del_acc)
                        print('Account sucessfully deleted')
                    else:
                        print('Account was not deleted')

                elif acc_op == '4':
                    for account in AccountsManager().listAccounts():
                        print(account)

                elif acc_op == '5':
                    run2 = False

                elif acc_op == '6':
                    run1 = False
                    run2 = False

                else:
                    print('\nOption is not valid!')

        elif bank_op == '2':
            new_bank = input('Bank name: ')
            BankManager().addBank(new_bank)
            print('Bank created sucessfully!')

        elif bank_op == '3':
            for bank in BankManager().listBanks():
                print(bank)
                
            del_bank = input('\nBank name (Type in exactly as shown): ')
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
            run1 = False

        else:
            print('\nOption is not valid!')


if __name__ == "__main__":
    mainLoop()

