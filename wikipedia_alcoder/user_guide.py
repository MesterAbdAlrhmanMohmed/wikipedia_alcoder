from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
class dialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.showFullScreen()
        self.setWindowTitle("دليل المستخدم")
        self.الدليل=qt.QListWidget()
        self.الدليل.addItem("CTRL+Q الانتقال سريعا الى مربع البحث")
        self.الدليل.addItem("L نسخ رابط المقال")
        self.الدليل.addItem("O عرض المقال في التطبيق")
        self.الدليل.addItem("B عرض المقال في المتصفح")
        self.الدليل.addItem("C نسخ سطر من المقال")
        self.الدليل.addItem("A نسخ المقال كاملا")        
        self.الدليل.addItem("P طباعة المقال")
        self.الدليل.addItem("S حفظ المقال كمستند نصي")
        l=qt.QVBoxLayout(self)
        l.addWidget(self.الدليل)                