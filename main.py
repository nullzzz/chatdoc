# -*- coding: UTF-8 -*-
import os.path
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTabWidget

from general import InfoTab
from info import sep, qa_bot
from picture import Picture
from query import Query
from my_operator import Operator


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatDoc v0.04")

        self.general = InfoTab()
        self.operator = Operator()
        self.picture = Picture()
        self.query = Query()

        self.setUI()
        self.link()

    def link(self):
        """
        链接QT中的信号与槽函数，即UI事件（如按钮点击）与对应的处理函数
        可参考QT文档
        :return:
        """
        self.general.warning.connect(self.warning)

        self.operator.gen_tex_bt.clicked.connect(self.generate_tex)
        self.operator.gen_word_bt.clicked.connect(self.generate_word)

        self.picture.update_bt.clicked.connect(self.update_inter_file)

    #
    def update_inter_file(self, filename="inter_file.txt"):
        """
        将UI界面上调整后的内容更新到中间文件
        :return:
        """

        background = qa_bot.get_answer_by_key("background", "")
        methods_str = qa_bot.get_answer_by_key("methods_string", "")
        abstract = qa_bot.get_answer_by_key("abstract", "")
        steps = self.picture.get_new_steps()

        all_list = (background, methods_str, abstract)

        with open(filename, "w", encoding="utf-8") as file:

            for ele in all_list:
                file.write(ele)
                file.write("\n")
                file.write(sep)
                file.write("\n")

            for step in steps:
                step: dict
                caption = step["caption"]
                text = step["text"]
                if isinstance(text, list):
                    text = "\n".join(text)
                file.write(f"{caption}\n{text}\n\n")

    #
    def request(self, order):
        if self.check_api():
            temperature = self.general.get_temperature()
            self.query.set_temperature(temperature)

            self.query.set_temperature(temperature)
            self.query.set_order(order)
            self.query.start()

    def setUI(self):
        tab = QTabWidget()
        tab.addTab(self.general, "文档设置")
        tab.addTab(self.operator, "生成")
        tab.addTab(self.picture, "附图调整")

        self.setCentralWidget(tab)

    def check_api(self):
        if os.environ.get("OPENAI_API_KEY") is None:
            if (key := self.general.get_api_key()) is None:
                self.warning("缺少API KEY")
                return False
            os.environ["OPENAI_API_KEY"] = key
        op
        return True

    def generate_picture(self):
        """
        生成说明书附图
        :param methods:
        :return:
        """
        self.picture.add_pictures(qa_bot.get_picture_steps())
        self.picture.generate_all_pictures()

    def warning(self, warning_info):
        """
        弹出提示框
        :param warning_info:
        :return:
        """
        msg = QMessageBox()
        msg.addButton(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setText("确定")

        msg.warning(self, "警告", warning_info)

    def generate_tex(self):
        """
        根据回答生成
        档
        :return:
        """
        with open("template.tex", encoding="utf-8") as file:
            temp = file.read()

        title = qa_bot.general_info.get("title", "")
        domain = qa_bot.general_info.get("domain", "")
        domain_detail = qa_bot.general_info.get("domain_detail", "")

        background = qa_bot.get_answer_by_key("background", "【内容缺失】")

        abstract = qa_bot.get_answer_by_key("abstract", "【内容缺失】")
        effect = qa_bot.get_answer_by_key("effect", "【内容缺失】")
        overall = qa_bot.get_answer_by_key("overall", "【内容缺失】")

        method_str: str = qa_bot.get_methods_str()

        try:
            picture_str = qa_bot.parse_methods()
            self.generate_picture()

            picture_tip_list = []
            for idx, step in enumerate(self.picture.get_new_steps()):
                caption = step["caption"]
                picture_tip_list.append(f"图{idx + 1}为本发明实施例中{caption}；")
            picture_tip = "\n\n".join(picture_tip_list)

            requirement: str = qa_bot.parse_requirement()
            example: str = qa_bot.parse_example()

            # 模板填空
            temp = temp.replace("【标题】", title)
            temp = temp.replace("【领域】", domain)
            temp = temp.replace("【详细领域】", domain_detail)

            temp = temp.replace("【方法】", title)
            temp = temp.replace("【摘要】", abstract)
            temp = temp.replace("【步骤】", method_str)
            temp = temp.replace("【权利要求书】", requirement)
            temp = temp.replace("【实施例】", example)

            temp = temp.replace("【有益效果】", effect)
            temp = temp.replace("【综上所述】", overall)

            temp = temp.replace("【背景技术】", background)
            temp = temp.replace("【其他图片】", picture_str)
            temp = temp.replace("【附图说明】", picture_tip)
        except Exception as error:
            print(type(error))
            print(error)
        with open(f"{title}.tex", "w", encoding="utf-8") as writer:
            writer.write(temp)
        print(f"生成tex文档完成: {title}.tex")

    def generate_word(self):
        print("生成word文档")
        title = self.general.get_title()
        ret = os.system(f"pandoc -s {title}.tex -o {title}.docx")

        print(f"pandoc -s {title}.tex -o {title}.docx")
        print(ret)
        print(f"生成word文档完成：{title}.docx")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
