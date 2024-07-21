from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from PyQt6.QtCore import QEvent, Qt, QLocale
from PyQt6.QtGui import QKeyEvent, QTextCursor
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import wikipedia, pyperclip, nltk
nltk.download('punkt')
class ArticleDialog(qt.QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.showFullScreen()
        self.article_content=qt.QTextEdit()
        self.article_content.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard | Qt.TextInteractionFlag.TextSelectableByMouse)
        self.article_content.setLineWrapMode(qt.QTextEdit.LineWrapMode.NoWrap)
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.article_content.setFont(font)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.article_content)
        self.setLayout(layout)
        self.load_thread=LoadArticleThread(title)
        self.load_thread.update_signal.connect(self.add_paragraph)
        self.load_thread.start()
        self.article_content.setFocus()
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_article)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_article)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_article_as_txt)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
    def add_paragraph(self, paragraph):
        self.article_content.append(paragraph)
        self.article_content.moveCursor(QTextCursor.MoveOperation.Start)
    def copy_line(self):
        try:
            cursor=self.article_content.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)
                qt.QMessageBox.information(self, "تم", "تم نسخ سطر من المقال بنجاح")
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_article(self):
        try:
            article_text=self.article_content.toPlainText()
            pyperclip.copy(article_text)
            qt.QMessageBox.information(self, "تم", "تم نسخ المقال بنجاح")
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def print_article(self):
        try:
            printer=QPrinter()
            dialog=QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.article_content.print_(printer)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def save_article_as_txt(self):
        try:
            file_dialog=qt.QFileDialog()
            file_dialog.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")
            file_dialog.setDefaultSuffix("txt")
            if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
                file_name=file_dialog.selectedFiles()[0]
                with open(file_name, 'w', encoding='utf-8') as file:
                    article_text = self.article_content.toPlainText()
                    file.write(article_text)                
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def increase_font_size(self):
        self.font_size += 1
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
        self.update_font_size()
    def update_font_size(self):
        cursor=self.article_content.textCursor()
        self.article_content.selectAll()
        font=self.article_content.font()
        font.setPointSize(self.font_size)
        self.article_content.setCurrentFont(font)        
        self.article_content.setTextCursor(cursor)
class LoadArticleThread(qt2.QThread):
    update_signal=qt2.pyqtSignal(str)
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title=title
    def run(self):
        try:
            page=wikipedia.page(self.title)
            paragraphs=nltk.tokenize.sent_tokenize(page.content)
            for paragraph in paragraphs:
                self.update_signal.emit(paragraph)
        except Exception as e:
            self.update_signal.emit(f"خطأ: {str(e)}")