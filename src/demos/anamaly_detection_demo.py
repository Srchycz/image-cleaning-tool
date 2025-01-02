from src.data_cleaning import anomaly_detection
from src.utils import file_io

path = "../samples"

images = file_io.read_images(path)
print(len(images))
anomaly_detection.detect_anomaly_values(images)
print("亮度检测完成")
anomaly_detection.detect_color_biases(images)

print("end!")