import torch
from torchvision import transforms
from PIL import Image
import os
import torch.nn.functional as F


def classify_image(input_dir,image_file):
    # 加载保存的 VGG16 模型
    vgg16 = torch.load("C:\\Users\\86178\\Desktop\\计软大作业\\.venv\\vgg.pth")
    vgg16.eval()

    # 类别映射字典
    class_map = {
        0: 'person',
        1: 'bicycle',
        2: 'car',
        3: 'motorbike',
        4: 'aeroplane',
        5: 'fruit',
        6: 'train',
        7: 'truck',
        8: 'boat',
        9: 'traffic light',
        10: 'ocean',
        11: 'stop sign',
        12: 'mountain',
        13: 'sun',
        14: 'bird',
        15: 'cat',
        16: 'dog',
        17: 'building',
        18: 'flower',
        19: 'sports'
    }

    # 图像预处理
    transform_set = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    # 配置设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    vgg16.to(device)


    image_path = os.path.join(input_dir, image_file)
    image_path = image_file.replace('\\', '/')  # 替换路径中的反斜杠

    # 加载图像并预处理
    image = Image.open(image_path).convert('RGB')  # 确保图像是 RGB 格式
    image = transform_set(image).unsqueeze(0)  # 添加 batch 维度
    image = image.to(device)

    # 模型预测
    with torch.no_grad():
        output = vgg16(image)
        output = torch.sigmoid(output)  # 使用 sigmoid 激活函数，得到每个标签的概率

    # 应用阈值进行二分类
    predicted_labels = (output > 0.628).float()

    # 获取预测的类名
    predicted_classes = [class_map[idx] for idx, val in enumerate(predicted_labels[0]) if val == 1]

    # 输出结果
    print(f"图片: {image_file}")
    print("预测的类别:")
    if predicted_classes:
        for cls in predicted_classes:
            print(f"- {cls}")
    else:
        print("未检测到任何类别")
    print("=" * 30)
    return ",".join(predicted_classes) if predicted_classes else None

# 使用示例
# input_dir = "C:\\Users\\86178\\Desktop\\计软大作业\\输入图片文件夹"  # 替换为实际文件夹路径
# classify_image(input_dir)
