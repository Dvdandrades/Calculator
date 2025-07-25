import tkinter as tk
import math

# Font styles and color configurations
SMALL_FONT_STYLE = ("Arial", 16)
LARGE_FONT_STYLE = ("Arial", 40, "bold")
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

TOTAL_COLOR_LABEL = "#F5F5F5"
LABEL_COLOR = "#25265E"

BUTTON_COLOR_DIGITS = "#FFFFFF"
BUTTON_COLOR_OPERATIONS = "#FAF9F6"
EQUAL_BUTTON_COLOR = "#0F52BA"
EQUAL_BUTTON_FG_COLOR = "#FFFFFF"



class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        # Set initial window size based on screen resolution
        screen_width = self.window.winfo_screenmmwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{int(screen_width * 0.75)}x{int(screen_height * 0.6)}")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        # Expressions to display and calculate
        self.total_expression = ""
        self.current_expression = ""

        # Create display area
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        # Digit and operation mappings for button placement
        self.digits = {
            7: (2, 1), 
            8: (2, 2),
            9: (2, 3),
            4: (3, 1),
            5: (3, 2),
            6: (3, 3),
            1: (4, 1),
            2: (4, 2),
            3: (4, 3),
            0: (5, 2),
            ".": (5, 3)
        }
        self.operations = {
            "/": "\u00F7",
            "*": "\u00D7",
            "-": "-",
            "+": "+"
        }

        # Frame to hold all calculator buttons
        self.buttons_frame = self.create_buttons_frame()

        # Configure grid layout for button frame
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # Create all buttons
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

        # Bind keyboard input
        self.bind_keys()

    def bind_keys(self):
        # Keyboard bindings for evaluation, backspace, digits and operators
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.delete())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def change_on_hover(self, button, hover_bg, default_bg):
        # Changes button color on hover
        button.bind("<Enter>", lambda event: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda event: button.config(bg=default_bg))


    def create_special_buttons(self):
        # Creates non-digit and non-operator buttons
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_percentage_button()
        self.create_backspace_button()
        self.create_reciprocal_button()
        self.create_negate_button()

    def create_display_labels(self):
        # Creates the labels to display expressions and results
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=TOTAL_COLOR_LABEL,
                               fg = LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=TOTAL_COLOR_LABEL,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label
    
    def create_display_frame(self):
        # Frame for expression display
        frame = tk.Frame(self.window, height=221, bg=TOTAL_COLOR_LABEL)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value):
        # Adds digits and decimal to the current expression
        if self.current_expression in ["Error", "Can't divide by zero"]:
            self.current_expression = ""

        # Prevents multiple decimals in the same number
        if value == ".":
            parts = self.current_expression.split()
            if parts and "." in parts[-1]:
                return
            
        self.current_expression += str(value)    
        self.update_label()

    def create_digit_buttons(self):
        # Creates digit and decimal buttons
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=BUTTON_COLOR_DIGITS, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
            self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_DIGITS)

    def append_operator(self, operator):
        # Appends operator to the current or total expression
        if self.current_expression in ["Error", "Can't divide by zero"]:
            self.current_expression = ""

        # Prevents invalid expressions starting with * or /
        if not self.current_expression and not self.total_expression:
            if operator in "*/":
                return
        
        # Prevents double operators
        if self.current_expression == "" and self.total_expression:
            if self.total_expression[-1] in self.operations.keys():
                return

        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        # Creates opeator buttons
        i = 1
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            self.change_on_hover(button, "#ececec", BUTTON_COLOR_OPERATIONS)
            i += 1

    def clear(self):
        # Clears all expressions
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        # Clear button
        button = tk.Button(self.buttons_frame, text="C", bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=2, sticky=tk.NSEW)
        self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_OPERATIONS)

    def square(self):
        # Squares the current value
        if self.current_expression:
            try:
                self.current_expression = str(eval(f"{self.current_expression}**2"))
                self.update_label()
            except:
                self.current_expression = "Error"
                self.update_label()

    def create_square_button(self):
        # Square button
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=1, column=2, sticky=tk.NSEW)
        self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_OPERATIONS)

    def sqrt(self):
        # Square root of the current value
        try:
            value = float(self.current_expression)
            if value < 0:
                raise ValueError("Negative square root")
            self.current_expression = str(math.sqrt(value))
        except:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_sqrt_button(self):
        # Square root button
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=1, column=3, sticky=tk.NSEW)
        self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_OPERATIONS)

    def percentage(self):
        # Converts current expression to percentage
        if self.current_expression:
            try:
                self.current_expression = str(eval(f"{self.current_expression}/100"))
                self.update_label()
            except:
                self.current_expression = "Error"
                self.update_label()

    def create_percentage_button(self):
        # Percentage button
        button = tk.Button(self.buttons_frame, text="%", bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.percentage)
        button.grid(row=0, column=1, sticky=tk.NSEW)
        self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_OPERATIONS)

    def reciprocal(self):
        # Reciprocal of the current value
        try:
            value = float(self.current_expression)
            if value == 0:
                raise ZeroDivisionError
            self.current_expression = str(1 / value)
        except ZeroDivisionError:
            self.current_expression = "Can't divide by zero"
        except:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_reciprocal_button(self):
        # Reciprocal button
        button = tk.Button(self.buttons_frame, text="1/x", bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.reciprocal)
        button.grid(row=1, column=1, sticky=tk.NSEW)
        self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_OPERATIONS)

    def negate(self):
        # Negate of the current value
        try:
            if self.current_expression:
                value = float(self.current_expression)
                value *= -1
                if value.is_integer():
                    self.current_expression = str(int(value))
                else:
                    self.current_expression = str(value)
                self.update_label()
        except:
            self.current_expression = "Error"
            self.update_label()

    def create_negate_button(self):
        # Negate button
        button = tk.Button(self.buttons_frame, text="+/-", bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.negate)
        button.grid(row=5, column=1, sticky=tk.NSEW)
        self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_OPERATIONS)

    def evaluate(self):
        # Evaluates the full expression and handles errors
        expression = self.total_expression + self.current_expression
        if not expression:
            return

        if expression[-1] in self.operations.keys():
            self.current_expression = "Error"
            self.total_expression = ""
            self.update_label()
            self.update_total_label()
            return

        try:
            result = str(eval(expression))
            self.current_expression = result
            self.total_expression = ""
        except ZeroDivisionError:
            self.current_expression = "Can't divide by zero"
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()
            self.update_total_label()

    def delete(self):
        # Deletes the last character
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def create_equals_button(self):
        # Equals button
        button = tk.Button(self.buttons_frame, text="=", bg=EQUAL_BUTTON_COLOR, fg=EQUAL_BUTTON_FG_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=5, column=4, sticky=tk.NSEW)
        self.change_on_hover(button, "#0047AB", EQUAL_BUTTON_COLOR)

    def create_backspace_button(self):
        # Backspace button
        button = tk.Button(self.buttons_frame, text="⌫", bg=BUTTON_COLOR_OPERATIONS, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.delete)
        button.grid(row=0, column=3, columnspan=2,  sticky=tk.NSEW)
        self.change_on_hover(button, "#e6e6e6", BUTTON_COLOR_OPERATIONS)

    def create_buttons_frame(self):
        # Frame for buttons
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    
    def update_total_label(self):
        # Updates total expression label
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.total_label.config(text=expression)

    def update_label(self):
        # Updates current expression label
        self.label.config(text=self.current_expression[:11])

    def run(self):
        # Launch the calculator app
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()