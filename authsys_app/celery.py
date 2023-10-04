# celery.py
from celery import Celery
from flask import Flask
from authsys_app import app

celery = Celery(
    app.import_name,
    backend=app.config['CELERY_RESULT_BACKEND'],
    broker=app.config['CELERY_BROKER_URL']
)
celery.conf.update(app.config)

@celery.task
def send_confirmation_email_task(email, fname, confirmation_token):
    print("Sending confirmation email to:", email)
    try:
        subject = "Registration Confirmation"
        body = f"Dear {fname},\n\nThank you for registering on YourApp! Your account has been successfully created.\n\nPlease click the following link to confirm your registration:\n\n{url_for('confirm', token=confirmation_token, _external=True)}"
        msg = Message(subject=subject, recipients=[email], body=body)
        mail.send(msg)
        print("Confirmation email sent successfully!")
    except Exception as e:
        print("Error sending confirmation email:", e)