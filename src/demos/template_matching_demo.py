from src.data_cleaning import template_matching
from src.utils import file_io

path = "../samples"
template = file_io.read_image("../samples/template.jpg")
images = file_io.read_images(path)
print(len(images))
template_matching(images, template)

print("end!")