# -*- coding: UTF-8 -*-
import platform

from PIL import Image, ImageDraw, ImageFont


def generate_image(method: str | list, sep="、", line_length: int = 15,
                   alignment="left",
                   font_size: int = 50, box_gap=50, line_width: int = 5, inner_gap: int = 10) -> Image:
    """

    :param alignment:
    :param line_width:
    :param method:
    :param sep:
    :param line_length: 每行最少字数
    :param font_size: 每行最少字数
    :param box_gap: 每行最少字数
    :param inner_gap: 每行最少字数
    :return:
    """

    box_gap = max(box_gap, font_size)
    left_gap = font_size
    top_gap = int(1.5 * font_size)
    arc_radius = top_gap // 2
    arc_width = min(line_width, arc_radius // 5)
    gen_gap = font_size // 2

    steps = {}

    if isinstance(method, str):
        method = method.split("\n")

    for step in method:
        if not step or step == "\n":
            continue
        if sep not in step:
            print(f"格式错误，步骤号与步骤内容请使用'{sep}'隔开")
            raise ValueError(f"格式错误，步骤号与步骤内容请使用'{sep}'隔开")
        text_list: list = step.split(sep)
        idx = text_list[0]
        text = f"{sep}".join(text_list[1:])

        steps[idx] = text.strip()

    boxes = []

    max_length = 0
    for idx, text in steps.items():
        max_length = max(len(text), max_length)

    length_of_line = line_length

    start = top_gap
    end = start
    for idx, text in steps.items():
        length = len(text)

        num_of_lines = (length - 1) // length_of_line + 1
        new_text = ""

        for i in range(num_of_lines):
            new_text += text[i * length_of_line: (i + 1) * length_of_line]
            new_text += "\n"
        steps[idx] = new_text

        box_height = num_of_lines * font_size + (num_of_lines - 1) * 2 + 2 * inner_gap + 2 * line_width
        end = start + box_height

        boxes.append((start, end))
        start = end + box_gap

    height = end + top_gap

    box_width = font_size * length_of_line + inner_gap * 2 + 2 * line_width

    width = left_gap + box_width + gen_gap + 2 * arc_radius + gen_gap + 3 * font_size + left_gap

    # 创建空白图像
    image = Image.new(mode="RGB", size=(width, height), color="white")

    draw = ImageDraw.Draw(image)

    # 判断平台，加载中文字体
    if platform.platform().startswith("Win"):
        font = ImageFont.truetype("simsun.ttc", font_size, encoding="unic")  # 设置字体
    else:
        font = ImageFont.truetype("Hiragino Sans GB.ttc", font_size, encoding="unic")  # 设置字体
    #

    i = 0
    for idx, text in steps.items():
        start, end = boxes[i]
        draw.text((left_gap + inner_gap + line_width, start + inner_gap + line_width), text, align=alignment, font=font,
                  fill="black")
        draw.rectangle((left_gap, start, left_gap + box_width, end), fill=None, outline='black', width=line_width)

        mid_y = start + (end - start) // 2

        # draw arc
        arc_x = left_gap + box_width + gen_gap
        arc_y = mid_y - 2 * arc_radius

        shape1 = (arc_x - arc_radius, arc_y, arc_x + arc_radius, arc_y + 2 * arc_radius)
        shape2 = (
            arc_x + arc_radius - arc_width + 1, arc_y, arc_x + 3 * arc_radius - arc_width + 1, arc_y + 2 * arc_radius)
        draw.arc(shape1, 0, 90, fill="black", width=arc_width)
        draw.arc(shape2, 180, 270, fill="black", width=arc_width)

        draw.text((arc_x + 2 * arc_radius + gen_gap, arc_y - font_size // 2), idx, align="left", font=font,
                  fill="black")

        arrow_line = max(box_gap // 5, line_width)
        if i:
            x1 = x2 = left_gap + box_width // 2 - line_width // 2
            y1 = boxes[i - 1][1]
            y2 = boxes[i][0]

            draw.line((x1, y1, x2, y2), fill="black", width=line_width)

            pt1 = (x1, y2 + line_width // 2)
            pt2 = (x1 - arrow_line, y2 - arrow_line)
            pt3 = (x1 + arrow_line, y2 - arrow_line)
            draw.polygon([pt1, pt2, pt3], fill="black")
        i += 1

    return image


def replace_all_punctuation(text: str):
    """
    替换英文符号，转义%
    :param text:
    :return:
    """
    en = [',', ':', '?', '!', '\'', '"']
    cn = ['，', '：', '？', '！', '’', '”']

    mp = dict(zip(en, cn))

    dollar = 0
    new_text = []
    for idx, char in enumerate(text):
        if char == '$' and idx > 0 and text[idx - 1] != '\\':
            dollar += 1
        # 转义%
        if char == '%' and idx > 0 and text[idx - 1].isdigit():
            new_text.append('\\')

        # 在公式中
        if dollar % 2 == 1:
            new_text.append(char)
        else:
            if char == '.' and idx > 0 and text[idx - 1].isdigit():
                new_text.append(char)
            else:
                new_text.append(mp.get(char, char))

    text = "".join(new_text)

    # for e, c in zip(en, cn):
    #     text = text.replace(e, c)

    text = text.replace("\%", "%").replace("%", "\%")

    return text


if __name__ == "__main__":
    text = "S4、对于新用户通过步骤\$1创建高级向量$X_{new}$,通过以下公式30%计算用户存在洗钱交易行为的异常分数$y_pred = X_new * w + b,..$。其中w 和 b是模型参数,根据步骤S2训练得到?"
    print(replace_all_punctuation(text))
