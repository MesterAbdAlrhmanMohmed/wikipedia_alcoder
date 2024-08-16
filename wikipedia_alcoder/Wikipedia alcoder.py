from PyQt6 import QtWidgets as qt
from PyQt6 import QtGui as qt1
from PyQt6 import QtCore as qt2
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import wikipedia,webbrowser,pyperclip,winsound,about,user_guide,dic,article_dialog
import speech_recognition as sr
class Main(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wikipedia AlCoder")
        self.setGeometry(100, 100, 800, 600)
        self.إظهار_اللغات=qt.QLabel("تحديد لغة الإدخال الصوتي")
        self.اللغات=qt.QComboBox()
        self.اللغات.setAccessibleName("تحديد لغة الإدخال الصوتي")
        self.اللغات.addItems(dic.languages.keys())
        self.إظهار_لغات_البحث=qt.QLabel("تحديد لغة البحث")
        self.لغة_البحث=qt.QComboBox()
        self.لغة_البحث.setAccessibleName("تحديد لغة البحث")
        self.لغة_البحث.addItems(dic.languages.keys())
        self.بدء_التحدث=qt.QPushButton("بدء التحدث")
        self.بدء_التحدث.setDefault(True)
        self.بدء_التحدث.clicked.connect(self.start_speech_recognition)
        self.إظهار_البحث=qt.QLabel("أكتب محتوى البحث")
        self.البحث=qt.QLineEdit("")
        self.البحث.setAccessibleName("أكتب محتوى البحث")
        self.بدء_البحث=qt.QPushButton("بدء البحث")
        self.بدء_البحث.setDefault(True)
        self.بدء_البحث.clicked.connect(self.search_wikipedia)
        self.نتائج_البحث=qt.QListWidget()
        self.نتائج_البحث.setAccessibleName("نتائج البحث")
        self.نتائج_البحث.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.نتائج_البحث.customContextMenuRequested.connect(self.show_context_menu)
        self.الدليل=qt.QPushButton("دليل المستخدم")
        self.الدليل.clicked.connect(self.user_guide)
        self.الدليل.setDefault(True)
        self.عن_المطور=qt.QPushButton("عن المطور")
        self.عن_المطور.setDefault(True)
        self.عن_المطور.clicked.connect(self.about)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.إظهار_اللغات)
        layout.addWidget(self.اللغات)
        layout.addWidget(self.بدء_التحدث)
        layout.addWidget(self.إظهار_البحث)
        layout.addWidget(self.البحث)
        layout.addWidget(self.إظهار_لغات_البحث)
        layout.addWidget(self.لغة_البحث)
        layout.addWidget(self.بدء_البحث)
        layout.addWidget(self.نتائج_البحث)
        layout.addWidget(self.الدليل)
        layout.addWidget(self.عن_المطور)
        container=qt.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        qt1.QShortcut("ctrl+o", self).activated.connect(self.VAA)
        qt1.QShortcut("ctrl+b", self).activated.connect(self.VAB)
        qt1.QShortcut("ctrl+l", self).activated.connect(self.CL)
        qt1.QShortcut("ctrl+q", self).activated.connect(lambda: self.البحث.setFocus())
        qt1.QShortcut("ctrl+t", self).activated.connect(self.CT)
    def search_wikipedia(self):
        if not self.البحث.text():
            qt.QMessageBox.warning(self, "تنبيه", "يرجى إدخال نص للبحث")
            return
        self.نتائج_البحث.clear()
        lang=dic.languages[self.لغة_البحث.currentText()]
        self.search_thread=SearchThread(self.البحث.text(), lang)
        self.search_thread.results_signal.connect(self.display_results)
        self.search_thread.start()
    def display_results(self, results):
        self.نتائج_البحث.clear()
        for result in results:
            self.نتائج_البحث.addItem(result)
        self.نتائج_البحث.setFocus()
    def show_context_menu(self, position):
        item=self.نتائج_البحث.itemAt(position)
        if item is None:
            return
        context_menu=qt.QMenu(self)
        view_article_action=context_menu.addAction("عرض المقال في التطبيق")
        view_in_browser_action=context_menu.addAction("عرض المقال في المتصفح")
        copy_link_action=context_menu.addAction("نسخ رابط المقال")
        copy_title_action = context_menu.addAction("نسخ عنوان المقال")        
        view_article_action.triggered.connect(lambda: self.view_article(item.text()))
        view_in_browser_action.triggered.connect(lambda: self.view_in_browser(item.text()))
        copy_link_action.triggered.connect(lambda: self.copy_link(item.text()))
        copy_title_action.triggered.connect(lambda: self.copy_title(item.text()))  # ربط الخيار بدالة نسخ العنوان
        context_menu.exec(qt1.QCursor.pos())
    def view_article(self, title):
        self.article_dialog=article_dialog.ArticleDialog(title)
        self.article_dialog.exec()
    def VAA(self):
        try:
            self.view_article(self.نتائج_البحث.currentItem().text())
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء عرض المقال في التطبيق: {e}")
    def view_in_browser(self, title):
        try:
            url=wikipedia.page(title).url
            webbrowser.open(url)
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء عرض المقال في المتصفح: {e}")
    def VAB(self):
        try:
            self.view_in_browser(self.نتائج_البحث.currentItem().text())
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء عرض المقال في المتصفح: {e}")
    def copy_link(self, title):
        try:
            url=wikipedia.page(title).url
            pyperclip.copy(url)            
            winsound.Beep(1000,100)
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء نسخ رابط المقال: {e}")
    def CL(self):
        try:
            self.copy_link(self.نتائج_البحث.currentItem().text())
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء نسخ رابط المقال: {e}")
    def CT(self):
        try:
            self.copy_title(self.نتائج_البحث.currentItem().text())
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء نسخ عنوان المقال: {e}")
    def copy_title(self, title):
        try:
            pyperclip.copy(title)            
            winsound.Beep(1000,100)
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء نسخ عنوان المقال: {e}")
    def about(self):
        try:
            about.dialog(self).exec()
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء عرض نافذة 'عن المطور': {e}")
    def user_guide(self):
        try:
            user_guide.dialog(self).exec()
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء عرض نافذة دليل المستخدم: {e}")
    def start_speech_recognition(self):
        try:
            self.speech_thread=SpeechRecognitionThread(self.اللغات.currentText())
            self.speech_thread.recognition_finished.connect(self.set_search_text)
            self.speech_thread.start()
        except Exception as e:
            qt.QMessageBox.warning(self, "تنبيه", f"حدث خطأ أثناء بدء التعرف على الكلام: {e}")
    def set_search_text(self, text):
        self.البحث.setText(text)
        self.البحث.setFocus()
class SearchThread(qt2.QThread):
    results_signal=qt2.pyqtSignal(list)
    def __init__(self, query, lang, parent=None):
        super().__init__(parent)
        self.query=query
        self.lang=lang
    def run(self):
        try:
            wikipedia.set_lang(self.lang)
            results=wikipedia.search(self.query)
            self.results_signal.emit(results)
        except Exception as e:
            self.results_signal.emit([f"خطأ: {str(e)}"])
class SpeechRecognitionThread(qt2.QThread):
    recognition_finished=qt2.pyqtSignal(str)
    def __init__(self, language, parent=None):
        super().__init__(parent)
        self.language=dic.languages[language]
        self.player_start=QMediaPlayer()
        self.audio_output_start=QAudioOutput()
        self.player_start.setAudioOutput(self.audio_output_start)
        self.player_start.setSource(qt2.QUrl.fromLocalFile("data/1.wav"))
        self.player_end=QMediaPlayer()
        self.audio_output_end=QAudioOutput()
        self.player_end.setAudioOutput(self.audio_output_end)
        self.player_end.setSource(qt2.QUrl.fromLocalFile("data/2.wav"))
    def run(self):
        recognizer=sr.Recognizer()
        with sr.Microphone() as source:
            self.player_start.play()
            audio_data=recognizer.listen(source)
        try:
            text=recognizer.recognize_google(audio_data, language=self.language)
            self.player_end.play()
            self.recognition_finished.emit(text)
        except sr.UnknownValueError:
            self.recognition_finished.emit("")
        except sr.RequestError as e:
            self.recognition_finished.emit(f"خطأ في الخدمة: {e}")
        except Exception as e:
            self.recognition_finished.emit(f"خطأ غير متوقع: {e}")
app=qt.QApplication([])        
app.setStyle('fusion')
window=Main()
window.show()
app.exec()