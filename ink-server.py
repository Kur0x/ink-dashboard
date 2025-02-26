import os
from flask import Flask, Response
import io
from PIL import Image
current_file_path = os.path.dirname(os.path.abspath(__file__))

# 单色图像转换函数
def convert_to_monochrome(image, color_type='black'):
    """
    将图像转换为黑色或红色单色图像的字节流。
    
    :param image: 输入的 PIL 图像对象（RGB）
    :param color_type: 'black' 表示黑色图像，'red' 表示红色图像
    :return: 转换后的字节流
    """
    width, height = image.size
    pixel_data = image.getdata()
    byte_array = bytearray()

    for i in range(0, len(pixel_data), 8):
        byte = 0
        for j in range(8):
            if i + j < len(pixel_data):
                r, g, b = pixel_data[i + j]
                if color_type == 'black':
                    # 黑色图像：黑色（RGB < 128）为 0，其他为 1
                    pixel = 0 if (r < 128 and g < 128 and b < 128) else 1
                elif color_type == 'red':
                    if r > 128 and g < 100 and b < 100:
                        pixel = 0  # 红色
                    else:
                        pixel = 1  # 白色
                byte = (byte << 1) | pixel
        byte_array.append(byte)
    # if byte_array.size
    return byte_array

# @app.route('/get_image/<color_type>', methods=['GET'])
def get_image(color_type):
    """
    根据 color_type 参数返回黑色或红色图像。
    
    :param color_type: 图像类型 ('black' 或 'red')
    :return: 图像的字节流
    """
    if color_type not in ['black', 'red']:
        return "Invalid color type. Use 'black' or 'red'.", 400

    # 读取 3 色 BMP 图像
    image_path = current_file_path +'/dashboard5.bmp'
    image = Image.open(image_path)
    image = image.convert('RGB')  # 转换为 RGB 格式

    # 获取转换后的图像字节流
    byte_array = convert_to_monochrome(image, color_type)

    # 返回字节流数据
    return Response(bytes(byte_array), mimetype='application/octet-stream')

if __name__ == '__main__':
    app = Flask(__name__)
    app.add_url_rule('/get_image/<color_type>', 'get_image', get_image, methods=['GET'])
    app.run(host='0.0.0.0', port=25001)
