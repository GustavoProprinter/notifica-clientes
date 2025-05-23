from flask import Flask, render_template, request
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)

# Mapeamento dos clientes e e-mails
clientes_emails = {
    "Gustavo": "suporte@proprinter.com.br",
    "Suporte": "suporte@proprinter.com.br",
    "Impressora": "impressoras@proprinter.com.br",
    "Felipe": "felipe@proprinter.com.br"
}

# Caminho do arquivo para armazenar localização
LOCALIZACAO_FILE = "ultima_localizacao.json"

def salvar_localizacao(lat, lon):
    with open(LOCALIZACAO_FILE, "w") as f:
        json.dump({"latitude": lat, "longitude": lon}, f)

def carregar_localizacao():
    if not os.path.exists(LOCALIZACAO_FILE):
        return None
    with open(LOCALIZACAO_FILE, "r") as f:
        data = json.load(f)
        lat = data.get("latitude")
        lon = data.get("longitude")
        if lat is not None and lon is not None:
            return f"https://www.google.com/maps?q={lat},{lon}"
    return None

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

    ultima_url = carregar_localizacao()
    print(f"Enviando email com localização: {ultima_url}")

    body = f"""
Olá {nome_cliente},

O técnico {nome_tecnico} está a caminho.
"""
    if ultima_url:
        body += f"\nAcompanhe a localização em tempo real: {ultima_url}\n"
    else:
        body += "\nA localização do técnico ainda não está disponível.\n"

    body += "\nAtenciosamente,\nProPrinter"
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
    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")

    print(f"Recebido latitude: {lat}, longitude: {lon}")

    if lat is None or lon is None:
        return {"error": "Dados inválidos"}, 400

    salvar_localizacao(lat, lon)
    print("Localização salva com sucesso.")
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
