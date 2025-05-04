from datastructures.array import Array
from datastructures.linkedlist import LinkedList
from datastructures.circularqueue import CircularQueue
from datastructures.hashmap import HashMap

class Drink:
    def __init__(self, name, price):
        self.name = name
        self.size = "Medium"
        self.price = price

class OrderItem:
    def __init__(self, drink, customization):
        self.drink = drink
        self.customization = customization

    def summary(self):
        return f"{self.drink.name} ({self.drink.size}) - {self.customization if self.customization else 'No customization'}"

class CustomerOrder:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = LinkedList()

    def add_item(self, order_item):
        self.items.append(order_item)   # ✅ Using append, not add_last

    def summary(self):
        s = f"{self.customer_name}:\n"
        for item in self.items:
            s += f" - {item.summary()}\n"
        return s

class BistroSystem:
    def __init__(self):
        self.menu = Array([None] * 5)  # ✅ Array fix
        self._load_menu()
        self.open_orders = CircularQueue(10)
        self.completed_orders = HashMap()
        self.total_revenue = 0.0

    def _load_menu(self):
        drinks = [
            ("Bearcat Mocha", 4.50),
            ("Caramel Catpuccino", 4.25),
            ("Meowcha Latte", 4.75),
            ("Vanilla Purrccino", 4.00),
            ("Espresso Whisker Shot", 3.50)
        ]
        for i, (name, price) in enumerate(drinks):
            self.menu[i] = Drink(name, price)

    def display_menu(self):
        print("\n🍹 Bearcat Bistro Menu:")
        for i in range(len(self.menu)):
            drink = self.menu[i]
            print(f"{i+1}. {drink.name} - ${drink.price:.2f}")

    def take_new_order(self):
        customer_name = input("\nWhat's your name? ")
        order = CustomerOrder(customer_name)
        try:
            num_drinks = int(input("How many drinks would you like to order? "))
        except ValueError:
            print("Invalid number. Cancelling order.")
            return

        for i in range(num_drinks):
            while True:
                try:
                    drink_num = int(input(f"Drink #{i+1}: Enter drink number (1-5): "))
                    if not (1 <= drink_num <= 5):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            customization = input(f"Any customization for {self.menu[drink_num-1].name}? ")
            order.add_item(OrderItem(self.menu[drink_num-1], customization))

        # Confirm the order
        print("\n📝 Order Summary:")
        print(order.summary())
        confirm = input("Confirm order? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.open_orders.enqueue(order)
            print("✅ Order placed successfully!")
        else:
            print("❌ Order cancelled.")

    def view_open_orders(self):
        if self.open_orders.empty:
            print("\nNo open orders.")
            return

        print("\n🕒 Open Orders:")
        temp_queue = CircularQueue(10)
        while not self.open_orders.empty:
            order = self.open_orders.dequeue()
            print(order.summary())
            temp_queue.enqueue(order)

        # Restore orders back to open_orders
        while not temp_queue.empty:
            self.open_orders.enqueue(temp_queue.dequeue())

    def mark_next_order_complete(self):
        if self.open_orders.empty:
            print("\nNo open orders to complete.")
            return

        order = self.open_orders.dequeue()
        print(f"\n✅ Completed Order for {order.customer_name}!")
        # Update completed_orders summary
        for item in order.items:
            drink_name = item.drink.name
            price = item.drink.price

            prev_qty = self.completed_orders.get(drink_name) or 0
            self.completed_orders[drink_name] = prev_qty + 1   # ✅ Fixed from .put to []=
            self.total_revenue += price

    def end_of_day_report(self):
        if len(self.completed_orders) == 0:
            print("\n📊 No completed orders today.")
            return

        print("\n📊 End-of-Day Report")
        print("----------------------------")
        print(f"{'Drink Name':25} {'Qty Sold':10} {'Total Sales'}")

        for drink_name in self.completed_orders:
            qty = self.completed_orders[drink_name]  # ✅ Fixed: get value manually
            for i in range(len(self.menu)):
                if self.menu[i].name == drink_name:
                    price = self.menu[i].price
                    break
            total_sales = qty * price
            print(f"{drink_name:25} {qty:<10} ${total_sales:.2f}")

        print(f"Total Revenue: ${self.total_revenue:.2f}")
        print("Thanks for using Bearcat Bistro POS System! 🐾 Come back soon!")

def main():
    system = BistroSystem()

    while True:
        print("\n📋 Main Menu")
        print("1. Display Menu")
        print("2. Take New Order")
        print("3. View Open Orders")
        print("4. Mark Next Order as Complete")
        print("5. View End-of-Day Report")
        print("6. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            system.display_menu()
        elif choice == "2":
            system.take_new_order()
        elif choice == "3":
            system.view_open_orders()
        elif choice == "4":
            system.mark_next_order_complete()
        elif choice == "5":
            system.end_of_day_report()
        elif choice == "6":
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
