from src.data_cleaning import image_quality
from src.utils import file

path = "../samples"

images = file.read_images(path)
print(len(images))
assessment = image_quality.ImageQualityAssessment(image_quality.TenengradAssessment())
assessment.assess_images_quality(images)

print("end!")