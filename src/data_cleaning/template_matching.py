import cv2
import numpy as np

def template_matching(images:dict, template):
    valid_images = []
    mark = {}
    for (key, image) in images.items():
        loc = single_image_template_matching(image, template)

        is_empty = sum([len(x) for x in loc]) == 0
        mark[key] = loc

        if not is_empty:
            valid_images.append(key)
        # print(is_empty)
        # cv2.imshow("Image", image)
        # key = cv2.waitKey()
        # if key == 27:
        #     break
        # cv2.destroyAllWindows()

    return valid_images, mark


def single_image_template_matching(image, template):
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    image_grey = image_grey.astype('float32')
    template = template.astype('float32')

    if all(x <= y for x, y in zip(template.shape, image_grey.shape)):
        res = cv2.matchTemplate(image_grey, template, cv2.TM_CCOEFF_NORMED)
        # print(image_grey.shape)
        # print(template.shape)
    else:
        res = 0

    threshold = 0.8
    loc = np.where(res >= threshold)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 2)
    return loc

def draw_loc(image:np.ndarray, loc, shape:tuple):
    cp = image.copy()
    for pt in zip(*loc[::-1]):
        cv2.rectangle(cp, pt, (pt[0] + shape[1], pt[1] + shape[0]), (0, 0, 255), 2)

    return cp