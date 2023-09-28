import cv2
import numpy as np
import torch
import os
from Model import mini_XCEPTION

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print("devicea:",device)
#使用GPU如果没有就使用CPU

def preprocess_input(x):
    x = x.astype('float32')  # 将输入转换为 float32 数据类型
    x = x / 255.0  # 将像素值缩放到 [0, 1] 范围
    x = x - 0.5  # 减去 0.5，使得像素值范围变为 [-0.5, 0.5]
    x = x * 2.0  # 将像素值范围缩放到 [-1, 1]
    return torch.tensor(x)  # 将处理后的输入转换为 PyTorch 的张量并返回


detection_model_path = 'weight/haarcascade_frontalface_default.xml'#人脸模型权重
emotion_model_path = 'weight/E135_0.6466.pth'#权重
emotion_labels={0:'pain1', 1:'non_pain', 2:'pain0', 
                3:'non_pain', 4:'pain1', 5:'non_pain',6:'pain0'}
face_detection = cv2.CascadeClassifier(detection_model_path)#人脸检测器
model = mini_XCEPTION(num_classes=7).to(device)
model.load_state_dict(torch.load(emotion_model_path,map_location=device))
#加载权重和GPU

def pain_convert(img,src):
    input_size = (48, 48)
    #转换为灰度图
    faces = face_detection.detectMultiScale(img, scaleFactor=1.1, minNeighbors=8)
    with torch.no_grad():
        for face_coordinates in faces:
            x, y, w, h = face_coordinates
            #提取坐标
            gray_face = img[y:y + h, x:x + w]
            #获取人脸的完整区域
            try:
                gray_face = cv2.resize(gray_face, input_size)
                #调整人脸大小，如果可以调整则调整，否则选择下一张图片
            except:
                continue
            gray_face = preprocess_input(gray_face)#预处理，归一化，缩放等
            inp = torch.unsqueeze(gray_face, 0)
            inp = torch.unsqueeze(inp, 0)
            inp=inp.to(device)
            #emotion_label_arg = np.argmax(model(inp)).item()
            emotion_label_arg = torch.argmax(model(inp).cpu(), dim=1).item()
            #首先通过模型 model 对输入张量 inp 进行推理，得到模型的输出结果。
            # .cpu() 用于将计算结果移动到 CPU 上
            #使用 torch.argmax() 函数在指定维度上取得输出结果中最大值的索引。
            # 在这里，我们选择 dim=1，表示在输出结果的第二个维度（即类别维度）上寻找最大值。
            # 这将返回一个包含最大值索引的张量。
            #最后，使用 .item() 方法将最大值索引转换为 Python 中的标量值，
            # 存储在 emotion_label_arg 变量中。这样，我们获得了预测的情绪标签的整数编码
            emotion_text = emotion_labels[emotion_label_arg]
            #取出对应的值
            print("predict：", emotion_text)
            cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 1)
            #框住人脸
            cv2.putText(src, emotion_text, (x, y +h+ 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            #把标签写在图片里面
    return src
    #cv2.imshow("Image Window",src)
    #cv2.waitKey(0)  # 等待用户按下任意键
    #cv2.destroyAllWindows()  # 关闭所有OpenCV窗口
'''   
if __name__=='main':
    path='test/11.jpeg'
    src = cv2.imread(path)
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    pain_convert(img,src)
'''

    

