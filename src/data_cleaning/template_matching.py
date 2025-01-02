import cv2
import numpy as np


def template_matching(images, template):
    mark = []
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    for image in images:
        loc = single_image_template_matching(image, template)

        is_empty = sum([len(x) for x in loc]) == 0
        mark.append(is_empty)
        print(is_empty)
        cv2.imshow("Image", image)
        key = cv2.waitKey()
        if key == 27:
            break
        cv2.destroyAllWindows()

    return mark


def single_image_template_matching(image, template):
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(image_grey, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 2)
    return loc