import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt


class CalculatorCore:
    def __init__(self):
        self.reset()

    def reset(self):
        self.expression = ''
        self.result = '0'
        self.dot_used = False

    def input_digit(self, digit):
        if self.result == '0' and digit != '.':
            self.result = digit
        else:
            self.result += digit
        self.expression = self.result

    def input_dot(self):
        if not self.dot_used:
            if self.result == '':
                self.result = '0.'
            else:
                self.result += '.'
            self.dot_used = True
            self.expression = self.result

    def add(self):
        self._add_operator('+')

    def subtract(self):
        self._add_operator('-')

    def multiply(self):
        self._add_operator('×')

    def divide(self):
        self._add_operator('÷')

    def _add_operator(self, op):
        if self.result and self.result[-1] not in '+-×÷':
            self.result += op
            self.dot_used = False
            self.expression = self.result

    def negate(self):
        try:
            if self.result.startswith('-'):
                self.result = self.result[1:]
            else:
                self.result = '-' + self.result
            self.expression = self.result
        except:
            self.result = 'Error'

    def percent(self):
        try:
            value = eval(self.result.replace('×', '*').replace('÷', '/'))
            self.result = str(round(value / 100, 6))
            self.expression = self.result
        except:
            self.result = 'Error'

    def equal(self):
        try:
            expr = self.result.replace('×', '*').replace('÷', '/')
            value = eval(expr)
            if isinstance(value, float):
                value = round(value, 6)
            self.result = str(value)
            self.expression = self.result
        except ZeroDivisionError:
            self.result = 'Error'
        except:
            self.result = 'Error'


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('calculator')
        self.setFixedSize(360, 560)
        self.core = CalculatorCore()
        self._create_ui()

    def _create_ui(self):
        main_layout = QVBoxLayout()
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._update_display_style('0')
        main_layout.addWidget(self.display)

        buttons = [
            [('AC', 'light'), ('±', 'light'), ('%', 'light'), ('÷', 'orange')],
            [('7', 'dark'), ('8', 'dark'), ('9', 'dark'), ('×', 'orange')],
            [('4', 'dark'), ('5', 'dark'), ('6', 'dark'), ('-', 'orange')],
            [('1', 'dark'), ('2', 'dark'), ('3', 'dark'), ('+', 'orange')],
            [('0', 'dark'), ('.', 'dark'), ('=', 'orange')],
        ]

        grid = QGridLayout()
        for row, row_buttons in enumerate(buttons):
            col_offset = 0
            for col, (text, color) in enumerate(row_buttons):
                button = QPushButton(text)

                if text == '0':
                    button.setFixedHeight(80)
                    button.setMinimumWidth(160)
                    button.setStyleSheet(
                        'font-size: 24px; background-color: #505050; color: white; border-radius: 40px; text-align: left; padding-left: 30px;')
                    grid.addWidget(button, row, col, 1, 2)
                    col_offset += 1
                else:
                    button.setFixedSize(80, 80)
                    button.setStyleSheet(self._get_button_style(color))
                    grid.addWidget(button, row, col + col_offset)

                button.clicked.connect(lambda _, t=text: self._on_click(t))

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def _get_button_style(self, color):
        styles = {
            'dark': 'background-color: #505050; color: white;',
            'light': 'background-color: #D4D4D2; color: black;',
            'orange': 'background-color: #FF9500; color: white;'
        }
        return f'font-size: 24px; border-radius: 40px; {styles[color]}'

    def _on_click(self, text):
        if text == 'AC':
            self.core.reset()
        elif text == '±':
            self.core.negate()
        elif text == '%':
            self.core.percent()
        elif text == '=':
            self.core.equal()
        elif text == '+':
            self.core.add()
        elif text == '-':
            self.core.subtract()
        elif text == '×':
            self.core.multiply()
        elif text == '÷':
            self.core.divide()
        elif text == '.':
            self.core.input_dot()
        else:
            self.core.input_digit(text)

        self.display.setText(self.core.result)
        self._update_display_style(self.core.result)

    def _update_display_style(self, text):
        length = len(text)
        if length <= 8:
            font_size = 48
        elif length <= 12:
            font_size = 36
        else:
            font_size = 28
        self.display.setStyleSheet(
            f'background-color: black; color: white; font-size: {font_size}px; padding: 30px 20px;')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
