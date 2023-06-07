# -*- coding: UTF-8 -*-
import os.path

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QPushButton, QGridLayout, QLabel, QFileDialog, QFormLayout, QWidget, \
    QVBoxLayout, QDoubleSpinBox

from info import qa_bot
from utils import load_questions


class FileBox(QGroupBox):
    question_loaded = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FileBox, self).__init__("模型设置", parent=parent)

        # 打开文件
        self.q_file_name = QLineEdit()
        self.open_q_bt = QPushButton("导入问题")

        self.key = QLineEdit("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")
        self.temperature = QDoubleSpinBox()
        self.temperature.setMinimum(0)
        self.temperature.setMaximum(2)
        self.temperature.setSingleStep(0.1)
        self.temperature.setValue(1.0)

        self.link()
        self.setUI()

    def link(self):
        self.open_q_bt.clicked.connect(self.open_q_file)

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("API Key"), 0, 0, 1, 1)
        layout.addWidget(self.key, 1, 0, 1, 3)

        layout.addWidget(QLabel("Temperature"), 2, 0, 1, 1)
        layout.addWidget(self.temperature, 3, 0, 1, 3)

        layout.setHorizontalSpacing(10)
        layout.addWidget(self.q_file_name, 4, 0, 1, 2)
        layout.addWidget(self.open_q_bt, 4, 2, 1, 1)

        self.setLayout(layout)

    def open_q_file(self, default_filename="questions.json"):
        filename = default_filename
        if default_filename and os.path.isfile(filename):
            ...
        else:
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getOpenFileName(self, "Find the question file", "*.json", options=options)
        if filename:
            self.q_file_name.setText(filename)

            self.question_loaded.emit(filename)


class DomainBox(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("专利信息", parent=parent)

        # 标题
        self.title = QLineEdit()
        self.title.setPlaceholderText("标题")

        # 技术领域
        self.domain_1 = QLineEdit()
        self.domain_1.setPlaceholderText("技术领域")
        self.domain_2 = QLineEdit()
        self.domain_2.setPlaceholderText("详细技术领域")

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("标题", self.title)
        layout.addRow("技术领域", self.domain_1)
        layout.addRow("详细技术领域", self.domain_2)

        self.setLayout(layout)

    def set_info(self, title, domain1, domain2):
        if title:
            self.title.setText(title)
        if domain1:
            self.domain_1.setText(domain1)
        if domain2:
            self.domain_2.setText(domain2)


class InfoTab(QWidget):
    warning = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file = FileBox()
        self.domain = DomainBox()

        self.setUI()

        self.file.question_loaded.connect(self.load)

    def load(self, filename):
        load_questions(filename)

        self.set_info()

    def setUI(self):
        layout = QVBoxLayout()

        layout.addWidget(self.file, 1)
        layout.addWidget(self.domain, 3)

        self.setLayout(layout)

    def get_title(self):
        return self.domain.title.text()

    def get_domain(self):
        return self.domain.domain_1.text()

    def get_domain_detail(self):
        return self.domain.domain_2.text()

    def get_temperature(self) -> float:
        return self.file.temperature.value()

    def set_info(self):
        """
        加载配置文件
        :param info:
        :return:
        """

        if title := qa_bot.general_info.get("title"):
            if not isinstance(title, str):
                title = None

        if domain1 := qa_bot.general_info.get("domain"):
            if not isinstance(domain1, str):
                domain1 = None

        if domain2 := qa_bot.general_info.get("domain_detail"):
            if not isinstance(domain2, str):
                domain2 = None

        self.domain.set_info(title, domain1, domain2)

    def get_api_key(self):
        if key := self.file.key.text():
            return key
