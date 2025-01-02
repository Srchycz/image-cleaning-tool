from src.data_cleaning import similarity_detection
from src.utils import file_io

path = "../samples"
template = file_io.read_image("../samples/template.jpg")
print(type(template))
images = file_io.read_images(path)

print(len(images))
similarity_detection.detect_similarity_images(images, template)