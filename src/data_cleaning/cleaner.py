import os

from src.utils import read_images
from src.data_cleaning.image_quality import ImageQualityAssessment, TenengradAssessment, LaplacianAssessment
from src.data_cleaning.anomaly_detection import detect_anomaly_values, detect_color_biases, detect_color_bias, detect_anomaly_value
from src.data_cleaning.template_matching import template_matching, single_image_template_matching, draw_loc
from src.data_cleaning.similarity_detection import *

""" 集成图像清理操作 """
class Cleaner:
    def __init__(self):
        self.folder_path = None
        self.images = dict()

        self.flag = 0
        self.marked = []
        self.details = dict()

    def set_folder_path(self, folder_path) -> None:
        self.folder_path = folder_path
        self.images = read_images(folder_path)

    def assess_sharpness_all(self, method=0, threshold=1000) -> (list, dict):
        if method == 0:
            tmp_ass = ImageQualityAssessment(TenengradAssessment(threshold))
        else:
            tmp_ass = ImageQualityAssessment(LaplacianAssessment(threshold))

        self.flag = 1
        self.marked, self.details = tmp_ass.assess_images_quality(self.images)
        return self.marked, self.details

    def assess_sharpness_single(self, filename, method=0, threshold=1000) -> float:
        if method == 0:
            tmp_ass = ImageQualityAssessment(TenengradAssessment(threshold))
        else:
            tmp_ass = ImageQualityAssessment(LaplacianAssessment(threshold))

        return tmp_ass.assess_image_quality(self.images[filename])

    def assess_brightness_all(self, threshold, invalidate_dark=True) -> (list, dict):
        self.flag = 1
        self.marked, self.details = detect_anomaly_values(self.images, threshold, invalidate_dark)
        return self.marked, self.details

    def assess_brightness_single(self, filename):
        return detect_anomaly_value(self.images[filename])

    def assess_color_bias_all(self, threshold) -> (list, dict):
        self.flag = 1
        self.marked, self.details = detect_color_biases(self.images, threshold)
        return self.marked, self.details

    def assess_color_bias_single(self, filename):
        return detect_color_bias(self.images[filename])

    def template_match_all(self, template) -> (list, dict):
        self.flag = 2
        self.marked, self.details = template_matching(self.images, template)
        return self.marked, self.details

    def template_match_single(self, filename, template):
        return single_image_template_matching(self.images[filename], template)

    def draw_loc(self, filename, loc, shape):
        return draw_loc(self.images[filename], loc, shape)

    def detect_similarity_all(self, similarity, method=0) -> (list, dict):
        pass # TODO: implement this

    def detect_similarity_single(self, filename, similarity, method=0):
        if method == 0:
            return detect_similarity_with_orb(similarity, self.images[filename])
        else:
            return detect_similarity_with_sift(similarity, self.images[filename])

    def show_in_norm_bytes(self, filename):
        return cv2.imencode('.png', self.images[filename])[1].tobytes()

    def delete(self, filename):
        self.images.pop(filename)
        try:
            self.marked.remove(filename)
        except ValueError:
            pass
        # os.remove(os.path.join(self.folder_path, filename))
        return

    def delete_mark_single(self, filename):
        self.images.pop(filename)
        self.marked.remove(filename)
        # os.remove(os.path.join(self.folder_path, filename))
        return

    def delete_mark_all(self):
        self.images.pop(x for x in self.marked)
        self.marked.clear()
        return
