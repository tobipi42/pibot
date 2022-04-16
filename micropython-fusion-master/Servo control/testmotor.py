
import RPi.GPIO as GPIO
import time

# motor_EN_A: Pin7         |  motor_EN_B: Pin11
# motor_A:  Pin8, Pin10    |  motor_B: Pin13, Pin12

Motor_A_EN    = 25
# Motor_B_EN    = 17

Motor_A_Pin1  = 23
Motor_A_Pin2  = 24
# Motor_B_Pin1  = 27
# Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

pwm_A = 0
# pwm_B = 0


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor_A_EN, GPIO.OUT)
#     GPIO.setup(Motor_B_EN, GPIO.OUT)
GPIO.setup(Motor_A_Pin1, GPIO.OUT)
GPIO.setup(Motor_A_Pin2, GPIO.OUT)
#     GPIO.setup(Motor_B_Pin1, GPIO.OUT)
#     GPIO.setup(Motor_B_Pin2, GPIO.OUT)
pwm_A = GPIO.PWM(Motor_A_EN, 1000)
#         pwm_B = GPIO.PWM(Motor_B_EN, 1000)


try:
  while True:
      GPIO.output(Motor_A_Pin1, GPIO.HIGH)
      GPIO.output(Motor_A_Pin2, GPIO.LOW)
      pwm_A.start(100)
      pwm_A.ChangeDutyCycle(75)


except KeyboardInterrupt:
    # def motorStop():#Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    #     GPIO.output(Motor_B_Pin1, GPIO.LOW)
    #     GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    #     GPIO.output(Motor_B_EN, GPIO.LOW)

    GPIO.cleanup()             # Release resource
    
    