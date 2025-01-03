from src.utils import read_images
from src.data_cleaning.image_quality import ImageQualityAssessment, TenengradAssessment, LaplacianAssessment
from src.data_cleaning.anomaly_detection import detect_anomaly_values, detect_color_biases, detect_color_bias, detect_anomaly_value

""" 集成图像清理操作 """
class Cleaner:
    def __init__(self):
        self.folder_path = None
        self.images = dict()

    def set_folder_path(self, folder_path) -> None:
        self.folder_path = folder_path
        self.images = read_images(folder_path)

    def assess_sharpness_all(self, method=0, threshold=1000) -> dict:
        if method == 0:
            tmp_ass = ImageQualityAssessment(TenengradAssessment(threshold))
        else:
            tmp_ass = ImageQualityAssessment(LaplacianAssessment(threshold))

        return tmp_ass.assess_images_quality(self.images)

    def assess_sharpness_single(self, filename, method=0, threshold=1000) -> float:
        if method == 0:
            tmp_ass = ImageQualityAssessment(TenengradAssessment(threshold))
        else:
            tmp_ass = ImageQualityAssessment(LaplacianAssessment(threshold))

        return tmp_ass.assess_image_quality(self.images[filename])

    def assess_brightness_all(self, threshold, invalidate_dark=True):
        return detect_anomaly_values(self.images, threshold, invalidate_dark)

    def assess_brightness_single(self, filename):
        return detect_anomaly_value(self.images[filename])

    def assess_color_bias_all(self, threshold):
        return detect_color_biases(self.images)

    def assess_color_bias_single(self, filename):
        return detect_color_bias(self.images[filename])