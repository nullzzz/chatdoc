# -*- coding: UTF-8 -*-
import os

import openai
from PyQt5.QtCore import QThread, pyqtSignal

from chat import ChatBot
from info import qa_bot

"""
提问不做校验
"""


class Query(QThread):
    # 回答信号
    q_answered = pyqtSignal(str)
    # 提问信号
    requested = pyqtSignal(str)
    # 警告信号
    warning = pyqtSignal(str)
    # 提示信号
    tip = pyqtSignal(str)

    over = pyqtSignal(int)

    def __init__(self):
        super(Query, self).__init__()
        self.question: dict = {}

        self.temperature: float = 1.0
        # 加载模型
        if os.environ.get("OPENAI_API_KEY"):
            self.bot = ChatBot(self.temperature)
        else:
            self.bot = None

        # 1 -> 技术背景
        # 2 -> 分步骤
        # 4 -> 总步骤
        # 8 -> 摘要
        # 16 -> 附图
        self.request_order = 0

    def set_temperature(self, temperature: float):
        self.temperature = temperature
        if self.bot:
            self.bot.set_temperature(temperature)

    def request_1(self):
        if questions := qa_bot.get_question_by_key("background"):
            self.tip.emit("背景技术提问...")
            back_answer = []
            for question in questions:
                self.requested.emit(question)

                answer: str = self.bot.q_single(question)
                back_answer.append(answer)

                self.q_answered.emit(answer)
            qa_bot.update_answer_by_key("background", "\n\n".join(back_answer))

    def request_2(self):
        if questions := qa_bot.get_question_by_key("methods"):
            self.tip.emit("技术方案提问...")
            methods = []
            for idx, question in enumerate(questions):
                detail_answer = []
                if detail := question.get("detail"):
                    self.requested.emit(detail)
                    detail_answer: list = self.bot.q_method(detail)
                    self.q_answered.emit("\n".join(detail_answer))

                methods.append({"detail": detail_answer})

            qa_bot.update_detail_answer(methods)

    def request_4(self):
        if questions := qa_bot.get_question_by_key("methods"):
            self.tip.emit("技术方案提问...")
            methods = []
            for idx, question in enumerate(questions):
                total_answer = "回答出错"
                if total := question.get("total"):
                    self.requested.emit(total)
                    total_answer: str = self.bot.q_single(total)

                # singleton_answers.setdefault("methods", [])[idx]["total"] = total_answer
                methods.append({"total": total_answer})

            qa_bot.update_total_answer(methods)

    def request_8(self):
        if question := qa_bot.get_question_by_key("abstract"):
            self.requested.emit(question)
            self.tip.emit("说明书提问...")

            answer = self.bot.q_single(question)
            qa_bot.update_answer_by_key("abstract", answer)
            self.q_answered.emit(answer)

        if question := qa_bot.get_question_by_key("overall"):
            self.requested.emit(question)
            self.tip.emit("综上所述提问...")
            answer: str = self.bot.q_single(question)
            qa_bot.update_answer_by_key("overall", answer)
            self.q_answered.emit(answer)

    def request_16(self):
        if questions := qa_bot.get_question_by_key("steps"):
            self.tip.emit("技术方案提问...")
            for idx, question in enumerate(questions):
                new_step = self.bot.q_single(question)
                # todo

    def set_order(self, order):
        self.request_order = order

    def run(self):
        # 检查API
        if self.bot is None:
            key = os.environ.get("OPENAI_API_KEY")
            openai.api_key = key
            self.bot = ChatBot(self.temperature)

        if self.bot:
            # 依次提问
            try:
                if self.request_order % 2:
                    self.request_1()
                if (self.request_order >> 1) % 2:
                    self.request_2()
                if (self.request_order >> 2) % 2:
                    self.request_4()
                if (self.request_order >> 3) % 2:
                    self.request_8()
                if (self.request_order >> 4) % 2:
                    self.request_16()
            except Exception as e:
                print(e)

