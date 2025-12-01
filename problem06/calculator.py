import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel
)
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('calculator')  
        self.setFixedSize(360, 560)        
        self.expression = ''              
        self._create_ui()                  

    def _create_ui(self):
        main_layout = QVBoxLayout()  # 전체 수직 레이아웃 생성

        # 화면 표시 영역 (라벨)
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet(
            'background-color: black; color: white; font-size: 48px; padding: 30px 20px;')
        main_layout.addWidget(self.display)

        # 버튼 구성 (텍스트, 스타일)
        buttons = [
            [('AC', 'light'), ('±', 'light'), ('%', 'light'), ('÷', 'orange')],
            [('7', 'dark'), ('8', 'dark'), ('9', 'dark'), ('×', 'orange')],
            [('4', 'dark'), ('5', 'dark'), ('6', 'dark'), ('-', 'orange')],
            [('1', 'dark'), ('2', 'dark'), ('3', 'dark'), ('+', 'orange')],
            [('0', 'dark'), ('.', 'dark'), ('=', 'orange')],
        ]

        grid = QGridLayout()  # 버튼 그리드 레이아웃

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
        # 버튼 클릭 이벤트 처리 함수
        
        if text == 'AC':
            self.expression = ''
            self.display.setText('0')

        elif text == '±':  # ± == ±
            if self.expression:
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
                self.display.setText(self.expression)

        elif text == '%':
            try:
                self.expression = str(eval(self.expression) / 100)
                self.display.setText(self.expression)
            except:
                self.display.setText('Error')
                self.expression = ''

        elif text == '=':
            try:
                # × ÷ → * /
                expr = self.expression.replace('×', '*').replace('÷', '/')
                result = eval(expr)
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText('Error')
                self.expression = ''

        else:
            # 숫자나 연산자 입력 처리
            if self.display.text() == '0' and text not in ['+', '-', '×', '÷', '.']:
                self.expression = text
            else:
                self.expression += text
            self.display.setText(self.expression)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
