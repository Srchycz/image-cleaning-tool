import cv2
import os

def read_images(image_path):
    """ 读入路径下的所有图片 默认 jpg 格式 以 BGR 格式返回 """
    filelist = os.listdir(image_path)

    images = []
    for file in filelist:
        if file.endswith('.jpg'): # or file.endswith('.png')
            image = cv2.imread(os.path.join(image_path, file))
            images.append(image)

    return images

def read_image(image_path):
    """ 读入路径指向的图片 默认 jpg 格式 以 BGR 格式返回 """
    image = cv2.imread(image_path)
    return image

def save_image(image, image_path):
    """ 保存图片到指定路径 """
    cv2.imwrite(image_path, image)
    return