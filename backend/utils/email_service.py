from flask_mail import Message
from extensions import mail


def send_staff_email(name,email,password):

    msg = Message(

        subject="Welcome to TrekTramp",

        recipients=[email]

    )

    msg.body = f"""
Hello {name},

Welcome to TrekTramp.

Your staff account has been created.

Email:
{email}

Temporary Password:
{password}

Please login using these credentials.

You will be asked to change your password and complete your profile.

Regards,

TrekTramp Team
"""

    mail.send(msg)