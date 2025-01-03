import cv2
import os
from PIL import Image

def read_images(image_path):
    """
    读入路径下的所有图片 默认 png 格式 以 BGR 格式读入
    返回一个字典，key为图片名，value为图片
    """
    filelist = os.listdir(image_path)
    # image_names_list = []
    # images = []
    images = {}

    for file in filelist:
        if file.endswith('.png'): # or file.endswith('.jpg')
            # clear_image_iccp(os.path.join(image_path, file))
            image = cv2.imread(os.path.join(image_path, file))
            # images.append(image)
            # image_names_list.append(file)
            images[file] = image

    return images

def read_image(image_path):
    """ 读入路径指向的图片 默认 png 格式 以 BGR 格式返回 """
    image = cv2.imread(image_path)
    return image

def save_image(image, image_path):
    """ 保存图片到指定路径 """
    cv2.imwrite(image_path, image)
    return

def images_jpg2png(path):
    """ 将指定路径下的所有 jpg 图片转换为 png 格式  并删除原有的 jpg """
    filelist = os.listdir(path)
    for file in filelist:
        if file.endswith('.jpg'):
            image = Image.open(os.path.join(path, file))
            image.save(os.path.join(path, file.replace('.jpg', '.png')))

            """ 删除原有的 jpg """
            os.remove(os.path.join(path, file))

def clear_image_iccp(image_path):
    """ 清除图片的 ICCP 信息 """
    image = Image.open(image_path)
    if "icc_profile" in image.info:
        del image.info['icc_profile']
    image.save(image_path, format='PNG')

def show_image(image_path):
    """ 显示图片 """
    image = cv2.imread(image_path)
    cv2.imshow("Image", image)
    cv2.waitKey()
    cv2.destroyAllWindows()