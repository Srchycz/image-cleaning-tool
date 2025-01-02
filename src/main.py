import data_cleaning
import utils
from src.utils import read_images

default_path = "../samples"

if __name__ == '__main__':

    template = utils.file_io.read_image("../samples/template.jpg")
    print(type(template))
    images = read_images(path)

    print(len(images))
    data_cleaning.similarity_detection.detect_similarity_images(images, template)
    print("end!")
    images = utils.file_io.read_images(path)
    print(len(images))
    assessment = data_cleaning.image_quality.ImageQualityAssessment(data_cleaning.image_quality.TenengradAssessment())
    assessment.assess_images_quality(images)

    print("end!")
    images = utils.file_io.read_images(path)
    print(len(images))
    data_cleaning.anomaly_detection.detect_anomaly_values(images)
    print("亮度检测完成")
    data_cleaning.anomaly_detection.detect_color_biases(images)

    print("end!")
    images = utils.file_io.read_images(path)
    print(len(images))
    data_cleaning.template_matching.template_matching(images, template)

    print("end!")


