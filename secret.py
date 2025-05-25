from flask import Flask, jsonify
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Email server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "mygmailaddress@gmail.com"
EMAIL_PASSWORD = "CREDENTIALS" # Replace with your actual email password

givers = [
    {'name': 'Pedro Pascal', 'email': 'ppascal@gmail.com'},
    {'name': 'Jhony Cash', 'email': 'jcash@gmail.com'}, 
    {'name': 'Ana de Armas', 'email': 'aarmas@gmail.com'}, 
    {'name': 'Juan Gabriel', 'email': 'jgabriel@gmail.com'}, 
    {'name': 'Luke Cage', 'email': 'lcage@gmail.com'},
    {'name': 'Cristian Castro', 'email': 'ccastro@gmail.com'}, 
    {'name': 'Roberto Carlos', 'email': 'rcarlos@gmail.com'}, 
    {'name': 'Cristiano Ronaldo', 'email': 'cronaldo@gmail.com'}, 
    {'name': 'Scarlett Johansson', 'email': 'sjohansson@gmail.com'}, 
    {'name': 'Leonel Messi', 'email': 'lmessi@gmail.com'} 
]

excludes = {
    'Pedro Pascal': ['Jhony Cash', 'Ana de Armas'],
    'Jhony Cash': ['Pedro Pascal', 'Ana de Armas'],
    'Ana de Armas': ['Pedro Pascal', 'Jhony Cash'],
    'Juan Gabriel': ['Luke Cage', 'Cristian Castro'],
    'Luke Cage': ['Juan Gabriel', 'Cristian Castro'],
    'Cristian Castro': ['Juan Gabriel', 'Luke Cage'],
    'Roberto Carlos': ['Cristiano Ronaldo', 'Scarlett Johansson'],
    'Cristiano Ronaldo': ['Roberto Carlos', 'Scarlett Johansson'],
    'Scarlett Johansson': ['Roberto Carlos', 'Cristiano Ronaldo'],
    'Leonel Messi': ['Pedro Pascal', 'Jhony Cash']
}

# Dictionary to store each person's assignments
assignments = {}

def gen_secret_santa():
    global assignments
    restart = True

    while restart:
        restart = False
        receivers = givers[:]
        temp_assignments = {}

        for giver in givers:
            giver_name = giver['name']
            possible_receivers = [
                receiver for receiver in receivers
                if receiver['name'] != giver_name and receiver['name'] not in excludes.get(giver_name, [])
            ]

            if not possible_receivers:
                restart = True
                break

            receiver = random.choice(possible_receivers)
            temp_assignments[giver_name] = receiver
            receivers.remove(receiver)
    
    assignments = temp_assignments

def send_secret_santa_email(receiver_email, giver_name, receiver_name):
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = receiver_email
    message["Subject"] = "🎅 ¡Tu amigo secreto ha sido asignado!"

    body = f"""
    <p>Hola {giver_name},</p>
    <p>Te ha tocado regalarle a: <strong>{receiver_name}</strong>.</p>
    <p>¡Diviértete planeando tu regalo!</p>
    """
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, receiver_email, message.as_string())
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error while sending email to {receiver_email}: {e}")

# Send mail to each participant after the assignment
def notify_participants():
    for giver_name, receiver in assignments.items():
        giver = next((g for g in givers if g['name'] == giver_name), None)
        if giver:
            send_secret_santa_email(giver['email'], giver_name, receiver['name'])

# We generate the assignments and notify at the beginning
gen_secret_santa()

@app.route('/send-emails', methods=['GET'])
def send_emails():
    notify_participants()
    return jsonify({"status": "Correos enviados a todos los participantes"}), 200

if __name__ == '__main__':
    app.run(debug=True)
