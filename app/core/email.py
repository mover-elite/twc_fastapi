from pydantic import EmailStr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl


password = "tradewithchun"
app_password = "vcmoxpwxijlkqzxs"
username = "tradchun@gmail.com"
port = 465  # For SSL
context = ssl.create_default_context()


def parse_otp_mail(otp: str, name: str, for_: str) -> str:
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


def parse_message(message: str, to: str, subject: str) -> str:
    email_message = MIMEMultipart()
    email_message["To"] = to
    email_message["From"] = username
    email_message["Subject"] = subject
    email_message.attach(MIMEText(message, "html"))
    email_string = email_message.as_string()
    return email_string


def send_verification_message(email_address: EmailStr, otp: str):
    subject = "Email Verification"
    message = parse_otp_mail(otp, "Mover", subject)
    email_string = parse_message(message, email_address, subject)
    send_otp_through_smtp(email_address, email_string)


def send_otp_through_smtp(to: EmailStr, message: str) -> None:
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(username, app_password)
        server.sendmail(username, to, message)


def send_password_change_mail(email_address: EmailStr, otp: str, name: str):
    html = parse_otp_mail(otp, name, "Change Password")
    email_string = parse_message(html, email_address, "Change Password")
    send_otp_through_smtp(email_address, email_string)
    return True
