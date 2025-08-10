from tkinter import Tk, Frame, Button, Label, messagebox, ttk
from PIL import Image, ImageTk
import csv
import os

# Load pizza prices from CSV
def load_pizza_prices():
    prices = {}
    try:
        with open("pizza_prices.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    pizza_name = row[0].strip()
                    try:
                        price = float(row[1])
                        prices[pizza_name] = price
                    except ValueError:
                        print(f"Skipping invalid price entry: {row}")
                else:
                    print(f"Skipping malformed row: {row}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Price file not found!")
    
    return prices

# Main Application Window
class PizzaStoreApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Pizza Store")
        self.geometry("800x600")
        self.configure(bg="white")

        # Load pizza prices
        self.pizza_prices = load_pizza_prices()
        self.cart = []

        # Frame Setup
        self.menu_buttons_frame = Frame(self, bg="lightgray")
        self.menu_buttons_frame.pack(fill="x")

        self.pizza_display_frame = Frame(self, bg="white")
        self.pizza_display_frame.pack(fill="both", expand=True)

        self.pizza_detail_frame = Frame(self, bg="lightgray")
        self.pizza_detail_frame.pack(fill="x")

        self.order_details_frame = Frame(self, bg="white")
        self.order_details_frame.pack(fill="both", expand=True)

        # Create Menu Buttons
        self.create_menu_buttons()

    def create_menu_buttons(self):
        Button(self.menu_buttons_frame, text="Show All Pizzas", command=self.show_pizzas).pack(side="left", padx=5)
        Button(self.menu_buttons_frame, text="Clear All Pizzas", command=self.clear_pizzas).pack(side="left", padx=5)
        Button(self.menu_buttons_frame, text="Quit", command=self.quit_app).pack(side="left", padx=5)

    def show_pizzas(self):
        for widget in self.pizza_display_frame.winfo_children():
            widget.destroy()

        row, col = 0, 0  # Grid positioning

        for pizza_name in self.pizza_prices.keys():
            image_path = f"images/{pizza_name}.jpg"
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((120, 120))  # Resize for uniform display
                photo = ImageTk.PhotoImage(img)

                btn = Button(self.pizza_display_frame, image=photo, text=pizza_name, compound="top",
                             command=lambda p=pizza_name: self.show_pizza_details(p))
                btn.photo = photo  # Keep reference to avoid garbage collection
                btn.grid(row=row, column=col, padx=5, pady=5)  # Use grid layout

                col += 1
                if col >= 4:  # Limit to 4 columns per row
                    col = 0
                    row += 1
            else:
                print(f"Image not found: {image_path}")

    def show_pizza_details(self, pizza_name):
        for widget in self.pizza_detail_frame.winfo_children():
            widget.destroy()

        image_path = f"images/{pizza_name}.jpg"
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((150, 150))
            photo = ImageTk.PhotoImage(img)
            Label(self.pizza_detail_frame, image=photo).pack()
            self.photo = photo  # Keep reference to prevent garbage collection
        else:
            print(f"Image not found: {image_path}")

        Label(self.pizza_detail_frame, text=f"{pizza_name} - £{self.pizza_prices[pizza_name]:.2f}").pack(pady=5)
        quantity = ttk.Spinbox(self.pizza_detail_frame, from_=1, to=10)
        quantity.pack(pady=5)
        Button(self.pizza_detail_frame, text="Add to Cart", command=lambda: self.add_to_cart(pizza_name, int(quantity.get()))).pack(pady=5)

    def add_to_cart(self, pizza_name, quantity):
        self.cart.append((pizza_name, quantity, self.pizza_prices[pizza_name] * quantity))
        self.update_order_details()

    def update_order_details(self):
        for widget in self.order_details_frame.winfo_children():
            widget.destroy()

        total = 0
        for pizza_name, qty, cost in self.cart:
            Label(self.order_details_frame, text=f"{pizza_name} - Qty: {qty} - £{cost:.2f}").pack()
            total += cost

        Label(self.order_details_frame, text=f"Grand Total: £{total:.2f}", font=("Arial", 12, "bold")).pack(pady=5)
        Button(self.order_details_frame, text="Cancel", command=self.clear_cart).pack(side="left", padx=5)
        Button(self.order_details_frame, text="Confirm", command=self.confirm_order).pack(side="left", padx=5)

    def clear_cart(self):
        self.cart.clear()
        self.update_order_details()
        messagebox.showinfo("Cart", "Your cart is empty")

    def confirm_order(self):
        if self.cart:
            self.cart.clear()
            self.update_order_details()
            messagebox.showinfo("Order", "Order successfully placed!")

    def clear_pizzas(self):
        for widget in self.pizza_display_frame.winfo_children():
            widget.destroy()
        for widget in self.pizza_detail_frame.winfo_children():
            widget.destroy()
        for widget in self.order_details_frame.winfo_children():
            widget.destroy()

    def quit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
            self.destroy()

# Run App
if __name__ == "__main__":
    app = PizzaStoreApp()
    app.mainloop()