import os
import sys
import time
# 获取PyQt5的platforms插件路径
import PyQt5.QtCore
from PyQt5 import QtWidgets, QtGui, QtCore
platforms_path = r"C:\Users\98039\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyQt5\Qt\plugins\platforms"

plugin_path = os.path.join(os.path.dirname(PyQt5.QtCore.__file__), 'plugins', 'platforms')
# 设置环境变量
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class PearlWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(150, 300)  # 根据图片调整大小
        self.load_ui()
        self.setup_timers()
        self.start_animation()

    def load_ui(self):
        # 加载绘梨衣图片
        self.pixmap = QtGui.QPixmap("pearl.png")
        self.label_image = QtWidgets.QLabel(self)
        self.label_image.setPixmap(self.pixmap)
        self.label_image.setGeometry(0, 0, self.width(), self.height())

        # 显示时间的标签
        self.time_label = QtWidgets.QLabel(self)
        self.time_label.setStyleSheet("color: white; font-size: 14px; background: transparent;")
        self.time_label.setGeometry(10, 10, 130, 20)
        self.update_time()

    def setup_timers(self):
        # 更新时间
        self.timer_time = QtCore.QTimer()
        self.timer_time.timeout.connect(self.update_time)
        self.timer_time.start(1000)

        # 走动动画
        QtCore.QTimer.singleShot(1000, self.start_movement)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.time_label.setText(current_time)

    def start_movement(self):
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        y_pos = QtWidgets.QApplication.desktop().screenGeometry().height() - self.height() - 50  # 右下角偏上50像素

        start_x = screen_width
        end_x = screen_width - self.width() * 1.25  # 约四分之一个屏幕距离

        self.move(start_x, y_pos)

        self.anim = QtCore.QPropertyAnimation(self, b"pos")
        self.anim.setDuration(3000)
        self.anim.setStartValue(QtCore.QPoint(start_x, y_pos))
        self.anim.setEndValue(QtCore.QPoint(end_x, y_pos))
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.anim.finished.connect(self.move_back)
        self.anim.start()

    def move_back(self):
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        y_pos = self.y()

        end_x = screen_width
        start_x = self.x()

        self.anim_back = QtCore.QPropertyAnimation(self, b"pos")
        self.anim_back.setDuration(3000)
        self.anim_back.setStartValue(QtCore.QPoint(start_x, y_pos))
        self.anim_back.setEndValue(QtCore.QPoint(end_x, y_pos))
        self.anim_back.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.anim_back.start()

    def mousePressEvent(self, event):
        # 判断是否点击在“口袋”区域（假设在图片右下角区域）
        x, y = event.x(), event.y()
        if x > self.width() * 0.8 and y > self.height() * 0.8:
            # 显示系统状态栏信息
            self.show_system_status()

    def show_system_status(self):
        # 弹出系统信息窗口
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("系统状态")
        msg.setText("系统正常运行。")  # 简单示例，可以扩展为实际信息
        msg.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)

    # 创建窗口实例
    pearl = PearlWidget()
    # 设置位置在右下角
    screen_geom = QtWidgets.QApplication.desktop().availableGeometry()
    y_pos = screen_geom.height() - pearl.height() - 50
    pearl.move(screen_geom.width(), y_pos)  # 在屏幕最右边外面开始

    pearl.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()