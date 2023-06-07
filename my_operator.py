# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QGridLayout, QLabel, QGroupBox, QVBoxLayout, QComboBox

from info import qa_bot
from query import Query
from utils import load_inter_file

query = Query()


class QABox(QGroupBox):
    def __init__(self, box_name: str):
        super().__init__(box_name)
        self.setWindowTitle("QA Viewer")

        self.mutil_qa = False
        self.box_name = box_name

        self.question = QTextEdit()
        self.answer = QTextEdit()

        self.update_bt = QPushButton("保存修改")

        if box_name == "分步骤":
            self.mutil_qa = True
        elif box_name == "总步骤":
            self.mutil_qa = True

        if self.mutil_qa:
            self.qa_selector = QComboBox()

        self.link_signal()
        self.setUI()

    def update_and_show(self):
        try:
            if self.box_name == "技术背景":
                q_text = "\n".join(qa_bot.get_question_by_key("background", []))
                a_text = qa_bot.get_answer_by_key("background", "")
            elif self.box_name == "分步骤":
                self.q_list = [method.get("detail") for method in qa_bot.get_question_by_key("methods", {})]
                self.a_list = ["\n".join(method.get("detail")) for method in qa_bot.get_answer_by_key("methods", {})]
                q_text = self.q_list[0] if self.q_list else ""
                a_text = self.a_list[0] if self.a_list else ""

            elif self.box_name == "总步骤":
                self.q_list = [method.get("total") for method in qa_bot.get_question_by_key("methods", {})]
                self.a_list = [method.get("total") for method in qa_bot.get_answer_by_key("methods", {})]
                q_text = self.q_list[0] if self.q_list else ""
                a_text = self.a_list[0] if self.a_list else ""

            else:
                q_text = qa_bot.get_question_by_key("abstract", "")
                a_text = qa_bot.get_answer_by_key("abstract", "")

            if self.mutil_qa:
                self.qa_selector.clear()
                length = max(len(self.q_list), len(self.a_list))
                for i in range(1, length + 1):
                    self.qa_selector.addItem(f"问答{i}")

            self.question.setPlainText(q_text)
            self.answer.setPlainText(a_text)

            self.show()
        except Exception as e:
            print(e)

    def link_signal(self):
        if self.mutil_qa:
            self.qa_selector.currentIndexChanged.connect(self.changeQA)

        self.update_bt.clicked.connect(self.updateQA)

    def updateQA(self):
        # todo: 将界面修改的内容保存到QA Manager中
        ...

    def changeQA(self, index: int):
        if index < 0:
            return

        print(self.q_list)
        print(self.a_list)

        if index < len(self.q_list):
            self.question.setText(self.q_list[index])
        else:
            self.question.setText("")

        if index < len(self.a_list):
            self.answer.setText(self.a_list[index])
        else:
            self.answer.setText("")

    def setUI(self):
        layout = QVBoxLayout()

        if self.mutil_qa:
            layout.addWidget(self.qa_selector, 1)

        layout.addWidget(self.question)
        layout.addWidget(self.answer)
        layout.addWidget(self.update_bt)

        self.setLayout(layout)


class SingleBox(QGroupBox):
    def __init__(self, box_name, parent=None):
        super(SingleBox, self).__init__(box_name, parent=parent)
        # 背景技术

        self.req_bt = QPushButton("提问")
        self.load_bt = QPushButton("导入")
        self.view_bt = QPushButton("查看问答")

        self.qa_box = QABox(box_name)

        self.link_signal()
        self.setUI()

    def link_signal(self):
        self.view_bt.clicked.connect(self.qa_box.update_and_show)

        self.load_bt.clicked.connect(lambda: load_inter_file("inter_file.txt"))

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(self.req_bt, 0, 0, 1, 1)

        layout.addWidget(self.load_bt, 1, 0, 1, 1)
        layout.addWidget(self.view_bt, 1, 1, 1, 1)

        self.setLayout(layout)


class Operator(QWidget):

    def __init__(self):
        super(Operator, self).__init__()

        self.status_label = QLabel()
        self.box1 = SingleBox("技术背景")
        self.box2 = SingleBox("分步骤")
        self.box3 = SingleBox("总步骤")
        self.box4 = SingleBox("摘要总结")

        self.gen_tex_bt = QPushButton("生成tex文档")
        self.gen_word_bt = QPushButton("生成word文档")

        self.link_signal()

        self.setUI()

    def link_signal(self):
        self.box1.req_bt.clicked.connect(lambda x: self.request(1))
        self.box2.req_bt.clicked.connect(lambda x: self.request(2))
        self.box3.req_bt.clicked.connect(lambda x: self.request(4))
        self.box4.req_bt.clicked.connect(lambda x: self.request(8))

    def request(self, order):
        query.set_order(order)
        query.start()

    def setUI(self):
        layout = QGridLayout()

        layout.addWidget(self.status_label, 0, 0, 1, 4)

        layout.addWidget(self.box1, 1, 0, 1, 4)
        layout.addWidget(self.box2, 2, 0, 1, 4)
        layout.addWidget(self.box3, 3, 0, 1, 4)
        layout.addWidget(self.box4, 4, 0, 1, 4)

        layout.addWidget(self.gen_tex_bt, 5, 0, 1, 2)
        layout.addWidget(self.gen_word_bt, 5, 2, 1, 2)

        self.setLayout(layout)
