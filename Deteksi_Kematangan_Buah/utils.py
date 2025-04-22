
import cv2
import numpy as np

def analyze_ripeness(image_path, fruit_type):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    fruit_hsv_ranges = {
    "Pisang": {
        "Mentah": ([35, 50, 50], [85, 255, 255]),
        "Matang": ([20, 100, 100], [30, 255, 255]),
        "Terlalu Matang": ([0, 0, 0], [20, 255, 100])
    },
    "Jeruk": {
        "Mentah": ([40, 50, 50], [80, 255, 255]),
        "Matang": ([10, 150, 100], [25, 255, 255])
    },
    "Apel": {
        "Mentah": ([40, 50, 50], [80, 255, 255]),
        "Matang": ([0, 100, 100], [10, 255, 255])
    },
    "Mangga": {
        "Mentah": ([40, 50, 50], [80, 255, 255]),
        "Matang": ([20, 100, 100], [30, 255, 255]),
        "Terlalu Matang": ([0, 0, 0], [20, 255, 100])

        }
    }

    if fruit_type not in fruit_hsv_ranges:
        return "Buah tidak dikenali"

    ratios = {}
    for stage, (lower, upper) in fruit_hsv_ranges[fruit_type].items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        ratio = np.sum(mask) / (image.shape[0] * image.shape[1])
        ratios[stage] = ratio

    predicted_stage = max(ratios, key=ratios.get)
    return f"{fruit_type} {predicted_stage}"
