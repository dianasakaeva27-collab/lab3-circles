import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

# Радиус круга (постоянный для всех кругов)
RADIUS = 30


# ========== КЛАСС КРУГА ==========
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
            painter.setPen(QPen(Qt.red, 4))
            painter.setBrush(QBrush(QColor(255, 240, 100)))
        else:
            painter.setPen(QPen(QColor(0, 0, 100), 2))
            painter.setBrush(QBrush(QColor(100, 150, 255)))
        painter.drawEllipse(self.x - RADIUS, self.y - RADIUS, RADIUS * 2, RADIUS * 2)


# ========== КЛАСС ХОЛСТА ==========
class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.circles = []
        self.setMinimumSize(800, 600)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet("background-color: #e0e0e0;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for circle in self.circles:
            circle.draw(painter)

    def mousePressEvent(self, event):
        self.setFocus()

        if event.button() == Qt.LeftButton:
            pos = event.pos()
            ctrl = event.modifiers() & Qt.ControlModifier

            # Собираем ВСЕ круги, которые содержат точку клика
            hit_circles = []
            for circle in self.circles:
                if circle.contains(pos):
                    hit_circles.append(circle)

            if hit_circles:
                # Попали в один или несколько кругов (пересечение)
                if ctrl:
                    # Ctrl + клик: переключаем выделение для каждого задетого круга
                    for circle in hit_circles:
                        circle.selected = not circle.selected
                else:
                    # Обычный клик: снимаем выделение со всех, выделяем только задетые
                    for circle in self.circles:
                        circle.selected = False
                    for circle in hit_circles:
                        circle.selected = True
            else:
                # Клик по пустому месту
                if ctrl:
                    # Ctrl + клик на пустом месте: выделяем ВСЕ круги
                    for circle in self.circles:
                        circle.selected = True
                else:
                    # Обычный клик на пустом месте: создаём новый круг
                    new_circle = CCircle(pos.x(), pos.y())
                    self.circles.append(new_circle)

            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.circles = [c for c in self.circles if not c.selected]
            self.update()


# ========== ГЛАВНОЕ ОКНО ==========
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Круги на форме - выделение и удаление")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)


# ========== ТОЧКА ВХОДА ==========
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())