import json
import re

from func import replace_all_punctuation
from info import sep, qa_bot


def load_methods_questions(filename: str) -> list[dict[str, str]]:
    methods_detail = []  #

    current_question = ""
    with open(filename, encoding="utf-8") as file:
        while line := file.readline():
            line = line.rstrip("\n").strip()
            if not line:
                continue

            if line.startswith("@detail"):
                if current_question:
                    methods_detail.append(dict(detail=current_question, total=""))
                    current_question = ""
            else:
                current_question += line + "\n"

    if current_question:
        methods_detail.append(dict(detail=current_question, total=""))

    return methods_detail


def replace_keywords(data: dict, *keywords):
    for word in keywords:
        if keyword := data.get(word):
            REPLACE_TEMPLATE = f"{{@{word}}}"
            print(REPLACE_TEMPLATE)
            for key, value in data.items():
                if isinstance(value, str) and REPLACE_TEMPLATE in value:
                    data[key] = value.replace(REPLACE_TEMPLATE, keyword)
                elif isinstance(value, list):
                    new_value = []
                    for val in value:
                        if isinstance(val, str) and REPLACE_TEMPLATE in val:
                            new_value.append(val.replace(REPLACE_TEMPLATE, keyword))
                        else:
                            new_value.append(val)
                    data[key] = new_value


def load_questions(filename: str):
    with open(filename, encoding="utf-8") as file:
        data = json.load(file)

    if methods_filename := data.get("methods_filename"):
        methods = load_methods_questions(methods_filename)
        data["methods"] = methods

    replace_keywords(data, "keyword1", "keyword2")

    for key in ("title", "domain", "domain_detail"):
        if value := data.get(key):
            qa_bot.general_info[key] = value

    for key in ("background", "abstract", "methods", "overall"):
        if value := data.get(key):
            qa_bot.update_question_by_key(key, value)


def parse_one_step(method: dict, index: int):
    total = f"S{index}、{method.get('total', '')}"
    detail = []
    for i, d in enumerate(method.get("detail", "")):
        detail.append(f"S{index}0{2 * i + 2}、{d}")

    return total, detail


# def to_methods_component() -> str:
#     """
#     from request answer
#     :return:
#     """
#     methods: list = qa_bot.get_answer_by_key("methods", ["【内容缺失】"])
#
#     methods_component = []
#     for index, method in enumerate(methods):
#         total, detail = parse_one_step(method, index + 1)
#         methods_component.append(total)
#         methods_component.extend(detail)
#     methods_str = "\n\n".join(methods_component)
#     return methods_str


def load_inter_file(filename):
    with open(filename, encoding="utf-8") as file:
        text = file.read()

    data = text.split(sep)

    if (size := len(data)) == 3:
        background, methods_str, steps = data
    elif size == 2:
        background, methods_str = data
        steps = ""
    elif size == 1:
        background = data
        methods_str = ""
        steps = ""
    else:
        return

    background = replace_all_punctuation(background)

    methods_str = replace_all_punctuation(methods_str)
    steps = steps.strip("\n")

    # S1:xxx
    # S102:XXX
    id2step = {}

    try:
        current_id = None
        for line in methods_str.split("\n"):
            line: str
            line = line.strip()
            if not line:
                continue

            if re.match(r"S\d+、", line):
                current_id, *text = line.split("、")
                if isinstance(text, list):
                    text = "、".join(text)
                id2step[current_id] = text
            else:
                if current_id is None:
                    continue
                id2step[current_id] += line
    except Exception as e:
        print(e)
        print(type(e))

    pic = {}
    methods: list[dict] = []
    for key, val in id2step.items():
        # S1 -> 2
        # S10 -> 3
        # S102 -> 4
        if len(key) <= 3:
            pic.setdefault("图1", []).append(f"{key}、{val}")
            # methods.setdefault("total", []).append(f"{key}、{val}")

            methods.append({"total": f"{key}、{val}"})
        else:
            # S102 -> 1
            # S1002 -> 10
            current_id = int(key[1:-2])
            pic.setdefault(f"图{current_id + 1}", []).append(f"{key}、{val}")
            # methods.setdefault(f"step{current_id}", []).append(f"{key}、{val}")

            methods[current_id - 1].setdefault("detail", []).append(f"{key}、{val}")

    # 判断是否存在修改后的附图步骤
    picture_steps: dict = {}
    if steps:
        for idx, step in enumerate(steps.split("\n\n")):
            caption, *details = step.split("\n")
            picture_steps[caption] = details
    else:
        picture_steps.update(pic)

    if background:
        qa_bot.update_answer_by_key("background", background)

    qa_bot.update_answer_by_key("methods", methods)
    qa_bot.update_answer_by_key("methods_string", methods_str)
    qa_bot.update_picture_steps(picture_steps)
