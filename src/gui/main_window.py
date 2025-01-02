import PySimpleGUI as psg

layout = [    [psg.Text('Folder Path:'), psg.InputText(key='Folder Path'), psg.FolderBrowse(), psg.OK()]]

window = psg.Window('图像清洗工具', layout)
while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break

    match event:
        case None, 'Exit':
            break

    # if event in (None, 'Exit'):
    #     break
    # print('You entered ', values[0])

window.close()