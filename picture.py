# -*- coding: UTF-8 -*-
import os
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QComboBox, QLineEdit, QSpinBox, QCheckBox, QGridLayout, \
    QLabel, QTextEdit, QScrollArea, QSizePolicy
from PIL.Image import Image

from func import generate_image


class Setting(QWidget):
    def __init__(self, parent=None):
        super(Setting, self).__init__(parent=parent)

        # self.file_path = os.path.abspath(os.path.dirname(__file__))
        self.file_path = os.path.abspath(os.path.join(os.getcwd()))

        # 打开文件
        self.file_name = QLineEdit(self.file_path)
        self.open_bt = QPushButton("浏览目录")

        self.dpi_ = QSpinBox()
        self.dpi_.setMaximum(8000)
        self.dpi_.setValue(72)
        self.dpi = 72

        # 文字数量
        self.char_count = QSpinBox()
        self.char_count.setValue(15)

        # 对齐方式
        self.align = QComboBox()
        self.align.addItems(["左对齐", "居中", "右对齐"])

        self.align_index = 0
        self.count = 15

        # 自动保存
        self.auto_save = QCheckBox("自动保存")
        self.auto_save.setCheckState(True)
        self.is_auto_saved = bool(self.auto_save.checkState())

        # 字体大小
        self.fontsize = QSpinBox()
        self.fontsize.setValue(50)

        # 线条粗细
        self.border = QSpinBox()
        self.border.setValue(5)

        # 框间距
        self.box = QSpinBox()
        self.box.setValue(50)

        # 框内间距
        self.inner = QSpinBox()
        self.inner.setValue(10)

        self.font_size = 50
        self.line_width = 5
        self.box_gap = 50
        self.inner_gap = 10

        # sep symbol
        self.sep_symbol = QLineEdit("、")

        self.sep = "、"

        self.ok_bt = QPushButton("确定")
        self.cancel_bt = QPushButton("取消")

        self.setUI()
        self.link()

    def link(self):

        self.open_bt.clicked.connect(self.openFile)
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt.clicked.connect(self.cancel)

    def ok(self):
        self.align_index = self.align.currentIndex()
        self.count = self.char_count.value()
        self.is_auto_saved = self.is_auto_save()

        self.font_size = self.fontsize.value()
        self.line_width = self.border.value()
        self.box_gap = self.box.value()
        self.inner_gap = self.inner.value()

        self.sep = self.sep_symbol.text()
        _dir = self.file_name.text()
        if os.path.isdir(_dir):
            self.file_path = _dir
        else:
            cur_dir = os.path.abspath(os.path.dirname(__file__))
            self.file_name.setText(cur_dir)
        self.close()

    def cancel(self):
        self.file_name.setText(self.file_path)
        self.dpi_.setValue(self.dpi)
        self.align.setCurrentIndex(self.align_index)
        self.char_count.setValue(self.count)

        self.fontsize.setValue(self.font_size)
        self.border.setValue(self.line_width)
        self.box.setValue(self.box_gap)
        self.inner.setValue(self.inner_gap)

        self.auto_save.setCheckState(self.is_auto_saved)
        self.sep_symbol.setText(self.sep)

    def setUI(self):
        # 打开文件按钮布局
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("保存文件夹"), 0, 0, 1, 6)
        layout1.addWidget(self.file_name, 1, 0, 1, 4)
        layout1.addWidget(self.open_bt, 1, 4, 1, 2)
        layout1.addWidget(self.auto_save, 2, 0, 1, 6)

        layout1.addWidget(QLabel("DPI"), 3, 0, 1, 1)
        layout1.addWidget(self.dpi_, 4, 0, 1, 6)

        layout1.addWidget(QLabel("对齐方式"), 5, 0, 1, 1)
        layout1.addWidget(self.align, 6, 0, 1, 6)
        layout1.addWidget(QLabel("单行文字数量"), 7, 0, 1, 1)
        layout1.addWidget(self.char_count, 8, 0, 1, 6)

        layout1.addWidget(QLabel("字体大小"), 9, 0, 1, 1)
        layout1.addWidget(self.fontsize, 10, 0, 1, 6)

        layout1.addWidget(QLabel("线条粗细"), 11, 0, 1, 1)
        layout1.addWidget(self.border, 12, 0, 1, 6)

        layout1.addWidget(QLabel("文本框间距"), 13, 0, 1, 1)
        layout1.addWidget(self.box, 14, 0, 1, 6)

        layout1.addWidget(QLabel("框内间距"), 15, 0, 1, 1)
        layout1.addWidget(self.inner, 16, 0, 1, 6)

        layout1.addWidget(QLabel("分隔符"), 17, 0, 1, 1)
        layout1.addWidget(self.sep_symbol, 18, 0, 1, 6)

        layout1.addWidget(self.cancel_bt, 19, 0, 1, 3)
        layout1.addWidget(self.ok_bt, 19, 3, 1, 3)

        self.setLayout(layout1)
        self.setWindowTitle("专利绘图——设置")

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name = QFileDialog.getExistingDirectory(self, "Find the image file", ".", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def getDir(self):
        _dir = self.file_name.text()
        if os.path.isdir(_dir):
            return _dir
        cur_dir = os.path.abspath(os.path.dirname(__file__))
        self.file_name.setText(cur_dir)
        return cur_dir

    def get_alignment(self):
        return ["left", "center", "right"][self.align_index]

    def get_length(self):
        return self.count

    def is_auto_save(self):
        return bool(self.auto_save.checkState())


class Picture(QWidget):
    def __init__(self, parent=None):
        super(Picture, self).__init__(parent=parent)
        self.setting_bt = QPushButton("设置")
        self.flows = QComboBox()
        self.draw_bt = QPushButton("生成")
        self.save_bt = QPushButton("另存为")
        self.update_bt = QPushButton("更新到中间文件")

        self.caption = QLineEdit()

        self.setting_window = Setting()

        self.text = QTextEdit()
        self.label = QLabel()
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.label_scroll = QScrollArea()
        self.label_scroll.setWidget(self.label)
        self.scale_factor = 1

        self.zoom_out_bt = QPushButton("缩小")
        self.zoom_in_bt = QPushButton("放大")

        self.image = None

        self.pictures: dict = {}

        self.setUI()
        self.link()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(self.setting_bt, 0, 0, 1, 1)
        layout.addWidget(self.flows, 0, 1, 1, 1)
        layout.addWidget(self.draw_bt, 0, 2, 1, 1)
        layout.addWidget(self.save_bt, 0, 3, 1, 1)

        layout.addWidget(self.caption, 1, 0, 1, 2)
        layout.addWidget(self.text, 2, 0, 5, 2)

        layout.addWidget(self.update_bt, 1, 2, 1, 2)
        layout.addWidget(self.label_scroll, 2, 2, 5, 2)
        layout.addWidget(self.zoom_in_bt, 6, 2, 1, 1)
        layout.addWidget(self.zoom_out_bt, 6, 3, 1, 1)
        layout.setHorizontalSpacing(10)

        self.setLayout(layout)

    def link(self):
        self.setting_bt.clicked.connect(self.set)
        self.draw_bt.clicked.connect(self.draw)
        self.save_bt.clicked.connect(self.save_as)
        self.flows.currentIndexChanged.connect(self.change_text)

        self.zoom_out_bt.clicked.connect(self.zoom_out)
        self.zoom_in_bt.clicked.connect(self.zoom_in)

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def change_text(self, index):
        pname = self.flows.itemText(index)
        data: dict = self.flows.itemData(index)
        caption: str = data["caption"]
        text = data["text"]
        if isinstance(text, str):
            self.text.setText(text)
        elif isinstance(text, list):
            self.text.setText("\n\n".join(text))

        self.caption.setText(caption)

    def update_steps(self):
        if (index := self.flows.currentIndex()) != -1:
            caption = self.caption.text()
            text = self.text.toPlainText()
            self.flows.setItemData(index, {"caption": caption, "text": text})

    def set(self):
        self.setting_window.show()

    def draw(self):
        self.update_steps()
        text = self.text.toPlainText()
        # reset scale factor
        self.scale_factor = 1.0
        if not text:
            self.image = None
            self.label.clear()

        else:
            cnt = self.setting_window.get_length()

            sep = self.setting_window.sep
            fontsize = self.setting_window.font_size
            box_gap = self.setting_window.box_gap
            inner_gap = self.setting_window.inner_gap
            line_width = self.setting_window.line_width

            align = self.setting_window.get_alignment()
            try:
                image = generate_image(text, sep=sep, line_length=cnt, alignment=align,
                                       font_size=fontsize, box_gap=box_gap, inner_gap=inner_gap, line_width=line_width)

                w, h = image.size
                self.label.resize(w, h)

                im = image.convert("RGBA")
                data = im.tobytes("raw", "RGBA")
                qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
                pix = QPixmap.fromImage(qim)
                self.label.setPixmap(pix)

                self.image = image

                if self.setting_window.is_auto_save():
                    auto_save_index = self.flows.currentIndex() + 1
                    dpi = self.setting_window.dpi
                    # path = os.path.join(self.setting_window.getDir(), f"s{auto_save_index}.png")
                    self.image.save(f"s{auto_save_index}.png", dpi=(dpi, dpi))
            except ValueError as error:
                self.image = None
                self.label.clear()

    def save_as(self):
        if (index := self.flows.currentIndex()) != -1:
            print(index)

            print(self.flows.itemData(index))

        if self.image:
            self.image: Image
            name, _ = QFileDialog.getSaveFileName(self, 'Save File', self.setting_window.getDir(),
                                                  "Images (*.png *.jpg)")
            if name:
                dpi = self.setting_window.dpi
                self.image.save(name, dpi=(dpi, dpi))
        else:
            ...

    def add_pictures(self, methods: dict):
        self.flows.clear()
        for key, value in methods.items():
            self.add_picture(key, value)

    def add_picture(self, pname: str, pcontent: list | str, caption=None):
        if (index := self.flows.findText(pname)) != -1:
            self.flows.removeItem(index)
        self.flows.addItem(pname, {
            "caption": caption if caption else pname,
            "text": pcontent
        })

    def scale_image(self, factor):
        if self.image:
            self.scale_factor *= factor
            self.label.resize(self.scale_factor * self.label.pixmap().size())

            self.adjust_scroll_bar(self.label_scroll.horizontalScrollBar(), factor)
            self.adjust_scroll_bar(self.label_scroll.verticalScrollBar(), factor)

            # self.zoom_in_bt.setEnabled(self.scale_factor < 3.0)
            # self.zoom_out_bt.setEnabled(self.scale_factor > 0.333)

    def adjust_scroll_bar(self, scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value()
                                + ((factor - 1) * scroll_bar.pageStep() / 2)))

    def generate_all_pictures(self):
        for i in range(self.flows.count()):
            self.flows.setCurrentIndex(i)
            self.draw()

    def get_new_steps(self):
        data = []
        for i in range(self.flows.count()):
            data.append(self.flows.itemData(i))
        return data


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    main = Picture()
    main.add_picture("图1", """S1、用户向选调器发送输入请求，选调器执行体上线，将输入请求分发给各执行体
S2、各执行体对输入请求进行处理，然后将处理结果返回给表决模块
S3、选调器的表决模块根据各服务器的响应进行处理，并将结果发送给用户和信誉度反馈模块
S4、选调器根据更新后的信誉度和各执行体的差异性，重新选取执行体集，等待用户的输入请求
""")
    main.show()

    sys.exit(app.exec_())
