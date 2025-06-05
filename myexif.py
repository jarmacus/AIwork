from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_data(image_path):
    # 打开图像文件
    image = Image.open(image_path)

    # 获取 EXIF 信息
    exif_data = image._getexif()

    if exif_data is not None:
        # 解析 EXIF 标签并获取可读的标签名称
        exif_info = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif_info[tag_name] = value
        return exif_info
    else:
        return None


# 示例：读取图像 EXIF 信息
image_path = 'C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\Alice.jpg'
exif_data = get_exif_data(image_path)

if exif_data:
    for key, value in exif_data.items():
        print(f"{key}: {value}")
else:
    print("No EXIF data found.")
