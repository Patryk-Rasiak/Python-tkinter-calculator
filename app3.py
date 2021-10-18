import tkinter as tk
from tkinter import ttk
import math
import functools
import random

# Colors for styling
LIGHT_GRAY = "#888"
BLACK = "#363636"
YELLOW = "#ffd900"
YELLOW2 = "#ffe866"
WHITE = "#e3e3e3"
DARK_GRAY = "#545454"


# Decorator function to check if error occurred
def check_errors(func):
    @functools.wraps(func)
    def secure_func(self, *args, **kwargs):
        if self.text.get() == "Error":
            self.blink()
            return

        return func(self, *args, **kwargs)

    return secure_func


class Calculator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Variables

        # Holds the current number
        self.element = "0"
        # Holds first number of operation
        self.first_num = ""
        self.operator = ""

        # Checks whether the next number that is input needs to be replaced or appended
        self.replace = True

        # textvariable of entry widget
        self.text = tk.StringVar(value="0")

        # Checking whether it's scientific form or basic
        self.expanded = False
        self.expand_text = tk.StringVar(value="Scientific")

        self.apply_style()
        self.build()

    def on_button_clicked(self, num):
        if self.replace:

            self.element = num
            if self.element != "0":
                self.replace = False
        else:
            self.element += num

        self.text.set(self.element)

    @check_errors
    def on_operator_clicked(self, operator):
        self.first_num = self.text.get()
        self.operator = operator
        self.replace = True
        self.element = "0"
        self.blink()

    @check_errors
    def on_equal_clicked(self):
        try:
            second_number = self.element
            if self.operator == "√":
                self.operator = "**"
                second_number = 1 / float(second_number)
            result = str(eval(self.first_num + self.operator + second_number))

            self.element = result
            self.text.set(result)
            self.first_num = result
            self.replace = True
            self.blink()
        except ArithmeticError and TypeError:
            self.error()

    def clear(self):
        self.text.set("0")
        self.first_num = ""
        self.replace = True
        self.operator = ""
        self.element = "0"
        self.blink()

    # Method to check the sign (+/-)
    @check_errors
    def sign_change(self):

        if float(self.text.get()) == 0:
            return
        # If a minus is already there, remove it, else insert it at the beginning
        if "-" in self.element:
            self.element.replace("-", "")
        else:
            self.element = "-" + self.element

        self.update_text()

        # If the last character is comma, remove the comma
        try:
            if self.text.get()[-1] == ".":
                self.text.set(self.text.get()[:-1])
        except IndexError:
            self.error()

        self.replace = True
        self.blink()

    # Method to put comma when clicked (On an entry it's actually a dot)
    @check_errors
    def on_comma_clicked(self):
        # Checking whether it does not already exist
        if "." not in self.element:
            self.element += "."
            self.text.set(self.element)

        self.replace = False

    # Method to delete one character
    @check_errors
    def delete(self):
        if len(self.element) == 1:
            self.element = "0"
            self.replace = True

        elif len(self.element) > 1:
            self.element = self.element[:-1]

        self.update_text()

    @check_errors
    def factorial(self):
        try:
            num = int(self.text.get())
            if num >= 0:
                self.element = str(math.factorial(num))
                self.update_text()
                self.replace = True

        except ArithmeticError and TypeError:
            self.error()

    # Method to generate random number between 0 and 1
    def rand(self):
        self.element = random.uniform(0, 1)
        self.update_text()

    @check_errors
    def power(self, exponent):
        try:
            base = float(self.text.get())
            self.element = base ** exponent
            self.update_text()

        except ArithmeticError:
            self.error()

    @check_errors
    def ten_to_x(self):
        self.element = 10 ** float(self.text.get())
        self.update_text()

    @check_errors
    def e_to_x(self):
        self.element = math.e ** float(self.text.get())
        self.update_text()

    @check_errors
    def root(self, exponent):
        try:
            base = float(self.text.get())
            self.element = base ** (1 / exponent)
            self.update_text()

        except ArithmeticError and TypeError:
            self.error()

    # Methods to calculate trigonometric functions
    @check_errors
    def trig_sin(self):
        self.element = math.sin(float(self.text.get()))
        self.update_text()

    @check_errors
    def trig_cos(self):
        self.element = math.cos(float(self.text.get()))
        self.update_text()

    @check_errors
    def trig_tan(self):
        self.element = math.tan(float(self.text.get()))
        self.update_text()

    @check_errors
    def trig_cot(self):
        self.element = 1 / math.tan(float(self.text.get()))
        self.update_text()

    # Methods with constant math variables
    def e(self):
        self.element = math.e
        self.update_text()

    def pi(self):
        self.element = math.pi
        self.update_text()

    # Methods to calculate logarithmic functions
    @check_errors
    def ln(self):
        self.element = math.log(float(self.text.get()))
        self.update_text()

    @check_errors
    def log(self):
        self.element = math.log10(float(self.text.get()))
        self.text.set(self.element)

    # Method to cut off decimal part of a number where possible
    def update_text(self):
        num = float(self.element)
        if int(num) == num:
            self.text.set(int(num))
            return

        self.text.set(self.element)

    # Method to blink a number when buttons are clicked
    def blink(self):
        value = self.text.get()
        self.text.set("")
        self.after(50, lambda: self.text.set(value))

    # Method to show Error and reset variables
    def error(self):
        self.text.set("Error")
        self.replace = True
        self.first_num = ""
        self.operator = ""
        self.element = "0"

    # Method to switch between scientific and basic calculator
    def expand(self):
        if self.expanded:
            self.advanced_buttons_container.grid(column=0)
            self.expanded = False
            self.expand_text.set("Scientific")
        else:
            self.advanced_buttons_container.grid(column=1)
            self.expanded = True
            self.expand_text.set("Basic")

    # Method to create and set widgets at the beginning of the program
    def build(self):

        # Input field

        ttk.Entry(
            self,
            font=("sans-serif", 20),
            textvariable=self.text,
            width=15,
            state="disabled"
        ).grid(row=0, column=0, columnspan=2, sticky="EW")

        # Frames

        self.advanced_buttons_container = ttk.Frame(self)
        self.advanced_buttons_container.grid(row=1, column=0, sticky="NS")

        self.button_container = ttk.Frame(self)
        self.button_container.grid(row=1, column=0)

        '''
        BUTTONS - BASIC
        '''

        # 1st row
        ttk.Button(self.button_container,
                   text="AC",
                   style="Button2.TButton",
                   command=self.clear
                   ).grid(row=0, column=0, columnspan=2)

        ttk.Button(self.button_container,
                   text="DEL",
                   style="Button2.TButton",
                   command=self.delete
                   ).grid(row=0, column=2)

        ttk.Button(self.button_container,
                   text="÷",
                   style="Operator.TButton",
                   command=lambda: self.on_operator_clicked("/")
                   ).grid(row=0, column=3)

        # 2nd row
        ttk.Button(self.button_container,
                   text="7",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("7")
                   ).grid(row=1, column=0)

        ttk.Button(self.button_container,
                   text="8",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("8")
                   ).grid(row=1, column=1)

        ttk.Button(self.button_container,
                   text="9",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("9")
                   ).grid(row=1, column=2)

        ttk.Button(self.button_container,
                   text="x",
                   style="Operator.TButton",
                   command=lambda: self.on_operator_clicked("*")
                   ).grid(row=1, column=3)

        # 3rd row
        ttk.Button(self.button_container,
                   text="4",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("4")
                   ).grid(row=2, column=0)

        ttk.Button(self.button_container,
                   text="5",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("5")
                   ).grid(row=2, column=1)

        ttk.Button(self.button_container,
                   text="6",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("6")
                   ).grid(row=2, column=2)

        ttk.Button(self.button_container,
                   text="-",
                   style="Operator.TButton",
                   command=lambda: self.on_operator_clicked("-")
                   ).grid(row=2, column=3)

        # 4th row
        ttk.Button(self.button_container,
                   text="1",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("1")
                   ).grid(row=3, column=0)

        ttk.Button(self.button_container,
                   text="2",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("2")
                   ).grid(row=3, column=1)

        ttk.Button(self.button_container,
                   text="3",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("3")
                   ).grid(row=3, column=2)

        ttk.Button(self.button_container,
                   text="+",
                   style="Operator.TButton",
                   command=lambda: self.on_operator_clicked("+")
                   ).grid(row=3, column=3)

        # 5th row
        ttk.Button(self.button_container,
                   text="0",
                   style="Button.TButton",
                   command=lambda: self.on_button_clicked("0")
                   ).grid(row=4, column=0,
                          columnspan=2)
        ttk.Button(self.button_container,
                   text=",",
                   style="Button.TButton",
                   command=self.on_comma_clicked
                   ).grid(row=4, column=2)

        ttk.Button(self.button_container,
                   text="=",
                   style="Operator.TButton",
                   command=self.on_equal_clicked
                   ).grid(row=4, column=3)

        # 6th row
        ttk.Button(self,
                   textvariable=self.expand_text,
                   style="Button2.TButton",
                   takefocus=False,
                   command=self.expand,
                   width=10
                   ).grid(row=2, pady=7, ipady=0, sticky="W", padx=10)

        '''
        BUTTONS - SCIENTIFIC
        '''

        # 1st row
        ttk.Button(self.advanced_buttons_container,
                   text="+/-",
                   command=self.sign_change
                   ).grid(row=0, column=0)

        ttk.Button(self.advanced_buttons_container,
                   text="1/x",
                   command=lambda: self.power(-1)
                   ).grid(row=0, column=1)

        ttk.Button(self.advanced_buttons_container,
                   text="x!",
                   command=self.factorial
                   ).grid(row=0, column=2)

        ttk.Button(self.advanced_buttons_container,
                   text="Rand",
                   command=self.rand
                   ).grid(row=0, column=3)

        # 2nd row
        ttk.Button(self.advanced_buttons_container,
                   text="x²",
                   command=lambda: self.power(2)
                   ).grid(row=1, column=0)

        ttk.Button(self.advanced_buttons_container,
                   text="x³",
                   command=lambda: self.power(3)
                   ).grid(row=1, column=1)

        ttk.Button(self.advanced_buttons_container,
                   text="xʸ",
                   command=lambda: self.on_operator_clicked("**")
                   ).grid(row=1, column=2)

        ttk.Button(self.advanced_buttons_container,
                   text="10ˣ",
                   command=self.ten_to_x
                   ).grid(row=1, column=3)

        # 3rd row
        ttk.Button(self.advanced_buttons_container,
                   text="√x",
                   command=lambda: self.root(2)
                   ).grid(row=2, column=0)

        ttk.Button(self.advanced_buttons_container,
                   text="³√x",
                   command=lambda: self.root(3)
                   ).grid(row=2, column=1)

        ttk.Button(self.advanced_buttons_container,
                   text="ʸ√x",
                   command=lambda: self.on_operator_clicked("√")
                   ).grid(row=2, column=2)

        ttk.Button(self.advanced_buttons_container,
                   text="eˣ",
                   command=self.e_to_x
                   ).grid(row=2, column=3)

        # 4th row
        ttk.Button(self.advanced_buttons_container,
                   text="sin",
                   command=self.trig_sin
                   ).grid(row=3, column=0)

        ttk.Button(self.advanced_buttons_container,
                   text="cos",
                   command=self.trig_cos
                   ).grid(row=3, column=1)

        ttk.Button(self.advanced_buttons_container,
                   text="tan",
                   command=self.trig_tan
                   ).grid(row=3, column=2)

        ttk.Button(self.advanced_buttons_container,
                   text="cot",
                   command=self.trig_cot
                   ).grid(row=3, column=3)

        # 5th row
        ttk.Button(self.advanced_buttons_container,
                   text="e",
                   command=self.e
                   ).grid(row=4, column=0)

        ttk.Button(self.advanced_buttons_container,
                   text="π",
                   command=self.pi
                   ).grid(row=4, column=1)

        ttk.Button(self.advanced_buttons_container,
                   text="ln",
                   command=self.ln
                   ).grid(row=4, column=2)

        ttk.Button(self.advanced_buttons_container,
                   text="log",
                   command=self.log
                   ).grid(row=4, column=3)

        # Settings for buttons
        for child in self.button_container.winfo_children():
            child.grid_configure(ipady=10, sticky="NSEW")
            child.configure(takefocus=False)
        for child in self.advanced_buttons_container.winfo_children():
            child.grid_configure(ipady=10, sticky="NSEW")
            child.configure(style="Button.TButton", takefocus=False)

    # Method to create styles for elements of the calculator
    def apply_style(self):

        style = ttk.Style(self)
        style.theme_use("clam")
        self["background"] = BLACK

        # Buttons Style

        style.configure("TButton", width=5)

        style.configure("Button.TButton",
                        background=DARK_GRAY,
                        foreground=WHITE,
                        bordercolor=DARK_GRAY,
                        lightcolor=LIGHT_GRAY
                        )
        style.map("Button.TButton",
                  foreground=[
                      ("pressed", "white"),
                      ("active", WHITE)],
                  background=[
                      ("pressed", "!focus", LIGHT_GRAY),
                      ("active", "#999")],
                  relief=[("pressed", "groove"),
                          ("!pressed", "ridge")])

        style.configure("Button2.TButton",
                        background=LIGHT_GRAY,
                        foreground=WHITE,
                        bordercolor="#676767",
                        lightcolor="#808080"
                        )
        style.map("Button2.TButton",
                  foreground=[("pressed", BLACK), ("active", DARK_GRAY)]
                  )

        style.configure("Operator.TButton",
                        background=YELLOW,
                        foreground=DARK_GRAY,
                        highlightthickness="10",
                        width=5,
                        bordercolor="#676767",
                        lightcolor="#bababa"
                        )
        style.map("Operator.TButton",
                  foreground=[
                      ("pressed", BLACK),
                      ("active", BLACK)],
                  background=[
                      ("pressed", "!focus", YELLOW),
                      ("active", YELLOW2)],
                  relief=[("pressed", "groove"),
                          ("!pressed", "ridge")])

        # Entry Style

        style.configure("TEntry",
                        padding="5 15 5 15",
                        fieldbackground=BLACK,
                        bordercolor=BLACK,
                        lightcolor=BLACK
                        )
        style.map(
            "TEntry",
            foreground=[("disabled", WHITE)]
        )


root = Calculator()
root.title("Calculator")
root.resizable(False, False)
root.mainloop()
