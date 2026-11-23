import tkinter as tk
from tkinter import ttk, messagebox
import math

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("UNIT CONVERTER")
root.geometry("600x720")
root.minsize(500, 650)
root.configure(bg="#172554")

# ---------------- UNIT DATA ----------------

units = {
    "Length": {
        "Meter": 1,
        "Kilometer": 1000,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.344,
        "Foot": 0.3048,
        "Inch": 0.0254
    },

    "Weight": {
        "Kilogram": 1,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.45359237,
        "Ounce": 0.028349523
    },

    "Time": {
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800
    },

    "Area": {
        "Square Meter": 1,
        "Square Kilometer": 1000000,
        "Square Centimeter": 0.0001,
        "Hectare": 10000,
        "Acre": 4046.856422
    },

    "Volume": {
        "Liter": 1,
        "Milliliter": 0.001,
        "Cubic Meter": 1000,
        "Gallon (US)": 3.785411784
    },

    "Speed": {
        "Meter/second": 1,
        "Kilometer/hour": 1 / 3.6,
        "Mile/hour": 0.44704
    },

    "Digital Storage": {
        "Byte": 1,
        "KB": 1024,
        "MB": 1024 ** 2,
        "GB": 1024 ** 3,
        "TB": 1024 ** 4
    },

    "Temperature": {
        "Celsius": 1,
        "Fahrenheit": 1,
        "Kelvin": 1
    }
}

# ---------------- VARIABLES ----------------

history = []
last_result = ""

# ---------------- FUNCTIONS ----------------

def format_number(number):
    if abs(number) < 0.0000000001:
        number = 0

    return f"{number:,.8f}".rstrip("0").rstrip(".")


def update_units(event=None):
    category = category_box.get()
    choices = list(units[category].keys())

    from_box["values"] = choices
    to_box["values"] = choices

    from_box.current(0)

    if len(choices) > 1:
        to_box.current(1)
    else:
        to_box.current(0)

    result_label.config(text="Your result will appear here")
    result_value_label.config(text="")
    

def convert_temperature(value, first, second):

    # Convert the input into Celsius first

    if first == "Celsius":
        celsius = value

    elif first == "Fahrenheit":
        celsius = (value - 32) * 5 / 9

    else:
        celsius = value - 273.15

    # Convert Celsius into the selected unit

    if second == "Celsius":
        return celsius

    elif second == "Fahrenheit":
        return (celsius * 9 / 5) + 32

    else:
        return celsius + 273.15


def convert():

    global last_result

    try:
        value_text = amount_entry.get().strip()

        if not value_text:
            messagebox.showwarning(
                "Missing Value",
                "Please enter a number."
            )
            return

        value = float(value_text)

        if not math.isfinite(value):
            messagebox.showerror(
                "Invalid Value",
                "Please enter a finite number."
            )
            return

        category = category_box.get()
        first = from_box.get()
        second = to_box.get()

        if category == "Temperature":
            result = convert_temperature(
                value, first, second
            )

        else:
            result = (
                value * units[category][first]
                / units[category][second]
            )

        formatted = format_number(result)

        result_label.config(
            text=f"{formatted} {second}"
        )

        result_value_label.config(
            text=f"{format_number(value)} {first} = {formatted} {second}"
        )

        last_result = f"{formatted} {second}"

        record = (
            f"{format_number(value)} {first} = "
            f"{formatted} {second}"
        )

        history.append(record)

        history_list.insert(tk.END, record)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number."
        )

    except Exception as error:
        messagebox.showerror(
            "Conversion Error",
            f"Something went wrong: {error}"
        )


def swap():

    first = from_box.get()
    second = to_box.get()

    from_box.set(second)
    to_box.set(first)


def clear():

    global last_result

    amount_entry.delete(0, tk.END)

    result_label.config(
        text="Your result will appear here"
    )

    result_value_label.config(text="")

    last_result = ""


def copy_result():

    if not last_result:
        messagebox.showinfo(
            "No Result",
            "Please convert a value first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(last_result)

    messagebox.showinfo(
        "Copied",
        "Result copied successfully!"
    )


def clear_history():

    history.clear()
    history_list.delete(0, tk.END)


# ---------------- TITLE ----------------

title = tk.Label(
    root,
    text="UNIT CONVERTER",
    font=("Arial", 25, "bold"),
    bg="#172554",
    fg="white"
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Convert measurements quickly and accurately",
    font=("Arial", 11),
    bg="#172554",
    fg="#bfdbfe"
)
subtitle.pack(pady=(0, 15))


# ---------------- MAIN FRAME ----------------

main_frame = tk.Frame(
    root,
    bg="white",
    padx=25,
    pady=20
)

main_frame.pack(
    padx=25,
    pady=10,
    fill="both",
    expand=True
)


# ---------------- CATEGORY ----------------

tk.Label(
    main_frame,
    text="Select Category",
    font=("Arial", 11, "bold"),
    bg="white"
).pack(anchor="w")

category_box = ttk.Combobox(
    main_frame,
    values=list(units.keys()),
    state="readonly",
    font=("Arial", 11)
)

category_box.pack(fill="x", pady=7)
category_box.set("Length")
category_box.bind(
    "<<ComboboxSelected>>",
    update_units
)


# ---------------- VALUE ----------------

tk.Label(
    main_frame,
    text="Enter Value",
    font=("Arial", 11, "bold"),
    bg="white"
).pack(anchor="w", pady=(8, 0))

amount_entry = tk.Entry(
    main_frame,
    font=("Arial", 14),
    bd=2
)

amount_entry.pack(fill="x", pady=7)


# ---------------- FROM UNIT ----------------

tk.Label(
    main_frame,
    text="Convert From",
    font=("Arial", 11, "bold"),
    bg="white"
).pack(anchor="w", pady=(5, 0))

from_box = ttk.Combobox(
    main_frame,
    state="readonly",
    font=("Arial", 11)
)

from_box.pack(fill="x", pady=7)


# ---------------- TO UNIT ----------------

tk.Label(
    main_frame,
    text="Convert To",
    font=("Arial", 11, "bold"),
    bg="white"
).pack(anchor="w", pady=(5, 0))

to_box = ttk.Combobox(
    main_frame,
    state="readonly",
    font=("Arial", 11)
)

to_box.pack(fill="x", pady=7)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(
    main_frame,
    bg="white"
)

button_frame.pack(pady=12)

convert_button = tk.Button(
    button_frame,
    text="CONVERT",
    command=convert,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12,
    pady=7
)

convert_button.pack(side="left", padx=4)

swap_button = tk.Button(
    button_frame,
    text="SWAP",
    command=swap,
    bg="#0891b2",
    fg="white",
    font=("Arial", 10, "bold"),
    width=9,
    pady=7
)

swap_button.pack(side="left", padx=4)

clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear,
    bg="#64748b",
    fg="white",
    font=("Arial", 10, "bold"),
    width=9,
    pady=7
)

clear_button.pack(side="left", padx=4)


# ---------------- RESULT ----------------

tk.Label(
    main_frame,
    text="CONVERSION RESULT",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#172554"
).pack(pady=(10, 3))

result_label = tk.Label(
    main_frame,
    text="Your result will appear here",
    font=("Arial", 19, "bold"),
    bg="white",
    fg="#15803d",
    wraplength=450
)

result_label.pack(pady=5)

result_value_label = tk.Label(
    main_frame,
    text="",
    font=("Arial", 10),
    bg="white",
    fg="#475569",
    wraplength=450
)

result_value_label.pack(pady=3)


copy_button = tk.Button(
    main_frame,
    text="COPY RESULT",
    command=copy_result,
    bg="#0f766e",
    fg="white",
    font=("Arial", 9, "bold"),
    padx=10,
    pady=5
)

copy_button.pack(pady=5)


# ---------------- HISTORY ----------------

tk.Label(
    main_frame,
    text="CONVERSION HISTORY",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#172554"
).pack(anchor="w", pady=(12, 5))

history_list = tk.Listbox(
    main_frame,
    height=4,
    font=("Arial", 10)
)

history_list.pack(fill="x", pady=3)

history_button = tk.Button(
    main_frame,
    text="CLEAR HISTORY",
    command=clear_history,
    bg="#dc2626",
    fg="white",
    font=("Arial", 9, "bold")
)

history_button.pack(pady=5)


# ---------------- START APPLICATION ----------------

update_units()

root.bind("<Return>", lambda event: convert())

root.mainloop()
