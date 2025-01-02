
import data_cleaning
import utils
import PySimpleGUI as psg
import os
import gui
from src.data_cleaning import ImageQualityAssessment, TenengradAssessment, LaplacianAssessment
from src.gui.demo import window

# default_path = "./samples"
default_path = 'C:/Users/29822/work/lockin/image_cleaning_tool/src/samples'

if __name__ == '__main__':
    window = psg.Window('图像清洗工具', gui.layout, enable_close_attempted_event=True)
    while True:
        event, values = window.read()

        if event == psg.WINDOW_CLOSE_ATTEMPTED_EVENT and psg.popup_yes_no('Do you want to exit?') == 'Yes':
            break

        match event:
            case 'Folder Path':
                folder = values['-FOLDER-']
                # todo: 把相对路径转换为绝对路径存下来
                if folder == "" :
                    folder = default_path
                    window['-FOLDER-'].update(folder)
                if not os.path.exists(folder):
                    psg.popup_error(f'Folder {folder} does not exist')
                else:
                    # utils.images_jpg2png(folder)
                    images, fname = utils.read_images(folder)
                    if len(images) == 0:
                        psg.popup_error(f'No images found in folder {folder}')
                    else:
                        psg.popup_ok(f'Found {len(images)} images in folder {folder}')
                        window['-FILE LIST-'].update(values=fname)

            case '-FILE LIST-':
                window['-TOUT-'].update(values['-FILE LIST-'][0])
                filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
                # print(filename)
                # show_image(filename)
                window['-IMAGE-'].update(source=filename)

            case "SHARPNESS_ASSESS":
                method = TenengradAssessment() if values['-TENENGRAD-'] else LaplacianAssessment()
                assessment = ImageQualityAssessment(method)

                is_all = values['-ALL-']

            case _:
                pass

    window.close()


