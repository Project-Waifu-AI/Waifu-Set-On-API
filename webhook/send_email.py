import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configs import config  

SERVER = 'smtp.gmail.com'
PORT = 587
MY_EMAIL = config.email
MY_PASSWORD = config.password_email

def send_verify_token(target_email: str, token: str):
    msg = MIMEMultipart()

    subject = "Konfirmasi Token untuk Aplikasi WaifuSetOn"
    sender_name = "Tim WaifuSetOn"
    sender_email = "no-reply@waifuseton.com"  # Email dari domain aplikasi Anda
    
    # Pesan dalam format HTML
    message_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="background-color: #f4f4f4; padding: 20px;">
            <h2 style="color: #333;">{subject}</h2>
            <p>Dear User,</p>
            <p>Thank you for choosing WaifuSetOn. Here is your confirmation token:</p>
            <p style="font-size: 18px; background-color: #ddd; padding: 10px;">{token}</p>
            <p>Please use this token to access our features and verify your identity in the WaifuSetOn app.</p>
            <p>If you did not initiate this request, please disregard this message. Thank you for your support!</p>
            <p style="margin-top: 20px;">Best regards,</p>
            <p>{sender_name}</p>
        </div>
    </body>
    </html>
    """

    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = subject

    # Set jenis konten email ke HTML
    msg.attach(MIMEText(message_body, 'html'))
    server = smtplib.SMTP(SERVER, PORT)
    try:
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(sender_email, target_email, msg.as_string())
        print('Email berhasil dikirim!')
        return True
    except Exception as e:
        print('Terjadi kesalahan:', str(e))
        return str(e)
    finally:
        server.quit()

def send_password_change(target_email: str, access_token):
    msg = MIMEMultipart()

    subject = "Password Reset - WaifuSetOn (WSO)"
    sender_name = "WSO Support Team"
    sender_email = "support@waifuseton.com"  # Email dari domain aplikasi Anda
    
    # Pesan dalam format HTML
    message_body = f"""
    <html>
        <body>
            <p>Dear WSO User,</p>
            <p>We have received a request to reset the password for your WaifuSetOn (WSO) account.</p>
            <p>If you initiated this request, please click the button below to proceed with the password reset:</p>
            <a href="http:localhost:3000/change-password?access_token={access_token}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Reset Password</a>
            <p>If you did not request a password reset, kindly ignore this email. Your account security is important to us.</p>
            <p>Best regards,<br>{sender_name}</p>
        </body>
    </html>
    """

    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = target_email
    msg['Subject'] = subject

    # Set jenis konten email ke HTML
    msg.attach(MIMEText(message_body, 'html'))
    server = smtplib.SMTP(SERVER, PORT)
    try:
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(sender_email, target_email, msg.as_string())
        print('Email berhasil dikirim!')
        return True
    except Exception as e:
        print('Terjadi kesalahan:', str(e))
        return str(e)
    finally:
        server.quit()