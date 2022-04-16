from picamera import PiCamera
from time import sleep

camera = PiCamera()

sleep(5)
camera.capture('/home/pi/LidarProject/captureImg.jpg')
