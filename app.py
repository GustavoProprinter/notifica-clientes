import os
import smtplib
from flask import Flask, render_template, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Dicionário para mapear nome do cliente para email
clientes_emails = {
    "Gustavo": "gustavo@proprinter.com.br",
    "Suporte": "suporte@proprinter.com.br",
    "Impressora": "impressora@proprinter.com.br",
    "Felipe": "felipe@proprinter.com.br"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/avisar", methods=["POST"])
def avisar():
    nome_cliente = request.form.get("nome_cliente")
    email_cliente = clientes_emails.get(nome_cliente)

    if not email_cliente:
        return f"Cliente {nome_cliente} não encontrado.", 400

    # Conteúdo do e-mail
    assunto = "Técnico a caminho"
    corpo = f"Olá {nome_cliente}, o técnico da ProPrinter está a caminho para atendimento do seu chamado."

    # Monta o e-mail
    msg = MIMEMultipart()
    msg["From"] = os.environ.get("EMAIL_USER")
    msg["To"] = email_cliente
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
            servidor.sendmail(msg["From"], msg["To"], msg.as_string())
    except Exception as e:
        return f"Erro ao enviar e-mail: {e}", 500

    return f"Notificação enviada para {nome_cliente} no email {email_cliente}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

