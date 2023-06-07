# -*- coding: UTF-8 -*-
import openai
from info import debug


class ChatBot:
    DEBUG = True

    def __init__(self, temperature: float = 1):
        """

        :param debug:
        :param temperature:
        """
        self.temperature: float = temperature

    def set_temperature(self, temperature: float):
        self.temperature = temperature

    def __call__(self, question: str, temperature: float = 1) -> \
            tuple[str, str]:
        if debug:
            return "测试回答", "stop"

        messages = [
            {
                "role": "user",
                "content": question
            }
        ]

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature if temperature else self.temperature,
                timeout=30,
                request_timeout=180,
            )
        except openai.error.Timeout:
            return "回答超时", "stop"

        except Exception as e:
            print(e)
            print(type(e))
            return "回答超时", "stop"

        answer = completion.choices[0].message["content"]

        finish_reason = completion.choices[0].finish_reason

        if finish_reason != "stop":
            print("可能有错误")

        return answer, finish_reason

    def q_single(self, question: str, *args) -> str:
        if ChatBot.DEBUG:
            return "测试回答，单步"
        answer, fr = self(question, *args)

        return answer

    def q_method(self, question: str, *args) -> list:
        if ChatBot.DEBUG:
            return ["测试步骤", "测试"]
        answer = self.q_single(question, *args)

        answer_list = [step for step in answer.split("\n\n") if step]
        return answer_list


if __name__ == "__main__":
    openai.api_key = "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"
    cb = ChatBot()
    ans, _ = cb("QoS的背景意义？")

    print(ans)
