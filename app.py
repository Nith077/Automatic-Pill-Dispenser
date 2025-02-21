from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
import RPi.GPIO as GPIO
import time
import os

cred = credentials.Certificate("/home/pi/Documents/team 19/medify-a650e-firebase-adminsdk-o70nc-ee64d72dc4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medify-a650e-default-rtdb.firebaseio.com/'
})

firebase_db = db.reference()

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servo_pins = {'Paracetamol': [26,3,53], 'Metformin': [12,3,31], 'Lisinopril': [6, 3,35], 'Amoxicillin': [18,3, 35]}
config = {}

def initialize_pwm(pin):
    if pin not in config:
        pwm = GPIO.PWM(pin, 50)
        pwm.start(0)
        config[pin] = pwm
    else:
        pwm = config[pin]
    return pwm

GPIO.cleanup()


for med, pin in servo_pins.items():
    GPIO.setup(pin[0], GPIO.OUT)
    initialize_pwm(pin[0])

def angle_to_duty_cycle(angle):
    return (angle / 18) + 2.5

def move_servo(angle, pwm):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)

def add_spaces_at_eof_and_save(file_path, num_spaces=1):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    modified_lines = lines + [' ' * num_spaces + '\n']
    with open(file_path, 'w') as f:
        f.writelines(modified_lines)


@app.route('/')
def index():
    return render_template('index.html', message="")

@app.route('/update_message', methods=['POST'])
def update_message():
    try:
        user_id = request.form['user_id']
        doc_ref = firebase_db.child("Prescriptions").child(user_id)
        doc = doc_ref.get()

        if doc is not None:
            data = doc
            if 'purchase' in data and not data['purchase']:
                message = "Please pay to get medicines"
            else:
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                for med, pin in servo_pins.items():
                    GPIO.setup(pin[0], GPIO.OUT)
                    initialize_pwm(pin[0])
                user_meds = [key for key in data if key != 'purchase']
                
                for med in user_meds:
                    move_servo(servo_pins[med][1], config[servo_pins[med][0]])
                    time.sleep(1.0)
                    move_servo(servo_pins[med][2], config[servo_pins[med][0]])
                    
                for med,pwm in config.items():  
                    pwm.stop()  
                GPIO.cleanup()
                doc_ref.update({'purchase': False})
                
                file_path = "/home/pi/Documents/team 19/Dispenser/app.py"
                add_spaces_at_eof_and_save(file_path)
                
                message = "Medicine dispensed successfully"
                render_template('index.html', message=message)
                #doc_ref.update({'purchase': False})
        else:
            message = "No prescriptions available" 
    except Exception as e:
        message = f"Error: {str(e)}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True,port=5000)


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
