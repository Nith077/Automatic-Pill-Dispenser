import RPi.GPIO as GPIO
import time

# Set the GPIO mode and the pin number
GPIO.setmode(GPIO.BCM)
servo_pins = {'para':13,'dolo':21,'serflo':12}
config = {}
user_meds = ['para','dolo','serflo']

# Set the GPIO pin as an output
for med,pin in servo_pins.items():
    GPIO.setup(pin, GPIO.OUT)

# Create a PWM instance
for med,pin in servo_pins.items():
    config[med] = GPIO.PWM(pin, 50)  # 50 Hz (20 ms PWM period)

# Function to convert angle to duty cycle
def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2.5
    return duty_cycle

# Function to move the servo to a specific angle
def move_servo(angle,pwm):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Wait for the servo to move

# Main function
if __name__ == "__main__":
    try:
        for med,pwm in config.items():
            pwm.start(0)  # Start PWM with 0% duty cycle
        for i in range(1):
            for med in user_meds:
                move_servo(float(1),config[med])
                time.sleep(1.0)
                move_servo(float(90),config[med])

    except KeyboardInterrupt:
        for med,pwm in config.items():
            pwm.stop()  
        GPIO.cleanup()  
