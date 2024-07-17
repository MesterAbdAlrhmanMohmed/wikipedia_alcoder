from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
import wikipedia,pyperclip,nltk
nltk.download('punkt')
class ArticleDialog(qt.QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.showFullScreen()
        self.article_content=qt.QListWidget()
        layout=qt.QVBoxLayout()
        layout.addWidget(self.article_content)
        self.setLayout(layout)
        self.load_thread=LoadArticleThread(title)
        self.load_thread.update_signal.connect(self.add_paragraph)
        self.load_thread.start()
        self.article_content.setFocus()
        qt1.QShortcut("c", self).activated.connect(self.copy_line)
        qt1.QShortcut("a", self).activated.connect(self.copy_article)        
    def add_paragraph(self, paragraph):
        for line in split_into_lines(paragraph, 200):
            self.article_content.addItem(line)
    def copy_line(self):
        try:
            current_item=self.article_content.currentItem()
            if current_item:
                pyperclip.copy(current_item.text())
                qt.QMessageBox.information(self, "تم", "تم نسخ سطر من المقال بنجاح")
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_article(self):
        try:
            article_text="\n".join(self.article_content.item(i).text() for i in range(self.article_content.count()))
            pyperclip.copy(article_text)
            qt.QMessageBox.information(self, "تم", "تم نسخ المقال بنجاح")
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))    
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
def split_into_lines(paragraph, max_length):
    words=paragraph.split()
    lines=[]
    current_line=""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line+=(word + " ")
        else:
            lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)
    return lines