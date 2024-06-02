import gradio as gr
import wordcloud
import numpy as np
from PIL import Image,ImageChops



def process(text, filepath, mask_img):

    # 读取mask图像
    im = Image.open(mask_img)
    # im = ImageChops.invert(im) # 获取反色、
    # im.save('test1.png')
    mask = np.array(im)

    # 创建词云
    wc = wordcloud.WordCloud(font_path = 'simhei.ttf',background_color="black", max_words=2000, mask=mask)
    if len(text) == 0:
        # 打开文件
        # print(filepath)
        with open(filepath, 'r', encoding='utf-8') as file:
            # 逐行读取并打印
            for line in file:
                # print(line, end='')  # 默认情况下，print会在每行末尾添加换行符，这里使用end=''来避免这个行为
                text += line
    wc.generate(text)


    # 返回图像
    wc.to_file("output_image.png")
    return "output_image.png"


# 创建Gradio界面
with gr.Blocks(css="footer {visibility: hidden}") as demo:
    with gr.Row(): # 创建一个行容器 只展示一个标题
        gr.HTML(value="""<h1 align="center">词云服务</h1>""")
    with gr.Row(): # 创建一个行容器 功能输入 输出
        with gr.Column():  # 三个列容器，分别展示文本框输入、文件输入、图片输入功能
            text = gr.Textbox(label="文本框输入【优先】")
            file = gr.File(label="文本输入")
            mask = gr.Image(label="上传Mask图像，黑图白底", type='filepath', height=400)
        with gr.Column(): # 输出展示
            output_image = gr.Image(label="词云输出")
    with gr.Row():  # 创建一个行容器 操作按钮，提交和删除按钮
        send_btn = gr.Button("生成")
        clear_btn = gr.Button("清除")
        send_btn.click(process, inputs=[text, file, mask], outputs=[output_image])
        clear_btn.click(lambda _: (None, None, None, None), inputs=clear_btn, outputs=[text, file, mask, output_image])


demo.launch()
