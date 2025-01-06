import PySimpleGUI as psg

list_column = [
    [psg.Text('Image Folder:'),
     psg.InputText(key='-FOLDER-', size=(20, 1)),
     psg.FolderBrowse(), psg.OK(key='Folder Path')],

    [psg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")],
]

marked_column = [
    [psg.Text('筛选结果:')],
    [psg.Listbox(values=[], enable_events=True, size=(30, 20), key="-MARKED FILE LIST-")],
    [psg.Button("单张删除", key="-SINGLE DELETE-"), psg.Button("全部删除", key="-ALL DELETE-")],
]

options_column = [
    [psg.Radio("单张图片", "num", key="-SINGLE-", default=True),
     psg.Radio("全部列表", "num", key="-ALL-")],

    # 清晰度评估
    [psg.Text("清晰度评估:")],
    [psg.Radio("Tenengrad", "sharpness", key="-TENENGRAD-", default=True),
     psg.Radio("Laplacian", "sharpness", key="-LAPLACIAN-")],
    [psg.Text("阈值:"),
     psg.InputText("1000", key="-SHARPNESS_THRESHOLD-", size=(5, 1)),
     psg.Button("开始评估", key="-SHARPNESS_ASSESS-")],

    # 亮度评估
    [psg.Text("亮度评估:")],
    [psg.Radio("过暗", "brightness", key="-DARK-", default=True),
     psg.Radio("曝光", "brightness", key="-LIGHT-")],
    [psg.Text("阈值:"),
     psg.InputText("1", key="-BRIGHTNESS_THRESHOLD-", size=(5, 1)),
     psg.Button("开始评估", key="-BRIGHTNESS_ASSESS-")],

    # 色偏评估
    [psg.Text("色偏评估:")],
    [psg.Text("阈值:"),
     psg.InputText("1.1", key="-COLOR_THRESHOLD-", size=(5, 1)),
     psg.Button("开始评估", key="-COLOR_ASSESS-")],

    # 图像模板匹配
    [psg.Text('模板路径:'),
     psg.InputText(key='-TEMPLATE-', size=(15, 1)),
     psg.FileBrowse(button_text='浏览')],
    [psg.Button("开始匹配", key="-TEMPLATE_MATCH-")],

    # 图像相似度检测
    [psg.Text('相似模板:'),
     psg.InputText(key='-SIMILARITY-', size=(15, 1)),
     psg.FileBrowse(button_text='浏览')],
    [psg.Radio("ORB", "similarity", key="-ORB-", default=True),
     psg.Radio("SIFT", "similarity", key="-SIFT-")],
    [psg.Button("开始检测", key="-SIMILARITY_DETECT-")],
]

image_viewer_column = [
    # [psg.Text("从左边图片列表中选择一张图片:")],
    [psg.Text(size=(40, 1), key="-TOUT-")],
    [psg.Image(key="-IMAGE-")],
    [psg.Text(size=(40, 1), key="-RESULT-"), psg.Button("删除", key="-DELETE-", button_color="red")],
]

layout = [
    [
        psg.Column(list_column),
        psg.VSeparator(),
        psg.Column(marked_column),
        psg.VSeparator(),
        psg.Column(options_column),
        psg.VSeparator(),
        psg.Column(image_viewer_column)
    ]
]
