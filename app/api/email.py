# API_KEY = "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"
# new_key = "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"
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import smtplib
import ssl, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .jwt_config import encode_jwt

env = "test"
domain = "http://localhost:5000" if env == "test" else "http://145.239.185.57:5000"


password = "tradewithchun"
app_password = "vcmoxpwxijlkqzxs"
username = "tradchun@gmail.com"
port = 465  # For SSL
context = ssl.create_default_context()


def send_forget_password_email(email_address):
    payload = {"for": "forget_password", "email": email_address}
    jwt_code = encode_jwt(json.dumps(payload))
    body = "Click the button below to reset your password"
    message = parse_verification_email(
        "Reset Password", body, "verify_password_reset", jwt_code, "Reset Password"
    )
    email_string = parse_message(message, email_address, "Reset Password")
    send_otp_through_smtp(email_address, email_string)
    return jwt_code


def parse_verification_email(subject, body, route, verification_link, button):
    html = f"""
    <html>
        <body>
            <h1>{subject}</h1>
            <h3 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">
                {body}
            </h3>

            <a href="{domain}/{route}/{verification_link}">
                <button style="font-size: 18px; text-decoration: none"> {button} </button>
            </a>
        </body>
    </html>
    """
    return html


def parse_otp_mail(otp, name, for_):
    html = f"""
    <html>
        <body style="font-family:Georgia, 'Times New Roman', Times, serif">
            <h1>OTP for {for_}</h1>
            <h3>
                Dear {name} below is the opt verification for {for_}
            </h3>

            <h1>{otp} </h1>
        </body>
    </html>
    """
    return html


def parse_message(message, to, subject):
    email_message = MIMEMultipart()
    email_message["To"] = to
    email_message["From"] = username
    email_message["Subject"] = subject
    email_message.attach(MIMEText(message, "html"))
    email_string = email_message.as_string()
    return email_string


def send_password_change_alert(email):
    subject = "Password Update Alert"
    body = "<h2>You just reset your password</h2><p>If this is not you please contact our customer service</p>"
    message_string = parse_message(body, email, subject)
    send_otp_through_smtp(email, message_string)


def send_verification_message(email_address, otp):
    subject = "Email Verification"
    message = parse_otp_mail(otp, "Mover", subject)
    email_string = parse_message(message, email_address, subject)
    send_otp_through_smtp(email_address, email_string)


def send_email(email_address, subject, message):
    email_message = MIMEMultipart()
    email_message["To"] = email_address
    email_message["From"] = username
    email_message["Subject"] = subject
    email_message.attach(MIMEText(message, "html"))
    email_string = email_message.as_string()
    send_otp_through_smtp(email_address, email_string)


def send_otp_through_smtp(to, message):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(username, app_password)
        server.sendmail(username, to, message)

