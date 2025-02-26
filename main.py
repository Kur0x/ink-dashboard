import machine
import time
import network
import socket
import urequests  # 用于 HTTP 请求
from epaper5in83b import EPD  # 墨水屏驱动文件
# import epaper7in5b  # 墨水屏驱动文件
import utime
import gc

# ESP32 网络连接设置
wifi_ssid = "23A"
wifi_password = "05722067"
server_url = "http://10.0.0.22:25001/get_image/"  # 获取图像的接口地址
print("start")
print (gc.mem_free())
# 初始化墨水屏
# MOSI = machine.Pin(0)
# SCK = machine.Pin(1)
# cs = machine.Pin(2, machine.Pin.OUT)
# dc = machine.Pin(3, machine.Pin.OUT)
# rst = machine.Pin(4, machine.Pin.OUT)
# busy = machine.Pin(5, machine.Pin.IN)

# 7.5inch
# MOSI = machine.Pin(18)
# SCK = machine.Pin(23)
# cs = machine.Pin(16, machine.Pin.OUT)
# dc = machine.Pin(17, machine.Pin.OUT)
# rst = machine.Pin(5, machine.Pin.OUT)
# busy = machine.Pin(4, machine.Pin.IN)

# 5.83inch
SCK = machine.Pin(19)
MOSI = machine.Pin(23)
rst = machine.Pin(18, machine.Pin.OUT)
dc = machine.Pin(5, machine.Pin.OUT)
cs = machine.Pin(17, machine.Pin.OUT)
busy = machine.Pin(16, machine.Pin.IN)


spi = machine.SPI(1, baudrate=2000000, polarity=0, phase=0, sck=SCK, mosi=MOSI)
epd = EPD(spi, cs, dc, rst, busy)
epd.init()

def connect_wifi():
    print("Connecting to wifi...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.connect(wifi_ssid, wifi_password)
        while not sta_if.isconnected():
            time.sleep(0.5)
    print('Network config:', sta_if.ifconfig())

def wifi_sleep():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)  # 关闭 Wi-Fi 模块，降低功耗

def fetch_image(url):
    try:
        print("Fetching image from server...")
        response = urequests.get(server_url + url)
        if response.status_code == 200:
            image_data = response.content  # 假设图像以字节流格式返回
            return image_data
        else:
            print(f"Error fetching image: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def sleep_until_target():
    sleep_seconds = 60 * 60
    print(f"Sleeping for {sleep_seconds} seconds...")
    # 进入深度睡眠（毫秒）
    machine.deepsleep(sleep_seconds * 1000)

def main():
    while True:
        # 每次醒来都从头开始执行
        connect_wifi()
        image_data_b = fetch_image('black')
        image_data_r = fetch_image('red')
        gc.collect()
        if image_data_b and image_data_r:
            epd.display_frame(image_data_b, image_data_r)  # 假设图像数据格式适合直接显示
        else:
            print("Failed to fetch image.")
        wifi_sleep()   # 关闭 Wi-Fi 降低功耗
        sleep_until_target()  # 进入深度睡眠，等待下次唤醒

if __name__ == "__main__":
    main()
