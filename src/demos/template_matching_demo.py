from src.data_cleaning import template_matching
from src.utils import file

path = "../samples"
template = file.read_image("../samples/template.png")

images = file.read_images(path)
print(len(images))
template_matching(images, template)

print("end!")