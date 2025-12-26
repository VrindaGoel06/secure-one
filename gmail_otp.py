import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SecureOneOTP:
    def __init__(self):
        
        self.gmail_user = "puneetk0207@gmail.com"         # meri mail id
        self.gmail_password = "ypwe chhd crul mzsg"     # gamil wala password 16 digit wala
        self.sender_name = "teamSecureOne"
    
    def send_otp_email(self, user_email, user_name=""):
        """OTP email bhejna"""
        otp = str(random.randint(100000, 999999))
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "SecureOne OTP"
            msg['From'] = f"{self.sender_name} <{self.gmail_user}>"
            msg['To'] = user_email
            
            html = f"""<div>Your OTP is: <b>{otp}</b></div>"""
            msg.attach(MIMEText(html, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            print(f"OTP sent: {otp}")
            return {"success": True, "otp": otp}
            
        except Exception as e:
            print(f"Error: {e}")
            return {"success": False, "error": str(e)}