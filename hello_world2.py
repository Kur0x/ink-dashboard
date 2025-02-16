# epd_framebuf_test.py
import machine
import framebuf
from time import sleep_ms
import epaper7in5b  # 请确保该驱动文件已上传到设备

# -------------------------------
# 设置屏幕分辨率（根据你的墨水屏规格调整）
# -------------------------------
w = 640
h = 384

# -------------------------------
# 创建黑色显示缓冲区
# -------------------------------
# 分配一块内存，每个像素1 bit，故总字节数为 w * h / 8
buf_black = bytearray(w * h // 8)
# 利用 framebuf 创建一个帧缓存对象，使用 MONO_HLSB 模式
fb_black = framebuf.FrameBuffer(buf_black, w, h, framebuf.MONO_HLSB)
# 用 1 填充整个画布（即白色背景）
fb_black.fill(1)

# -------------------------------
# 创建红色显示缓冲区
# -------------------------------
buf_red = bytearray(w * h // 8)
fb_red = framebuf.FrameBuffer(buf_red, w, h, framebuf.MONO_HLSB)
fb_red.fill(1)

# -------------------------------
# 在黑色缓冲区上绘制图形（黑色部分）  
# 注意：framebuf中绘图时，像素“0”表示绘制（即黑色），而“1”表示空白（白色）
# -------------------------------
fb_black.text("Hello, 棒棒的Black!", 50, 50, 0)   # 在坐标(50,50)处绘制文字，颜色0（黑色）
fb_black.rect(40, 40, 200, 50, 0)             # 绘制一个矩形轮廓
fb_black.line(50, 100, 300, 100, 0)            # 绘制一条直线

# -------------------------------
# 在红色缓冲区上绘制图形（红色部分）
# -------------------------------
fb_red.text("Red Alert!", 300, 200, 0)        # 在坐标(300,200)处绘制文字，颜色0（红色区域将由此缓冲区控制）
fb_red.fill_rect(290, 190, 150, 80, 0)         # 绘制一个填充矩形

# -------------------------------
# 初始化电子墨水屏
# -------------------------------
# 定义引脚（请根据你的硬件连接情况修改）
MOSI = machine.Pin(0)                     # SPI 数据输入 (MOSI)
SCK  = machine.Pin(1)                     # SPI 时钟
cs   = machine.Pin(2, machine.Pin.OUT)     # 片选
dc   = machine.Pin(3, machine.Pin.OUT)     # 数据/命令控制
rst  = machine.Pin(4, machine.Pin.OUT)     # 复位
busy = machine.Pin(5, machine.Pin.IN)      # 屏幕忙信号

# 初始化 SPI（频率、极性和相位根据实际需求调整）
spi = machine.SPI(1, baudrate=2000000, polarity=0, phase=0, sck=SCK, mosi=MOSI)

# 创建墨水屏对象
epd = epaper7in5b.EPD(spi, cs, dc, rst, busy)
print("初始化墨水屏...")
epd.init()

# -------------------------------
# 将绘制好的缓冲区数据发送给墨水屏并刷新显示
# -------------------------------
print("刷新显示...")
epd.display_frame(buf_black, buf_red)

# 显示3秒后进入休眠模式
sleep_ms(3000)
print("进入休眠模式...")
epd.sleep()

print("测试完成。")
