import json
import os
from datetime import datetime

class SzMUnitConverter:
    def __init__(self, history_filename="conversion_history_szm.json"):
        self.history_filename = history_filename
        self.history = self.szm_load_history()

        self.rates = {
            "Length": {
                "cm": 0.01,
                "m": 1.0,
                "km": 1000.0,
                "inch": 0.0254,
                "foot": 0.3048
            },
            "Weight": {
                "g": 0.001,
                "kg": 1.0,
                "lb": 0.453592
            },
            "Currency": {
                "HUF": 1.0,
                "EUR": 400.0,
                "USD": 370.0,
                "GBP": 470.0
            }
        }

    def szm_convert_units(self, category, value, from_unit, to_unit):
        if category == "Temperature":
            return self.szm_convert_temperature(value, from_unit, to_unit)

        if category in self.rates:
            cat_rates = self.rates[category]
            if from_unit in cat_rates and to_unit in cat_rates:
                base_value = value * cat_rates[from_unit]
                result = base_value / cat_rates[to_unit]
                return round(result, 4)
        return None

    def szm_convert_temperature(self, value, from_unit, to_unit):
        if from_unit == to_unit:
            return value

        if from_unit == "°C":
            celsius = value
        elif from_unit == "°F":
            celsius = (value - 32) * 5/9
        elif from_unit == "K":
            celsius = value - 273.15

        if to_unit == "°C":
            return round(celsius, 2)
        elif to_unit == "°F":
            return round((celsius * 9/5) + 32, 2)
        elif to_unit == "K":
            return round(celsius + 273.15, 2)

    def szm_save_conversion(self, category, value, from_unit, result, to_unit):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "input": f"{value} {from_unit}",
            "result": f"{result} {to_unit}"
        }
        self.history.append(entry)

        if len(self.history) > 20:
            self.history.pop(0)

        try:
            with open(self.history_filename, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")

    def szm_load_history(self):
        if os.path.exists(self.history_filename):
            try:
                with open(self.history_filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def szm_delete_history_item(self, index):
        if 0 <= index < len(self.history):
            self.history.pop(index)
            self.szm_save_all_history()

    def szm_save_all_history(self):
        try:
            with open(self.history_filename, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error while saving: {e}")

    def szm_clear_all_history(self):
        self.history = []
        self.szm_save_all_history()