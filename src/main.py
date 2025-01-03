import utils
import PySimpleGUI as psg
import os
import gui
import data_cleaning

# default_path = "./samples"
default_path = 'C:/Users/29822/work/lockin/image_cleaning_tool/src/samples'

if __name__ == '__main__':
    cleaner = data_cleaning.Cleaner()
    window = psg.Window('图像清洗工具', gui.layout, enable_close_attempted_event=True)

    while True:
        event, values = window.read()

        if event == psg.WINDOW_CLOSE_ATTEMPTED_EVENT and psg.popup_yes_no('Do you want to exit?') == 'Yes':
            break

        match event:
            case 'Folder Path':
                folder = values['-FOLDER-']
                # todo: 把相对路径转换为绝对路径存下来
                if folder == "":
                    folder = default_path
                    window['-FOLDER-'].update(folder)
                if not os.path.exists(folder):
                    psg.popup_ok(f'Folder {folder} does not exist')
                else:
                    # utils.images_jpg2png(folder)
                    cleaner.set_folder_path(folder)

                    if len(cleaner.images) == 0:
                        psg.popup_ok(f'No images found in folder {folder}')
                    else:
                        psg.popup_ok(f'Found {len(cleaner.images)} images in folder {folder}')
                        window['-FILE LIST-'].update(values=cleaner.images.keys())

            case '-FILE LIST-':
                window['-TOUT-'].update(values['-FILE LIST-'][0])
                window['-RESULT-'].update('')
                filename = os.path.join(cleaner.folder_path, values['-FILE LIST-'][0])
                window['-IMAGE-'].update(source=filename)

            case "-SHARPNESS_ASSESS-":
                method = 0 if values['-TENENGRAD-'] else 1
                threshold = values['-SHARPNESS_THRESHOLD-']
                is_all = values['-ALL-']

                if is_all:
                    invalid_images, _ = cleaner.assess_sharpness_all(method, threshold)
                    psg.popup_ok(f'Found {len(invalid_images)} invalid images')
                else:
                    try:
                        filename = values['-FILE LIST-'][0]
                    except IndexError:
                        psg.popup_ok('Please select an image first')
                        continue
                    score = cleaner.assess_sharpness_single(filename, method, threshold)
                    window['-RESULT-'].update(f"Sharpness Score: %.4f (分数越大越清晰)" % score)

            case "-BRIGHTNESS_ASSESS-":
                threshold = values['-BRIGHTNESS_THRESHOLD-']
                is_all = values['-ALL-']

                if is_all:
                    invalid_images, _ = cleaner.assess_brightness_all(threshold)
                    psg.popup_ok(f'Found {len(invalid_images)} invalid images')
                else:
                    try:
                        filename = values['-FILE LIST-'][0]
                    except IndexError:
                        psg.popup_ok('Please select an image first')
                        continue
                    score = cleaner.assess_brightness_single(filename)
                    window['-RESULT-'].update(f"Brightness Score: %.4f (分数越大越亮)" % score)

            case "-COLOR_ASSESS-":
                threshold = values['-COLOR_THRESHOLD-']
                is_all = values['-ALL-']

                if is_all:
                    invalid_images, _ = cleaner.assess_color_bias_all(threshold)
                    psg.popup_ok(f'Found {len(invalid_images)} invalid images')
                else:
                    try:
                        filename = values['-FILE LIST-'][0]
                    except IndexError:
                        psg.popup_ok('Please select an image first')
                        continue
                    score = cleaner.assess_color_bias_single(filename)
                pass

            case "-TEMPLATE_MATCH-":
                pass

            case "-SIMILARITY_DETECT-":
                pass

            case _:
                pass

    window.close()
