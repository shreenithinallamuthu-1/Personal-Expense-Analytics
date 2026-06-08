import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Filename setup
CSV_FILE = "personal_expenses.csv"

# Custom color palette dictionary based on your requirements
CATEGORY_COLORS = {
    "Food": "seagreen",
    "Utilities": "cyan",
    "Rent": "red",
    "Transport": "royalblue",
    "Entertainment": "hotpink",
    "Shopping": "greenyellow",
    "Others": "#cd7f32",        # Hex code for bronze
    "Uncategorized": "gray"    # Fallback default color
}


def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount (\u20B9)"])
        print(f" Data file created successfully: {CSV_FILE}")


def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter Amount: \u20B9"))
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g., 12.50).")


def collect_expense():
    print("\n--- Enter New Expense Details ---")

    date_input = input(
        "Enter Date (YYYY-MM-DD) or press Enter for today: "
    ).strip()
    if not date_input:
        date_str = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            date_str = (
                datetime.strptime(date_input, "%Y-%m-%d")
                .date()
                .strftime("%Y-%m-%d")
            )
        except ValueError:
            print("❌ Invalid date format. Using today's date instead.")
            date_str = datetime.today().strftime("%Y-%m-%d")

    print("\nCommon Categories: Food, Utilities, Rent, Transport, Entertainment, Shopping, Others")
    # Changed from .capitalize() to .title() as requested
    category = input("Enter Common Category: ").strip().title()
    if not category:
        category = "Uncategorized"

    description = input("Enter Description/Notes: ").strip()
    if not description:
        description = "N/A"

    amount = get_valid_amount()

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date_str, category, description, amount])

    print(f" Successfully logged: \u20B9{amount} for {category}!")


def view_expenses():
    print("\n--- 📋 All Expense Records ---")
    if not os.path.exists(CSV_FILE):
        print("No records found. Try adding an expense first!")
        return

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader, None)

        if not header:
            print("No data found in the file.")
            return

        print(f"{'Date':<15} | {'Category':<15} | {'Description':<25} | {'Amount (\u20B9)':<10}")
        print("-" * 75)

        count = 0
        for row in reader:
            if len(row) == 4:
                print(f"{row[0]:<15} | {row[1]:<15} | {row[2]:<25} | \u20B9{row[3]:<10}")
                count += 1

        if count == 0:
            print("No transactions found.")


def run_analytics():
    print("\n--- 📊 Expense Analytics Dashboard ---")
    if not os.path.exists(CSV_FILE):
        print("No data available to analyze yet.")
        return

    total_expense = 0.0
    transaction_count = 0
    category_totals = {}

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) == 4:
                try:
                    amount = float(row[3])
                    category = row[1]

                    total_expense += amount
                    transaction_count += 1
                    category_totals[category] = category_totals.get(category, 0.0) + amount
                except ValueError:
                    continue

    if total_expense == 0:
        print("No numeric data found to process analytics.")
        return

    print(f"🔢 TOTAL TRANSACTIONS LOGGED : {transaction_count}")
    print(f"💰 TOTAL EXPENSE ACCUMULATED : \u20B9{total_expense:,.2f}")
    print("-" * 55)

    print(f"{'Category':<18} | {'Total Spent':<15} | {'Percentage'}")
    print("-" * 55)

    for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total_expense) * 100
        print(f"{category:<18} | \u20B9{amount:<14,.2f} | {percentage:.1f}%")


def generate_bar_chart():
    """Generates a chart with Dates on X-axis, Amount on Y-axis, and custom colors per Category."""
    print("\n--- 📉 Generating Custom Bar Chart... ---")
    if not os.path.exists(CSV_FILE):
        print("No data available to plot chart.")
        return

    dates = []
    amounts = []
    colors = []
    categories = []

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header

        for row in reader:
            if len(row) == 4:
                try:
                    date = row[0]
                    category = row[1]
                    amount = float(row[3])

                    dates.append(date)
                    amounts.append(amount)
                    categories.append(category)
                    
                    # Assign the requested color or default to gray if category matches nothing
                    color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["Uncategorized"])
                    colors.append(color)
                except ValueError:
                    continue

    if not dates:
        print("No valid data found to plot.")
        return

    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot bars with Date on X, Amount on Y, specific category colors, and permanent black edges
    bars = plt.bar(dates, amounts, color=colors, edgecolor='black', width=0.5)

    # Chart Label Configurations
    plt.title("Daily Spending Breakup by Category", fontsize=14, fontweight='bold')
    plt.xlabel("Date (YYYY-MM-DD)", fontsize=12)
    plt.ylabel("Amount Spent (\u20B9)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)  # Tilts dates so they don't overlap

    # Add dynamic legends so you know what color means what
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, edgecolor='black', label=cat) 
                       for cat, color in CATEGORY_COLORS.items() if cat in categories]
    if legend_elements:
        plt.legend(handles=legend_elements, title="Categories", loc="upper right")

    # Add transaction value tracking labels right on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + (max(amounts)*0.01), f'\u20B9{yval:,.0f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    print("✨ Showing your custom chart window. Close it to return to the menu.")
    plt.show()


def main():
    initialize_csv()
    
    while True:
        print("\n====================================")
        print("    PERSONAL EXPENSE DATA ANALYTICS ")
        print("====================================")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Analytics (Totals & Breakdown)")
        print("4. Generate Bar Chart")
        print("5. Exit Program")
        print("====================================")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            while True:
                collect_expense()
                cont = input("\nDo you want to add another expense? (yes/no): ").strip().lower()
                if cont != "yes":
                    break
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            run_analytics()
        elif choice == "4":
            generate_bar_chart()
        elif choice == "5":
            print("\n Data saved safely. Goodbye!")
            break
        else:
            print("❌ Invalid selection. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
