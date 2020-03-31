"""CalculatorApp

A sample GUI based on the Kivy library that represents a basic calculator application.

The calculator allows for simple operations:

[+]
[-]
[*]
[/]
A solution is received by using the '=' button.

TODO: Update functionality to include parenthesis to control order of operations
TODO: Add new operations such as exponents, square root, factorial, etc
TODO: Add coloring to enhance GUI
TODO: Remove reliance on eval() method to improve security
"""
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class CalculatorApp(App):
    def __init__(self):
        super(CalculatorApp, self).__init__()
        self.operators = ['/', '*', '-', '+']
        self.last_was_operator = None
        self.last_button = None
        self.last_was_solution = None
        self.has_decimal = None
        self.solution = TextInput(
            text='0',
            multiline=False,
            readonly=True,
            halign='right',
            font_size=55
        )

    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.solution)
        buttons = [
            ['7', '8', '9', '+'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '*'],
            ['.', '0', 'C', '/']
        ]
        for rows in buttons:
            h_layout = BoxLayout()
            for label in rows:
                button = Button(
                    text=label,
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text='=',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        # Process button pressed
        if button_text == 'C':
            # Clear input
            new_text = '0'
        elif button_text in self.operators:
            if self.last_was_operator:
                # Overwrite last operator
                new_text = current[:-1] + button_text
            elif self.last_button == '.':
                # Single decimal should be treated as zero
                new_text = current + '0' + button_text
            else:
                # Concatenate the button value to the current value
                new_text = current + button_text
            self.has_decimal = False
        else:
            if button_text == '.':
                if self.has_decimal:
                    # Prevent double decimal points
                    return
                elif self.last_was_solution:
                    # Place a zero before the decimal
                    new_text = '0' + button_text
                else:
                    new_text = current + button_text
                self.has_decimal = True
            elif self.last_was_solution:
                # Replace last solution with new calculation
                new_text = button_text
            elif button_text != '.' and current == '0':
                # Replace zero value with current button value
                new_text = button_text
            else:
                # Concatenate the button value to the current value
                new_text = current + button_text

        self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators
        self.last_was_solution = False

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                solution = str(eval(text))
            except ZeroDivisionError:
                solution = 'Error'
            except SyntaxError:
                solution = '0'
            self.solution.text = solution
            self.last_was_solution = True
            self.has_decimal = False


if __name__ == '__main__':
    # Configure window
    Config.set('graphics', 'width', '300')
    Config.set('graphics', 'height', '400')
    Config.write()

    app = CalculatorApp()
    app.run()
