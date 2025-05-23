from flask import Flask, render_template, request
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Dados dos clientes e e-mails
clientes_emails = {
    "Gustavo": "suporte@proprinter.com.br",
    "Suporte": "suporte@proprinter.com.br",
    "Impressora": "impressoras@proprinter.com.br",
    "Felipe": "felipe@proprinter.com.br"
}

# Última localização recebida (variável global simples)
ULTIMA_LOCALIZACAO_URL = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/avisar", methods=["POST"])
def avisar():
    nome_cliente = request.form.get("nome_cliente")
    nome_tecnico = request.form.get("nome_tecnico")
    email_cliente = clientes_emails.get(nome_cliente)

    if not email_cliente:
        return f"Cliente {nome_cliente} não encontrado.", 400

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    if not email_user or not email_pass:
        return "Configurações de email não encontradas.", 500

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_cliente
    msg['Subject'] = "Técnico a caminho - ProPrinter"

    body = f"""
    Olá {nome_cliente},

    O técnico {nome_tecnico} está a caminho.

    """
    if ULTIMA_LOCALIZACAO_URL:
        body += f"Acompanhe a localização em tempo real: {ULTIMA_LOCALIZACAO_URL}\n\n"
    else:
        body += "A localização do técnico ainda não está disponível.\n\n"

    body += "Atenciosamente,\nProPrinter"

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, email_cliente, msg.as_string())
        server.quit()
    except Exception as e:
        return f"Erro ao enviar email: {e}", 500

    return f"Notificação enviada para {nome_cliente} no email {email_cliente}!"

@app.route("/localizacao", methods=["POST"])
def receber_localizacao():
    global ULTIMA_LOCALIZACAO_URL
    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")
    if lat is None or lon is None:
        return {"error": "Dados inválidos"}, 400

    ULTIMA_LOCALIZACAO_URL = f"https://www.google.com/maps?q={lat},{lon}"
    print(f"Localização atualizada: {ULTIMA_LOCALIZACAO_URL}")
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
