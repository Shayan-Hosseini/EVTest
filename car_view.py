import tkinter as tk
from tkinter import ttk, messagebox

class CarView:
    def __init__(self, root, car_controller):
        self.controller = car_controller

        self.frame = ttk.LabelFrame(root, text="Car Database Search")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.frame, text="Brand:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_brand_entry = tk.Entry(self.frame)
        self.search_brand_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Model:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.search_model_entry = tk.Entry(self.frame)
        self.search_model_entry.grid(row=1, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(self.frame, text="Search", command=self.search_ev)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Results tree
        self.results_tree = ttk.Treeview(self.frame, 
                                         columns=("id", "brand", "model", "bodystyle", "seat", "priceeuro"), 
                                         show='headings')
        self.results_tree.heading("id", text="ID")
        self.results_tree.heading("brand", text="Brand")
        self.results_tree.heading("model", text="Model")
        self.results_tree.heading("bodystyle", text="Body Style")
        self.results_tree.heading("seat", text="Seat")
        self.results_tree.heading("priceeuro", text="Price (Euro)")
        self.results_tree.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)

        self.info_button = ttk.Button(self.frame, text="Get Car Info", command=self.get_car_info)
        self.info_button.grid(row=4, column=0, columnspan=2, pady=5)

        #expandable frame
        self.frame.rowconfigure(3, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def search_ev(self):
        brand = self.search_brand_entry.get().strip()
        model = self.search_model_entry.get().strip()
        self.clear_search_results()

        if brand and model:
            results = self.controller.search_ev_by_brand_and_model(brand, model)
        elif brand:
            results = self.controller.search_ev_by_brand(brand)
        elif model:
            results = self.controller.search_ev_by_model(model)
        else:
            messagebox.showerror("Error", "Please provide at least one search criterion.")
            return

        self.populate_search_results(results)

    def populate_search_results(self, results):
        for res in results:
            self.results_tree.insert("", "end", values=res)

    def clear_search_results(self):
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)

    def get_car_info(self):
        selected_item = self.results_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No car selected.")
            return
        item = self.results_tree.item(selected_item)
        car_id = item['values'][0]

        perf = self.controller.get_performance_info(car_id)
        bat = self.controller.get_battery_info(car_id)

        info_msg = ""
        if perf:
            for p in perf:
                info_msg += f"Performance:\nAccel: {p[2]}s, Top Speed: {p[3]} km/h\n\n"

        if bat:
            for b in bat:
                info_msg += f"Battery:\nFast Charge: {b[2]} km/h, Rapidcharge: {b[3]}, Plugtype: {b[4]}\n\n"
                range_id = b[5]
                rng = self.controller.get_range_info(range_id)
                if rng:
                    for r in rng:
                        info_msg += f"Range:\nFastcharge: {r[2]} km/h, Rapidcharge: {r[3]}, Plugtype: {r[4]}, Powertrain: {r[5]}, Range_km: {r[6]}, Efficiency: {r[7]} Wh/km\n"

        if not perf and not bat:
            info_msg = "No detailed info found for this car."

        messagebox.showinfo("Car Info", info_msg)