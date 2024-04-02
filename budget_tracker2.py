import json
from datetime import datetime

class BudgetTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, category, amount, transaction_type):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({"category": category, "amount": amount, "type": transaction_type, "timestamp": timestamp})

    def calculate_budget(self, income):
        total_expenses = sum(transaction["amount"] for transaction in self.transactions if transaction["type"] == "expense")
        remaining_budget = income - total_expenses
        return remaining_budget

    def analyze_expenses(self):
        expense_categories = {}
        for transaction in self.transactions:
            if transaction["type"] == "expense":
                category = transaction["category"]
                amount = transaction["amount"]
                if category in expense_categories:
                    expense_categories[category] += amount
                else:
                    expense_categories[category] = amount
        return expense_categories

    def calculate_avg_expenses_per_day(self):
        expense_dates = {}
        for transaction in self.transactions:
            if transaction["type"] == "expense":
                date = transaction["timestamp"].split()[0]
                amount = transaction["amount"]
                if date in expense_dates:
                    expense_dates[date].append(amount)
                else:
                    expense_dates[date] = [amount]

        avg_expenses_per_day = {}
        for date, amounts in expense_dates.items():
            avg_expenses_per_day[date] = sum(amounts) / len(amounts)

        return avg_expenses_per_day

    def save_transactions(self, file_name):
        with open(file_name, "w") as file:
            json.dump(self.transactions, file)

    def load_transactions(self, file_name):
        with open(file_name, "r") as file:
            self.transactions = json.load(file)

def main():
    budget_tracker = BudgetTracker()

    # Load previous transactions
    try:
        budget_tracker.load_transactions("transactions.json")
    except FileNotFoundError:
        print("No previous transactions found.")

    # Input income
    income = float(input("Enter your income: "))

    while True:
        print("\n1. Add expense")
        print("2. Add income")
        print("3. Calculate remaining budget")
        print("4. Analyze expenses")
        print("5. Calculate average expenses per day")
        print("6. Save and exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            category = input("\nEnter expense category: ")
            amount = float(input("Enter expense amount: "))
            budget_tracker.add_transaction(category, amount, "expense")
            print("Expense added successfully.")

        elif choice == "2":
            category = input("\nEnter income category: ")
            amount = float(input("Enter income amount: "))
            budget_tracker.add_transaction(category, amount, "income")
            print("Income added successfully.")

        elif choice == "3":
            remaining_budget = budget_tracker.calculate_budget(income)
            print(f"Remaining budget: {remaining_budget}")

        elif choice == "4":
            expense_categories = budget_tracker.analyze_expenses()
            print("\nExpense Analysis:")
            for category, amount in expense_categories.items():
                print(f"{category}: {amount}")

        elif choice == "5":
            avg_expenses_per_day = budget_tracker.calculate_avg_expenses_per_day()
            print("\nAverage Expenses Per Day:")
            for date, avg_expense in avg_expenses_per_day.items():
                print(f"{date}: {avg_expense}")

        elif choice == "6":
            budget_tracker.save_transactions("transactions.json")
            print("Transactions saved. Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()