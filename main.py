import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pins = {'para':[26,1,42],'dolo':[12,1,40],'serflo':[6,19]}
config = {}
user_meds = ['para','dolo']



for med,pin in servo_pins.items():
    GPIO.setup(pin[0], GPIO.OUT)

for med,pin in servo_pins.items():
    config[med] = GPIO.PWM(pin[0], 50) 

def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2.5
    return duty_cycle

def move_servo(angle,pwm):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5) 

if __name__ == "__main__":
    try:
        for med,pwm in config.items():
            pwm.start(0)  
        
        for med in user_meds:
            move_servo(float(servo_pins[med][1]),config[med])
            time.sleep(1.0)
            move_servo(float(servo_pins[med][2]),config[med])
        
        for med,pwm in config.items():
            pwm.stop()  
        GPIO.cleanup() 

    except KeyboardInterrupt:
        for med,pwm in config.items():
            pwm.stop()  
        GPIO.cleanup()  

