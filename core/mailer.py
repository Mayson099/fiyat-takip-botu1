import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_mail(self, to_email, subject, message):
        
        
        
        msg = MIMEMultipart()
        msg["From"] = self.email #gönderen kişi 
        msg["To"] = to_email     #alıcı 
        msg["Subject"] = subject #posta konusu
        msg.attach(MIMEText(message, "plain", "utf-8")) 

        try:
            #belirlenen sunucu ve port üzerinden gmaile bağlan
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls() 
                server.login(self.email, self.password)
                server.send_message(msg)
            
            
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Hata: E-posta veya uygulama şifresi yanlış.")
        except Exception as e:
            print(f"Mail gönderilirken beklenmedik bir hata oluştu: {e}")
        
        return False