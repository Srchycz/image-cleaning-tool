import cv2
import numpy as np

'''
异常值检测
'''
BRIGHTNESS_THRESHOLD = 1 # 亮度阈值
BIAS_THRESHOLD = 1.1 # 色偏阈值
NORMAL = 127.5

def detect_anomaly_value(image):
    # 按输入为彩色图片处理
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    delta = np.mean(gray_image) - NORMAL
    avg = np.mean(np.abs(gray_image - 128 - delta))
    k = delta / avg
    return k
    # return np.mean(gray_image)

'''检测图像亮度'''
def detect_anomaly_values(images:dict, threshold=BRIGHTNESS_THRESHOLD, invalidate_dark=True):
    """ 评估图像亮度 返回不合法列表和亮度分数 """
    scores = dict()
    invalid_images = []

    threshold = -abs(float(threshold)) if invalidate_dark else abs(float(threshold))

    for (key, image) in images.items():
        score = detect_anomaly_value(image)
        scores[key] = score

        if score > threshold:
            invalid_images.append(key)

        # if score > BRIGHTNESS_THRESHOLD:
        #     print("该图亮度异常")
        # print(score)
        # cv2.imshow("Image", image)
        # key = cv2.waitKey()
        # if key == 27:
        #     break
        # cv2.destroyAllWindows()

    return invalid_images, scores

'''检测色偏'''
def detect_color_bias(image):
    # 按输入为彩色图片RGB处理
    img_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(img_lab)
    da = np.mean(a) - NORMAL
    db = np.mean(b) - NORMAL
    D = np.sqrt(da ** 2 + db ** 2)

    ma = np.mean(np.abs(a - 128 - da))
    mb = np.mean(np.abs(b - 128 - db))
    M = np.sqrt(ma ** 2 + mb ** 2)

    k = abs(D / M)
    return k

def detect_color_biases(images:dict, threshold=BIAS_THRESHOLD):
    """ 评估图像色偏程度 返回不合法列表和分数 """
    scores = dict()
    invalid_images = []

    for (key, image) in images.items():
        score = detect_color_bias(image)

        if score > threshold:
            invalid_images.append(key)

        # if score > BIAS_THRESHOLD:
        #     print("该图存在色偏")
        # print(score)
        # cv2.imshow("Image", image)
        # key = cv2.waitKey()
        # if key == 27:
        #     break
        # cv2.destroyAllWindows()

        scores[key] = score
    return invalid_images, scores


def normalize_scores(scores):
    pass # todo: implement this function
