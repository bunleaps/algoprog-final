import os
import json
from prettytable import PrettyTable


class FinanceTracker:
    def __init__(self, database):
        self.database = database
        self.menu_path = "./assets/"
        self.clear_console = lambda: os.system("cls" if os.name == "nt" else "clear")

    def menu(self, indexMenu):
        menu_instructions = open(f"{self.menu_path}{indexMenu}.txt", "r")
        for i in menu_instructions.readlines():
            print(i, end="")
        menu_instructions.close()

    def read_database(self):
        data = open(self.database, "r")
        transactions = json.load(data)["transactions"]
        data.close()

        return transactions

    def printTable(self, transactions):
        tableContent = ["ID", "Date", "Account", "Amount", "Notes"]
        transactionsTable = PrettyTable(tableContent)

        for i in tableContent:
            transactionsTable.align[i] = "l"

        for entry in transactions:
            transactionsTable.add_row(
                [
                    entry["id"],
                    entry["date"],
                    entry["account"],
                    f'$ {entry["amount"]}',
                    entry["notes"],
                ]
            )

        print(transactionsTable)

    def read_transactions(self, filter):
        while True:
            self.clear_console()
            if filter == "a":
                transactions = self.read_database()
            elif filter == "e":
                transactions = [
                    transaction
                    for transaction in self.read_database()
                    if transaction["expense"] == True
                ]
            elif filter == "i":
                transactions = [
                    transaction
                    for transaction in self.read_database()
                    if transaction["expense"] == False
                ]

            self.printTable(transactions)

            user_input = input("\n? q to go back): ")
            if user_input == "q":
                break

    def run(self):
        while True:
            self.clear_console()
            self.menu("menu")

            user_input = input("\n? Enter option: ")

            if user_input == "0":
                break
            elif user_input == "1":
                while True:
                    self.clear_console()
                    self.menu("transactions")
                    user_input = input("\n? Enter option: ")
                    if user_input == "0":
                        break
                    elif user_input == "1":
                        self.read_transactions("a")
                    elif user_input == "2":
                        self.read_transactions("e")
                    elif user_input == "3":
                        self.read_transactions("i")


if __name__ == "__main__":
    app = FinanceTracker("data.json")
    app.run()
