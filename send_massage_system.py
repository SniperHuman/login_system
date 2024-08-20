import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# メールの送信者と受信者の情報
receiver_email = "spider0713@icloud.com"
sender_email = "bunnun.login.system202@gmail.com"
password = "jrauylrbzghybesp"  # 通常のパスワードを使用

# メールの内容を設定
subject = "書道教室文運ログインシステム"
body = "This is a test email sent from Python."

# メールのメッセージを作成
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

# GmailのSMTPサーバーに接続
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # TLS（Transport Layer Security）を開始
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()