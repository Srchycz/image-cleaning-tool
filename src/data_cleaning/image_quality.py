import cv2
import numpy as np

'''
评估图像质量(清晰度)
'''

class AssessmentStrategy:
    def __init__(self, threshold:float):
        self.threshold = threshold

    def assess_image_quality(self, image) -> float:
        pass

class TenengradAssessment(AssessmentStrategy):
    def __init__(self, threshold=1000):
        super().__init__(threshold)

    def assess_image_quality(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

        tenengrad_image = cv2.magnitude(sobelx, sobely) # 计算梯度幅值
        score = np.mean(tenengrad_image ** 2)
        return score

class LaplacianAssessment(AssessmentStrategy):
    def __init__(self, threshold=100):
        super().__init__(threshold)

    def assess_image_quality(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        score = np.mean(laplacian ** 2)
        return score

class ImageQualityAssessment:
    def __init__(self, method : AssessmentStrategy = TenengradAssessment()):
        self.method = method

    def assess_images_quality(self, images : dict):
        """ 评估图像清晰度 返回一个标记列表，1表示清晰，0表示模糊 """
        scores = {}
        invalid_images = []

        print(type(images))
        # Assess image quality
        # todo: 显示进度条
        for (key, image) in images.items():
            score = self.assess_image_quality(image)
            scores[key] = score
            if score < float(self.method.threshold):
                invalid_images.append(key)

            # print(score)
            # cv2.imshow("Image", image)
            # key = cv2.waitKey()
            # if key == 27:
            #     break
            # cv2.destroyAllWindows()

        return invalid_images, scores

    def assess_image_quality(self, image):
        return self.method.assess_image_quality(image)

    def normalize_scores(self, scores):
        pass # todo: implement this function