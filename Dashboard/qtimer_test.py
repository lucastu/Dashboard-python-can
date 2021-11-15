from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
import sys
 
def Bluetooth_reading_loop():
    print("bluetooth reading")
 
app = QApplication(sys.argv)
win = QMainWindow()
  
# Create a timer that execute Bluetooth_reading_loop function every 500ms
# Better than a while True : Loop 
Bluetooth_timer = QtCore.QTimer()
Bluetooth_timer.timeout.connect(Bluetooth_reading_loop)
Bluetooth_timer.start(500)
 
win.show()
sys.exit(app.exec_())
