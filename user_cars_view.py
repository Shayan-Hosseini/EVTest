import tkinter as tk
from tkinter import ttk, messagebox

class UserCarsView:
    def __init__(self, root, user_cars_controller, car_controller, car_view):
        self.controller = user_cars_controller
        self.car_controller = car_controller
        self.car_view = car_view

        # Frame for user's cars
        self.frame = ttk.LabelFrame(root, text="Your Logged EVs")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.user_evs_tree = ttk.Treeview(self.frame, columns=("id", "brand", "model"), show='headings')
        self.user_evs_tree.heading("id", text="ID")
        self.user_evs_tree.heading("brand", text="Brand")
        self.user_evs_tree.heading("model", text="Model")
        self.user_evs_tree.pack(fill="both", expand=True)

        self.update_user_evs_tree()

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", pady=5)

        self.add_ev_button = ttk.Button(button_frame, text="Add EV", command=self.add_ev_ui)
        self.add_ev_button.pack(side="left", padx=5)

        self.delete_ev_button = ttk.Button(button_frame, text="Delete Selected EV", command=self.delete_ev)
        self.delete_ev_button.pack(side="left", padx=5)

        self.search_with_ev_button = ttk.Button(button_frame, text="Search DB with Selected EV", command=self.search_db_with_selected_ev)
        self.search_with_ev_button.pack(side="left", padx=5)

    def update_user_evs_tree(self):
        for i in self.user_evs_tree.get_children():
            self.user_evs_tree.delete(i)
        evs = self.controller.get_user_evs()
        for ev in evs:
            self.user_evs_tree.insert("", "end", values=ev)

    def add_ev_ui(self):
        # Popup to add a new EV
        top = tk.Toplevel()
        top.title("Add New EV")

        tk.Label(top, text="Brand:").pack(pady=5)
        brand_entry = tk.Entry(top)
        brand_entry.pack()

        tk.Label(top, text="Model:").pack(pady=5)
        model_entry = tk.Entry(top)
        model_entry.pack()

        def add_ev_action():
            brand = brand_entry.get().strip()
            model = model_entry.get().strip()
            if brand and model:
                msg = self.controller.log_ev(brand, model)
                messagebox.showinfo("Info", msg)
                self.update_user_evs_tree()
                top.destroy()
            else:
                messagebox.showerror("Error", "Brand and model are required.")

        ttk.Button(top, text="Add", command=add_ev_action).pack(pady=10)

    def delete_ev(self):
        selected_item = self.user_evs_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No EV selected.")
            return
        item = self.user_evs_tree.item(selected_item)
        car_id = item['values'][0]
        msg = self.controller.delete_user_ev(car_id)
        messagebox.showinfo("Info", msg)
        self.update_user_evs_tree()

    def search_db_with_selected_ev(self):
        selected_item = self.user_evs_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No user EV selected.")
            return
        item = self.user_evs_tree.item(selected_item)
        user_car_id, user_car_brand, user_car_model = item['values']

        # Clear existing search results
        self.car_view.clear_search_results()

        # Search with brand and model
        results = self.car_controller.search_ev_by_brand_and_model(user_car_brand, user_car_model)
        if not results:
            if user_car_brand:
                results = self.car_controller.search_ev_by_brand(user_car_brand)
            if not results and user_car_model:
                results = self.car_controller.search_ev_by_model(user_car_model)

        self.car_view.populate_search_results(results)