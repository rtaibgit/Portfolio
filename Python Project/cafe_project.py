from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

TEAM_NAME = "PaperCup"  
EMPLOYEE_PASSWORD = "password"  

# Data Models
@dataclass
class Product:
    id: str
    category: str  # "drinks" | "food" | "books"
    name: str
    price: float
    stock: int
    details: str  # ingredients / author / description
    delivery_eligible: bool = False 

@dataclass
class BasketItem:
    product_id: str
    name: str
    unit_price: float
    qty: int

# Inventory
def seed_inventory() -> Dict[str, Product]:
    return {
        # Drinks
        "D1": Product("D1", "drinks", "Flat White", 3.60, 30, "Espresso + steamed milk"),
        "D2": Product("D2", "drinks", "Matcha Latte", 4.10, 20, "Matcha + milk"),
        "D3": Product("D3", "drinks", "Iced Americano", 3.20, 25, "Espresso + water + ice"),
        "D4": Product("D4", "drinks", "Tea", 2.00, 10, "Tea + hot water"),  
        "D5": Product("D5", "drinks", "Herbal Tea", 3.00, 15, "Tea + herbs + hot water"), 

        # Food (cakes/snacks)
        "F1": Product("F1", "food", "Chocolate Brownie", 2.90, 15, "Cocoa, butter, eggs, sugar, flour"),
        "F2": Product("F2", "food", "Carrot Cake Slice", 3.40, 10, "Carrot, cinnamon, cream cheese frosting"),
        "F3": Product("F3", "food", "Cheese Cake", 4.00, 10, "Cream cheese, digestive, vanilla"),
        "F4": Product("F4", "food", "Croissant", 3.00, 15, "Bread"),
        "F5": Product("F5", "food", "Chesse Bagel", 4.00, 7, "Cheese, Bread"),
 

        # Books
        "B1": Product("B1", "books", "Atomic Habits", 12.99, 8, "James Clear — Habit building", delivery_eligible=True),
        "B2": Product("B2", "books", "The Midnight Library", 9.99, 6, "Matt Haig — Fiction", delivery_eligible=True),
        "B3": Product("B3", "books", "Deep Work", 11.50, 5, "Cal Newport — Focus & productivity", delivery_eligible=True),
        "B4": Product("B4", "books", "Seven Habits of Highly Effective People", 14.99, 7, "Steven Cohen — Habit building", delivery_eligible=True), 
        "B5": Product("B5", "books", "Harry Potter", 14.99, 7, "J K Rowling — Fiction", delivery_eligible=True), 
        
    }


# ---------- Extra Functions for mathematical operations being called elsewhere ----------
def money(x: float) -> str:
    return f"£{x:.2f}"

def pause():
    input("\nPress Enter to continue...")

def ask_int(prompt: str, min_v: int, max_v: int) -> int:
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            val = int(raw)
            if min_v <= val <= max_v:
                return val
        print(f"Please enter a number between {min_v} and {max_v}.")

def ask_yes_no(prompt: str) -> bool:
    while True:
        raw = input(prompt + " (Y/N): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please type Y or N.")


# ----------  functions for User Interface Screens ----------
def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"{TEAM_NAME} — {title}")
    print("=" * 60)

def list_products(inventory: Dict[str, Product], category: str) -> List[Product]:
    return [p for p in inventory.values() if p.category == category]

def show_category(inventory: Dict[str, Product], category: str):
    print_header(category.upper())
    products = list_products(inventory, category)
    if not products:
        print("No items found.")
        return

    for idx, p in enumerate(products, start=1):
        stock_note = f"(stock: {p.stock})"
        print(f"{idx}. {p.name} — {money(p.price)} {stock_note}")

def choose_product(inventory: Dict[str, Product], category: str) -> Optional[Product]:
    products = list_products(inventory, category)
    if not products:
        return None

    show_category(inventory, category)
    print("\n0. Back")

    choice = ask_int("Select an item number: ", 0, len(products))
    if choice == 0:
        return None
    return products[choice - 1]

# Showing Output 

def show_product_details(product: Product):
    print_header("DETAILS")
    print(f"Item: {product.name}")
    print(f"Price: {money(product.price)}")
    print(f"Stock: {product.stock}")
    print(f"Details: {product.details}")
    if product.category == "books":
        print(f"Delivery eligible: {'Yes' if product.delivery_eligible else 'No'}")

def add_to_basket(basket: List[BasketItem], product: Product, qty: int):
    # If already in basket, increase qty
    for item in basket:
        if item.product_id == product.id:
            item.qty += qty
            return
    basket.append(BasketItem(product.id, product.name, product.price, qty))

def basket_total(basket: List[BasketItem]) -> float:
    return sum(i.unit_price * i.qty for i in basket)

def print_basket(basket: List[BasketItem]):
    print_header("YOUR ORDER")
    if not basket:
        print("Basket is empty.")
        return
    for idx, item in enumerate(basket, start=1):
        line_total = item.unit_price * item.qty
        print(f"{idx}. {item.name} x{item.qty} — {money(item.unit_price)} each = {money(line_total)}")
    print("-" * 60)
    print(f"Total: {money(basket_total(basket))}")

def remove_from_basket(basket: List[BasketItem]):
    if not basket:
        return
    print_basket(basket)
    choice = ask_int("Remove which line? (0 to cancel): ", 0, len(basket))
    if choice == 0:
        return
    removed = basket.pop(choice - 1)
    print(f"Removed: {removed.name}")

def adjust_basket_qty(basket: List[BasketItem]):
    if not basket:
        return
    print_basket(basket)
    choice = ask_int("Adjust which line? (0 to cancel): ", 0, len(basket))
    if choice == 0:
        return
    item = basket[choice - 1]
    new_qty = ask_int(f"New quantity for {item.name} (1-99): ", 1, 99)
    item.qty = new_qty
    print("Updated.")

def apply_discount(total: float) -> Tuple[float, float]:
    # matches your flowchart: apply 10% discount
    discount_rate = 0.10
    discount_amount = total * discount_rate
    new_total = total - discount_amount
    return new_total, discount_amount


# ---------- Employee Functions (dicounts + delivery)----------
def employee_login() -> bool:
    print_header("EMPLOYEE LOGIN")
    pw = input("Enter employee password: ").strip()
    return pw == EMPLOYEE_PASSWORD

def employee_add_item(inventory: Dict[str, Product]):
    print_header("ADD NEW ITEM")
    new_id = input("New ID (e.g. D4 / F3 / B9): ").strip().upper()
    if new_id in inventory:
        print("That ID already exists.")
        return

    category = input("Category (drinks/food/books): ").strip().lower()
    if category not in ("drinks", "food", "books"):
        print("Invalid category.")
        return

    name = input("Name: ").strip()
    price = float(input("Price (e.g. 3.50): ").strip())
    stock = int(input("Stock (e.g. 10): ").strip())
    details = input("Details (ingredients/author/etc): ").strip()
    delivery_eligible = False
    if category == "books":
        delivery_eligible = ask_yes_no("Delivery eligible?")

    inventory[new_id] = Product(
        id=new_id,
        category=category,
        name=name,
        price=price,
        stock=stock,
        details=details,
        delivery_eligible=delivery_eligible,
    )
    print("Item added!")

def employee_update_stock(inventory: Dict[str, Product]):
    print_header("UPDATE STOCK")
    pid = input("Enter product ID: ").strip().upper()
    if pid not in inventory:
        print("Not found.")
        return
    p = inventory[pid]
    print(f"Current: {p.name} stock={p.stock}")
    new_stock = int(input("New stock value: ").strip())
    p.stock = new_stock
    print("Stock updated.")


# ---------- USER JOURNEY ----------
def customer_flow(inventory: Dict[str, Product]):
    basket: List[BasketItem] = []
    discounted = False
    discount_amount = 0.0

    while True:
        print_header("WELCOME TO PAPERCUP")
        print("What would you like to order today?")
        print("1. Drinks")
        print("2. Food")
        print("3. Books")
        print("4. Review order")
        print("5. Checkout")
        print("0. Exit")

        choice = ask_int("Select an option: ", 0, 5)

        if choice == 0:
            print("Thank you for visitng, hope to see you soon!")
            return

        if choice in (1, 2, 3):
            category = {1: "drinks", 2: "food", 3: "books"}[choice]
            product = choose_product(inventory, category)
            if not product:
                continue

            # User asked if they want details (flowchart)
            if ask_yes_no("View additional details?"):
                show_product_details(product)
                pause()

            if product.stock <= 0:
                print("Sorry, out of stock.")
                pause()
                continue

            qty = ask_int(f"How many '{product.name}'? ", 1, min(99, product.stock))
            add_to_basket(basket, product, qty)
            product.stock -= qty  # reduce stock when added to basket
            print("Added to basket!")
            pause()
            continue

        if choice == 4:
            # Review order (flowchart)
            while True:
                print_basket(basket)
                print("\n1. Remove an item")
                print("2. Adjust quantity")
                print("0. Back")
                sub = ask_int("Select: ", 0, 2)
                if sub == 0:
                    break
                if sub == 1:
                    remove_from_basket(basket)
                    pause()
                elif sub == 2:
                    adjust_basket_qty(basket)
                    pause()
            continue

        if choice == 5:
            # Checkout flow with employee discount option (your diagram)
            if not basket:
                print("Basket is empty.")
                pause()
                continue

            print_basket(basket)
            total = basket_total(basket)

            # Ask employee Y/N then apply 10% discount (diagram)
            if ask_yes_no("Are you an employee?"):
                if employee_login():
                    if not discounted and ask_yes_no("Apply 10% promotional discount?"):
                        new_total, disc = apply_discount(total)
                        discounted = True
                        discount_amount = disc
                        total = new_total
                        print(f"Discount applied: -{money(discount_amount)}")
                    else:
                        print("No discount applied.")
                else:
                    print("Incorrect password. Continuing as customer.")

            # Delivery stretch: if books exist in basket
            has_books = any(inventory.get(i.product_id, Product("", "", "", 0, 0, "")).category == "books" for i in basket)
            delivery = False
            if has_books:
                delivery = ask_yes_no("Do you want book delivery (where eligible)?")
                if delivery:
                    name = input("Delivery name: ").strip()
                    address = input("Delivery address: ").strip()
                    print(f"Delivery set for: {name}, {address}")

            print_header("CONFIRMATION")
            if discounted:
                print(f"Discount: -{money(discount_amount)}")
            print(f"Final total: {money(total)}")
            if ask_yes_no("Place order?"):
                print_header("STATUS")
                print("Preparing your order ☕📚")
                if delivery:
                    print("Your books will be delivered as requested.")
                print("Thank you!")
                pause()
                return
            else:
                print("Order not placed. Returning to menu.")
                pause()
                continue


def employee_portal(inventory: Dict[str, Product]):
    if not employee_login():
        print("Access denied.")
        pause()
        return

    while True:
        print_header("EMPLOYEE PORTAL")
        print("1. Add new menu/book item")
        print("2. Update stock")
        print("3. View inventory")
        print("0. Back")

        choice = ask_int("Select: ", 0, 3)
        if choice == 0:
            return
        if choice == 1:
            employee_add_item(inventory)
            pause()
        elif choice == 2:
            employee_update_stock(inventory)
            pause()
        elif choice == 3:
            print_header("INVENTORY")
            for p in inventory.values():
                print(f"{p.id} | {p.category} | {p.name} | {money(p.price)} | stock={p.stock}")
            pause()


def main():
    inventory = seed_inventory()

    while True:
        print_header("HOME")
        print("1. Customer ordering")
        print("2. Employee admin")
        print("0. Exit")

        choice = ask_int("Select: ", 0, 2)
        if choice == 0:
            print("Goodbye!")
            break
        elif choice == 1:
            customer_flow(inventory)
        elif choice == 2:
            employee_portal(inventory)


if __name__ == "__main__":
    main()