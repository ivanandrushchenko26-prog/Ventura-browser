import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit,
    QTabWidget, QWidget, QVBoxLayout
)
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView


class BrowserTab(QWidget):
    def __init__(self, url="https://google.com"):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(url))
        self.layout.addWidget(self.webview)


class MacBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ventura")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)

        navbar = QToolBar("Навігація")
        navbar.setMovable(False)
        self.addToolBar(navbar)

        back_btn = QAction("◀", self)
        back_btn.setToolTip("Назад")
        back_btn.triggered.connect(lambda: self.current_webview().back())
        navbar.addAction(back_btn)

        forward_btn = QAction("▶", self)
        forward_btn.setToolTip("Вперед")
        forward_btn.triggered.connect(lambda: self.current_webview().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction("↻", self)
        reload_btn.setToolTip("Оновити сторінку")
        reload_btn.triggered.connect(lambda: self.current_webview().reload())
        navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введіть адресу сайту або пошуковий запит...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        new_tab_btn = QAction("+", self)
        new_tab_btn.setToolTip("Нова вкладка")
        new_tab_btn.triggered.connect(lambda: self.add_new_tab("https://google.com"))
        navbar.addAction(new_tab_btn)

        self.add_new_tab("https://google.com", "Нова вкладка")

    def add_new_tab(self, url="https://google.com", label="Завантаження..."):
        tab = BrowserTab(url)
        index = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(index)

        tab.webview.urlChanged.connect(lambda qurl, browser=tab.webview: self.update_urlbar(qurl, browser))
        tab.webview.titleChanged.connect(lambda title, i=index: self.tabs.setTabText(i, title[:20]))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_webview(self):
        return self.tabs.currentWidget().webview

    def current_tab_changed(self, index):
        if index >= 0:
            qurl = self.current_webview().url()
            self.update_urlbar(qurl, self.current_webview())

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        if "." not in text or " " in text:
            url = f"https://google.com/search?q={text}"
        elif not text.startswith(("http://", "https://")):
            url = "https://" + text
        else:
            url = text

        self.current_webview().setUrl(QUrl(url))

    def update_urlbar(self, qurl, browser=None):
        if browser != self.current_webview():
            return
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MacBrowser()
    window.show()
    sys.exit(app.exec())
