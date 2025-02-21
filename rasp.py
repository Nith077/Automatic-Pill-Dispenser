import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("/home/pi/Documents/team 19/medify-a650e-firebase-adminsdk-o70nc-ee64d72dc4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medify-a650e-default-rtdb.firebaseio.com/'
})
firebase_db = db.reference()

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
servo_pins = {'para': [26, 35], 'dolo': [6, 52], 'serflo': [12, 19]}
config = {}

for med, pin in servo_pins.items():
    GPIO.setup(pin[0], GPIO.OUT)

for med, pin in servo_pins.items():
    config[med] = GPIO.PWM(pin[0], 50)

def angle_to_duty_cycle(angle):
    duty_cycle = (angle / 18) + 2.5
    return duty_cycle

def move_servo(angle, pwm):
    duty_cycle = angle_to_duty_cycle(angle)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)


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
                message = "Please Pay to get medicines"
            else:
                #continue from here
                user_meds = [key for key in data if key != 'purchase']
                for med in user_meds:
                    move_servo(float(1), config[med])
                    time.sleep(1.0)
                    move_servo(float(servo_pins[med][1]), config[med])
                message = "Medicine dispensed successfully"
                doc_ref.update({'purchase': False})
        else:
            message = "No prescriptions available"
    except UserNotFoundError:
        message = 'User does not exist'

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
