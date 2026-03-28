import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush

RADIUS = 30

class CCircle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False

    def contains(self, point):
        dx = point.x() - self.x
        dy = point.y() - self.y
        return dx*dx + dy*dy <= RADIUS * RADIUS

    def draw(self, painter):
        if self.selected:
            painter.setPen(QPen(Qt.red, 3))
        else:
            painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.lightGray))
        painter.drawEllipse(self.x - RADIUS, self.y - RADIUS, RADIUS * 2, RADIUS * 2)

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.circles = []
        self.setMinimumSize(800, 600)
        self.setFocusPolicy(Qt.StrongFocus)  # ← ВАЖНО: холст может получать фокус

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for circle in self.circles:
            circle.draw(painter)

    def mousePressEvent(self, event):
        self.setFocus()  # ← ВАЖНО: при клике даём фокус холсту
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            ctrl = event.modifiers() & Qt.ControlModifier
            
            hit = None
            for circle in self.circles:
                if circle.contains(pos):
                    hit = circle
                    break
            
            if hit:
                if ctrl:
                    hit.selected = not hit.selected
                else:
                    for circle in self.circles:
                        circle.selected = False
                    hit.selected = True
            else:
                new_circle = CCircle(pos.x(), pos.y())
                self.circles.append(new_circle)
            
            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            # Удаляем выделенные круги
            self.circles = [c for c in self.circles if not c.selected]
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Круги на форме - выделение и удаление")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())