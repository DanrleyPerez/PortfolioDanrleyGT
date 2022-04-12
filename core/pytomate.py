import smtplib, ssl
from email.mime.text import MIMEText


def enviar_email(remetente, destinatario, mensagem, assunto):
    port = 465  # For SSL
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("danrley2109@gmail.com", "xenmorkvoyxghcnx")
        mensagem = MIMEText(mensagem)
        mensagem['Subject'] = assunto
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        server.sendmail(remetente, destinatario, mensagem.as_string())



