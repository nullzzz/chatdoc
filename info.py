import prompt

debug = False
sep = "=============="


class QAManager:
    def __init__(self):
        self.answers = {}

        self.questions = {}

        self.general_info = {
            "title": "",
            "domain": "",
            "domain_detail": ""
        }

        self.picture_steps: dict = {}

    def save_to_inter_file(self):
        ...

    def update_detail_answer(self, details: list):
        if old_methods := self.answers.get("methods"):
            if len(details) == len(old_methods):
                for i, m in enumerate(old_methods):
                    details[i]["total"] = m.get("total")
            else:
                print("有错误，待排查")
        self.answers["methods"] = details

        self.update_total_question(details)

    def update_total_answer(self, totals: list):
        if old_methods := self.answers.get("methods"):
            if len(totals) == len(old_methods):
                for i, m in enumerate(old_methods):
                    totals[i]["detail"] = m.get("detail")
            else:
                print("有错误，待排查")
        self.answers["methods"] = totals

    def update_total_question(self, details: list):
        if old_methods := self.questions.get("methods"):
            if len(details) == len(old_methods):
                for i, m in enumerate(old_methods):
                    old_methods[i]["total"] = prompt.prompt_total.replace("{text}", "\n".join(details[i].get("detail")))
            else:
                print("有错误，待排查")
        self.questions["methods"] = old_methods

    def update_answer_by_key(self, key, value):
        self.answers[key] = value

    def update_question_by_key(self, key, value):
        self.questions[key] = value

    def get_answer_by_key(self, key, default=None):
        return self.answers.get(key, default)

    def get_question_by_key(self, key, default=None):
        return self.questions.get(key, default)

    def update_picture_steps(self, picture_steps: dict):
        self.picture_steps.update(picture_steps)

    def parse_requirement(self) -> str:
        """
        :param methods: list，每个元素为一个步骤，该步骤为list，总分结构如：["S1", "S102", "S104"]
        :param title:
        :param method_str:
        :return:
        """
        title = self.general_info.get("title", "")

        methods: list = self.answers.get("methods", [])

        s1 = [m.get("total", "") for m in methods]

        method_str = "\n".join(s1)

        index = 1
        requirement = f"{index}. {title}，其特征在于，包括：\n\n{method_str}\n\n"
        index += 1

        for i, method in enumerate(methods):
            if s102 := method.get("detail"):
                s102 = '\n'.join(s102)
                requirement += f"{index}. 根据权利要求1所述的{title}，其特征在于，步骤S{i + 1}包括：\n\n{s102}\n\n"
                index += 1
        return requirement

    def parse_example(self) -> str:
        """
        解析实施例
        :param methods:
        :param title:
        :return:
        """
        title = self.general_info.get("title", "")

        methods: list = self.answers.get("methods", [])

        s1 = [m.get("total", "") for m in methods]
        method_str = "\n".join(s1)

        index = 1
        example = f"实施例{index}、本申请实施例{index}提供{title}，包括以下步骤：\n\n{method_str}\n\n"
        index += 1

        for i, method in enumerate(methods):
            if s102 := method.get("detail"):
                s102 = '\n'.join(s102)
                example += f"实施例{index}、如图{index}所示，本申请实施例{index}包括以下步骤：\n\n{s102}\n\n"
                index += 1
        return example

    def parse_methods(self) -> str:
        """
        解析步骤，methods具体见load_infer_file函数
        :param methods: dict，每个元素为一个步骤，该步骤为list，如methods['total'] = [S1,S2,...], methods['step1'] = [s102,s104...]
        :param title:
        :return:
        """
        title = self.general_info.get("title", "")

        methods: list = self.answers.get("methods", [])
        picture_tip = [f"图1为本发明实施例中{title}流程图；"]

        idx = 2
        for method in methods:
            picture_tip.append(f"图{idx}为本发明实施例中{method.get('total', '')}；")
            idx += 1

        # latex模板替换
        pic_temp = r"""
               \begin{figure*}
                 \centering
                 \includegraphics[width=\linewidth]{s【index】.png}
                 \caption{图【index】}
               \end{figure*}
               """

        picture_tex = []
        for idx in range(len(picture_tip)):
            if idx == 0:
                continue
            picture_tex.append(
                pic_temp.replace("【index】", f"{idx + 1}")
            )

        return "\n\n".join(picture_tex)

    def add_prefix(self):
        idx = 1
        for method in self.answers.get("methods", []):
            prefix = f"S{idx}"

            total: str = method.get('total', "")
            if total.startswith(prefix):
                break
            else:
                total = f"{prefix}、{total}"
            method["total"] = total

            i = 2

            new_steps = []
            for sub_step in method.get("detail", []):
                prefix = f"S{idx}{i:02d}"

                if not sub_step.startswith(prefix):
                    sub_step = f"{prefix}、{sub_step}"

                new_steps.append(sub_step)
                i += 2
            method["detail"] = new_steps
            idx += 1

    def get_methods_str(self):
        if string := self.answers.get("methods_string"):
            return string

        self.add_prefix()

        string = ""

        idx = 1
        for method in self.answers.get("methods", []):
            total: str = method.get('total', "")

            string += total
            string += "\n"

            i = 2
            for sub_step in method.get("detail", []):
                string += sub_step
                string += "\n"

                i += 2
            idx += 1
        return string

    def get_picture_steps(self):
        self.add_prefix()

        pic = {}

        methods = self.answers.get("methods", [])
        total = "\n".join([method.get("total", "") for method in methods])
        pic["图1"] = total

        idx = 2

        for method in methods:
            pic[f"图{idx}"] = "\n".join(method.get("detail", []))
            idx += 1

        return pic


qa_bot = QAManager()
