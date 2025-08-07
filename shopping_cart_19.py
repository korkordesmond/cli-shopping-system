import os

# Catalogue Items
product_catalog = {
    1001: {"name": "Notebook Pack (5 pcs)", "price": 4.99, "quantity": 12},
    2001: {"name": "Scientific Calculator", "price": 14.50, "quantity": 6},
    3001: {"name": "Ballpoint Pens (10 pcs)", "price": 3.25, "quantity": 20},
    4001: {"name": "Highlighter Set (6 pcs)", "price": 5.75, "quantity": 8},
    5001: {"name": "Backpack", "price": 29.99, "quantity": 4},
    6001: {"name": "Laptop Stand", "price": 19.99, "quantity": 5},
    # Add more items if needed
}

def align_center(string):
    return f"{string:^70}"


def show_available_products():
    print(f"\n{'Id':<6}{'Products':<37}{'Price':<15}{'Quantity Available':<15}")
    for idx, product in product_catalog.items():
        print(f"{str(idx).zfill(4):<6}"
              f"{product['name']:<35}"
              f"${product['price']:>7.2f}"
              f"{str(product['quantity']).rjust(10):>15}")


class Cart:

    def __init__(self):
        """Initialize all variables used in the cart"""
        self.idx = None
        self.name = ''
        self.price = 0
        self.quantity = 0
        self.total_quantity = 0
        self.total_price = 0.0
        self.products = {}

    def get_total_price(self):
        """Get total price for all products in Cart"""
        self.total_quantity = sum(product['quantity'] for product in self.products.values())
        self.total_price = sum(product['price'] for product in self.products.values())
        return self.total_price

    def add_product(self, idx):
        """Allows User to add a product to cart"""

        if idx not in product_catalog:
            print("Product does not exist.")
            return

        if idx not in self.products:
            self.products[idx] = {
                "name": product_catalog[idx]["name"],
                "price": product_catalog[idx]["price"],
                "quantity": 1
            }
        else:
            self.products[idx]["quantity"] += 1
            self.products[idx]["price"] = product_catalog[idx]["price"] * self.products[idx]["quantity"]

        # Apply discount logic: Buy 3 get 1 free (i.e., pay for 3 only)
        if self.products[idx]["quantity"] == 4:
            print("Discount Applied: Buy 3 Get 1 Free!")
            self.products[idx]["price"] = product_catalog[idx]["price"] * 3

    def remove_product(self, idx):
        """Allows user to remove a product from the cart"""

        if self.products[idx]['quantity'] > 1:
            self.products[idx]['quantity'] -= 1
            self.products[idx]["price"] = product_catalog[idx]["price"] * self.products[idx]["quantity"]
        else:
            del self.products[idx]

    def show_cart(self):
        """Shows the items in the cart"""

        if not self.products:
            print(align_center('No Item in Cart'))
            return
        else:
            print(f"\n{str(f'Total Costs to Checkout: ${self.get_total_price():.2f}'):<50}No. of Items: {self.total_quantity}")
            print(f"{'Id':<6}{'Products':<37}{'Quantity':<15}{'Cost':<15}")
            for idx, product in self.products.items():
                print(f"{str(idx).zfill(4):<6}"
                      f"{product['name']:<37}"
                      f"{str(product['quantity']).rjust(5):<15}"
                      f"${product['price']:>6.2f}")
            return self.products

    @staticmethod
    def generate_unique_filename(base_name):
        i = 1
        filename = f"{base_name}.txt"
        while os.path.exists(filename):
            filename = f"{base_name}_{i}.txt"
            i += 1
        return filename

    def checkout(self, customer_name):
        """Generates and saves an invoice as a .txt file with customer's name."""

        if not self.products:
            print(align_center('Your cart is empty. Nothing to checkout.'))
            return

        invoice_lines = ["=" * 70, f"{'INVOICE':^70}", f"{'Customer: ' + customer_name:^70}", "=" * 70,
                         f"{'Id':<8}{'Product':<35}{'Quantity':<15}{'Cost':<15}", "-" * 70]

        total = 0
        for idx, product in self.products.items():
            cost = product['price']
            total += cost
            invoice_lines.append(
                f"{str(idx).zfill(4):<8}"
                f"{product['name']:<35}"
                f"{str(product['quantity']).rjust(5):<15}"
                f"${cost:>6.2f}"
            )

        invoice_lines.append("-" * 70)
        invoice_lines.append(f"{'TOTAL':<58}${total:>6.2f}")
        invoice_lines.append("=" * 70)
        invoice_lines.append("Thank you for shopping with us!")

        base_name = f"invoice_{customer_name.replace(' ', '_').lower()}"
        filename = self.generate_unique_filename(base_name)

        with open(filename, "w") as f:
            for line in invoice_lines:
                f.write(line + "\n")

        print(f"\nInvoice saved as '{filename}'.")
        print("\n".join(invoice_lines))

        self.products.clear()
        self.total_price = 0


my_cart = Cart()


def add_item():
    """Shows GUI for addition of item to cart"""

    try:
        idx = int(input("\nEnter the Id of the product ID to add to your cart: "))
    except ValueError:
        return align_center('Invalid input! Please enter a numeric product ID.')

    if idx in product_catalog:
        my_cart.add_product(idx)
        return f"\n{product_catalog[idx]['name']} added to cart successfully"
    else:
        return align_center('Product not found')


def remove_item():
    """Shows GUI for removal of item from cart"""
    my_cart.show_cart()
    try:
        idx = int(input("\nEnter the Id of the product ID to remove from cart: "))
    except ValueError:
        return align_center('Invalid input! Please enter a numeric product ID.')

    if idx in my_cart.products:
        my_cart.remove_product(idx)
        return f"\n{product_catalog[idx]['name']} removed from cart, successfully"
    else:
        return "Product Not In Cart"


def start():
    """Starts the whole program"""

    count = 0
    user = input('Enter your name: ') or "Unknown"
    while True:
        if count == 0:
            print(f"Welcome {user}, which operation do you want to perform")
            count += 1
        else:
            print(f"\n{user}, choose your next operation")
            count += 1

        print("1.Add an Item\t\t\t2.Remove an item\t\t\t3.Show Cart\t\t\t4.Checkout")
        option = input("Reply: ")

        if option == '1':
            show_available_products()
            print(add_item())
            continue
        elif option == '2':
            print(remove_item())
            continue
        elif option == '3':
            my_cart.show_cart()
            continue
        elif option == '4':
            if my_cart.checkout(user):
                continue
            else:
                break
        else:
            print(align_center('Operation not Valid'))
            continue


if __name__ == "__main__":
    start()
