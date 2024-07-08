from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import isEmpty, isNumOrDot, isValidNumber, convertToIntOrFloat
from display import Display
from info import Info
import math


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow
    
    


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info,window: 'MainWindow', *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = "Sua conta fica aqui"
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equation
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):

        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPress.connect(self._eq)
        self.display.delPress.connect(self._backspace)
        self.display.clearPress.connect(self._clear)
        self.display.inputPress.connect(self._insertToDisplay)
        self.display.operatorPress.connect(self._configLeftOp)
        
        for row_number, row in enumerate(self._grid_mask):

            for column_number, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                self.addWidget(button, row_number, column_number)

                slot = self._makeSlot(self._insertToDisplay, buttonText)

                self._conectButtonClicked(button, slot)

    def _conectButtonClicked(self, button: Button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button: Button):
        text = button.text()

        if text == "C":
            self._conectButtonClicked(button, self._clear)
        if text == "N":
            self._conectButtonClicked(button, self._invertNumber)
            
        if text == '◀':
            self._conectButtonClicked(button, self.display.backspace)
        
        if text in "+-*/^":
            self._conectButtonClicked(
                button, self._makeSlot(self._configLeftOp, text)
            )
        if text == "=":
            self._conectButtonClicked(button, self._eq)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return

        newNumber = convertToIntOrFloat(displayText) *-1
        self.display.setText(str(newNumber))
        
    def _insertToDisplay(self, text):
        newDisplay = self.display.text() + text

        if not isValidNumber(newDisplay):
            return

        self.display.setText(newDisplay)
        self.display.setFocus()

    def _clear(self):
        self.display.clear()
        self.equation = ""
        self._left = None
        self._right = None
        self._op = None
        self.display.setFocus()

    def _configLeftOp(self, text):
        
        displayText = self.display.text()
        self.display.clear()
        
        if not isValidNumber:
            self._showError('Você não digitou nada')
            
        if self._left is None:
            self._left = convertToIntOrFloat(displayText)
    
        self._op = text
        self.equation = f"{self._left} {self._op}"
        self.display.setFocus()

    @Slot()
    def _eq(self):
        displayText = self.display.text()
        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta Incompleta')
            return
        self._right = convertToIntOrFloat(displayText)
        self.equation = f"{self._left} {self._op} {self._right}"
        result: float| int | str = "error"
        try:
            if "^" in self.equation and isinstance(self._left, float|int):
                result = math.pow(self._left, self._right)
                result = convertToIntOrFloat(str(result))
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Divisão por Zero')
        except OverflowError:
            self._showError('Error: Numero Muito Grande')

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self._left = result
        self._right = None

        if result == "error":
            self._left = None
        self.display.setFocus()
            
    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox
    
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()
    
    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()
        
    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information) 
        msgBox.exec()
        self.display.setFocus()
