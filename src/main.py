import utils
import PySimpleGUI as psg
import os
import gui
import data_cleaning

# default_path = "./samples"
default_path = 'C:/Users/29822/work/lockin/image_cleaning_tool/src/samples'

def refresh(w):
    w['-FILE LIST-'].update(values=cleaner.images.keys())
    w['-MARKED FILE LIST-'].update(values=cleaner.marked.keys())
    w['-IMAGE-'].update(data=b'')
    w['-RESULT-'].update('')
    w['-TOUT-'].update('')

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
                filename = values['-FILE LIST-'][0]
                # filename = os.path.join(cleaner.folder_path, values['-FILE LIST-'][0])
                # window['-IMAGE-'].update(source=filename)
                window['-IMAGE-'].update(data=cleaner.show_in_norm_bytes(filename))

            case '-MARKED FILE LIST-':
                filename = values['-MARKED FILE LIST-'][0]
                window['-TOUT-'].update(filename)
                if cleaner.flag == 1:
                    window['-RESULT-'].update(f'Result: {cleaner.details[filename]}')
                else:
                    window['-RESULT-'].update('')
                window['-IMAGE-'].update(data=cleaner.show_in_norm_bytes(filename))
                window['-FILE LIST-'].update(set_to_index=[])

            case "-SHARPNESS_ASSESS-":
                method = 0 if values['-TENENGRAD-'] else 1
                threshold = values['-SHARPNESS_THRESHOLD-']
                is_all = values['-ALL-']

                if is_all:
                    invalid_images, _ = cleaner.assess_sharpness_all(method, threshold)
                    psg.popup_ok(f'Found {len(invalid_images)} invalid images')
                    window['-MARKED FILE LIST-'].update(values=invalid_images)
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
                    window['-MARKED FILE LIST-'].update(values=invalid_images)
                else:
                    try:
                        filename = values['-FILE LIST-'][0]
                    except IndexError:
                        psg.popup_ok('Please select an image first')
                        continue
                    score = cleaner.assess_brightness_single(filename)
                    window['-RESULT-'].update(f"Color Bias Score: %.4f (分数越大越亮)" % score)

            case "-COLOR_ASSESS-":
                threshold = values['-COLOR_THRESHOLD-']
                is_all = values['-ALL-']

                if is_all:
                    invalid_images, _ = cleaner.assess_color_bias_all(threshold)
                    psg.popup_ok(f'Found {len(invalid_images)} invalid images')
                    window['-MARKED FILE LIST-'].update(values=invalid_images)
                else:
                    try:
                        filename = values['-FILE LIST-'][0]
                    except IndexError:
                        psg.popup_ok('Please select an image first')
                        continue
                    score = cleaner.assess_color_bias_single(filename)
                    window['-RESULT-'].update(f"Brightness Score: %.4f (分数越大色偏越严重)" % score)

            case "-TEMPLATE_MATCH-":
                template_path = values['-TEMPLATE-']
                if template_path == '':
                    psg.popup_ok('Please select a template first')
                    continue

                template = utils.read_image(template_path)
                is_all = values['-ALL-']

                if is_all:
                    valid_images, mark = cleaner.template_match_all(template)
                    psg.popup_ok(f'Found {len(valid_images)} valid images')
                    window['-MARKED FILE LIST-'].update(values=valid_images)
                else:
                    try:
                        filename = values['-FILE LIST-'][0]
                    except IndexError:
                        psg.popup_ok('Please select an image first')
                        continue

                    loc = cleaner.template_match_single(filename, template)
                    if sum([len(x) for x in loc]) == 0:
                        window['-RESULT-'].update("无匹配结果")
                        continue
                    marked_image = cleaner.draw_loc(filename, loc, template.shape)
                    window['-RESULT-'].update("匹配成功")
                    window['-IMAGE-'].update(data=utils.cv2_to_bytes(marked_image))

            case "-SIMILARITY_DETECT-":
                method = 0 if values['-ORB-'] else 1
                similarity_path = values['-SIMILARITY-']
                if similarity_path == '':
                    psg.popup_ok('Please select a similarity template first')
                    continue

                similarity = utils.read_image(similarity_path)
                is_all = values['-ALL-']

                if is_all:
                    pass
                else:
                    try:
                        filename = values['-FILE LIST-'][0]
                    except IndexError:
                        psg.popup_ok('Please select an image first')
                        continue
                    cleaner.detect_similarity_single(filename, similarity, method)
                    pass # todo: implement this branch

            case '-DELETE-':
                try:
                    filename = values['-FILE LIST-'][0]
                except IndexError:
                    psg.popup_ok('Please select an image first')
                    continue

                ch = psg.popup_ok_cancel(f'Delete {filename}?')
                if ch == 'OK':
                    cleaner.delete(filename)

                    window['-FILE LIST-'].update(values=cleaner.images.keys())
                    window['-IMAGE-'].update(data=b'')
                    window['-RESULT-'].update('')
                    window['-TOUT-'].update('')

            case '-SINGLE DELETE-':
                try:
                    filename = values['-MARKED FILE LIST-'][0]
                except IndexError:
                    psg.popup_ok('Please select an image first')
                    continue

                ch = psg.popup_ok_cancel(f'Delete {filename}?')
                if ch == 'OK':
                    cleaner.delete_mark_single(filename)

                    refresh(window)

            case '-ALL DELETE-':
                ch = psg.popup_ok_cancel('Delete all images?')

                if ch == 'OK':
                    cleaner.delete_mark_all()

                    refresh(window)

            case _:
                pass

    window.close()
