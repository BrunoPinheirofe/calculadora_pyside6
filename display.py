from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from variables import BIG_FONT_SIZE,TEXT_MARGIN, MINIMUM_WIDTH
from utils import isEmpty, isNumOrDot


class Display(QLineEdit):
    
    eqPress = Signal()
    delPress = Signal()
    clearPress = Signal()
    inputPress = Signal(str)
    operatorPress = Signal(str)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
                
    def configStyle(self):
        
        self.setStyleSheet(f'font-size:{BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])
        self.setMinimumWidth(MINIMUM_WIDTH)
        
        
    def keyPressEvent(self, event: QKeyEvent) -> None:
        
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace,KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_Return]
        isOperator = key in [
            KEYS.Key_Plus,
            KEYS.Key_Less,
            KEYS.Key_multiply,
            KEYS.Key_Minus,
            KEYS.Key_Asterisk,
            KEYS.Key_Slash,
            KEYS.Key_P
        ]
        
        
        if isEnter:
            self.eqPress.emit()
            return event.ignore()
        
        elif isDelete:
            self.delPress.emit()
            return event.ignore()
        elif isEsc:
            self.clearPress.emit()
            return event.ignore()
        
        elif isOperator:
            if text.lower().strip() == 'p':
                text = '^'
            self.operatorPress.emit(text)
            return event.ignore()
        
        
        if isEmpty(text):
            event.ignore()
        else:
            if isNumOrDot(text):
                self.inputPress.emit(text)
                return event.ignore()