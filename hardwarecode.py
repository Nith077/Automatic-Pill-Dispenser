import firebase_admin
from firebase_admin import credentials,auth,firestore
from firebase_admin._auth_utils import UserNotFoundError

cred = credentials.Certificate(r"C:\Amrita College\DIL Lab\Online Medic\Medify\medify-a650e-firebase-adminsdk-o70nc-ee64d72dc4.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

while True:
    try:
        #user_id = input("Enter your UID : ")
        user_id = R6s3id0yJ1Z7QGzBMhP3idXWbgl1
        user = auth.get_user(user_id)

        doc_ref = db.collection("Prescriptions").document(user.uid)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if(data['purchase'] == False) :
                print("Please Pay to get medicines")
            else :
                user_meds = [key for key in data if key != 'purchase']
                print(user_meds)
                doc_ref.update({
                    'purchase' : False
                })

        else:
            print("No prescriptions available")
    except UserNotFoundError:
        print('User does not exist')
