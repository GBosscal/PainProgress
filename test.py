"""
@Project: BackendForPain
@File: test.py
@Auth: Bosscal
@Date: 2023/10/20
@Description: 
"""
import cv2

from pain_model.convert import pain_convert

image_path = "pain_data/patient_5/11.jpeg"
new_image_path = "pain_data/patient_5/11_new.jpeg"

cv_img = cv2.imread(image_path)
img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
result = pain_convert(img, cv_img)
cv2.imwrite(new_image_path, result)
print(result)

