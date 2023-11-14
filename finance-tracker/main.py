import os
import json
from prettytable import PrettyTable


class FinanceTracker:
    def __init__(self, database):
        self.__database = database
        self.__menu_path = "./assets/"
        self.__clear_console = lambda: os.system("cls" if os.name == "nt" else "clear")

    def __menu(self, indexMenu):
        menu_instructions = open(f"{self.__menu_path}{indexMenu}.txt", "r")
        for i in menu_instructions.readlines():
            print(i, end="")
        menu_instructions.close()

    def __read_database(self):
        data = open(self.__database, "r")
        transactions = json.load(data)["transactions"]
        data.close()

        return transactions

    def __write_database(self, new_data):
        with open(self.__database, "r+") as file:
            file_data = json.load(file)
            file_data["transactions"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def __printTable(self, transactions):
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
            self.__clear_console()
            if filter == "all":
                transactions = self.__read_database()
            elif filter == "expense":
                transactions = [
                    transaction
                    for transaction in self.__read_database()
                    if transaction["expense"] == True
                ]
            elif filter == "income":
                transactions = [
                    transaction
                    for transaction in self.__read_database()
                    if transaction["expense"] == False
                ]

            self.__printTable(transactions)

            user_input = input("\n? q to go back): ")
            if user_input == "q":
                break

    def add_transactions(self):
        # loop through a list to give out input
        input_list = ["id", "date", "account", "amount", "notes"]
        # make dict output
        data = {
            "id": 123123,
            "date": "8/1/2023",
            "account": "Transportation Expense",
            "amount": 213.0,
            "notes": "Flights Tickets to Indonesia",
        }
        # add True to expense of it is an expense
        if data["account"] == "Expense":
            data.append({"expense": True})
        else:
            data.append({"expense": False})
        # save to a new dict
        self.__write_database(data)
        pass

    def init(self):
        while True:
            self.__clear_console()
            self.__menu("menu")

            user_input = input("\n? Enter option: ")

            if user_input == "q":
                break
            elif user_input == "1":
                while True:
                    self.__clear_console()
                    self.__menu("transactions")
                    user_input = input("\n? Enter option: ")
                    if user_input == "q":
                        break
                    elif user_input == "1":
                        self.read_transactions("all")
                    elif user_input == "2":
                        self.read_transactions("expense")
                    elif user_input == "3":
                        self.read_transactions("income")


if __name__ == "__main__":
    app = FinanceTracker("data.json")
    app.init()
