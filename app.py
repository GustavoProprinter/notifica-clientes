from flask import Flask, render_template, request
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Clientes e emails
clientes_emails = {
    "Gustavo": "suporte@proprinter.com.br",
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
    tecnico = request.form.get("tecnico")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    email_cliente = clientes_emails.get(nome_cliente)
    if not email_cliente:
        return f"Cliente {nome_cliente} não encontrado.", 400

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    if not email_user or not email_pass:
        return "Configurações de email não encontradas.", 500

    # Monta link do Google Maps
    link_maps = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude and longitude else "Localização não informada"

    # Monta mensagem do email
    corpo_email = f"""
    Técnico: {tecnico}
    Cliente: {nome_cliente}
    Localização atual do técnico: {link_maps}
    """

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_cliente
    msg['Subject'] = "Técnico a caminho - ProPrinter"
    msg.attach(MIMEText(corpo_email, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, email_cliente, msg.as_string())
        server.quit()
    except Exception as e:
        return f"Erro ao enviar email: {e}", 500

    return f"Notificação enviada para {nome_cliente} no email {email_cliente}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
