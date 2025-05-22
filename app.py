from flask import Flask, render_template, request
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Mapeamento correto de nomes para e-mails
clientes_emails = {
    "Gustavo": "g7761273@gmail.com",
    "Suporte": "suporte@proprinter.com.br",
    "Impressora": "impressoras@proprinter.com.br",
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

    # Enviar e-mail real
    try:
        email_user = os.environ.get("EMAIL_USER")
        email_pass = os.environ.get("EMAIL_PASS")

        if not email_user or not email_pass:
            return "Credenciais de e-mail não configuradas.", 500

        msg = EmailMessage()
        msg["Subject"] = "Técnico a caminho - ProPrinter"
        msg["From"] = email_user
        msg["To"] = email_cliente
        msg.set_content(f"Olá {nome_cliente},\n\nUm técnico da ProPrinter está a caminho do seu local.\n\nAtenciosamente,\nEquipe ProPrinter")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)

        return f"Notificação enviada para {nome_cliente} no email {email_cliente}!"
    except Exception as e:
        return f"Erro ao enviar e-mail: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
