from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
class dialog(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.showFullScreen()
        self.setWindowTitle("دليل المستخدم")
        self.الدليل=qt.QListWidget()
        self.الدليل.addItem("إختصارات النافذة الرئسية")
        self.الدليل.addItem("CTRL+Q الانتقال سريعا الى مربع البحث")
        self.الدليل.addItem("CTRL+L نسخ رابط المقال")
        self.الدليل.addItem("CTRL+O عرض المقال في التطبيق")
        self.الدليل.addItem("CTRL+B عرض المقال في المتصفح")
        self.الدليل.addItem("إختصارات نافذة عرض المقال")
        self.الدليل.addItem("CTRL+C نسخ سطر من المقال")
        self.الدليل.addItem("CTRL+A نسخ المقال كاملا")        
        self.الدليل.addItem("CTRL+P طباعة المقال")
        self.الدليل.addItem("CTRL+S حفظ المقال كمستند نصي")
        l=qt.QVBoxLayout(self)
        l.addWidget(self.الدليل)                