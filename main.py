import tkinter as tk
from tkinter import ttk, messagebox
import sajat_modul_szm as szm_modul

class UniConvertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UniConvert GUI")
        self.root.geometry("520x600")
        self.root.resizable(False, False)

        self.converter = szm_modul.SzMUnitConverter()
        self.skip_delete_confirm = False

        self.categories = {
            "Length": ["cm", "m", "km", "inch", "foot"],
            "Weight": ["g", "kg", "lb"],
            "Temperature": ["°C", "°F", "K"],
            "Currency": ["HUF", "EUR", "USD", "GBP"]
        }

        self.setup_ui()

    def setup_ui(self):
        header = ttk.Label(self.root, text="UniConvert GUI", font=("Arial", 18, "bold"))
        header.pack(pady=10)

        cat_frame = ttk.LabelFrame(self.root, text=" Select Category ", padding=10)
        cat_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(cat_frame, text="Category:").grid(row=0, column=0, sticky="w", padx=5)
        self.cat_combo = ttk.Combobox(cat_frame, values=list(self.categories.keys()), state="readonly")
        self.cat_combo.grid(row=0, column=1, padx=5, sticky="ew")
        self.cat_combo.current(0)
        self.cat_combo.bind("<<ComboboxSelected>>", self.on_category_change)

        conv_frame = ttk.LabelFrame(self.root, text=" Conversion ", padding=10)
        conv_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(conv_frame, text="Value:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.val_entry = ttk.Entry(conv_frame)
        self.val_entry.grid(row=0, column=1, padx=5, pady=5)
        self.val_entry.insert(0, "1.0")

        ttk.Label(conv_frame, text="From:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.from_combo = ttk.Combobox(conv_frame, state="readonly")
        self.from_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(conv_frame, text="To:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.to_combo = ttk.Combobox(conv_frame, state="readonly")
        self.to_combo.grid(row=2, column=1, padx=5, pady=5)

        self.val_entry.bind("<KeyRelease>", self.check_duplicate_conversion)
        self.from_combo.bind("<<ComboboxSelected>>", self.check_duplicate_conversion)
        self.to_combo.bind("<<ComboboxSelected>>", self.check_duplicate_conversion)

        self.convert_btn = ttk.Button(conv_frame, text="Convert", command=self.handle_convert)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(conv_frame, text="Result: -", font=("Arial", 12, "bold"), foreground="blue")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        hist_frame = ttk.LabelFrame(self.root, text=" History (Saved to JSON) ", padding=10)
        hist_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.history_list = tk.Listbox(hist_frame, height=8)
        self.history_list.pack(fill="both", expand=True)

        delete_btn = ttk.Button(hist_frame, text="Delete", command=self.handle_delete_selected)
        delete_btn.pack(anchor="e", pady=2)

        clear_btn = ttk.Button(hist_frame, text="Clear All", command=self.handle_clear_all)
        clear_btn.pack(anchor="e", pady=2)

        self.update_unit_combos()
        self.refresh_history_list()

    def on_category_change(self, event):
        self.update_unit_combos()

    def update_unit_combos(self):
        cat = self.cat_combo.get()
        units = self.categories[cat]

        self.from_combo['values'] = units
        self.to_combo['values'] = units
        self.from_combo.current(0)
        self.to_combo.current(1 if len(units) > 1 else 0)

    def handle_convert(self):
        from_u = self.from_combo.get()
        to_u = self.to_combo.get()

        if from_u == to_u:
            messagebox.showwarning("Warning", "The source and target units are the same! No conversion needed.")
            return

        try:
            val = float(self.val_entry.get().replace(",","."))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value!")
            return

        cat = self.cat_combo.get()

        res = self.converter.szm_convert_units(cat, val, from_u, to_u)

        if res is not None:
            self.result_label.config(text=f"Result: {val} {from_u} = {res} {to_u}")
            self.converter.szm_save_conversion(cat, val, from_u ,res, to_u)
            self.refresh_history_list()
        else:
            messagebox.showerror("Error", "Conversion failed!")

    def check_duplicate_conversion(self, event=None):
        try:
            from_u = self.from_combo.get()
            to_u = self.to_combo.get()

            if from_u == to_u and from_u != "":
                self.convert_btn.config(state="disabled")
            else:
                self.convert_btn.config(state="normal")
        except Exception:
            pass

    def refresh_history_list(self):
        self.history_list.delete(0, tk.END)
        for item in reversed(self.converter.history):
            line = f"[{item['timestamp']}] {item['input']} -> {item['result']}"
            self.history_list.insert(tk.END, line)

    def handle_delete_selected(self):
        try:
            selected_indices = self.history_list.curselection()
            if not selected_indices:
                messagebox.showwarning("Selection Error", "Please click on an item in the history list (blue background) to delete it")
                return

            if not self.skip_delete_confirm:
                dialog = tk.Toplevel(self.root)
                dialog.title("Confirmation")
                dialog.geometry("340x140")
                dialog.resizable(False, False)
                dialog.transient(self.root)
                dialog.grab_set()

                self.root.update_idletasks()

                root_x = self.root.winfo_rootx()
                root_y = self.root.winfo_rooty()
                root_w = self.root.winfo_width()
                root_h = self.root.winfo_height()

                dlg_w = 340
                dlg_h = 140

                pos_x = root_x + (root_w - dlg_w) // 2
                pos_y = root_y + (root_h - dlg_h) // 2

                dialog.geometry(f"{dlg_w}x{dlg_h}+{pos_x}+{pos_y}")

                dont_ask_var = tk.BooleanVar(value=False)

                ttk.Label(dialog, text="Are you sure you want to delete the selected item?", font=("Arial", 9)).pack(pady=15, padx=10)

                chk = ttk.Checkbutton(dialog, text="Don't ask it again", variable=dont_ask_var)
                chk.pack(anchor="w", padx=20, pady=2)

                btn_frame = ttk.Frame(dialog)
                btn_frame.pack(pady=10)

                confirmed = [False]

                def on_yes():
                    confirmed[0] = True
                    if dont_ask_var.get():
                        self.skip_delete_confirm = True
                    dialog.destroy()

                def on_no():
                    dialog.destroy()

                yes_btn = ttk.Button(btn_frame, text="Yes", command=on_yes, width=10)
                yes_btn.pack(side="left", padx=5)
                no_btn = ttk.Button(btn_frame, text="No", command=on_no, width=10)
                no_btn.pack(side="left", padx=5)

                self.root.wait_window(dialog)

                if not confirmed[0]:
                    return

            listbox_index = selected_indices[0]
            real_index = len(self.converter.history) - 1 - listbox_index

            self.converter.szm_delete_history_item(real_index)
            self.refresh_history_list()

        except Exception as e:
            messagebox.showerror("Error", f"Could not delete item {e}")

    def handle_clear_all(self):
        if not self.converter.history:
            messagebox.showinfo("Info", "The history is already empty!")
            return

        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete all conversion history?")
        if confirm:
            self.converter.szm_clear_all_history()
            self.refresh_history_list()

if  __name__ == "__main__":
    root = tk.Tk()
    app = UniConvertApp(root)
    root.mainloop()

