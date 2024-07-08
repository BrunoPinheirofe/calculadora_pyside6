from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from PySide6.QtGui import QIcon
from variables import WINDOW_ICON_PATH
from display import Display
from info import Info
from buttons import ButtonsGrid
import styles


if __name__ == "__main__":
    # config padrao
    app = QApplication()
    styles.setupTheme()
    window = MainWindow()
    styles.setupTheme()

    # set icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # config info
    info = Info("???")
    window.addWidgetToVLayout(info)

    # config display
    display = Display()
    window.addWidgetToVLayout(display)

    # config grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    window.ajustFixedSize()
    window.show()
    app.exec()
