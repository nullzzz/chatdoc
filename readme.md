# Chat Doc

## 使用说明

### Python环境配置

### mac

```
pip3 install -r ./requirements.txt 
```

### windows

```angular2html
pip install -r ./requirements.txt 
```
### [Pandoc安装](https://pandoc.org/installing.html)

### 运行

### mac

```
python3 main.py
```

### windows

```angular2html
python main.py
```

1. 设置问题
   1. 通过配置文件导入问题
   2. 通过图形界面输入、调整问题
2. 点击生成按钮
   1. 【提问背景、步骤】，调用chatgpt回答背景、步骤问题，生成中间文档
   2. 【导入中间文件】，将修改后的中间文件导入
   3. 【提问摘要、总结】，调用chatgpt回答摘要、总结问题（该步骤不会自动生成文档）
   4. 【生成tex文档】，根据前述步骤中的内容，生成tex文档（该步骤包括附图的生成）
   5. 【生成word文档】，将tex文档转换为word文档
3. 附图调整
   1. 通过选择框，选择不同的步骤
   2. 调整文本框中的文字
   3. 点击【生成】按钮（默认自动保存，图一为s1.png，图二为s2.png......）

### 问题配置文件
例见：`question.txt`
#### 字符串
* `i_filename` 中间文件，单行
* `title` 方法名称，单行
* `domain`: 领域，单行
* `domain_detail`: 详细领域，单行
* `abstract`: 摘要问题，单行
* `effect`: 有益效果问题，单行
* `overall`: 综上所述问题，单行
#### 列表
* `background` 多个技术背景问题，单行
* `total` 总结性问题，用于生成一级步骤S1\S2\S3...，支持多行
* `detail` 分步骤问题，用于生成二级步骤S102\S104\S106...，支持多行
### 中间文件
#### 背景技术
* 由背景技术问题提问得到
* 格式无要求
#### 详细步骤
* 由步骤问题提问得到
* 每个步骤以S1、S102等开头，支持多行
#### 附图步骤
* 附图之间以**空行**分割
* 每个附图包括两个部分
  * 第一行：图说明文字
  * 低二行起：每行为一个步骤，以S1、S102等开头，不支持跨行

## 流程说明

依次提问以下问题，见`.\tab\operator.py`：
* background（多个问题） -> 背景技术
* methods （多个问题）-> 技术方案步骤
***
* abstract -> 说明书摘要
* effect -> 有效效果
* overall -> 综上所述

**注：上述关键字对应于配置文件的key**

## 文件说明

* tab文件夹：不同页面的UI，以及页面处理
  * `background.py` 背景摘要页面
  * `content.py`    发明内容页面
  * `operator.py`   生成页面
  * `picture.py`    附图调整页面 
  * `general.py`    文档设置页面
* `chat.py`调用API接口的ChatBot类
  * `parse_step` 根据回答，解析步骤
* `query.py`调用API接口的过程类
* `main.py`主界面类
  * `request` 调用API接口
  * `generate` 生成文档
  * `collect_question` 从UI界面采集问题
* `func.py`一些单独的处理函数
  * `parse_requirement` 解析权利要求书
  * `parse_example` 解析实施例
  * `parse_methods` 解析步骤
  * `generate_picture` 生成说明书附图
  * `replace_text` 替换英文符号，转义%，$$内的不替换
* `temp.tex`latex模板文件
* `question.json`问题配置文件
* `inter_file`中间文件，该文件名任意，可以通过question.json配置或界面修改
  * `sep = "=============="`见`main.py`15行
  * 分割背景和步骤的回答
  * `load_inter_file`函数，用于导入中间文件，见`main.py`
  * `update_inter_file`函数，用于更新中间文件，将调整后的附图步骤写入文件，见`main.py`


## 更新说明
* 步骤提问中的子步骤划分：`chat.py -> parse_step`
* 答案解析到模板的处理规则：`func.py`中的对应函数
* 更新文档模板：`main.py -> generate_1`