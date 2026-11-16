import sys
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow

radius = 30
circle_color = QtGui.QColor(52, 195, 235, 255)
outer_circle_color = QtGui.QColor(100, 161, 227, 50)
background_color = QtGui.QColor(255, 255, 255)
distance_outer_inner = 10 # distance between circle and outer circle
starting_offset_x = radius
starting_offset_y = radius
step_x = radius * 4 # how far each space press moves the circle (x)
step_y = radius * 4 # how far each space press moves the circle (y)
touch_count = 3 # how many times the touch should be recorded

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.click = -1
        self.setWindowTitle("My App")
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        self.pos_x = starting_offset_x
        self.pos_y = starting_offset_y

        self.w = 0
        self.h = 0

    def paint_circle(self, event, center_x, center_y, radius, color):
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.painter.setBrush(background_color)
        self.painter.drawRect(event.rect())

        self.painter.setBrush(color)
        center = QPointF(center_x, center_y)
        self.painter.drawEllipse(center, radius, radius)
        self.painter.drawEllipse(center, radius-distance_outer_inner, radius-distance_outer_inner)

    def move_circle(self, new_centerx, new_centery):
        self.pos_x = new_centerx
        self.pos_y = new_centery
        self.update()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.paint_circle(event=event, center_x = self.pos_x, center_y = self.pos_y, radius = radius, color = circle_color)
        self.painter.end()

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key.Key_Space:
            self.click += 1
            key = self.click % 3
            if key == 2: self.pos_x += step_x
            print(str(self.pos_x))
            if self.pos_x >= self.w - radius * 2: # edge of screen
                print("width")
                if self.pos_y >= self.h - radius * 2: #finish
                    # do something
                    print("end")
                    sys.exit()

                self.pos_y += step_y
                self.pos_x = 0
                print("POS: " + str(self.pos_x) + ", " + str(self.pos_y))
                print (str(self.h - radius * 2))

            self.move_circle(self.pos_x, self.pos_y)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.w = self.width()
        self.h = self.height()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())